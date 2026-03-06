from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Model


async def get_models_by_brand(brand_id, session:AsyncSession):
    query = Select(Model).filter_by(brand_id=brand_id)
    result = await session.execute(query)

    return result.scalars().all()

#todo add method for getting model by id

async def get_model_by_id(model_id, session:AsyncSession):
    model = await session.execute(select(Model).where(Model.id == model_id))
    model = model.scalar_one_or_none()
    return model
