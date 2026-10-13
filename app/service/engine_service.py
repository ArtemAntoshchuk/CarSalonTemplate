from app.db.db import SessionLocal as AsyncSession
from app.db.engine_orm_query import *

async def get_all_engines():
    async with SessionLocal() as session:
        return await find_all_engines(session)

async def get_engine_names():
    # async with AsyncSession() as session:
    #     engine_names = []
    #
    #     for engine in await get_all_engines():
    #         engine_names.append(engine.name)
    #
    #     return engine_names
    return [engine.name for engine in await get_all_engines()]


async def get_engine_by_id(engine_id: int) -> CarEngine:
    async with SessionLocal() as session:
        engine = await get_engine_by_id_orm(engine_id, session)
        return engine

async def create_engine(engine_name,
                        engine_type_id,
                        engine_gen,
                        engine_volume,
                        engine_horse_power):
    async with SessionLocal() as session:
        car_engine = CarEngine(name=engine_name, engine_type_id=engine_type_id, gen=engine_gen, volume=engine_volume, horse_power=engine_horse_power)
        await create_engine_orm(car_engine=car_engine, session=session)

        return car_engine.id


async def get_all_engine_types():
    async with SessionLocal() as session:
        return await find_all_engine_types(session)