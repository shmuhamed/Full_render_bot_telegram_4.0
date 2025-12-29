from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()
engine = create_engine("sqlite:///database/suvtekin.db", echo=False)
Session = sessionmaker(bind=engine)

# 🚗 Бренды
class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    cars = relationship("Car", back_populates="brand")

# 🚘 Автомобили
class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    model = Column(String)
    year = Column(String)
    transmission = Column(String)
    fuel = Column(String)
    price = Column(String)
    image = Column(String)  # 🆕 путь к изображению
    brand = relationship("Brand", back_populates="cars")


# 👨‍💼 Менеджеры
class Manager(Base):
    __tablename__ = "managers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(String)
    email = Column(String)
    telegram_username = Column(String)

# 🧾 Заявки на продажу
class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)
    details = Column(String)
    done = Column(Boolean, default=False)

# ------------------- CRUD -------------------

def get_session(): return Session()

# --- Бренды ---
def get_all_brands():
    return get_session().query(Brand).all()

def add_brand(name):
    s = get_session()
    s.add(Brand(name=name))
    s.commit()

def delete_brand(brand_id):
    s = get_session()
    brand = s.get(Brand, brand_id)
    if brand:
        s.delete(brand)
        s.commit()

# --- Автомобили ---
def get_all_cars():
    return get_session().query(Car).all()

def get_cars_by_brand(brand_id):
    return get_session().query(Car).filter_by(brand_id=brand_id).all()

def add_car(brand_id, model, year, transmission, fuel, price):
    s = get_session()
    s.add(Car(brand_id=brand_id, model=model, year=year, transmission=transmission, fuel=fuel, price=price))
    s.commit()

def delete_car(car_id):
    s = get_session()
    car = s.get(Car, car_id)
    if car:
        s.delete(car)
        s.commit()

# --- Менеджеры ---
def get_all_managers():
    return get_session().query(Manager).all()

def add_manager(name, surname, phone, email, telegram):
    s = get_session()
    s.add(Manager(name=name, surname=surname, phone=phone, email=email, telegram_username=telegram))
    s.commit()

def delete_manager(manager_id):
    s = get_session()
    manager = s.get(Manager, manager_id)
    if manager:
        s.delete(manager)
        s.commit()

# --- Заявки ---
def get_all_requests():
    return get_session().query(Request).all()

def get_pending_requests():
    return get_session().query(Request).filter_by(done=False).all()

def add_sell_request(name, contact, details):
    s = get_session()
    s.add(Request(name=name, contact=contact, details=details))
    s.commit()

def mark_request_done(req_id):
    s = get_session()
    req = s.get(Request, req_id)
    if req:
        req.done = True
        s.commit()
