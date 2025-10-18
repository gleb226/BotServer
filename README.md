# 📁 BotServer - Telegram File Manager Bot

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![aiogram](https://img.shields.io/badge/aiogram-3.15.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**Powerful Telegram bot for file management with automatic categorization and subcategories**

[🤖 Use the Bot](https://t.me/MedlebServerBot) • [🐛 Report Bug](https://github.com/gleb226/BotServer/issues) • [💬 Telegram Support](https://t.me/medleb7)

---

### 🚀 Bot is already running and ready to use!

**Just follow the link:** [@MedlebServerBot](https://t.me/MedlebServerBot)

</div>

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [How to Use](#-how-to-use)
- [File Categories](#️-file-categories)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Technologies](#-technologies)
- [For Developers](#-for-developers)
- [FAQ](#-faq)
- [Contact](#-contact)

---

## 🎯 About the Project

**BotServer** is a Telegram bot for convenient file storage and organization. The bot automatically sorts files by categories, supports creating custom subcategories, and provides a user-friendly interface for managing your data.

> 💡 **The bot runs on a remote server 24/7** - you don't need to install anything!

### ✨ Key Features

- 🗂️ **Automatic Categorization** - files are automatically sorted by type
- 📂 **Unlimited Subcategories** - create your own folder structure
- 💾 **All File Types Supported** - photos, videos, documents, code, archives
- 🔐 **Personal Storage** - each user has their own file system
- 📱 **Simple Interface** - intuitive management via buttons
- 🗑️ **File Management** - view and delete files
- 💾 **Reliable Storage** - all files on a secure server
- ⚡ **Fast Performance** - instant request processing
- 🌐 **Access from Any Device** - works on phone, tablet, computer

---

## 🚀 Features

### 📤 File Upload
- ✅ Support for documents, photos, videos, audio
- ✅ Automatic category detection by extension
- ✅ Preserve original file names
- ✅ Upload to subcategories
- ✅ Save text data (passwords, contacts)

### 📂 Organization
- ✅ 9 main categories (Photos, Videos, Programming, Documents, Music, Archives, Passwords, Contacts, Other)
- ✅ Create custom subcategories
- ✅ Nested subcategories (unlimited depth)
- ✅ Delete subcategories with all files
- ✅ Navigate through folder structure

### 📊 Management
- ✅ View list of all files
- ✅ View text file contents directly in chat
- ✅ Download files from bot to your device
- ✅ Delete individual files
- ✅ Delete all files at once
- ✅ Return to previous category

### 🔐 Security
- ✅ Personal storage for each user
- ✅ Other users cannot see your files
- ✅ Automatic error logging
- ✅ Protection against unauthorized access

---

## 📱 How to Use

### Quick Start

1. **Open the bot**: [@MedlebServerBot](https://t.me/MedlebServerBot)
2. **Press** `/start` or "START" button
3. **Select a category** from the menu
4. **Send a file** or create a subcategory

### 🎮 Main Actions

#### 1️⃣ Select Category
```
Press one of the categories:
┌─────────────────────────┐
│ [Photos]   [Videos]     │
│ [Programing] [Documents]│
│ [Music]    [Archives]   │
│ [Passwords] [Contacts]  │
│ [Other]                 │
└─────────────────────────┘
```

#### 2️⃣ Upload Files
- Simply send a file to the bot after selecting a category
- Bot will automatically save it to the correct folder
- Confirmation: "File saved: your_file.pdf"

#### 3️⃣ Create Subcategories
```
Press "Add Subcategory" button
Enter name (e.g., "Work" or "Personal")
Done! Now you can save files in this subcategory
```

#### 4️⃣ View Files
```
Press "View Files"
Bot will show all your files
Text files will be displayed in chat
Other files can be downloaded
```

#### 5️⃣ Delete Files
```
Press "Delete Files"
Select specific file or "Delete All"
Confirm deletion
```

### 🎯 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show category menu |

### 🔘 Control Buttons

| Button | Function |
|--------|----------|
| **Add Subcategory** | Create new subcategory |
| **Delete Subcategory** | Delete subcategory |
| **View Files** | View all files |
| **Delete Files** | Delete files |
| **Back to Menu** | Return to previous menu |

---

## 🗂️ File Categories

### 📸 Photos
**Supported formats:** JPG, JPEG, PNG, GIF, BMP, TIFF  
**Purpose:** Photographs, images, pictures  
**Example use:** Vacation photos, screenshots, memes

### 🎬 Videos
**Supported formats:** MP4, MKV, AVI, MOV, WMV, FLV  
**Purpose:** Video files of all types  
**Example use:** Movies, video tutorials, recordings

### 💻 Programming
**Supported formats:** PY, JAVA, JS, HTML, CSS, SQL, JSON, XML, C, CPP, GO, RS, PHP, TXT, MD  
**Purpose:** Source code and development files  
**Example use:** Projects, scripts, configurations, code documentation

### 📄 Documents
**Supported formats:** PDF, DOCX, TXT, XLSX, PPTX  
**Purpose:** Documents and office files  
**Example use:** Reports, resumes, spreadsheets, presentations

### 🎵 Music
**Supported formats:** MP3, WAV, FLAC, AAC, OGG  
**Purpose:** Audio files and music  
**Example use:** Songs, podcasts, audiobooks

### 📦 Archives
**Supported formats:** ZIP, RAR, 7Z, TAR, GZ, TAR.GZ, TGZ, BZ2, TBZ  
**Purpose:** Archives and compressed files  
**Example use:** Backups, project archives, packages

### 🔐 Passwords
**Supported formats:** TXT, CSV  
**Purpose:** Store passwords in text format  
**Example use:** Password list, credentials  
⚠️ **Warning:** Use with caution, not recommended for critical passwords

### 👥 Contacts
**Supported formats:** VCF, TXT  
**Purpose:** Contact information  
**Example use:** Business cards, contact lists, address book

### 📋 Other
**Supported formats:** Any other  
**Purpose:** Files that don't fit other categories  
**Example use:** Rare formats, special files

---

## 💡 Usage Examples

### Example 1: Store Work Documents

```
1. Open bot → /start
2. Select "Documents"
3. Press "Add Subcategory" → enter "Work"
4. Press "Work"
5. Press "Add Subcategory" → enter "Project-2025"
6. Send project files
7. Result: Documents/Work/Project-2025/files.pdf
```

### Example 2: Organize Photos

```
1. Select "Photos"
2. Create subcategory "Vacation-2025"
3. Create nested: "Beach", "Mountains", "City"
4. Upload photos to each location
5. Use "View Files" to browse
```

### Example 3: Save Code and Projects

```
1. Select "Programing"
2. Create subcategories: "Python", "JavaScript", "HTML"
3. In each create project subfolders
4. Upload source codes
5. Download them when needed on another device
```

### Example 4: Archive Passwords

```
1. Select "Passwords"
2. Enter text in format:
   Gmail: mypassword123
   Facebook: pass456
3. Bot saves to text file
4. Use "View Files" to see password
```

---

## 📁 Project Structure

<details>
<summary>🔍 Click to expand structure (for developers)</summary>

```
BotServer/
│
├── 📁 app/
│   ├── 📁 common/                    # Common modules
│   │   ├── __init__.py
│   │   ├── config.py                # Category configuration
│   │   ├── token.py                 # Bot token
│   │   ├── bot_cmd_list.py          # Command list
│   │   └── username.txt             # Bot username
│   │
│   ├── 📁 databases/                 # Database operations
│   │   ├── __init__.py
│   │   ├── user_database.py         # User management
│   │   ├── categories_database.py   # Subcategory management
│   │   ├── users.db                 # SQLite users DB
│   │   ├── categories.db            # SQLite categories DB
│   │   └── errors.db                # SQLite errors DB
│   │
│   ├── 📁 handlers/                  # Event handlers
│   │   ├── __init__.py
│   │   ├── user_handlers.py         # Command and file handling
│   │   └── error_handler.py         # Error logging
│   │
│   ├── 📁 keyboards/                 # Bot keyboards
│   │   ├── __init__.py
│   │   └── user_keyboards.py        # Reply keyboards
│   │
│   └── 📁 utils/                     # Utility functions
│       ├── __init__.py
│       └── file_utils.py            # File system operations
│
├── 📁 user_files/                    # User files (auto-created)
│   └── [user_id]/                   # Separate folder per user
│       ├── photos/                  # Photos category
│       │   └── [subcategories]/
│       ├── videos/                  # Videos category
│       ├── documents/               # Documents category
│       ├── programing/              # Programming category
│       ├── music/                   # Music category
│       ├── archives/                # Archives category
│       ├── passwords/               # Passwords category
│       ├── contacts/                # Contacts category
│       └── other/                   # Other category
│
├── 📄 bot.py                         # Main launch file
├── 📄 requirements.txt               # Python dependencies
├── 📄 README.md                      # This documentation
└── 📄 .gitignore                     # Ignored files for Git
```

</details>

---

## 🛠️ Technologies

### Backend

- **Python 3.8+** - programming language
- **aiogram 3.15.0** - async library for Telegram Bot API
- **SQLite3** - database for storing users and structure
- **asyncio** - asynchronous request processing

### Libraries

```python
aiogram==3.15.0           # Telegram Bot API
python-dotenv==1.0.0      # Environment variables
tabulate==0.9.0           # Table formatting
aiohttp==3.10.11          # HTTP client
```

### Architecture

- **FSM (Finite State Machine)** - user state management
- **Callback Queries** - interactive buttons
- **Reply Keyboards** - main menus
- **Error Handling** - automatic error logging
- **Database ORM** - custom SQLite implementation

---

## 👨‍💻 For Developers

> ℹ️ This section is for those who want to study the code or deploy their own copy of the bot

### For Educational Purposes

If you want to study the code and run your own version of the bot:

#### Step 1: Clone

```bash
git clone https://github.com/gleb226/BotServer.git
cd BotServer
```

#### Step 2: Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

#### Step 3: Configuration

1. Get token from [@BotFather](https://t.me/BotFather)
2. Edit `app/common/token.py`:
```python
TOKEN = "your_token_here"
```

#### Step 4: Run

```bash
python bot.py
```

### 🔧 Customization

#### Add New Category

Edit `app/common/config.py`:

```python
main_categories = {
    "Your_Category": {
        "path": "folder_name",
        "extensions": ["ext1", "ext2", "ext3"]
    }
}
```

#### Modify Category Extensions

```python
"Photos": {
    "path": "photos",
    "extensions": ["jpg", "jpeg", "png", "gif", "webp", "svg"]  # Add more
}
```

### 📊 Database Structure

#### `users` table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    language_code TEXT,
    is_premium BOOLEAN,
    chat_id INTEGER,
    chat_type TEXT,
    joined_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### `subcategories` table
```sql
CREATE TABLE subcategories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    parent_subcategory TEXT DEFAULT NULL,
    UNIQUE(user_id, category, subcategory, parent_subcategory)
);
```

#### `errors` table
```sql
CREATE TABLE errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    firstname TEXT,
    lastname TEXT,
    command TEXT,
    error_message TEXT,
    timestamp TEXT
);
```

### 🔒 Security Best Practices

#### Never commit tokens to Git!

Create `.gitignore`:

```gitignore
# Sensitive data
.env
app/common/token.py
*.key

# Databases
*.db
*.sqlite

# User files
user_files/

# Python
__pycache__/
*.pyc
venv/
```

#### Use environment variables

**Option 1: .env file**

```bash
# .env
BOT_TOKEN=your_token
```

```python
# token.py
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
```

**Option 2: System variables**

```bash
# Linux/Mac
export BOT_TOKEN="your_token"

# Windows
set BOT_TOKEN=your_token
```

---

## ❓ FAQ

### How do I start using the bot?

Simply open [@MedlebServerBot](https://t.me/MedlebServerBot) and press `/start`. No installation required!

### Can other users see my files?

No! Each user has a completely isolated personal storage. Your files are only visible to you.

### What's the file size limit?

Telegram bots can receive files up to 20MB. For larger files, consider using archives.

### Can I create nested subcategories?

Yes! You can create unlimited levels of subcategories to organize your files exactly how you want.

### What happens if I delete a subcategory?

All files and nested subcategories inside it will be permanently deleted. Be careful!

### Can I download files back from the bot?

Yes! Use the "View Files" button and the bot will send you all files from that category.

### Is my data secure?

Yes! The bot runs on a secure server. Each user has isolated storage. However, for critical passwords, we recommend using dedicated password managers.

### Can I use the bot on multiple devices?

Yes! Since it's a Telegram bot, you can access it from any device where you have Telegram installed.

### What if I accidentally delete important files?

Unfortunately, deleted files cannot be recovered. Always double-check before deleting!

### Can I search for specific files?

Currently, searching is not implemented, but you can navigate through categories and subcategories to find your files.

---

## 🐛 Troubleshooting

### Bot doesn't respond

- Check if you're using the correct bot: [@MedlebServerBot](https://t.me/MedlebServerBot)
- Try restarting the conversation with `/start`
- Check your internet connection

### File won't upload

- Ensure file size is under 20MB
- Check if file extension is supported in that category
- Try sending as document instead of compressed

### Can't create subcategory

- Ensure you're in a category (not main menu)
- Check if subcategory name already exists
- Avoid special characters in names

### Text files show incorrectly

- Ensure file is encoded in UTF-8
- Try sending as regular message instead of file

---

## 🌟 Features Coming Soon

- 🔍 File search functionality
- 🌐 Multi-language support
- 📊 Storage statistics
- 🔄 File synchronization
- 📤 Share files with other users
- 🎨 Custom category icons
- 📱 Mobile-friendly web interface

---

## 💬 Contact

### Bot
- 🤖 Telegram Bot: [@MedlebServerBot](https://t.me/MedlebServerBot)

### Support
- 📧 Telegram Support: [@medleb7](https://t.me/medleb7)
- 🐛 Report Issues: [GitHub Issues](https://github.com/gleb226/BotServer/issues)

### Developer
- 👤 GitHub: [@gleb226](https://github.com/gleb226)
- 💼 Project: [github.com/gleb226/BotServer](https://github.com/gleb226/BotServer)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 gleb226

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- [aiogram](https://github.com/aiogram/aiogram) - Excellent Telegram Bot framework
- [Telegram Bot API](https://core.telegram.org/bots/api) - Powerful bot platform
- All contributors and users of the bot

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/gleb226/BotServer?style=social)
![GitHub forks](https://img.shields.io/github/forks/gleb226/BotServer?style=social)
![GitHub issues](https://img.shields.io/github/issues/gleb226/BotServer)
![GitHub last commit](https://img.shields.io/github/last-commit/gleb226/BotServer)

---

<div align="center">

### ⭐ If you like this project, please give it a star!

**Made with ❤️ by [gleb226](https://github.com/gleb226)**

[⬆ Back to Top](#-botserver---telegram-file-manager-bot)

</div>