from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Model, Brand
from app.db.models_orm_query import get_model_by_id as get_model

async def get_brand_by_model_id(model_id, session: AsyncSession):
    model = get_model(model_id, session)

    if not model:
        return None

    brand_id = model.brand_id
    brand = await session.execute(select(Brand).where(Brand.id == brand_id))
    brand = brand.scalar_one_or_none()

    return brand
