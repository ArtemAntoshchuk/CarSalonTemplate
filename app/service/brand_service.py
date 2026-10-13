from app.db.db import SessionLocal

from app.db.brand_orm_query import get_all_brands as get_all_brands_from_db
from app.db.brand_orm_query import get_brand_by_name as get_brand_by_name_from_db
from app.db.brand_orm_query import get_brand_name_by_id as get_brand_name_by_id_from_db


async def get_all_brands():
    async with SessionLocal() as session:
        return await get_all_brands_from_db(session)

async def get_brands_names():
    brands = await get_all_brands()
    return [brand.name for brand in brands]

async def get_brand_by_name(name):
    async with SessionLocal() as session:
        return await get_brand_by_name_from_db(session, name)

async def get_brand_name_by_id(id):
    async with SessionLocal() as session:
        return await get_brand_name_by_id_from_db(session, id)

