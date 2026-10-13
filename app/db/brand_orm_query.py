from sqlalchemy import select
from app.db.db import SessionLocal as AsyncSession

from app.db.models import Model, Brand
from app.db.models_orm_query import get_model_by_id as get_model

async def get_brand_by_model_id(model_id, session: AsyncSession):
    model = await get_model(model_id, session)

    if not model:
        return None

    brand_id = model.brand_id
    brand = await session.execute(select(Brand).where(Brand.id == brand_id))
    brand = brand.scalar_one_or_none()

    return brand

async def get_all_brands(session: AsyncSession):
    brands = await session.execute(select(Brand).order_by(Brand.id))
    brands = brands.scalars().all()
    return brands

async def get_brand_by_name(session: AsyncSession, name: str):
    brand = await session.execute(select(Brand).where(Brand.name == name))
    brand = brand.scalar_one_or_none()
    return brand


async def get_brand_name_by_id(brand_id, session: AsyncSession):
    brand_name = await session.execute(select(Brand.name).where(id==brand_id))
    return brand_name.scalar_one_or_none()

