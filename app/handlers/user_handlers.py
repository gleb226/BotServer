import os
import shutil
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from app.keyboards import user_keyboards as kb
from app.common.config import main_categories, USER_FILES_DIR, translations, user_selections, icons, VERSION, STORAGE_PLANS, LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY
from app.databases.categories_database import categories_database
from app.databases.user_database import user_database, db
from app.handlers.error_handler import log_error_to_db, notify_admin
from app.utils.file_utils import clear_user_data
import uuid
import json
import base64
import hashlib
import aiohttp
user_router = Router()
cat_db = categories_database()
class LiqPayManager:
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
    def _get_signature(self, data):
        sign_str = self.private_key + data + self.private_key
        return base64.b64encode(hashlib.sha1(sign_str.encode()).digest()).decode()
    def get_checkout_url(self, params):
        params.update({'public_key': self.public_key})
        data = base64.b64encode(json.dumps(params).encode()).decode()
        signature = self._get_signature(data)
        return f"https://www.liqpay.ua/api/3/checkout?data={data}&signature={signature}"
    async def get_status(self, order_id):
        params = {
            'action': 'status',
            'public_key': self.public_key,
            'version': '3',
            'order_id': order_id
        }
        data = base64.b64encode(json.dumps(params).encode()).decode()
        signature = self._get_signature(data)
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.liqpay.ua/api/request', data={'data': data, 'signature': signature}) as response:
                return await response.json()
LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "common", "logo.jpeg")
class FileAction(CallbackData, prefix="f"):
    action: str
    category: str
    subcategory: str = ""
    filename: str = ""
class UserStates(StatesGroup):
    selecting_language = State()
    waiting_for_file = State()
    waiting_for_text = State()
    waiting_for_subcategory_name = State()
    selecting_category = State()
    selecting_subcategory = State()
    deleting_subcategory = State()
def get_category_from_translated(text, lang):
    t_cats = translations[lang]["categories"]
    for eng_name, trans_name in t_cats.items():
        if text == trans_name:
            return eng_name
    return None
def get_user_storage_usage(user_id):
    path = os.path.join(USER_FILES_DIR) if VERSION == "personal" else os.path.join(USER_FILES_DIR, str(user_id))
    total_size = 0
    if os.path.exists(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                total_size += os.path.getsize(os.path.join(dirpath, f))
    return round(total_size / (1024 * 1024 * 1024), 2)
@user_router.message(Command("language"))
async def language_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_language(user_id) or "English"
    await message.answer(translations[lang]["select_language"], reply_markup=kb.get_language_keyboard())
    await state.set_state(UserStates.selecting_language)
@user_router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        user_selections[user_id] = {"category": None, "subcategory_path": []}
        db.add_user(
            user_id=user_id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name or "",
            username=message.from_user.username or "",
            language_code=message.from_user.language_code or "unknown",
            is_premium=bool(getattr(message.from_user, 'is_premium', False)),
            chat_id=message.chat.id,
            chat_type=message.chat.type
        )
        lang_code = message.from_user.language_code
        auto_lang = "Ukrainian" if lang_code in ["uk", "ru"] else "English"
        await message.answer(translations[auto_lang]["select_language"], reply_markup=kb.get_language_keyboard())
        await state.set_state(UserStates.selecting_language)
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A", "N/A", "N/A", "/start", str(e))
        if VERSION == "commercial":
            await notify_admin(message.bot, message.from_user.id, message.from_user.username or "N/A", "/start", str(e))
        await message.answer("⚠️ Error.")
@user_router.message(UserStates.selecting_language)
async def select_language(message: Message, state: FSMContext):
    user_id = message.from_user.id
    selected_lang = message.text
    if selected_lang not in ["English", "Ukrainian"]:
        await message.answer("🌐 Please select a language.")
        return
    db.set_language(user_id, selected_lang)
    await message.answer(translations[selected_lang]["welcome"], reply_markup=kb.get_categories_keyboard(selected_lang))
    await state.set_state(UserStates.selecting_category)
@user_router.message(Command("storage"))
async def storage_command(message: Message):
    if VERSION != "commercial":
        return
    user_id = message.from_user.id
    lang = db.get_language(user_id) or "English"
    t = translations[lang]
    usage = get_user_storage_usage(user_id)
    limit = db.get_storage_limit(user_id)
    await message.answer(t["storage_info"].format(usage, limit), reply_markup=kb.get_storage_plans_keyboard(lang))
@user_router.callback_query(F.data == "renew_sub")
async def renew_sub_handler(callback: CallbackQuery):
    await storage_command(callback.message)
    await callback.answer()
@user_router.callback_query(F.data == "cancel_sub_confirm")
async def cancel_sub_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = db.get_language(user_id) or "English"
    db.set_storage_limit(user_id, 2.0)
    clear_user_data(user_id)
    await callback.message.answer(translations[lang]["subscription_cancelled"])
    await callback.answer()
@user_router.callback_query(F.data.startswith("buy_"))
async def buy_storage_plan(callback: CallbackQuery):
    try:
        plan_id = callback.data.split("_", 1)[1]
        if plan_id not in STORAGE_PLANS:
            return
        plan = STORAGE_PLANS[plan_id]
        user_id = callback.from_user.id
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        if not LIQPAY_PUBLIC_KEY or not LIQPAY_PRIVATE_KEY:
            await callback.message.answer("⚠️ Configuration error.")
            return
        liqpay = LiqPayManager(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        order_id = str(uuid.uuid4())
        params = {
            'action': 'pay',
            'amount': str(plan['price']),
            'currency': 'UAH',
            'description': f"Upgrade to {plan['size']} GB",
            'order_id': order_id,
            'version': '3'
        }
        checkout_url = liqpay.get_checkout_url(params)
        db.set_pending_payment(user_id, order_id, plan_id)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t["pay_button"], url=checkout_url)]
        ])
        await callback.message.answer(
            t["plan_info"].format(plan['label'], plan['price']),
            reply_markup=markup,
            parse_mode="HTML"
        )
        await callback.answer()
    except Exception as e:
        log_error_to_db(callback.from_user.id, callback.from_user.username or "N/A", "N/A", "N/A", "buy_storage", str(e))
        await callback.answer()
