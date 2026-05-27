import os
import sys
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.realpath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path, override=True)

VERSION = os.getenv("VERSION", "personal")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "513546547"))
LIQPAY_PUBLIC_KEY = os.getenv("LIQPAY_PUBLIC_KEY")
LIQPAY_PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

if VERSION == "commercial":
    DATABASE_TYPE = "mongodb"
    USER_FILES_DIR = os.path.join(BASE_DIR, "user_files")
    SQLITE_DB_PATH = None
else:
    DATABASE_TYPE = "sqlite"
    USER_FILES_DIR = os.path.join(BASE_DIR, "files")
    SQLITE_DB_PATH = os.path.join(BASE_DIR, "bot.db")

os.makedirs(USER_FILES_DIR, exist_ok=True)

STORAGE_PLANS = {
    "plan_10gb": {"size": 10, "price": 50, "label": "10 GB Storage"},
    "plan_100gb": {"size": 100, "price": 125, "label": "100 GB Storage"},
    "plan_200gb": {"size": 200, "price": 200, "label": "200 GB Storage"},
    "plan_250gb": {"size": 250, "price": 245, "label": "250 GB Storage"},
    "plan_500gb": {"size": 500, "price": 450, "label": "500 GB Storage"}
}

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
        "storage_info": "📊 Storage: {}/{} GB used",
        "buy_storage": "💳 Buy Storage",
        "payment_success": "🎉 Payment successful! Your storage has been increased by {} GB.",
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
        "storage_info": "📊 Сховище: {}/{} ГБ використано",
        "buy_storage": "💳 Купити місце",
        "payment_success": "🎉 Оплата успішна! Ваше сховище збільшено на {} ГБ.",
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
    "Photos": {"path": "photos", "extensions": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "heic"]},
    "Videos": {"path": "videos", "extensions": ["mp4", "mkv", "avi", "mov", "wmv", "flv"]},
    "Programing": {"path": "programing", "extensions": ["py", "java", "js", "html", "css", "sql", "json", "xml", "db", "c", "cpp", "cs", "go", "rs", "h", "php", "txt", "md"]},
    "Documents": {"path": "documents", "extensions": ["pdf", "docx", "txt", "xlsx", "pptx"]},
    "Music": {"path": "music", "extensions": ["mp3", "wav", "flac", "aac", "ogg"]},
    "Archives": {"path": "archives", "extensions": ["7z", "rar", "zip", "tar", "gz", "tar.gz", "tgz", "bz2", "tbz"]},
    "Passwords": {"path": "passwords", "extensions": ["txt", "csv"]},
    "Contacts": {"path": "contacts", "extensions": ["vcf", "txt"]}
}

user_selections = {}
