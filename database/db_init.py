from database.models import Base, engine, Session, Brand, Car, Manager

def init_db():
    """Создаёт базу данных и заполняет тестовыми данными при первом запуске."""
    Base.metadata.create_all(engine)
    session = Session()

    if not session.query(Brand).first():
        suvtekin = Brand(name="Suvtekin")
        session.add(suvtekin)
        session.commit()

        # 🚗 Тестовые автомобили с разными типами топлива
        cars = [
            Car(brand_id=suvtekin.id, model="Falcon X", year="2022", transmission="Автомат", fuel="Бензин", price="25000"),
            Car(brand_id=suvtekin.id, model="Storm EV", year="2024", transmission="Автомат", fuel="Электрический", price="45000"),
            Car(brand_id=suvtekin.id, model="Hybrid Pro", year="2023", transmission="Вариатор", fuel="Гибрид", price="38000"),
            Car(brand_id=suvtekin.id, model="GasOne", year="2021", transmission="Механика", fuel="Газ", price="19000"),
            Car(brand_id=suvtekin.id, model="DualDrive", year="2022", transmission="Автомат", fuel="Газ и бензин", price="29000")
        ]
        session.add_all(cars)

        # 👨‍💼 Менеджер по умолчанию
        manager = Manager(
            name="Ali",
            surname="Karimov",
            phone="+998900000000",
            email="ali@suvtekin.com",
            telegram_username="alikarimov"
        )
        session.add(manager)
        session.commit()

        print("✅ База данных инициализирована с тестовыми данными.")
    else:
        print("📦 База данных уже существует.")