@user_router.message(UserStates.selecting_category)
async def select_category(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        if message.text == t["buy_storage"] and VERSION == "commercial":
            await storage_command(message)
            return
        category = get_category_from_translated(message.text, lang)
        if not category:
            await message.answer(t["invalid_category"])
            return
        user_selections[user_id] = {"category": category, "subcategory_path": []}
        buttons = [
            [
                InlineKeyboardButton(text=t["view_files"], callback_data=FileAction(action="view", category=category).pack()),
                InlineKeyboardButton(text=t["delete_files"], callback_data=FileAction(action="delete_menu", category=category).pack())
            ]
        ]
        await message.answer(t["select_subcategory"], reply_markup=kb.get_subcategories_keyboard(user_id, category, "", language=lang))
        await message.answer(t["file_actions"], reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        if category in ["Passwords", "Contacts"]:
            await state.set_state(UserStates.waiting_for_text)
        else:
            await state.set_state(UserStates.waiting_for_file)
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A", "N/A", "N/A", "select_category", str(e))
@user_router.message(UserStates.waiting_for_text, F.text)
async def handle_text(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        text = message.text
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        if text == t["add_subcategory"]:
            await message.answer(t["enter_subcategory_name"], reply_markup=ReplyKeyboardRemove())
            await state.set_state(UserStates.waiting_for_subcategory_name)
            return
        if text == t["delete_subcategory"]:
            category = user_selections[user_id]["category"]
            sub_path = user_selections[user_id]["subcategory_path"]
            curr = "/".join(sub_path) if sub_path else ""
            subcats = cat_db.get_subcategories(user_id, category, curr)
            if not subcats:
                await message.answer(t["no_subcategories"])
                return
            await message.answer(t["select_subcategory_to_delete"], reply_markup=kb.get_delete_subcategories_keyboard(user_id, category, curr, language=lang))
            await state.set_state(UserStates.deleting_subcategory)
            return
        if text == t["back"]:
            sub_path = user_selections[user_id]["subcategory_path"]
            if not sub_path:
                await message.answer(t["welcome"], reply_markup=kb.get_categories_keyboard(lang))
                await state.set_state(UserStates.selecting_category)
            else:
                user_selections[user_id]["subcategory_path"].pop()
                category = user_selections[user_id]["category"]
                new_p = "/".join(user_selections[user_id]["subcategory_path"])
                buttons = [[InlineKeyboardButton(text=t["view_files"], callback_data=FileAction(action="view", category=category, subcategory=new_p).pack()),
                            InlineKeyboardButton(text=t["delete_files"], callback_data=FileAction(action="delete_menu", category=category, subcategory=new_p).pack())]]
                await message.answer(t["select_subcategory"], reply_markup=kb.get_subcategories_keyboard(user_id, category, new_p, language=lang))
                await message.answer(t["file_actions"], reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            return
        if text.startswith("📁 "):
            actual = text[2:]
            category = user_selections[user_id]["category"]
            sub_path = user_selections[user_id]["subcategory_path"]
            curr = "/".join(sub_path) if sub_path else ""
            if cat_db.subcategory_exists(user_id, category, actual, curr):
                user_selections[user_id]["subcategory_path"].append(actual)
                new_p = "/".join(user_selections[user_id]["subcategory_path"])
                buttons = [[InlineKeyboardButton(text=t["view_files"], callback_data=FileAction(action="view", category=category, subcategory=new_p).pack()),
                            InlineKeyboardButton(text=t["delete_files"], callback_data=FileAction(action="delete_menu", category=category, subcategory=new_p).pack())]]
                await message.answer(t["select_subcategory"], reply_markup=kb.get_subcategories_keyboard(user_id, category, new_p, language=lang))
                await message.answer(t["file_actions"], reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
                return
        if user_id not in user_selections:
            await message.answer(t["start_over"])
            return
        category = user_selections[user_id]["category"]
        if VERSION == "commercial" and get_user_storage_usage(user_id) >= db.get_storage_limit(user_id):
            await message.answer("⚠️ Full. Buy more: /storage")
            return
        from app.utils.file_utils import save_text_to_file
        save_text_to_file(user_id, category, user_selections[user_id]["subcategory_path"], text)
        await message.answer(t["text_saved"])
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A", "N/A", "N/A", "handle_text", str(e))
@user_router.message(UserStates.waiting_for_file, F.text)
async def handle_file_text_commands(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        text = message.text
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        if text == t["add_subcategory"]:
            await message.answer(t["enter_subcategory_name"], reply_markup=ReplyKeyboardRemove())
            await state.set_state(UserStates.waiting_for_subcategory_name)
            return
        if text == t["delete_subcategory"]:
            category = user_selections[user_id]["category"]
            sub_path = user_selections[user_id]["subcategory_path"]
            curr = "/".join(sub_path) if sub_path else ""
            subcats = cat_db.get_subcategories(user_id, category, curr)
            if not subcats:
                await message.answer(t["no_subcategories"])
                return
            await message.answer(t["select_subcategory_to_delete"], reply_markup=kb.get_delete_subcategories_keyboard(user_id, category, curr, language=lang))
            await state.set_state(UserStates.deleting_subcategory)
            return
        if text == t["back"]:
            sub_path = user_selections[user_id]["subcategory_path"]
            if not sub_path:
                await message.answer(t["welcome"], reply_markup=kb.get_categories_keyboard(lang))
                await state.set_state(UserStates.selecting_category)
            else:
                user_selections[user_id]["subcategory_path"].pop()
                category = user_selections[user_id]["category"]
                new_p = "/".join(user_selections[user_id]["subcategory_path"])
                buttons = [[InlineKeyboardButton(text=t["view_files"], callback_data=FileAction(action="view", category=category, subcategory=new_p).pack()),
                            InlineKeyboardButton(text=t["delete_files"], callback_data=FileAction(action="delete_menu", category=category, subcategory=new_p).pack())]]
                await message.answer(t["select_subcategory"], reply_markup=kb.get_subcategories_keyboard(user_id, category, new_p, language=lang))
                await message.answer(t["file_actions"], reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            return
        if text.startswith("📁 "):
            actual = text[2:]
            category = user_selections[user_id]["category"]
            sub_path = user_selections[user_id]["subcategory_path"]
            curr = "/".join(sub_path) if sub_path else ""
            if cat_db.subcategory_exists(user_id, category, actual, curr):
                user_selections[user_id]["subcategory_path"].append(actual)
                new_p = "/".join(user_selections[user_id]["subcategory_path"])
                buttons = [[InlineKeyboardButton(text=t["view_files"], callback_data=FileAction(action="view", category=category, subcategory=new_p).pack()),
                            InlineKeyboardButton(text=t["delete_files"], callback_data=FileAction(action="delete_menu", category=category, subcategory=new_p).pack())]]
                await message.answer(t["select_subcategory"], reply_markup=kb.get_subcategories_keyboard(user_id, category, new_p, language=lang))
                await message.answer(t["file_actions"], reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A", "N/A", "N/A", "handle_file_text", str(e))
        if VERSION == "commercial": await notify_admin(message.bot, message.from_user.id, message.from_user.username or "N/A", "handle_file_text", str(e))
@user_router.message(UserStates.waiting_for_subcategory_name)
async def add_subcategory_finish(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        sub_name = message.text.strip()
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        if user_id not in user_selections:
            await message.answer(t["start_over"])
            return
        category = user_selections[user_id]["category"]
        sub_path = user_selections[user_id]["subcategory_path"]
        parent = "/".join(sub_path) if sub_path else ""
        if cat_db.add_subcategory(user_id, category, sub_name, parent):
            buttons = [[InlineKeyboardButton(text=t["view_files"], callback_data=FileAction(action="view", category=category, subcategory=parent).pack()),
                        InlineKeyboardButton(text=t["delete_files"], callback_data=FileAction(action="delete_menu", category=category, subcategory=parent).pack())]]
            await message.answer(t["subcategory_added"].format(sub_name), reply_markup=kb.get_subcategories_keyboard(user_id, category, parent, language=lang))
            await message.answer(t["file_actions"], reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        else:
            await message.answer(t["subcategory_exists"], reply_markup=kb.get_subcategories_keyboard(user_id, category, parent, language=lang))
        await state.set_state(UserStates.waiting_for_text if category in ["Passwords", "Contacts"] else UserStates.waiting_for_file)
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A", "N/A", "N/A", "add_subcategory", str(e))
@user_router.message(UserStates.deleting_subcategory)
async def delete_subcategory_confirm(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        subcat = message.text
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        if user_id not in user_selections:
            await message.answer(t["start_over"])
            return
        category = user_selections[user_id]["category"]
        sub_path = user_selections[user_id]["subcategory_path"]
        curr = "/".join(sub_path) if sub_path else ""
        if subcat == t["back"]:
            await message.answer(t["select_subcategory"], reply_markup=kb.get_subcategories_keyboard(user_id, category, curr, language=lang))
            await state.set_state(UserStates.waiting_for_text if category in ["Passwords", "Contacts"] else UserStates.waiting_for_file)
            return
        cat_db.delete_subcategory(user_id, category, subcat, curr)
        from app.utils.file_utils import get_folder_path
        full = get_folder_path(user_id, category, sub_path + [subcat] if sub_path else [subcat])
        if os.path.exists(full): shutil.rmtree(full)
        await message.answer(t["subcategory_deleted"].format(subcat), reply_markup=kb.get_subcategories_keyboard(user_id, category, curr, language=lang))
        await state.set_state(UserStates.waiting_for_text if category in ["Passwords", "Contacts"] else UserStates.waiting_for_file)
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A", "N/A", "N/A", "delete_subcategory", str(e))
@user_router.message(UserStates.waiting_for_file, F.document | F.photo | F.video | F.audio)
async def handle_file(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        if user_id not in user_selections:
            await message.answer(t["start_over"])
            return
        category = user_selections[user_id]["category"]
        sub_path = user_selections[user_id]["subcategory_path"]
        if VERSION == "commercial" and get_user_storage_usage(user_id) >= db.get_storage_limit(user_id):
            await message.answer("⚠️ Full. Buy more: /storage")
            return
        if message.document:
            f = message.document; f_id = f.file_id; f_name = f.file_name; f_ext = f_name.split('.')[-1].lower() if '.' in f_name else ""
        elif message.photo:
            f = message.photo[-1]; f_id = f.file_id; f_name = f"photo_{f.file_unique_id}.jpg"; f_ext = "jpg"
        elif message.video:
            f = message.video; f_id = f.file_id; f_name = f"video_{f.file_unique_id}.mp4"; f_ext = "mp4"
        elif message.audio:
            f = message.audio; f_id = f.file_id; f_name = f"audio_{f.file_unique_id}.mp3"; f_ext = "mp3"
        else: return
        allowed = main_categories[category]["extensions"]
        if f_ext not in allowed:
            await message.answer(t["invalid_file_type"].format(', '.join(allowed)))
            return
        from app.utils.file_utils import get_folder_path
        full = get_folder_path(user_id, category, sub_path)
        os.makedirs(full, exist_ok=True)
        f_p = os.path.join(full, f_name)
        f_obj = await message.bot.get_file(f_id)
        await message.bot.download_file(f_obj.file_path, f_p)
        await message.answer(t["file_saved_msg"].format(f_name))
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A", "N/A", "N/A", "handle_file", str(e))
        if VERSION == "commercial": await notify_admin(message.bot, message.from_user.id, message.from_user.username or "N/A", "handle_file", str(e))
        await message.answer("⚠️ Error.")
@user_router.callback_query(FileAction.filter(F.action == "view"))
async def view_files(callback: CallbackQuery, callback_data: FileAction):
    try:
        user_id = callback.from_user.id
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        category = callback_data.category
        subcat = callback_data.subcategory
        from app.utils.file_utils import get_folder_path
        full = get_folder_path(user_id, category, subcat)
        if not os.path.exists(full):
            await callback.message.answer(t["no_files"])
            await callback.answer()
            return
        files = [f for f in os.listdir(full) if os.path.isfile(os.path.join(full, f))]
        if not files:
            await callback.message.answer(t["no_files"])
            await callback.answer()
            return
        for file in files:
            f_p = os.path.join(full, file)
            if file.endswith('.txt'):
                with open(f_p, 'r', encoding='utf-8') as f: content = f.read()
                if len(content) > 4000:
                    chunks = [content[i:i+4000] for i in range(0, len(content), 4000)]
                    for idx, chunk in enumerate(chunks): await callback.message.answer(f"📄 {file} ({idx+1}/{len(chunks)}):\n\n{chunk}")
                else: await callback.message.answer(f"📄 {file}:\n\n{content}")
            else: await callback.message.answer_document(FSInputFile(f_p))
        await callback.answer()
    except Exception as e:
        log_error_to_db(callback.from_user.id, callback.from_user.username or "N/A", "N/A", "N/A", "view_files", str(e))
        await callback.answer()
@user_router.callback_query(FileAction.filter(F.action == "delete_menu"))
async def delete_files_menu(callback: CallbackQuery, callback_data: FileAction):
    try:
        user_id = callback.from_user.id
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        category = callback_data.category
        subcat = callback_data.subcategory
        from app.utils.file_utils import get_folder_path
        full = get_folder_path(user_id, category, subcat)
        if not os.path.exists(full):
            await callback.message.answer(t["no_files"])
            await callback.answer()
            return
        files = [f for f in os.listdir(full) if os.path.isfile(os.path.join(full, f))]
        if not files:
            await callback.message.answer(t["no_files"])
            await callback.answer()
            return
        buttons = []
        row = []
        for file in files:
            row.append(InlineKeyboardButton(text=f"🗑️ {file}", callback_data=FileAction(action="delete_file", category=category, subcategory=subcat, filename=file).pack()))
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row: buttons.append(row)
        buttons.append([InlineKeyboardButton(text=t["delete_all"], callback_data=FileAction(action="delete_all", category=category, subcategory=subcat).pack())])
        await callback.message.answer(t["select_file_delete"], reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        await callback.answer()
    except Exception as e:
        log_error_to_db(callback.from_user.id, callback.from_user.username or "N/A", "N/A", "N/A", "delete_files_menu", str(e))
        await callback.answer()
@user_router.callback_query(FileAction.filter(F.action == "delete_file"))
async def delete_file_handler(callback: CallbackQuery, callback_data: FileAction):
    try:
        user_id = callback.from_user.id
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        category = callback_data.category
        subcat = callback_data.subcategory
        filename = callback_data.filename
        from app.utils.file_utils import get_folder_path
        full = get_folder_path(user_id, category, subcat)
        f_p = os.path.join(full, filename)
        if os.path.exists(f_p):
            os.remove(f_p)
            await callback.message.answer(t["deleted_msg"].format(filename))
            try:
                await callback.message.delete()
            except:
                pass
        else:
            await callback.message.answer(t["no_files"])
        await callback.answer()
    except Exception as e:
        log_error_to_db(callback.from_user.id, callback.from_user.username or "N/A", "N/A", "N/A", "delete_file", str(e))
        await callback.answer()
@user_router.callback_query(FileAction.filter(F.action == "delete_all"))
async def delete_all_files_handler(callback: CallbackQuery, callback_data: FileAction):
    try:
        user_id = callback.from_user.id
        lang = db.get_language(user_id) or "English"
        t = translations[lang]
        category = callback_data.category
        subcat = callback_data.subcategory
        from app.utils.file_utils import delete_all_files
        count = delete_all_files(user_id, category, subcat)
        await callback.message.answer(t["deleted_count"].format(count))
        try:
            await callback.message.delete()
        except:
            pass
        await callback.answer()
    except Exception as e:
        log_error_to_db(callback.from_user.id, callback.from_user.username or "N/A", "N/A", "N/A", "delete_all_files", str(e))
        await callback.answer()
