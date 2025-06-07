# 📊 Telegram Data Analytics Bot

**A lightweight data analysis bot for Telegram that processes CSV/Excel files and provides statistics & visualizations.**

---

## 🚀 Features

- **Upload CSV/Excel files** directly in Telegram
- **Generate basic statistics** (mean, median, count, std dev)
- **Create simple visualizations** (bar charts)
- **Lightweight & fast** (Pandas + Matplotlib backend)
- **Free hosting** on Railway.app

## 🔧 Setup

### Prerequisites
- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- Railway.app account (for deployment)

### Local Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/telegram-analytics-bot.git
   cd telegram-analytics-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   echo "TELEGRAM_TOKEN=your_bot_token_here" > .env
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## 🚀 Deployment on Railway.app

1. **Fork this repository** to your GitHub account
2. **Create a new Railway project** and connect your GitHub repo
3. **Add environment variable**:
   - `TELEGRAM_TOKEN` (your bot token)
4. Railway will automatically deploy your bot!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| (Send file) | Upload CSV/Excel for analysis |
| `/stats` | Show basic statistics |
| `/plot` | Generate a bar chart |

## 📂 Project Structure

```
telegram-analytics-bot/
├── bot.py               # Main bot logic
├── requirements.txt     # Python dependencies
├── Procfile             # Railway deployment config
├── README.md            # This file
└── .env.example         # Environment variables template
```

## 🛠 Tech Stack

- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram API wrapper
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [Matplotlib](https://matplotlib.org/) - Visualizations
- [Railway.app](https://railway.app/) - Free hosting

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For help or feature requests, please [open an issue](https://github.com/wegulohillary/telegram-analytics-bot/issues).

---

**Happy analyzing!** 📈✨