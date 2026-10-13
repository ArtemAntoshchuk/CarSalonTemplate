from app.db.db import SessionLocal
from app.db.shifter_type_orm_query import find_all_shifter_types, get_shifter_type_by_id as get_shifter_type_by_id_from_db

async def get_shifter_types():
    async with SessionLocal() as session:
        return await find_all_shifter_types(session)

async def get_shifter_types_names():
    shifter_types = await get_shifter_types()
    return [shifter_type.name for shifter_type in shifter_types]

async def get_shifter_type_by_id(shifter_type_id: int):
    async with SessionLocal() as session:
        return await get_shifter_type_by_id_from_db(shifter_type_id, session)