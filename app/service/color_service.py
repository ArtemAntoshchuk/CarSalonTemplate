from app.db.db import SessionLocal
from app.db.color_orm_query import get_color_by_id_orm, find_all_colors

async def get_all_colors():
    async with SessionLocal() as session:
        return await find_all_colors(session)

async def get_color_by_id(color_id):
    async with SessionLocal() as session:
        return await get_color_by_id_orm(color_id, session)

async def get_color_names():
    return [color.name for color in await get_all_colors()]

