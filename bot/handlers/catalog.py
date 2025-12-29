from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_all_brands, get_cars_by_brand
from bot.utils.lang import translations, user_langs, get_text

router = Router()

@router.message(commands=["start"])
async def start_command(message: types.Message):
    # Предложим выбор языка, если пользователь новый
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
    for brand in get_all_brands():
        markup.add(InlineKeyboardButton(text=brand.name, callback_data=f"brand_{brand.id}"))
    markup.add(
        InlineKeyboardButton(text=get_text(message.from_user.id, "support"), callback_data="support"),
        InlineKeyboardButton(text=get_text(message.from_user.id, "sell_car"), callback_data="sell_car")
    )
    await message.answer(get_text(message.from_user.id, "welcome") + "\n" + get_text(message.from_user.id, "choose_brand"), reply_markup=markup)

@router.callback_query(lambda c: c.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user_langs[callback.from_user.id] = lang
    await callback.message.answer(f"✅ Язык установлен: {translations[lang]['lang_name']}")
    await start_command(callback.message)

@router.callback_query(lambda c: c.data.startswith("brand_"))
async def show_cars(callback: types.CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "ru")
    brand_id = int(callback.data.split("_")[1])
    cars = get_cars_by_brand(brand_id)
    if not cars:
        await callback.message.answer(get_text(callback.from_user.id, "no_cars"))
        return
    for car in cars:
        text = (
            f"<b>{car.brand.name} {car.model}</b>\n"
            f"{get_text(callback.from_user.id, 'choose_brand')}:\n"
            f"Год / Yil: {car.year}\n"
            f"КПП / Uzatma: {car.transmission}\n"
            f"Топливо / Yoqilg‘i: {car.fuel}\n"
            f"Цена / Narx: {car.price}$"
        )
        await callback.message.answer(text)
