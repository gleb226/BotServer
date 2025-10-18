from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.common.config import main_categories
from app.databases.categories_database import categories_database

cat_db = categories_database()


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


def get_subcategories_keyboard(user_id, category, parent_subcategory=None):
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

    buttons.append([KeyboardButton(text="Add Subcategory"), KeyboardButton(text="Delete Subcategory")])
    buttons.append([KeyboardButton(text="Back to Menu")])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def get_delete_subcategories_keyboard(user_id, category, parent_subcategory=None):
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

    buttons.append([KeyboardButton(text="Back to Menu")])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)