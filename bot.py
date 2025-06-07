import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Initialize bot
TOKEN = os.getenv("TELEGRAM_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("📊 **Data Analytics Bot**\nSend me a CSV/Excel file!")

def handle_file(update: Update, context: CallbackContext):
    file = update.message.document.get_file()
    file_bytes = BytesIO(file.download_as_bytearray())
    
    # Read data (CSV/Excel)
    try:
        if update.message.document.file_name.endswith('.csv'):
            df = pd.read_csv(file_bytes)
        elif update.message.document.file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_bytes)
        else:
            update.message.reply_text("❌ Only CSV/Excel files supported!")
            return
    except Exception as e:
        update.message.reply_text(f"❌ Error: {str(e)}")
        return
    
    # Store DataFrame in user session
    context.user_data['df'] = df
    update.message.reply_text(f"✅ Loaded {len(df)} rows. Use /stats or /plot")

def stats(update: Update, context: CallbackContext):
    if 'df' not in context.user_data:
        update.message.reply_text("❌ No data loaded! Send a file first.")
        return
    
    df = context.user_data['df']
    stats = df.describe().to_markdown()
    update.message.reply_text(f"📈 **Statistics**\n```\n{stats}\n```", parse_mode="Markdown")

def plot(update: Update, context: CallbackContext):
    if 'df' not in context.user_data:
        update.message.reply_text("❌ No data loaded! Send a file first.")
        return
    
    df = context.user_data['df']
    plt.figure()
    df.plot(kind='bar')  # Simple bar plot
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    update.message.reply_photo(photo=InputFile(buf, filename='plot.png'))
    plt.close()

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("plot", plot))
    dp.add_handler(MessageHandler(Filters.document, handle_file))
    
    # Webhook (for Railway)
    PORT = int(os.getenv("PORT", 8000))
    APP_URL = os.getenv("RAILWAY_STATIC_URL", "")
    
    if APP_URL:  # Production (webhook)
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f"{APP_URL}/{TOKEN}"
        )
    else:  # Local (polling)
        updater.start_polling()
    
    updater.idle()

if __name__ == '__main__':
    main()
