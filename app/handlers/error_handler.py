from datetime import datetime
from functools import wraps
from app.databases.mongodb_client import errors_collection


def log_error_to_db(user_id: int, username: str, firstname: str, lastname: str, command: str, error_message: str):
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


def error_handler(command: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(message):
            try:
                return await func(message)
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
                await message.answer("Function is currently unavailable. Please try again later.")

        return wrapper

    return decorator
