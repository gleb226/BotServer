import os
import shutil
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from app.keyboards import user_keyboards as kb
from app.common.config import main_categories, USER_FILES_DIR, translations, user_selections
from app.databases.categories_database import categories_database
from app.databases.user_database import user_database
from app.handlers.error_handler import log_error_to_db

user_router = Router()
cat_db = categories_database()
db = user_database()


class FileAction(CallbackData, prefix="f"):
    action: str
    category: str
    subcategory: str = ""
    filename: str = ""


class UserStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_text = State()
    waiting_for_subcategory_name = State()
    selecting_category = State()
    selecting_subcategory = State()
    deleting_subcategory = State()


@user_router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        user_selections[user_id] = {"category": None, "subcategory_path": []}

        await message.answer(
            translations["English"]["welcome"],
            reply_markup=kb.get_categories_keyboard()
        )
        await state.set_state(UserStates.selecting_category)

        db.add_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name if message.from_user.last_name else "",
            username=message.from_user.username if message.from_user.username else "",
            language_code=message.from_user.language_code if message.from_user.language_code else "unknown",
            is_premium=message.from_user.is_premium if hasattr(message.from_user, 'is_premium') else False,
            chat_id=message.chat.id,
            chat_type=message.chat.type
        )
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A",
                        message.from_user.first_name or "N/A", message.from_user.last_name or "N/A",
                        "/start", str(e))
        await message.answer("Function is currently unavailable. Please try again later.")


