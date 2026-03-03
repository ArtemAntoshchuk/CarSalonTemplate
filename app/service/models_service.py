from app.db.db import AsyncSession
from app.db.models_orm_query import get_models_by_brand as get_models

async def get_models_by_brand(brand_id):
    async with AsyncSession() as session:
        return await get_models(brand_id, session)


