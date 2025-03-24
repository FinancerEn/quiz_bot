import os
from typing import Optional
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, CallbackQuery, Message
from database.models import OrderFSM
from filters.chat_types import ChatTypeFilter
# Импорты для машины состояний
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# импорт админа
from dotenv import load_dotenv

# Импорт Bold для того что бы сделать шрифт жирным
from aiogram.utils.formatting import Bold

# Кастомные
from text_message import text
from kbds import inline

load_dotenv()

GROUP_ID_ENV = os.getenv("GROUP_ID")
GROUP_ID: Optional[int] = (
    int(GROUP_ID_ENV) if GROUP_ID_ENV and GROUP_ID_ENV.isdigit() else None
)

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


class UserState(StatesGroup):
    start = State()  # Интересно не интересно
    type_property = State()  # Тип недвижимости
    budget = State()  # Бюджет
    district = State()  # Район
    specifications = State()  # Характеристики
    custom_specification = State()  # Свой вариант
    contacts = State()  # Контакты
    name = State()  # Имя


# Словари соответствий
START_NAMES = {
    "test": "✅ «Пройти тест»",
    "interesting": "❌ «Не интересно»",
}

PROPERTY_NAMES = {
    "apartment": "1️⃣ Квартира",
    "commercial": "2️⃣ Коммерческая недвижимость",
    "house": "3️⃣ Дом",
    "room": "4️⃣ Комната"
}

BUDGET_NAMES = {
    "low": "💵 «До 3 млн ₽»",
    "medium": "💵 «3–6 млн ₽»",
    "high": "💵 «6–10 млн ₽»",
    "high_xx": "💵 «Более 10 млн ₽»"
}

DISTRICT_NAMES = {
    "center": "🏙 «Центр»",
    "kirovskiy": "«Кировский»",
    "kuibyshevskiy": "«Куйбышевский»",
    "leninskiy": "«Ленинский»",
    "oktyabrskiy": "«Октябрьский»",
    "sverdlovskiy": "«Свердловский»",
    "outside": "«За городом»"
}

SPECIFICATIONS_NAMES = {
    "balcony": "✅ «Балкон»",
    "parking": "✅ «Парковка»",
    "newfinish": "✅ «Новая отделка»",
    "park": "✅ «Рядом с парком»",
    "next": "✅ «Большая кухня»"
}


@user_private_router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    user_name = message.from_user.first_name if message.from_user else 'Вы'
    user_id = message.from_user.id if message.from_user else 0

    # Сохраняем данные в FSM
    await state.update_data(user_id=user_id, user_name=user_name)

    # Устанавливаем начальное состояние
    await state.set_state(UserState.type_property)

    photo = FSInputFile('images/start_image.webp')
    await message.answer_photo(photo)
    await message.answer(f"{user_name} {text.greeting}", reply_markup=inline.inline_keyboard_main)


@user_private_router.callback_query(F.data.startswith("take_test"))
async def handle_start_test(callback: CallbackQuery, state: FSMContext):
    if not callback.data:
        return
    type_start = callback.data.split("_")[1]
    user_choice = START_NAMES.get(type_start, "❓ Неизвестно")

    if isinstance(callback.message, Message):
        await state.update_data(start=user_choice)
        await state.set_state(UserState.type_property)

        await callback.message.edit_text(
            text.text_type_of_property, reply_markup=inline.inline_type_of_property
        )
        await callback.answer()


@user_private_router.callback_query(F.data.startswith('property_'))
async def handler_property_text(callback: CallbackQuery, state: FSMContext):
    if not callback.data:
        return
    type_housing = callback.data.split('_')[1]
    user_choice = PROPERTY_NAMES.get(type_housing, "❓ Неизвестно")

    texts = Bold(f"💰 Какой бюджет ты рассматриваешь? \n\nВы выбрали: {user_choice}")

    await state.update_data(type_property=user_choice)
    await state.set_state(UserState.budget)
    if isinstance(callback.message, Message):
        await callback.message.edit_text(texts.as_html(), parse_mode="HTML",
                                         reply_markup=inline.inline_budget)
        await callback.answer()


@user_private_router.callback_query(F.data.startswith('budget_'))
async def handler_budget(callback: CallbackQuery, state: FSMContext):
    if not callback.data:
        return
    type_budget = callback.data.split('_')[1]
    user_choice = BUDGET_NAMES.get(type_budget, "❓ Неизвестно")

    texts = Bold(f"📍 В каком районе вы хотите жить? \n\nВы выбрали: {user_choice}")
    await state.update_data(budget=user_choice)
    await state.set_state(UserState.district)
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            texts.as_html(), parse_mode="HTML", reply_markup=inline.inline_district
        )
        await callback.answer()


@user_private_router.callback_query(F.data.startswith('district_'))
async def handle_district(callback: CallbackQuery, state: FSMContext):
    if not callback.data:
        return
    type_district = callback.data.split('_')[1]
    user_choice = DISTRICT_NAMES.get(type_district, "❓ Неизвестно")

    texts = Bold(f"🔎 Что для тебя важно при выборе жилья? (Выбери до 3 пунктов)"
                 f"\n\nВы выбрали: {user_choice}")
    await state.update_data(district=user_choice)
    await state.set_state(UserState.specifications)
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            texts.as_html(), parse_mode="HTML", reply_markup=inline.inline_specifications
        )
        await callback.answer()


