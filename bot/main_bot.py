import os, asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv
from bot.handlers import catalog, sell_car, support
from bot.utils.webhook import set_webhook

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_router(catalog.router)
dp.include_router(sell_car.router)
dp.include_router(support.router)

async def start_bot():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/webhook/{os.getenv('BOT_USERNAME')}")
    setup_application(app, dp, bot=bot)
    await set_webhook(bot, os.getenv("RENDER_EXTERNAL_URL"), os.getenv("BOT_USERNAME"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("🚀 SuvtekinBot запущен (Webhook активен).")
    while True:
        await asyncio.sleep(3600)
