# 📁 BotServer - Telegram File Manager Bot

Powerful Telegram bot for file management with automatic categorization and subcategories. Now with Ukrainian localization!

## 🚀 Features

- 🗂️ **Automatic Categorization** - files sorted by type
- 📂 **Unlimited Subcategories** - create your own folder structure
- 🌐 **Multi-language Support** - English and Ukrainian
- 💾 **All File Types Supported** - photos, videos, documents, code, archives
- 🔐 **Personal Storage** - each user has their own file system

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- MongoDB

### Automatic Installation

#### Windows
1. Run `install.bat`
2. Configure `.env` file with your `BOT_TOKEN` and `MONGO_URL`
3. Run `python bot.py`

#### Linux / Mac
1. Run `chmod +x install.sh && ./install.sh`
2. Configure `.env` file
3. Run `python3 bot.py`

### Manual Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate it:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   MONGO_URL=mongodb://localhost:27017
   ```
6. Run the bot: `python bot.py`

## 🎯 Commands
- `/start` - Start the bot and select language
- `/language` - Change language

## 🗂️ Project Structure
- `app/` - Application logic
  - `common/` - Configuration and constants
  - `databases/` - Database models and clients
  - `handlers/` - Message and callback handlers
  - `keyboards/` - Bot keyboards
  - `utils/` - Utility functions
- `bot.py` - Main entry point
- `install.sh` / `install.bat` - Setup scripts

## 👥 Contact
- 👤 GitHub: [@gleb226](https://github.com/gleb226)
