from aiogram import Router, types
from database.models import get_all_managers
from bot.utils.lang import get_text

router = Router()

@router.callback_query(lambda c: c.data == "support")
async def show_support(callback: types.CallbackQuery):
    managers = get_all_managers()
    if not managers:
        await callback.message.answer("❌ Нет доступных менеджеров.")
        return

    text = get_text(callback.from_user.id, "manager_contacts") + "\n\n"
    for m in managers:
        text += (
            f"{m.name} {m.surname}\n"
            f"📞 {m.phone}\n"
            f"✉️ {m.email}\n"
            f"Telegram: @{m.telegram_username}\n\n"
        )
    await callback.message.answer(text)
