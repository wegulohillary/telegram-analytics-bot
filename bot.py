import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Initialize environment
TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", 8000))
APP_URL = os.getenv("RAILWAY_STATIC_URL", "")

# --- Bot Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message"""
    await update.message.reply_text(
        "📊 **Data Analytics Bot**\n\n"
        "Send me a CSV/Excel file to analyze!\n"
        "Available commands:\n"
        "/stats - Show basic statistics\n"
        "/plot - Generate a bar chart"
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process uploaded files"""
    if not update.message.document:
        await update.message.reply_text("❌ Please send a file")
        return

    try:
        file = await update.message.document.get_file()
        file_bytes = BytesIO(await file.download_as_bytearray())
        
        if update.message.document.file_name.endswith('.csv'):
            df = pd.read_csv(file_bytes)
        elif update.message.document.file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_bytes)
        else:
            await update.message.reply_text("❌ Only CSV/Excel files supported!")
            return

        context.user_data['df'] = df
        await update.message.reply_text(
            f"✅ Loaded {len(df)} rows, {len(df.columns)} columns\n"
            f"Use /stats or /plot to analyze"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error processing file: {str(e)}")

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Calculate basic statistics"""
    if 'df' not in context.user_data:
        await update.message.reply_text("❌ No data loaded! Send a file first.")
        return

    df = context.user_data['df']
    stats = df.describe().to_markdown()
    await update.message.reply_text(
        f"📈 **Basic Statistics**\n```\n{stats}\n```",
        parse_mode="Markdown"
    )

async def generate_plot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create visualization"""
    if 'df' not in context.user_data:
        await update.message.reply_text("❌ No data loaded! Send a file first.")
        return

    df = context.user_data['df']
    
    try:
        plt.figure(figsize=(10, 6))
        df.plot(kind='bar')
        plt.title("Data Visualization")
        plt.tight_layout()
        
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        
        await update.message.reply_photo(
            photo=buf,
            caption="📊 Here's your visualization"
        )
        plt.close()
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating plot: {str(e)}")

# --- Bot Setup ---
def main() -> None:
    """Run the bot"""
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", show_stats))
    application.add_handler(CommandHandler("plot", generate_plot))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    # Start the bot
    if APP_URL:  # Production (webhook)
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f"{APP_URL}/{TOKEN}"
        )
    else:  # Development (polling)
        application.run_polling()

if __name__ == "__main__":
    main()
