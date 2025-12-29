from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.models import add_sell_request
from bot.utils.lang import get_text

router = Router()

class SellCarForm(StatesGroup):
    name = State()
    contact = State()
    car_info = State()

@router.callback_query(lambda c: c.data == "sell_car")
async def start_sell(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SellCarForm.name)
    await callback.message.answer(get_text(callback.from_user.id, "enter_name"))

@router.message(SellCarForm.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(SellCarForm.contact)
    await message.answer(get_text(message.from_user.id, "enter_phone"))

@router.message(SellCarForm.contact)
async def get_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(SellCarForm.car_info)
    await message.answer(get_text(message.from_user.id, "enter_car_info"))

@router.message(SellCarForm.car_info)
async def finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    add_sell_request(data["name"], data["contact"], message.text)
    await message.answer(get_text(message.from_user.id, "request_sent"))
    await state.clear()
