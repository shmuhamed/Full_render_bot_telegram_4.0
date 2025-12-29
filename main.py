import os
import threading
from flask import Flask
from dotenv import load_dotenv
from admin.app import create_app
from database.db_init import init_db
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import asyncio

# ---------------------- #
#       ИНИЦИАЛИЗАЦИЯ
# ---------------------- #
load_dotenv()
init_db()  # создаёт БД при первом запуске

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Импортируем маршруты бота
from bot.handlers.catalog import router as catalog_router
from bot.handlers.sell_car import router as sell_router
from bot.handlers.language import router as lang_router

dp.include_router(catalog_router)
dp.include_router(sell_router)
dp.include_router(lang_router)

# ---------------------- #
#     ЗАПУСК FLASK
# ---------------------- #
flask_app = create_app()


def run_flask():
    """Запуск Flask админки"""
    port = int(os.getenv("PORT", 5000))
    print(f"🌐 Flask админка запущена на порту {port}")
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


# ---------------------- #
#     ЗАПУСК БОТА
# ---------------------- #
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"🤖 Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    print("🛑 Webhook удалён")

async def start_aiogram():
    """Запуск Telegram-бота с Webhook через aiohttp"""
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    app.on_startup.append(lambda _: on_startup(bot))
    app.on_shutdown.append(lambda _: on_shutdown(bot))

    port = int(os.getenv("AIORUN_PORT", 8080))
    print(f"🚀 Telegram Bot Webhook слушает порт {port}")
    web.run_app(app, host="0.0.0.0", port=port)


# ---------------------- #
#      ГЛАВНЫЙ ЗАПУСК
# ---------------------- #
if __name__ == "__main__":
    # Flask в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()

    # aiogram Webhook в основном потоке
    asyncio.run(start_aiogram())
