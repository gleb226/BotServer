# 📁 BotServer: Professional Telegram File Management System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![aiogram 3.x](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://github.com/aiogram/aiogram)
[![SQLite](https://img.shields.io/badge/database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![MongoDB](https://img.shields.io/badge/database-MongoDB-green.svg)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**BotServer** is an advanced, open-source Telegram bot for seamless file storage, organization, and management. It supports a structured hierarchy of subdirectories, multiple categories, and works with both **SQLite** (for simple local setups) and **MongoDB** (for scalable environments).

---

## ⚡ One-Line Quick Installation

### **For Linux / macOS:**
```bash
git clone https://github.com/gleb226/BotServer.git && cd BotServer && chmod +x install.sh && ./install.sh
```

### **For Windows (PowerShell):**
```powershell
git clone https://github.com/gleb226/BotServer.git; cd BotServer; .\install.bat
```

### **For Windows (CMD):**
```cmd
git clone https://github.com/gleb226/BotServer.git && cd BotServer && install.bat
```

> 💡 *The interactive installer will automatically prompt you for your Bot Token and Database preference.*

---

## 🛠️ Detailed Manual Installation

If you prefer to set up the project step-by-step:

### 1. Clone the Repository
```bash
git clone https://github.com/gleb226/BotServer.git
cd BotServer
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
# Activate on Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory:
```env
BOT_TOKEN=your_telegram_bot_token
DATABASE_TYPE=sqlite  # or 'mongodb'
# If using mongodb, add:
# MONGO_URL=mongodb://localhost:27017
```

### 5. Launch
```bash
python bot.py
```

---

## 🌟 Key Features

- 🗂️ **Automated Categorization**: Sorts files by extension (Photos, Videos, Programming, Documents, etc.).
- 📂 **Dynamic Folder Structure**: Create and navigate through unlimited nested subdirectories.
- 🌐 **Multi-language Support**: Full English and Ukrainian localization (switch via `/language`).
- 🔐 **Isolated User Storage**: Secure, private workspace for every user.
- 💾 **Hybrid Database Engine**: Choose between SQLite (default, zero-config) or MongoDB.
- 📝 **Interactive Setup**: No manual `.env` editing required with our quick installers.

---

## 🗂️ File Categories & Extensions

| Category | Supported Extensions |
| :--- | :--- |
| **Photos** | jpg, jpeg, png, gif, bmp, tiff |
| **Videos** | mp4, mkv, avi, mov, wmv, flv |
| **Programming** | py, java, js, html, css, sql, json, c, cpp, rs, etc. |
| **Documents** | pdf, docx, txt, xlsx, pptx |
| **Music** | mp3, wav, flac, aac, ogg |
| **Archives** | zip, rar, 7z, tar, gz |

---

## 🎯 Bot Commands

- `/start` - Initialize the bot and select language.
- `/language` - Change the interface language.

---

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Contact

**Project Lead**: [@gleb226](https://github.com/gleb226)

---
<div align="center">
  Developed with ❤️ for the community.
</div>