@user_router.message(UserStates.selecting_category)
async def select_category(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        category = message.text

        if category not in main_categories:
            await message.answer("Invalid category. Please select from the menu.")
            return

        user_selections[user_id] = {"category": category, "subcategory_path": []}

        buttons = [
            [
                InlineKeyboardButton(text="View Files", callback_data=FileAction(action="view", category=category, subcategory="").pack()),
                InlineKeyboardButton(text="Delete Files", callback_data=FileAction(action="delete_menu", category=category, subcategory="").pack())
            ]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(
            "Send files or manage subcategories",
            reply_markup=kb.get_subcategories_keyboard(user_id, category, "")
        )
        await message.answer("File actions:", reply_markup=markup)

        if category in ["Passwords", "Contacts"]:
            await state.set_state(UserStates.waiting_for_text)
        else:
            await state.set_state(UserStates.waiting_for_file)
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A",
                        message.from_user.first_name or "N/A", message.from_user.last_name or "N/A",
                        "select_category", str(e))
        await message.answer("Function is currently unavailable. Please try again later.")


@user_router.message(UserStates.waiting_for_text, F.text)
async def handle_text(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        text = message.text

        if text == "Add Subcategory":
            await message.answer(translations["English"]["enter_subcategory_name"], reply_markup=ReplyKeyboardRemove())
            await state.set_state(UserStates.waiting_for_subcategory_name)
            return

        if text == "Delete Subcategory":
            category = user_selections[user_id]["category"]
            subcategory_path = user_selections[user_id]["subcategory_path"]
            current_path = "/".join(subcategory_path) if subcategory_path else ""
            subcategories = cat_db.get_subcategories(user_id, category, current_path)

            if not subcategories:
                await message.answer(translations["English"]["no_subcategories"])
                return

            await message.answer(
                translations["English"]["select_subcategory_to_delete"],
                reply_markup=kb.get_delete_subcategories_keyboard(user_id, category, current_path)
            )
            await state.set_state(UserStates.deleting_subcategory)
            return

        if text == "Back to Menu":
            subcategory_path = user_selections[user_id]["subcategory_path"]
            if not subcategory_path:
                await message.answer(
                    translations["English"]["welcome"],
                    reply_markup=kb.get_categories_keyboard()
                )
                await state.set_state(UserStates.selecting_category)
            else:
                user_selections[user_id]["subcategory_path"].pop()
                category = user_selections[user_id]["category"]
                new_path = "/".join(user_selections[user_id]["subcategory_path"]) if user_selections[user_id]["subcategory_path"] else ""

                buttons = [
                    [
                        InlineKeyboardButton(text="View Files", callback_data=FileAction(action="view", category=category, subcategory=new_path).pack()),
                        InlineKeyboardButton(text="Delete Files", callback_data=FileAction(action="delete_menu", category=category, subcategory=new_path).pack())
                    ]
                ]
                markup = InlineKeyboardMarkup(inline_keyboard=buttons)

                await message.answer(
                    "Send files or manage subcategories",
                    reply_markup=kb.get_subcategories_keyboard(user_id, category, new_path)
                )
                await message.answer("File actions:", reply_markup=markup)
            return

        category = user_selections[user_id]["category"]
        subcategory_path = user_selections[user_id]["subcategory_path"]
        current_path = "/".join(subcategory_path) if subcategory_path else ""

        if cat_db.subcategory_exists(user_id, category, text, current_path):
            user_selections[user_id]["subcategory_path"].append(text)
            new_path = "/".join(user_selections[user_id]["subcategory_path"])

            buttons = [
                [
                    InlineKeyboardButton(text="View Files", callback_data=FileAction(action="view", category=category, subcategory=new_path).pack()),
                    InlineKeyboardButton(text="Delete Files", callback_data=FileAction(action="delete_menu", category=category, subcategory=new_path).pack())
                ]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)

            await message.answer(
                "Send files or manage subcategories",
                reply_markup=kb.get_subcategories_keyboard(user_id, category, new_path)
            )
            await message.answer("File actions:", reply_markup=markup)
            return

        if user_id not in user_selections:
            await message.answer("Please start over with /start")
            return

        category = user_selections[user_id]["category"]
        subcategory_path = user_selections[user_id]["subcategory_path"]

        category_path = main_categories[category]["path"]
        full_path = os.path.join(USER_FILES_DIR, str(user_id), category_path)

        if subcategory_path:
            for subcat in subcategory_path:
                full_path = os.path.join(full_path, subcat)

        os.makedirs(full_path, exist_ok=True)

        file_path = os.path.join(full_path, f"{category}.txt")

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(text + "\n")

        await message.answer("Text saved successfully!")
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A",
                        message.from_user.first_name or "N/A", message.from_user.last_name or "N/A",
                        "handle_text", str(e))
        await message.answer("Function is currently unavailable. Please try again later.")


@user_router.message(UserStates.waiting_for_file, F.text)
async def handle_file_text_commands(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        text = message.text

        if text == "Add Subcategory":
            await message.answer(translations["English"]["enter_subcategory_name"], reply_markup=ReplyKeyboardRemove())
            await state.set_state(UserStates.waiting_for_subcategory_name)
            return

        if text == "Delete Subcategory":
            category = user_selections[user_id]["category"]
            subcategory_path = user_selections[user_id]["subcategory_path"]
            current_path = "/".join(subcategory_path) if subcategory_path else ""
            subcategories = cat_db.get_subcategories(user_id, category, current_path)

            if not subcategories:
                await message.answer(translations["English"]["no_subcategories"])
                return

            await message.answer(
                translations["English"]["select_subcategory_to_delete"],
                reply_markup=kb.get_delete_subcategories_keyboard(user_id, category, current_path)
            )
            await state.set_state(UserStates.deleting_subcategory)
            return

        if text == "Back to Menu":
            subcategory_path = user_selections[user_id]["subcategory_path"]
            if not subcategory_path:
                await message.answer(
                    translations["English"]["welcome"],
                    reply_markup=kb.get_categories_keyboard()
                )
                await state.set_state(UserStates.selecting_category)
            else:
                user_selections[user_id]["subcategory_path"].pop()
                category = user_selections[user_id]["category"]
                new_path = "/".join(user_selections[user_id]["subcategory_path"]) if user_selections[user_id]["subcategory_path"] else ""

                buttons = [
                    [
                        InlineKeyboardButton(text="View Files", callback_data=FileAction(action="view", category=category, subcategory=new_path).pack()),
                        InlineKeyboardButton(text="Delete Files", callback_data=FileAction(action="delete_menu", category=category, subcategory=new_path).pack())
                    ]
                ]
                markup = InlineKeyboardMarkup(inline_keyboard=buttons)

                await message.answer(
                    "Send files or manage subcategories",
                    reply_markup=kb.get_subcategories_keyboard(user_id, category, new_path)
                )
                await message.answer("File actions:", reply_markup=markup)
            return

        category = user_selections[user_id]["category"]
        subcategory_path = user_selections[user_id]["subcategory_path"]
        current_path = "/".join(subcategory_path) if subcategory_path else ""

        if cat_db.subcategory_exists(user_id, category, text, current_path):
            user_selections[user_id]["subcategory_path"].append(text)
            new_path = "/".join(user_selections[user_id]["subcategory_path"])

            buttons = [
                [
                    InlineKeyboardButton(text="View Files", callback_data=FileAction(action="view", category=category, subcategory=new_path).pack()),
                    InlineKeyboardButton(text="Delete Files", callback_data=FileAction(action="delete_menu", category=category, subcategory=new_path).pack())
                ]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)

            await message.answer(
                "Send files or manage subcategories",
                reply_markup=kb.get_subcategories_keyboard(user_id, category, new_path)
            )
            await message.answer("File actions:", reply_markup=markup)
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A",
                        message.from_user.first_name or "N/A", message.from_user.last_name or "N/A",
                        "handle_file_text", str(e))


@user_router.message(UserStates.waiting_for_subcategory_name)
async def add_subcategory_finish(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        subcategory_name = message.text.strip()

        if user_id not in user_selections:
            await message.answer("Please start over with /start")
            return

        category = user_selections[user_id]["category"]
        subcategory_path = user_selections[user_id]["subcategory_path"]
        parent_path = "/".join(subcategory_path) if subcategory_path else ""

        if cat_db.add_subcategory(user_id, category, subcategory_name, parent_path):
            buttons = [
                [
                    InlineKeyboardButton(text="View Files", callback_data=FileAction(action="view", category=category, subcategory=parent_path).pack()),
                    InlineKeyboardButton(text="Delete Files", callback_data=FileAction(action="delete_menu", category=category, subcategory=parent_path).pack())
                ]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)

            await message.answer(
                translations["English"]["subcategory_added"].format(subcategory_name),
                reply_markup=kb.get_subcategories_keyboard(user_id, category, parent_path)
            )
            await message.answer("File actions:", reply_markup=markup)
        else:
            await message.answer(
                "Subcategory already exists!",
                reply_markup=kb.get_subcategories_keyboard(user_id, category, parent_path)
            )

        if category in ["Passwords", "Contacts"]:
            await state.set_state(UserStates.waiting_for_text)
        else:
            await state.set_state(UserStates.waiting_for_file)
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A",
                        message.from_user.first_name or "N/A", message.from_user.last_name or "N/A",
                        "add_subcategory", str(e))
        await message.answer("Function is currently unavailable. Please try again later.")


@user_router.message(UserStates.deleting_subcategory)
async def delete_subcategory_confirm(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        subcategory = message.text

        if user_id not in user_selections:
            await message.answer("Please start over with /start")
            return

        category = user_selections[user_id]["category"]
        current_path = ""

        if subcategory == "Back to Menu":
            await message.answer(
                "Send files or manage subcategories",
                reply_markup=kb.get_subcategories_keyboard(user_id, category, current_path)
            )
            if category in ["Passwords", "Contacts"]:
                await state.set_state(UserStates.waiting_for_text)
            else:
                await state.set_state(UserStates.waiting_for_file)
            return

        cat_db.delete_subcategory(user_id, category, subcategory, current_path)

        category_path = main_categories[category]["path"]
        full_path = os.path.join(USER_FILES_DIR, str(user_id), category_path, subcategory)

        if os.path.exists(full_path):
            shutil.rmtree(full_path)

        await message.answer(
            translations["English"]["subcategory_deleted"].format(subcategory),
            reply_markup=kb.get_subcategories_keyboard(user_id, category, current_path)
        )
        if category in ["Passwords", "Contacts"]:
            await state.set_state(UserStates.waiting_for_text)
        else:
            await state.set_state(UserStates.waiting_for_file)
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A",
                        message.from_user.first_name or "N/A", message.from_user.last_name or "N/A",
                        "delete_subcategory", str(e))
        await message.answer("Function is currently unavailable. Please try again later.")


@user_router.message(UserStates.waiting_for_file, F.document | F.photo | F.video | F.audio)
async def handle_file(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id

        if user_id not in user_selections:
            await message.answer("Please start over with /start")
            return

        category = user_selections[user_id]["category"]
        subcategory_path = user_selections[user_id]["subcategory_path"]

        if message.document:
            file = message.document
            file_id = file.file_id
            file_name = file.file_name
            file_ext = file_name.split('.')[-1].lower() if '.' in file_name else ""
        elif message.photo:
            file = message.photo[-1]
            file_id = file.file_id
            file_name = f"photo_{file.file_unique_id}.jpg"
            file_ext = "jpg"
        elif message.video:
            file = message.video
            file_id = file.file_id
            file_name = f"video_{file.file_unique_id}.mp4"
            file_ext = "mp4"
        elif message.audio:
            file = message.audio
            file_id = file.file_id
            file_name = f"audio_{file.file_unique_id}.mp3"
            file_ext = "mp3"
        else:
            return

        allowed_extensions = main_categories[category]["extensions"]

        if file_ext not in allowed_extensions:
            await message.answer(f"Invalid file type. Allowed: {', '.join(allowed_extensions)}")
            return

        category_path = main_categories[category]["path"]
        full_path = os.path.join(USER_FILES_DIR, str(user_id), category_path)

        if subcategory_path:
            for subcat in subcategory_path:
                full_path = os.path.join(full_path, subcat)

        os.makedirs(full_path, exist_ok=True)

        file_path = os.path.join(full_path, file_name)

        file_obj = await message.bot.get_file(file_id)
        await message.bot.download_file(file_obj.file_path, file_path)

        await message.answer(f"File saved: {file_name}")
    except Exception as e:
        log_error_to_db(message.from_user.id, message.from_user.username or "N/A",
                        message.from_user.first_name or "N/A", message.from_user.last_name or "N/A",
                        "handle_file", str(e))
        await message.answer("Function is currently unavailable. Please try again later.")


@user_router.callback_query(FileAction.filter(F.action == "view"))
async def view_files(callback: CallbackQuery, callback_data: FileAction):
    try:
        user_id = callback.from_user.id
        category = callback_data.category
        subcategory = callback_data.subcategory

        category_path = main_categories[category]["path"]
        full_path = os.path.join(USER_FILES_DIR, str(user_id), category_path)
        if subcategory:
            full_path = os.path.join(full_path, subcategory)

        if not os.path.exists(full_path):
            await callback.message.answer("No files found!")
            await callback.answer()
            return

        files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

        if not files:
            await callback.message.answer("No files found!")
            await callback.answer()
            return

        for file in files:
            file_path = os.path.join(full_path, file)
            if file.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if len(content) > 4000:
                    chunks = [content[i:i+4000] for i in range(0, len(content), 4000)]
                    for idx, chunk in enumerate(chunks):
                        await callback.message.answer(f"{file} (part {idx+1}/{len(chunks)}):\n\n{chunk}")
                else:
                    await callback.message.answer(f"{file}:\n\n{content}")
            else:
                await callback.message.answer_document(FSInputFile(file_path))

        await callback.answer()
    except Exception as e:
        log_error_to_db(callback.from_user.id, callback.from_user.username or "N/A",
                        callback.from_user.first_name or "N/A", callback.from_user.last_name or "N/A",
                        "view_files", str(e))
        await callback.message.answer("Function is currently unavailable. Please try again later.")
        await callback.answer()


@user_router.callback_query(FileAction.filter(F.action == "delete_menu"))
async def delete_files_menu(callback: CallbackQuery, callback_data: FileAction):
    try:
        user_id = callback.from_user.id
        category = callback_data.category
        subcategory = callback_data.subcategory

        category_path = main_categories[category]["path"]
        full_path = os.path.join(USER_FILES_DIR, str(user_id), category_path)
        if subcategory:
            full_path = os.path.join(full_path, subcategory)

        if not os.path.exists(full_path):
            await callback.message.answer("No files found!")
            await callback.answer()
            return

        files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

        if not files:
            await callback.message.answer("No files found!")
            await callback.answer()
            return

        buttons = []
        row = []
        for file in files:
            row.append(InlineKeyboardButton(text=file, callback_data=FileAction(action="delete_file", category=category, subcategory=subcategory, filename=file).pack()))
            if len(row) == 2:
                buttons.append(row)
                row = []

        if row:
            buttons.append(row)

        buttons.append([InlineKeyboardButton(text="Delete All", callback_data=FileAction(action="delete_all", category=category, subcategory=subcategory).pack())])

        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.answer("Select a file to delete or delete all:", reply_markup=markup)
        await callback.answer()
    except Exception as e:
        log_error_to_db(callback.from_user.id, callback.from_user.username or "N/A",
                        callback.from_user.first_name or "N/A", callback.from_user.last_name or "N/A",
                        "delete_files_menu", str(e))
        await callback.message.answer("Function is currently unavailable. Please try again later.")
        await callback.answer()


@user_router.callback_query(FileAction.filter(F.action == "delete_file"))
async def delete_file(callback: CallbackQuery, callback_data: FileAction):
    try:
        user_id = callback.from_user.id
        category = callback_data.category
        subcategory = callback_data.subcategory
        filename = callback_data.filename

        category_path = main_categories[category]["path"]
        full_path = os.path.join(USER_FILES_DIR, str(user_id), category_path)
        if subcategory:
            full_path = os.path.join(full_path, subcategory)

        file_path = os.path.join(full_path, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            await callback.message.answer(f"Deleted: {filename}")
            try:
                await callback.message.delete()
            except:
                pass
        else:
            await callback.message.answer("File not found!")

        await callback.answer()
    except Exception as e:
        log_error_to_db(callback.from_user.id, callback.from_user.username or "N/A",
                        callback.from_user.first_name or "N/A", callback.from_user.last_name or "N/A",
                        "delete_file", str(e))
        await callback.message.answer("Function is currently unavailable. Please try again later.")
        await callback.answer()


@user_router.callback_query(FileAction.filter(F.action == "delete_all"))
async def delete_all_files(callback: CallbackQuery, callback_data: FileAction):
    try:
        user_id = callback.from_user.id
        category = callback_data.category
        subcategory = callback_data.subcategory

        category_path = main_categories[category]["path"]
        full_path = os.path.join(USER_FILES_DIR, str(user_id), category_path)
        if subcategory:
            full_path = os.path.join(full_path, subcategory)

        if not os.path.exists(full_path):
            await callback.message.answer("No files found!")
            await callback.answer()
            return

        files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

        deleted_count = 0
        for file in files:
            file_path = os.path.join(full_path, file)
            try:
                os.remove(file_path)
                deleted_count += 1
            except:
                pass

        await callback.message.answer(f"Deleted {deleted_count} files")
        try:
            await callback.message.delete()
        except:
            pass
        await callback.answer()
    except Exception as e:
        log_error_to_db(callback.from_user.id, callback.from_user.username or "N/A",
                        callback.from_user.first_name or "N/A", callback.from_user.last_name or "N/A",
                        "delete_all_files", str(e))
        await callback.message.answer("Function is currently unavailable. Please try again later.")
        await callback.answer()