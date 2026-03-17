from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, TIMESTAMP, Numeric, Boolean, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    phone_number = Column(String, nullable=False, unique=True)


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Model(Base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False)
    model_class = Column(String, nullable=False, name='class')


class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    price = Column(Numeric(15,2), nullable=False)
    vin = Column(String, nullable=False)
    mileage = Column(Integer)
    engine_type = Column(String, nullable=False)
    engine_gen = Column(String, nullable=False)
    description = Column(String, nullable=False)
    shifter_type = Column(String, nullable=False)
    year_produced = Column(Integer, nullable=False)
    horse_power = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    status = Column(String, nullable=False, default='available')
    created_at = Column(TIMESTAMP, nullable=False)
    engine_volume = Column(Numeric(3,1), nullable=False)
    was_in_accident = Column(Boolean, nullable=False)


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    chat_id = Column(Integer, nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    status = Column(String)


class OrderItems(Base):
    __tablename__ = 'orders_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('car.id'), nullable=False, unique=True)
    sale_price = Column(Numeric(15,2), nullable=False)


class Favorites(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('car.id'), nullable=False)


class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False)
    car_id = Column(Integer, ForeignKey('car.id'), nullable=False)