from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.common.config import main_categories, translations
from app.databases.categories_database import categories_database

cat_db = categories_database()

def get_language_keyboard():
    buttons = [
        [KeyboardButton(text="English"), KeyboardButton(text="Ukrainian")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_categories_keyboard():
    buttons = []
    row = []
    categories = list(main_categories.keys())

    for i, category in enumerate(categories):
        row.append(KeyboardButton(text=category))
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_subcategories_keyboard(user_id, category, parent_subcategory=None, language="English"):
    subcategories = cat_db.get_subcategories(user_id, category, parent_subcategory)

    buttons = []
    row = []

    for subcategory in subcategories:
        row.append(KeyboardButton(text=subcategory))
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    t = translations[language]
    buttons.append([KeyboardButton(text=t["add_subcategory"]), KeyboardButton(text=t["delete_subcategory"])])
    buttons.append([KeyboardButton(text=t["back"])])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_delete_subcategories_keyboard(user_id, category, parent_subcategory=None, language="English"):
    subcategories = cat_db.get_subcategories(user_id, category, parent_subcategory)

    buttons = []
    row = []

    for subcategory in subcategories:
        row.append(KeyboardButton(text=subcategory))
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    t = translations[language]
    buttons.append([KeyboardButton(text=t["back"])])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
