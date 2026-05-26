import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getcwd()

APP_DIR = os.path.join(BASE_DIR, "app")

DB_DIR = os.path.join(APP_DIR, "databases")

USER_FILES_DIR = os.path.join(BASE_DIR, "user_files")

USERS_DB_PATH = os.path.join(DB_DIR, "users.db")
ERRORS_DB_PATH = os.path.join(DB_DIR, "errors.db")
CATEGORIES_DB_PATH = os.path.join(DB_DIR, "categories.db")

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(USER_FILES_DIR, exist_ok=True)

main_categories = {
    "Photos": {
        "path": "photos",
        "extensions": ["jpg", "jpeg", "png", "gif", "bmp", "tiff"]
    },
    "Videos": {
        "path": "videos",
        "extensions": ["mp4", "mkv", "avi", "mov", "wmv", "flv"]
    },
    "Programing": {
        "path": "programing",
        "extensions": ["py", "java", "js", "html", "css", "sql", "json", "xml", "db", "jpg", "jpeg", "png", "gif", "c", "cpp", "cs", "go", "rs", "h", "php", "txt", "md"]
    },
    "Documents": {
        "path": "documents",
        "extensions": ["pdf", "docx", "txt", "xlsx", "pptx"]
    },
    "Music": {
        "path": "music",
        "extensions": ["mp3", "wav", "flac", "aac", "ogg"]
    },
    "Archives": {
        "path": "archives",
        "extensions": ["7z", "rar", "zip", "tar", "gz", "tar.gz", "tgz", "bz2", "tbz"]
    },
    "Passwords": {
        "path": "passwords",
        "extensions": ["txt", "csv"]
    },
    "Contacts": {
        "path": "contacts",
        "extensions": ["vcf", "txt"]
    },
}

translations = {
    "English": {
        "welcome": "Welcome! Please select a category.",
        "select_category": "Select a category:",
        "select_subcategory": "Select a subcategory or upload here:",
        "manage_subcategories": "Manage subcategories",
        "add_subcategory": "Add subcategory",
        "delete_subcategory": "Delete subcategory",
        "enter_subcategory_name": "Enter the name of the new subcategory:",
        "subcategory_added": "Subcategory '{}' has been added successfully!",
        "subcategory_deleted": "Subcategory '{}' has been deleted successfully!",
        "select_subcategory_to_delete": "Select a subcategory to delete:",
        "no_subcategories": "No subcategories available.",
        "send_file": "Send your files here. Type 'Back to Menu' to return.",
        "file_too_large": "The file is too large. Please send a smaller file.",
        "file_saved": "{} has been saved successfully!",
        "folder_error": "Invalid folder selected. Please try again.",
        "back": "Back to Menu",
        "view_files": "View Files",
        "delete_files": "Delete Files",
        "file_actions": "File actions:",
        "delete_all": "Delete All",
        "no_files": "No files found!",
        "invalid_category": "Invalid category. Please select from the menu.",
        "invalid_file_type": "Invalid file type. Allowed: {}",
        "text_saved": "Text saved successfully!",
        "file_saved_msg": "File saved: {}",
        "deleted_msg": "Deleted: {}",
        "deleted_count": "Deleted {} files",
        "select_file_delete": "Select a file to delete or delete all:",
        "subcategory_exists": "Subcategory already exists!",
        "start_over": "Please start over with /start",
        "unavailable": "Function is currently unavailable. Please try again later.",
        "select_language": "Please select your language:"
    },
    "Ukrainian": {
        "welcome": "Ласкаво просимо! Будь ласка, оберіть категорію.",
        "select_category": "Оберіть категорію:",
        "select_subcategory": "Оберіть підкатегорію або завантажте сюди:",
        "manage_subcategories": "Керування підкатегоріями",
        "add_subcategory": "Додати підкатегорію",
        "delete_subcategory": "Видалити підкатегорію",
        "enter_subcategory_name": "Введіть назву нової підкатегорії:",
        "subcategory_added": "Підкатегорію '{}' успішно додано!",
        "subcategory_deleted": "Підкатегорію '{}' успішно видалено!",
        "select_subcategory_to_delete": "Оберіть підкатегорію для видалення:",
        "no_subcategories": "Підкатегорії відсутні.",
        "send_file": "Надсилайте ваші файли сюди. Напишіть 'Назад до меню' для повернення.",
        "file_too_large": "Файл занадто великий. Будь ласка, надішліть менший файл.",
        "file_saved": "{} успішно збережено!",
        "folder_error": "Обрано невірну папку. Спробуйте ще раз.",
        "back": "Назад до меню",
        "view_files": "Переглянути файли",
        "delete_files": "Видалити файли",
        "file_actions": "Дії з файлами:",
        "delete_all": "Видалити все",
        "no_files": "Файлів не знайдено!",
        "invalid_category": "Невірна категорія. Будь ласка, оберіть з меню.",
        "invalid_file_type": "Невірний тип файлу. Дозволені: {}",
        "text_saved": "Текст успішно збережено!",
        "file_saved_msg": "Файл збережено: {}",
        "deleted_msg": "Видалено: {}",
        "deleted_count": "Видалено {} файлів",
        "select_file_delete": "Оберіть файл для видалення або видаліть все:",
        "subcategory_exists": "Підкатегорія вже існує!",
        "start_over": "Будь ласка, почніть спочатку з /start",
        "unavailable": "Функція наразі недоступна. Будь ласка, спробуйте пізніше.",
        "select_language": "Будь ласка, оберіть мову:"
    }
}

user_selections = {}