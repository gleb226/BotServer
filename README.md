# 📁 BotServer: Professional Telegram File Management System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![aiogram 3.x](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://github.com/aiogram/aiogram)
[![MongoDB](https://img.shields.io/badge/database-MongoDB-green.svg)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**BotServer** is an advanced, open-source Telegram bot designed for seamless file storage, organization, and management. It provides a structured environment for users to store their data across multiple categories with support for unlimited nested subdirectories and multi-language support (English & Ukrainian).

---

## 🌟 Key Features

- 🗂️ **Automated Categorization**: Intelligently sorts incoming files based on their extensions (Photos, Videos, Programming, Documents, etc.).
- 📂 **Dynamic Folder Structure**: Create, manage, and navigate through an unlimited hierarchy of subcategories.
- 🌐 **Multi-language Support**: Full English and Ukrainian localization, switchable at any time via `/language`.
- 🔐 **Isolated User Storage**: Every user gets a private, secure file system workspace.
- ⚡ **Asynchronous Core**: Built on top of `aiogram 3.x`, ensuring high performance even under load.
- 📝 **Text Management**: Specialized handling for contacts and passwords with direct in-chat content viewing.
- 🛠️ **Administrative Logging**: Built-in error tracking and database logging for robust maintenance.

---

## 🛠️ Technology Stack

- **Framework**: [aiogram 3.x](https://docs.aiogram.dev/) (Asynchronous Telegram Bot API)
- **Database**: [MongoDB](https://www.mongodb.com/) (NoSQL storage for user settings and structure)
- **Language**: Python 3.8+
- **Environment**: [python-dotenv](https://pypi.org/project/python-dotenv/) for secure configuration
- **UI/UX**: Custom Reply & Inline keyboards with state-driven navigation (FSM)

---

## 🚀 Quick Installation

### Automated Setup (Recommended)

We provide one-click installation scripts that handle virtual environment creation and dependency installation.

#### **For Windows Users:**
1. Clone the repository: `git clone https://github.com/gleb226/BotServer.git`
2. Run `install.bat`
3. Fill in your `BOT_TOKEN` and `MONGO_URL` in the generated `.env` file.
4. Launch: `python bot.py`

#### **For Linux/Mac Users:**
1. Clone the repository: `git clone https://github.com/gleb226/BotServer.git`
2. Run: `chmod +x install.sh && ./install.sh`
3. Edit the `.env` file with your credentials.
4. Launch: `python3 bot.py`

### Manual Setup
If you prefer manual control:
```bash
# 1. Clone
git clone https://github.com/gleb226/BotServer.git
cd BotServer

# 2. Virtual Env
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Dependencies
pip install -r requirements.txt

# 4. Configuration
echo BOT_TOKEN=your_token_here > .env
echo MONGO_URL=mongodb://localhost:27017 >> .env

# 5. Run
python bot.py
```

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

- `/start` - Initialize the bot and select your preferred language.
- `/language` - Change the interface language (English/Ukrainian).

---

## 🤝 Contributing

As an open-source project, contributions are highly encouraged! 

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
