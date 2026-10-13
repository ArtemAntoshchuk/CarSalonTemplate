from sqlalchemy import Select, select
from app.db.db import SessionLocal as AsyncSession

from app.db.models import Model


async def get_models_by_brand(brand_id, session:AsyncSession):
    query = Select(Model).filter_by(brand_id=brand_id)
    result = await session.execute(query)

    return result.scalars().all()



async def get_model_by_id(model_id, session:AsyncSession):
    model = await session.execute(select(Model).where(Model.id == model_id))
    model = model.scalar_one_or_none()
    return model
