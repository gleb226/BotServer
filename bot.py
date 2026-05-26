import asyncio
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.databases.user_database import user_database
from app.databases.categories_database import categories_database
from app.handlers.user_handlers import user_router

# Determine base directory
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.realpath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    # If not in env, we might be in the middle of installation or misconfigured
    pass

async def main():
    if not TOKEN:
        print("Error: BOT_TOKEN not found in .env file.")
        return

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # Initialize databases
    user_db = user_database()
    cat_db = categories_database()

    dp.include_router(user_router)

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        pass
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Critical error: {e}")
        input("Press Enter to exit...")
