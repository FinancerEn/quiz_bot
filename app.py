# Импорты Питона.
import asyncio
import os

# Импорты фреймворка.
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# # Импорты Middleware для базы данных..
# from middlewares.db import DataBaseSession
# from database.engine import create_db, drop_db, session_maker

# Подключаем наш кастомный файл взаимодействия с пользователем.
from handlers.user_private import user_private_router


load_dotenv()

# Указанны то что мы хотим что бы приходило из серверов телеграмма(те методы).
# Затем указываем эту нашу переменную ALLOWED_UPDATES в main, остальное приходить не будет.
ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения 'TOKEN' не задана.")

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Подключение маршрутов
dp.include_router(user_private_router)


async def on_shutdown(bot):
    print("бот лег")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
