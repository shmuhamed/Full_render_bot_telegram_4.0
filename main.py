import asyncio
import threading
from admin.app import create_app
from bot.main_bot import start_bot
from database.db_init import init_db

def run_flask():
    app = create_app()
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    print("© 2025 Suvtekin Auto Marketplace — Developed by Muha")
    init_db()
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    asyncio.run(start_bot())
