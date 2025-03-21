from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, CallbackQuery, Message
from filters.chat_types import ChatTypeFilter
# Импорты для машины состояний
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Импорт Bold для того что бы сделать шрифт жирным
# from aiogram.utils.formatting import Bold

# Кастомные
from text_message import text
from kbds import inline


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


class UserState(StatesGroup):
    type_property = State()  # Тип недвижимости
    budget = State()  # Бюджет
    district = State()  # Район
    specifications = State()  # Характеристики
    contacts = State()  # Контакты
    name = State()  # Имя


@user_private_router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    user_name = message.from_user.first_name if message.from_user else "Вы"
    user_id = message.from_user.id if message.from_user else 0  # ID юзера

    # Сохраняем данные в FSM
    await state.update_data(user_id=user_id, user_name=user_name)

    photo = FSInputFile("images/start_image.webp")
    await message.answer_photo(photo)
    await message.answer(f"{user_name} {text.greeting}", reply_markup=inline.inline_keyboard_main)


@user_private_router.callback_query(F.data.startswith("take_test"))
async def handle_start_test(callback: CallbackQuery, state: FSMContext):
    if not callback.data:
        return

    type_housing = callback.data.split("_")[1]
    if isinstance(callback.message, Message):
        await state.update_data(type_property=type_housing)
        await state.set_state(UserState.budget)

        await callback.message.edit_text(
            text.text_type_of_property, reply_markup=inline.inline_type_of_property
        )
        await callback.answer()


@user_private_router.message(UserState.budget, F.text)
async def handle_save_wishes(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await state.set_state(UserState.district)
    await message.answer('💰 Какой бюджет ты рассматриваешь?')


# # Последний хендлер который:
# # 1)Сохраняет имя 2)Сохраняет данные в гугл таблицу
# @user_private_router.message(UserState.name, F.text)
# async def handle_name(message: Message, state: FSMContext):
#     """Последний этап сбора данных: ввод имени"""
#     await state.update_data(name=message.text)

#     # Сохраняем все данные в Google Sheets
#     await save_to_google_sheets(state)

#     await message.answer("✅ Ваши данные успешно сохранены! Спасибо за участие.")

#     # Завершаем FSM
#     await state.clear()
