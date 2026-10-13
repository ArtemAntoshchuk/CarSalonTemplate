from sqlalchemy import select, delete
from app.db.db import SessionLocal

from app.db.models import CarEngine, EngineType

async def create_engine_orm(car_engine: CarEngine, session: SessionLocal):
    session.add(car_engine)
    await session.commit()
    await session.refresh(car_engine)

async def find_all_engines(session: SessionLocal):
    query = select(CarEngine)
    result = await session.execute(query)
    return result.scalars().all()

async def get_engine_by_id_orm(engine_id: int, session: SessionLocal):
    query = select(CarEngine).where(CarEngine.id == engine_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()




async def find_all_engine_types(session: SessionLocal):
    query = select(EngineType)
    result = await session.execute(query)
    return result.scalars().all()