import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getcwd()
APP_DIR = os.path.join(BASE_DIR, "app")
DB_DIR = os.path.join(APP_DIR, "databases")

# Version control: 'personal' or 'commercial'
VERSION = os.getenv("VERSION", "personal")

if VERSION == "personal":
    USER_FILES_DIR = os.path.join(BASE_DIR, "files")
else:
    USER_FILES_DIR = os.path.join(BASE_DIR, "user_files")

SQLITE_DB_PATH = os.path.join(DB_DIR, "bot.db")
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(USER_FILES_DIR, exist_ok=True)

# Icons for categories
icons = {
    "Photos": "🖼️",
    "Videos": "🎬",
    "Programing": "💻",
    "Documents": "📄",
    "Music": "🎵",
    "Archives": "📦",
    "Passwords": "🔑",
    "Contacts": "👥"
}

category_map = {
    "Photos": "photos",
    "Videos": "videos",
    "Programing": "programing",
    "Documents": "documents",
    "Music": "music",
    "Archives": "archives",
    "Passwords": "passwords",
    "Contacts": "contacts"
}

translations = {
    "English": {
        "welcome": "👋 Welcome! Please select a category.",
        "select_category": "📂 Select a category:",
        "select_subcategory": "📁 Select a subcategory or upload here:",
        "add_subcategory": "➕ Add subcategory",
        "delete_subcategory": "❌ Delete subcategory",
        "enter_subcategory_name": "📝 Enter the name of the new subcategory:",
        "subcategory_added": "✅ Subcategory '{}' added!",
        "subcategory_deleted": "🗑️ Subcategory '{}' deleted!",
        "select_subcategory_to_delete": "🗑️ Select a subcategory to delete:",
        "no_subcategories": "📭 No subcategories available.",
        "back": "⬅️ Back",
        "view_files": "👁️ View Files",
        "delete_files": "🗑️ Delete Files",
        "file_actions": "⚙️ File actions:",
        "delete_all": "🧨 Delete All",
        "no_files": "📭 No files found!",
        "invalid_category": "🚫 Invalid category.",
        "invalid_file_type": "🚫 Invalid file type. Allowed: {}",
        "text_saved": "✅ Saved successfully!",
        "file_saved_msg": "✅ File saved: {}",
        "deleted_msg": "🗑️ Deleted: {}",
        "deleted_count": "🗑️ Deleted {} files",
        "select_file_delete": "🗑️ Select a file to delete:",
        "subcategory_exists": "⚠️ Already exists!",
        "start_over": "🔄 Please use /start",
        "unavailable": "⚠️ Error. Try later.",
        "select_language": "🌐 Select language:",
        "categories": {
            "Photos": "🖼️ Photos",
            "Videos": "🎬 Videos",
            "Programing": "💻 Coding",
            "Documents": "📄 Documents",
            "Music": "🎵 Music",
            "Archives": "📦 Archives",
            "Passwords": "🔑 Passwords",
            "Contacts": "👥 Contacts"
        }
    },
    "Ukrainian": {
        "welcome": "👋 Вітаємо! Оберіть категорію.",
        "select_category": "📂 Оберіть категорію:",
        "select_subcategory": "📁 Оберіть підкатегорію або завантажте:",
        "add_subcategory": "➕ Додати підкатегорію",
        "delete_subcategory": "❌ Видалити підкатегорію",
        "enter_subcategory_name": "📝 Введіть назву підкатегорії:",
        "subcategory_added": "✅ Підкатегорію '{}' додано!",
        "subcategory_deleted": "🗑️ Підкатегорію '{}' видалено!",
        "select_subcategory_to_delete": "🗑️ Оберіть підкатегорію для видалення:",
        "no_subcategories": "📭 Підкатегорії відсутні.",
        "back": "⬅️ Назад",
        "view_files": "👁️ Переглянути файли",
        "delete_files": "🗑️ Видалити файли",
        "file_actions": "⚙️ Дії з файлами:",
        "delete_all": "🧨 Видалити все",
        "no_files": "📭 Файлів не знайдено!",
        "invalid_category": "🚫 Невірна категорія.",
        "invalid_file_type": "🚫 Невірний тип. Дозволені: {}",
        "text_saved": "✅ Збережено успішно!",
        "file_saved_msg": "✅ Файл збережено: {}",
        "deleted_msg": "🗑️ Видалено: {}",
        "deleted_count": "🗑️ Видалено {} файлів",
        "select_file_delete": "🗑️ Оберіть файл для видалення:",
        "subcategory_exists": "⚠️ Вже існує!",
        "start_over": "🔄 Використовуйте /start",
        "unavailable": "⚠️ Помилка. Спробуйте пізніше.",
        "select_language": "🌐 Оберіть мову:",
        "categories": {
            "Photos": "🖼️ Фото",
            "Videos": "🎬 Відео",
            "Programing": "💻 Програмування",
            "Documents": "📄 Документи",
            "Music": "🎵 Музика",
            "Archives": "📦 Архіви",
            "Passwords": "🔑 Паролі",
            "Contacts": "👥 Контакти"
        }
    }
}

main_categories = {
    "Photos": {"path": "photos", "extensions": ["jpg", "jpeg", "png", "gif", "bmp", "tiff"]},
    "Videos": {"path": "videos", "extensions": ["mp4", "mkv", "avi", "mov", "wmv", "flv"]},
    "Programing": {"path": "programing", "extensions": ["py", "java", "js", "html", "css", "sql", "json", "xml", "db", "c", "cpp", "cs", "go", "rs", "h", "php", "txt", "md"]},
    "Documents": {"path": "documents", "extensions": ["pdf", "docx", "txt", "xlsx", "pptx"]},
    "Music": {"path": "music", "extensions": ["mp3", "wav", "flac", "aac", "ogg"]},
    "Archives": {"path": "archives", "extensions": ["7z", "rar", "zip", "tar", "gz", "tar.gz", "tgz", "bz2", "tbz"]},
    "Passwords": {"path": "passwords", "extensions": ["txt", "csv"]},
    "Contacts": {"path": "contacts", "extensions": ["vcf", "txt"]}
}

user_selections = {}