import os

from store_telega.crud import create_db
from store_telega.handlers import (
    user_handlers,
    other_handlers,
)
from store_telega.keyboards.set_menu import set_main_menu
from config.config import load_config

import asyncio
from aiogram import Bot, Dispatcher


config = load_config()

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = config.tg_bot.token

# Подключаемся к базе данных
create_db()


async def main():

    # Создаем объекты бота и диспетчера
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Запускаем поллинг
if __name__ == "__main__":
    asyncio.run(main())
