from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()
engine = create_engine("sqlite:///database/suvtekin.db", echo=False)
Session = sessionmaker(bind=engine)

# ---- Модели ----

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    cars = relationship("Car", back_populates="brand")

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    model = Column(String)
    year = Column(String)
    transmission = Column(String)
    fuel = Column(String)
    price = Column(String)
    brand = relationship("Brand", back_populates="cars")
    images = relationship("CarImage", back_populates="car", cascade="all, delete")

class CarImage(Base):
    __tablename__ = "car_images"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    path = Column(String)
    car = relationship("Car", back_populates="images")

class Manager(Base):
    __tablename__ = "managers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(String)
    email = Column(String)
    telegram_username = Column(String)

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)
    details = Column(String)
    done = Column(Boolean, default=False)

# ---- CRUD ----
def get_session(): return Session()

def get_all_cars():
    return get_session().query(Car).all()

def get_cars_by_brand(brand_id):
    return get_session().query(Car).filter_by(brand_id=brand_id).all()

def add_car_with_images(brand_id, model, year, transmission, fuel, price, image_paths):
    s = get_session()
    car = Car(brand_id=brand_id, model=model, year=year,
              transmission=transmission, fuel=fuel, price=price)
    s.add(car)
    s.commit()
    for path in image_paths:
        s.add(CarImage(car_id=car.id, path=path))
    s.commit()
