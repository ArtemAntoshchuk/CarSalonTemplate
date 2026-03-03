from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Model


async def get_models_by_brand(brand_id, session:AsyncSession):
    query = Select(Model).filter_by(brand_id=brand_id)
    result = await session.execute(query)

    return result.scalars().all()


