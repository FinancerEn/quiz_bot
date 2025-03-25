import os
from typing import Optional
from aiogram import Router, F
from aiogram.types import FSInputFile, CallbackQuery, Message
from database.models import OrderFSM
from filters.chat_types import ChatTypeFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# импорт админа
from dotenv import load_dotenv

# Кастомные
from kbds import inline
from text_message import text


load_dotenv()

GROUP_ID_ENV = os.getenv("GROUP_ID")
GROUP_ID: Optional[int] = (
    int(GROUP_ID_ENV) if GROUP_ID_ENV and GROUP_ID_ENV.isdigit() else None
)

dop_user_private_router = Router()
dop_user_private_router.message.filter(ChatTypeFilter(['private']))


# Хендлеры финального блока бота
@dop_user_private_router.callback_query(F.data.startswith('final_catalog'))
async def handler_final(callback: CallbackQuery):
    if callback.message is None:
        await callback.answer("Ошибка: Не удалось обработать запрос.", show_alert=True)
        return

    catalog_link = "https://www.avito.ru/irkutsk/nedvizhimost"
    message_text = text.sample_url_text

    # Создаём inline-кнопку со ссылкой
    link_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Открыть каталог", url=catalog_link)],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="return_")],
        ]
    )
    await callback.message.answer(
        message_text,
        parse_mode='Markdown',
        disable_web_page_preview=True,
        reply_markup=link_button,
    )

    await callback.answer()


@dop_user_private_router.callback_query(F.data.startswith('final_updates'))
async def handler_updates(callback: CallbackQuery):
    if callback.message is None:
        await callback.answer("Ошибка: Не удалось обработать запрос.", show_alert=True)
        return

    group_link = "https://t.me/+DDiXtpAlb7AxZmIy"
    message_text = text.sample_url_text

    # Создаём inline-кнопку со ссылкой
    link_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Открыть группу", url=group_link)],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="return_")],
        ]
    )
    await callback.message.answer(
        message_text,
        parse_mode='Markdown',
        disable_web_page_preview=True,
        reply_markup=link_button,
    )

    await callback.answer()


@dop_user_private_router.callback_query(F.data.startswith('final_question'))
async def handler_question(callback: CallbackQuery):
    if callback.message is None:
        await callback.answer("Ошибка: Не удалось обработать запрос.", show_alert=True)
        return

    admin_link = "https://t.me/DebugDemon_101"
    message_text = text.sample_url_text

    # Создаём inline-кнопку со ссылкой
    link_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Задайте вопрос специалисту", url=admin_link)],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="return_")],
        ]
    )
    await callback.message.answer(
        message_text,
        parse_mode='Markdown',
        disable_web_page_preview=True,
        reply_markup=link_button,
    )

    await callback.answer()


@dop_user_private_router.callback_query(F.data.startswith('return_'))
async def handler_back(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            text.choice_text, reply_markup=inline.inline_final
        )
        await callback.answer()
