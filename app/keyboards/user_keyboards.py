from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.common.config import main_categories, translations, icons, VERSION, STORAGE_PLANS

def get_language_keyboard():
    buttons = [
        [KeyboardButton(text="English"), KeyboardButton(text="Ukrainian")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_categories_keyboard(language="English"):
    buttons = []
    row = []
    categories = list(main_categories.keys())
    t_cats = translations[language]["categories"]
    t = translations[language]

    for category in categories:
        row.append(KeyboardButton(text=t_cats.get(category, category)))
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    if VERSION == "commercial":
        buttons.append([KeyboardButton(text=t["buy_storage"])])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_subcategories_keyboard(user_id, category, parent_subcategory=None, language="English"):
    from app.databases.categories_database import categories_database
    cat_db = categories_database()
    subcategories = cat_db.get_subcategories(user_id, category, parent_subcategory)

    buttons = []
    row = []

    for subcategory in subcategories:
        row.append(KeyboardButton(text=f"📁 {subcategory}"))
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
    from app.databases.categories_database import categories_database
    cat_db = categories_database()
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

def get_storage_plans_keyboard(language="English"):
    buttons = []
    for plan_id, plan in STORAGE_PLANS.items():
        label = f"{plan['label']} - {plan['price']} UAH"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"buy_{plan_id}")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)