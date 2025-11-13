import os

BASE_DIR = os.getcwd()

APP_DIR = os.path.join(BASE_DIR, "app")

DB_DIR = os.path.join(APP_DIR, "databases")

USER_FILES_DIR = os.path.join(BASE_DIR, "user_files")

USERS_DB_PATH = os.path.join(DB_DIR, "users.db")
ERRORS_DB_PATH = os.path.join(DB_DIR, "errors.db")
CATEGORIES_DB_PATH = os.path.join(DB_DIR, "categories.db")

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
        "back": "Back to Menu"
    }
}

user_selections = {}