from app.db.db import SessionLocal
from app.db.models_orm_query import get_models_by_brand as get_models
from app.db.brand_orm_query import get_brand_by_model_id as get_brand
from app.db.models_orm_query import get_model_by_id as get_model

async def get_models_by_brand(brand_id):
    async with SessionLocal() as session:
        return await get_models(brand_id, session)




async def get_brand_by_model_id(model_id):
    async with SessionLocal() as session:
        return await get_brand(model_id, session)


async def get_model_by_id(model_id):
    async with SessionLocal() as session:
        return await get_model(model_id, session)

async def get_models_names_by_brand_id(brand_id):
    models = await get_models_by_brand(brand_id)
    return [model.name for model in models]

