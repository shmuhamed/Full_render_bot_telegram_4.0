async def set_webhook(bot, render_url, bot_username):
    if not render_url:
        print("⚠️ Webhook не установлен — переменная RENDER_EXTERNAL_URL отсутствует.")
        return
    webhook_url = f"{render_url}/webhook/{bot_username}"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")
