import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.databases.user_database import user_database
from app.databases.categories_database import categories_database
from app.handlers.user_handlers import user_router

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env file")

bot = Bot(token=TOKEN)

dp = Dispatcher()
user_db = user_database()
cat_db = categories_database()

dp.include_router(user_router)


async def main():
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        pass
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
