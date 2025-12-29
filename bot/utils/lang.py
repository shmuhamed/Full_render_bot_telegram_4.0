# Переводы для двух языков
translations = {
    "ru": {
        "lang_name": "🇷🇺 Русский",
        "welcome": "👋 Добро пожаловать в Suvtekin Auto Marketplace!",
        "choose_brand": "Выберите бренд:",
        "support": "💬 Поддержка",
        "sell_car": "🚘 Продать авто",
        "no_cars": "Пока нет машин у этого бренда 😔",
        "enter_name": "Введите ваше имя:",
        "enter_phone": "Введите ваш контактный номер:",
        "enter_car_info": "Опишите ваш автомобиль (бренд, модель, год, состояние):",
        "request_sent": "✅ Ваша заявка отправлена! Менеджер скоро свяжется с вами.",
        "choose_language": "Выберите язык / Tilni tanlang:",
        "manager_contacts": "📞 Контакты менеджеров:"
    },
    "uz": {
        "lang_name": "🇺🇿 Oʻzbekcha",
        "welcome": "👋 Suvtekin Auto Marketplace’ga xush kelibsiz!",
        "choose_brand": "Brendni tanlang:",
        "support": "💬 Qo'llab-quvvatlash",
        "sell_car": "🚘 Avtomobil sotish",
        "no_cars": "Bu brendda hozircha mashinalar yo'q 😔",
        "enter_name": "Ismingizni kiriting:",
        "enter_phone": "Telefon raqamingizni kiriting:",
        "enter_car_info": "Avtomobilingizni tasvirlab bering (brend, model, yil, holati):",
        "request_sent": "✅ So'rovingiz yuborildi! Menejer tez orada siz bilan bog'lanadi.",
        "choose_language": "Tilni tanlang / Выберите язык:",
        "manager_contacts": "📞 Menejerlar bilan bog‘lanish uchun:"
    }
}

# Память пользователей (временное хранилище)
user_langs = {}

def get_text(user_id, key):
    lang = user_langs.get(user_id, "ru")
    return translations[lang].get(key, key)
