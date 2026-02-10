from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    phone_number = Column(String, nullable=False, unique=True)
