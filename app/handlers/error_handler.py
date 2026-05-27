from datetime import datetime
from functools import wraps
from app.common.config import DATABASE_TYPE, ADMIN_ID, VERSION

async def notify_admin(bot, user_id: int, username: str, command: str, error_message: str):
    try:
        text = (
            f"❌ <b>Error Report</b>\n\n"
            f"👤 <b>User ID:</b> {user_id}\n"
            f"👤 <b>Username:</b> @{username}\n"
            f"🤖 <b>Command:</b> {command}\n"
            f"⚠️ <b>Error:</b> <code>{error_message}</code>\n"
            f"🕒 <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"🏢 <b>Version:</b> {VERSION}"
        )
        await bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="HTML")
    except Exception as e:
        print(f"Failed to notify admin: {e}")

def log_error_to_db(user_id: int, username: str, firstname: str, lastname: str, command: str, error_message: str):
    if DATABASE_TYPE == "sqlite":
        # We can still log to a local file or just ignore for sqlite
        pass
    else:
        try:
            from app.databases.mongodb_client import errors_collection
            error_data = {
                "user_id": user_id,
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "command": command,
                "error_message": error_message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            errors_collection.insert_one(error_data)
        except Exception as e:
            print(f"Failed to log error to MongoDB: {e}")

def error_handler(command: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(message, *args, **kwargs):
            try:
                return await func(message, *args, **kwargs)
            except Exception as e:
                user = message.from_user
                log_error_to_db(
                    user_id=user.id,
                    username=user.username if user.username else "N/A",
                    firstname=user.first_name if user.first_name else "N/A",
                    lastname=user.last_name if user.last_name else "N/A",
                    command=command,
                    error_message=str(e)
                )
                if VERSION == "commercial":
                    await notify_admin(
                        bot=message.bot,
                        user_id=user.id,
                        username=user.username or "N/A",
                        command=command,
                        error_message=str(e)
                    )
                await message.answer("Function is currently unavailable. Please try again later.")
        return wrapper
    return decorator
