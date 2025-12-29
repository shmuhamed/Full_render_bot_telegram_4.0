from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()
engine = create_engine("sqlite:///database/suvtekin.db", echo=False)
Session = sessionmaker(bind=engine)

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
    is_featured = Column(Boolean, default=False)  # ⭐ Новое поле
    brand = relationship("Brand", back_populates="cars")
    images = relationship("CarImage", back_populates="car", cascade="all, delete")

class CarImage(Base):
    __tablename__ = "car_images"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    path = Column(String)
    car = relationship("Car", back_populates="images")

# Остальные модели (Manager, Request) — без изменений

def get_session(): return Session()

# Получаем авто, где избранные идут первыми
def get_cars_by_brand(brand_id):
    session = get_session()
    return session.query(Car).filter_by(brand_id=brand_id).order_by(Car.is_featured.desc()).all()

def add_car_with_images(brand_id, model, year, transmission, fuel, price, image_paths, is_featured=False):
    s = get_session()
    car = Car(
        brand_id=brand_id, model=model, year=year,
        transmission=transmission, fuel=fuel, price=price,
        is_featured=is_featured
    )
    s.add(car)
    s.commit()
    for path in image_paths:
        s.add(CarImage(car_id=car.id, path=path))
    s.commit()
def get_featured_cars():
    """Возвращает все избранные автомобили (⭐)"""
    session = get_session()
    return session.query(Car).filter_by(is_featured=True).all()
    def search_cars_by_model(query):
    """Ищет автомобили по названию модели (без учёта регистра)."""
    session = get_session()
    return session.query(Car).filter(Car.model.ilike(f"%{query}%")).all()

