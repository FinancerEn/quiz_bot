from aiogram import Router
from aiogram.types import Message

chat_info_router = Router()


@chat_info_router.message()
async def get_chat_id(message: Message):
    if message.text == "/getchatid":
        await message.answer(f"ID этой группы: {message.chat.id}")
