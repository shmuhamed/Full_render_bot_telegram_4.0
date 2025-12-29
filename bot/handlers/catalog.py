import os
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.models import get_all_brands, get_cars_by_brand, get_featured_cars, search_cars_by_model
from bot.utils.lang import translations, user_langs, get_text

router = Router()

# --- Состояние FSM для поиска ---
class SearchStates(StatesGroup):
    waiting_for_query = State()

@router.message(Command("start"))
async def start_command(message: types.Message):
    if message.from_user.id not in user_langs:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇺🇿 Oʻzbekcha", callback_data="lang_uz")
        )
        await message.answer(translations["ru"]["choose_language"], reply_markup=markup)
        return

    lang = user_langs[message.from_user.id]
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="⭐ " + ("Рекомендуемые авто" if lang == "ru" else "Tavsiya etilganlar"), callback_data="featured")
    )
    markup.add(
        InlineKeyboardButton(text="🔍 " + ("Поиск автомобиля" if lang == "ru" else "Avtomobil qidirish"), callback_data="search")
    )
    for brand in get_all_brands():
        markup.add(InlineKeyboardButton(text=brand.name, callback_data=f"brand_{brand.id}"))
    markup.add(
        InlineKeyboardButton(text=get_text(message.from_user.id, "support"), callback_data="support"),
        InlineKeyboardButton(text=get_text(message.from_user.id, "sell_car"), callback_data="sell_car")
    )

    await message.answer(
        get_text(message.from_user.id, "welcome") + "\n" + get_text(message.from_user.id, "choose_brand"),
        reply_markup=markup
    )

# --- Обработчик нажатия "Поиск" ---
@router.callback_query(lambda c: c.data == "search")
async def ask_search(callback: types.CallbackQuery, state: FSMContext):
    lang = user_langs.get(callback.from_user.id, "ru")
    msg = "🔍 Введите название модели для поиска:" if lang == "ru" else "🔍 Model nomini kiriting:"
    await callback.message.answer(msg)
    await state.set_state(SearchStates.waiting_for_query)

# --- Принимаем текст поиска ---
@router.message(SearchStates.waiting_for_query)
async def perform_search(message: types.Message, state: FSMContext):
    lang = user_langs.get(message.from_user.id, "ru")
    query = message.text.strip()
    results = search_cars_by_model(query)
    await state.clear()

    if not results:
        msg = "❌ Ничего не найдено." if lang == "ru" else "❌ Hech narsa topilmadi."
        await message.answer(msg)
        return

    msg = "🔎 Найдено автомобилей:" if lang == "ru" else "🔎 Topilgan avtomobillar:"
    await message.answer(f"{msg} {len(results)}")

    for car in results:
        star = "⭐ " if car.is_featured else ""
        text = (
            f"{star}<b>{car.brand.name} {car.model}</b>\n"
            f"Год / Yil: {car.year}\n"
            f"КПП / Uzatma: {car.transmission}\n"
            f"Топливо / Yoqilg‘i: {car.fuel}\n"
            f"Цена / Narx: {car.price}$"
        )

        if car.images:
            album = []
            for img in car.images[:5]:
                photo_url = f"{os.getenv('RENDER_EXTERNAL_URL')}{img.path}"
                album.append(types.InputMediaPhoto(media=photo_url, caption=text if img == car.images[0] else None))
            await message.answer_media_group(media=album)
        else:
            await message.answer(text)