@user_private_router.callback_query(F.data.startswith('specifications_'))
async def handle_specifications(callback: CallbackQuery, state: FSMContext):
    if not callback.data:
        return

    selected_option = callback.data.split('_')[1]
    user_choice = SPECIFICATIONS_NAMES.get(selected_option, "❓ Неизвестно")

    if isinstance(callback.message, Message):
        # Обновляем список характеристик
        user_data = await state.get_data()
        selected_specs = user_data.get('selected_specifications', [])

        # Добавляем или удаляем характеристику
        # Проверяем, что user_choice не None
        if user_choice and user_choice != "❓ Неизвестно":
            if user_choice in selected_specs:
                selected_specs.remove(user_choice)
            else:
                selected_specs.append(user_choice)

        await state.update_data(selected_specifications=selected_specs)

        if selected_option == 'mine':
            await state.set_state(UserState.custom_specification)
            await callback.message.edit_text('✍️ Введите свой вариант', reply_markup=inline.inline_keyboard_back)
            await callback.answer()
            return

        if selected_option == "next":
            await state.set_state(UserState.contacts)
            await callback.message.edit_text('📞 Теперь укажите ваш номер телефона и удобный способ связи',
                                             reply_markup=inline.inline_keyboard_back)
            await callback.answer()
            return

        selected_specs = [spec for spec in selected_specs if isinstance(spec, str)]
        await callback.answer(f"Вы выбрали: {', '.join(selected_specs)}")


@user_private_router.message(UserState.custom_specification, F.text)
async def handler_your_version(message: Message, state: FSMContext):
    await state.update_data(custom_specification=message.text)
    await state.set_state(UserState.contacts)
    await message.answer(
        '📞 Теперь укажите ваш номер телефона и удобный способ связи',
        reply_markup=inline.inline_keyboard_back
    )


@user_private_router.message(UserState.contacts, F.text)
async def handler_custom_specification_contacts(message: Message, state: FSMContext):
    """Обрабатывает ввод контактов и завершает оформление заказа"""

    # Получаем текущее состояние пользователя
    current_state = await state.get_state()

    # Если пользователь вводил свой вариант, сохраняем его, иначе только контакт
    if current_state == "UserState:custom_specification":
        await state.update_data(custom_specification=message.text)
    else:
        await state.update_data(contacts=message.text)

    # !!! Теперь снова получаем обновлённые данные !!!
    user_data = await state.get_data()
    print(f"Данные из FSM: {user_data}")  # Логирование данных

    # Преобразуем данные в удобочитаемый формат
    start = user_data.get("start", "❌ «Не интересно»")
    type_property = user_data.get("type_property", "Не указано")
    budget = user_data.get("budget", "Не указано")
    district = user_data.get("district", "Не указано")
    specifications = ", ".join(user_data.get("selected_specifications", []))
    custom_specification = user_data.get("custom_specification", "")  # Теперь не затирается!
    contacts = user_data.get("contacts", "")

    # Если пользователь не вводил свой вариант, оставляем поле пустым
    if "custom_specification" not in user_data:
        custom_specification = ""

    # Заполняем данные о заказе
    order = OrderFSM(
        user_id=message.from_user.id if message.from_user else 0,
        user_name=message.from_user.full_name if message.from_user else "Аноним",
        start=start,
        type_property=type_property,
        budget=budget,
        district=district,
        specifications=specifications,
        custom_specification=custom_specification,
        contacts=contacts
    )

    order_info = (
        f"🛒 *Новый заказ в quiz боте!*\n"
        f"👤 Имя: {order.user_name}\n"
        f"👤 start: {order.start}\n"
        f"🏡 Тип недвижимости: {order.type_property}\n"
        f"💰 Бюджет: {order.budget}\n"
        f"📍 Район: {order.district}\n"
        f"📌 Характеристики: {order.specifications}\n"
        f"✍️ Свой вариант: {order.custom_specification if order.custom_specification else '—'}\n"
        f"📞 Контакты: {order.contacts}\n"
        f"🔗 ID пользователя: {order.user_id}"
    )

    if GROUP_ID_ENV and message.bot:
        await message.bot.send_message(GROUP_ID_ENV, order_info, parse_mode="Markdown")

    # Отправляем подтверждение пользователю
    await message.answer('Спасибо! Наш менеджер скоро свяжется с тобой. А пока можешь посмотреть наши лучшие предложения!',
                         reply_markup=inline.inline_final)

    # Очищаем состояние после оформления заказа
    await state.clear()


@user_private_router.callback_query(F.data.startswith('back_'))
async def handler_back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)  # Переводит состояние FSM в None
    await state.update_data({})  # Удаляет сохранённые данные FSM
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            text.text_type_of_property, reply_markup=inline.inline_type_of_property
        )
        await callback.answer()
