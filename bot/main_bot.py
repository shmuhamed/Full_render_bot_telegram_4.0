import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv
from bot.handlers import catalog, sell_car, support
from bot.utils.webhook import set_webhook

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# подключаем все роутеры
dp.include_router(catalog.router)
dp.include_router(sell_car.router)
dp.include_router(support.router)

async def start_bot():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/webhook/{BOT_USERNAME}")
    setup_application(app, dp, bot=bot)
    await set_webhook(bot, RENDER_URL, BOT_USERNAME)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("🚀 SuvtekinBot запущен с поддержкой RU 🇷🇺 и UZ 🇺🇿.")
    while True:
        await asyncio.sleep(3600)
