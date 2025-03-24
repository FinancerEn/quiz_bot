from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class ServiceCallback(CallbackData, prefix="property_"):
    name: str


class BudgetCallback(CallbackData, prefix="budget_"):
    name: str


class DistrictCallback(CallbackData, prefix="district_"):
    name: str


class SpecificationsCallback(CallbackData, prefix="specifications_"):
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
    ],
)

inline_budget = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💵 «До 3 млн ₽»", callback_data="budget_low")],
        [InlineKeyboardButton(text="💵 «3–6 млн ₽»", callback_data="budget_medium")],
        [InlineKeyboardButton(text="💵 «6–10 млн ₽»", callback_data="budget_high")],
        [InlineKeyboardButton(text="💵 «Более 10 млн ₽»", callback_data="budget_commercial_2")],
        [InlineKeyboardButton(text="🔙 Назад к началу теста", callback_data="back_")],
    ],
)

inline_district = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏙 «Центр»", callback_data="district_center")],
        [InlineKeyboardButton(text="«Кировский»", callback_data="district_kirovskiy")],
        [InlineKeyboardButton(text="«Куйбышевский»", callback_data="district_kuibyshevskiy")],
        [InlineKeyboardButton(text="«Ленинский»", callback_data="district_leninskiy")],
        [InlineKeyboardButton(text="«Октябрьский»", callback_data="district_oktyabrskiy")],
        [InlineKeyboardButton(text="«Свердловский»", callback_data="district_sverdlovskiy")],
        [InlineKeyboardButton(text="«За городом»", callback_data="district_outside")],
        [InlineKeyboardButton(text="🔙 Назад к началу теста", callback_data="back_")],
    ],
)


inline_specifications = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📝 «Написать свой вариант»", callback_data="specifications_mine")],
        [InlineKeyboardButton(text="✅ «Балкон»", callback_data="specifications_balcony")],
        [InlineKeyboardButton(text="✅ «Парковка»", callback_data="specifications_parking")],
        [InlineKeyboardButton(text="✅ «Новая отделка»", callback_data="specifications_newfinish")],
        [InlineKeyboardButton(text="✅ «Рядом с парком»", callback_data="specifications_park")],
        [InlineKeyboardButton(text="✅ «Большая кухня»", callback_data="specifications_big_kitchen")],
        [InlineKeyboardButton(text="⏭️ «Далее»", callback_data="specifications_next")],
        [InlineKeyboardButton(text="🔙 Назад к началу теста", callback_data="back_")],
    ],
)

inline_final = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📜 Посмотреть каталог", callback_data="final_")],
        [InlineKeyboardButton(text="🔔 Подписаться на обновления", callback_data="final_")],
        [InlineKeyboardButton(text="🆘 Задать вопрос", callback_data="final_")],
    ],
)

inline_keyboard_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад к началу теста", callback_data="back_")],
    ]
)
