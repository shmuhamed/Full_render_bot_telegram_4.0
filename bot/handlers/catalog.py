import os
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from database.models import get_all_brands, get_cars_by_brand
from bot.utils.lang import translations, user_langs, get_text

router = Router()

@router.callback_query(lambda c: c.data.startswith("brand_"))
async def show_cars(callback: types.CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "ru")
    brand_id = int(callback.data.split("_")[1])
    cars = get_cars_by_brand(brand_id)

    if not cars:
        await callback.message.answer(get_text(callback.from_user.id, "no_cars"))
        return

for car in cars:
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
                album.append(InputMediaPhoto(media=photo_url, caption=text if img == car.images[0] else None))
            await callback.message.answer_media_group(media=album)
        else:
            await callback.message.answer(text)
