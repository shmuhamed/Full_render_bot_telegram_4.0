from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_all_brands, get_cars_by_brand

router = Router()

@router.message(commands=["start"])
async def start_command(message: types.Message):
    markup = InlineKeyboardMarkup()
    for brand in get_all_brands():
        markup.add(InlineKeyboardButton(text=brand.name, callback_data=f"brand_{brand.id}"))
    markup.add(InlineKeyboardButton(text="💬 Поддержка", callback_data="support"))
    markup.add(InlineKeyboardButton(text="🚘 Продать авто", callback_data="sell_car"))
    await message.answer("👋 Добро пожаловать в Suvtekin Auto Marketplace!\nВыберите бренд:", reply_markup=markup)

@router.callback_query(lambda c: c.data.startswith("brand_"))
async def show_cars(callback: types.CallbackQuery):
    brand_id = int(callback.data.split("_")[1])
    cars = get_cars_by_brand(brand_id)
    if not cars:
        await callback.message.answer("❌ Машины не найдены.")
        return
    for car in cars:
        await callback.message.answer(
            f"<b>{car.brand.name} {car.model}</b>\n"
            f"Год: {car.year}\nКПП: {car.transmission}\nТопливо: {car.fuel}\nЦена: {car.price}$"
        )
