import asyncio
from aiogram import Bot, Dispatcher
from app.databases.user_database import user_database
from app.databases.categories_database import categories_database
from app.handlers.user_handlers import user_router
from app.common.token import TOKEN

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
