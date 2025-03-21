from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class ServiceCallback(CallbackData, prefix="property_"):
    name: str


inline_keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ «Пройти тест»", callback_data="take_test")],
        [InlineKeyboardButton(text="❌ «Не интересно»", callback_data="not_interesting")],
    ],
)

inline_type_of_property = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1️⃣ «Квартира»", callback_data="property_apartment")],
        [InlineKeyboardButton(text="2️⃣ «Дом»", callback_data="property_house")],
        [InlineKeyboardButton(text="3️⃣ «Коммерческая недвижимость»", callback_data="property_commercial")],
        [InlineKeyboardButton(text="2️⃣ «Назад к началу»", callback_data="Back_beginning")],
    ],
)
