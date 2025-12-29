import os
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from database.models import get_all_brands, get_cars_by_brand, get_featured_cars
from bot.utils.lang import translations, user_langs, get_text

router = Router()

@router.message(commands=["start"])
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
    markup.add(InlineKeyboardButton(text="⭐ " + ("Рекомендуемые авто" if lang == "ru" else "Tavsiya etilganlar"), callback_data="featured"))
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

# --- обработчик избранных авто ---
@router.callback_query(lambda c: c.data == "featured")
async def show_featured(callback: types.CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "ru")
    cars = get_featured_cars()
    if not cars:
        msg = "❌ Нет рекомендованных автомобилей." if lang == "ru" else "❌ Tavsiya etilgan avtomobillar yo‘q."
        await callback.message.answer(msg)
        return

    msg = "⭐ Рекомендуемые автомобили:" if lang == "ru" else "⭐ Tavsiya etilgan avtomobillar:"
    await callback.message.answer(msg)

    for car in cars:
        text = (
            f"⭐ <b>{car.brand.name} {car.model}</b>\n"
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
            await callback.message.answer_media_group(media=album)
        else:
            await callback.message.answer(text)
