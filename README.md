# 📁 BotServer: Professional Telegram File Management System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![aiogram 3.x](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://github.com/aiogram/aiogram)
[![SQLite](https://img.shields.io/badge/database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**BotServer** is an advanced, open-source Telegram bot for seamless file storage and organization.

---

## ⚡ One-Line Installation & Build

This command will clone the project, install everything, ask for your token, and **create a standalone executable file** for you.

### **For Linux / macOS:**
```bash
git clone https://github.com/gleb226/BotServer.git && cd BotServer && chmod +x install.sh && ./install.sh
```

### **For Windows (PowerShell):**
```powershell
git clone https://github.com/gleb226/BotServer.git; cd BotServer; .\install.bat
```

> 💡 *The installer will create a `BotLauncher.exe` (Windows) or `BotLauncher` (Linux/Mac) inside the `dist` folder. You can use this file to start the bot anytime!*

---

## 🚀 How to Launch
1. **Run the installation** (see above).
2. **Enter your Bot Token** when prompted.
3. **Choose 'y'** to start the bot immediately.
4. **Future launches**: Simply double-click `dist/BotLauncher.exe`.

---

## 🌟 Key Features
- 🗂️ **Automated Categorization**: Sorts files by type.
- 📂 **Dynamic Folder Structure**: Unlimited nested subdirectories.
- 🌐 **Multi-language**: English and Ukrainian support.
- 💾 **Zero Configuration**: Uses SQLite by default – no server setup required.
- 📦 **Standalone Executable**: Compiles into a single file for easy portability.

---

## 🎯 Bot Commands
- `/start` - Initialize the bot and select language.
- `/language` - Change the interface language.

---

## ⚙️ Configuration & Setup

### 1. Telegram Bot Token
To use this bot, you need a token from Telegram's official bot manager.
1.  Open Telegram and search for **[@BotFather](https://t.me/botfather)**.
2.  Send the command `/newbot`.
3.  Follow the instructions to name your bot.
4.  Copy the **API Token** provided (it looks like `123456:ABC-DEF...`).

### 2. LiqPay API Keys (Commercial Version Only)
For accepting payments via LiqPay website:
1.  Register on [LiqPay.ua](https://www.liqpay.ua/).
2.  Create a company/shop and get your **Public Key** and **Private Key**.
3.  Add them to your `.env` file:
    ```env
    LIQPAY_PUBLIC_KEY=your_public_key
    LIQPAY_PRIVATE_KEY=your_private_key
    ```

### 3. Database
The bot uses **SQLite** by default. For commercial versions, **MongoDB** is supported via `.env` configuration.

---

## 🤝 Contributing
1. Fork the Project
2. Create your Feature Branch
3. Open a Pull Request

---

## 📝 License
Distributed under the MIT License.

## 👥 Contact
**Project Lead**: [@gleb226](https://github.com/gleb226)
