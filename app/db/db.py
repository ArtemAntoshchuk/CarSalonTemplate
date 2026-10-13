from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import Config

engine = create_async_engine(Config.DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
