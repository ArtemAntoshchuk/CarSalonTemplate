from app.db.favorites_orm_query import add_to_fav, get_favorite_by_car_id_and_customer_id as get_favorite_by_car_id_and_customer_id_orm, delete_from_favorites as delete_from_favorites_orm
from app.db.db import SessionLocal
from app.db.models import Favorites

async def save_to_favorites(car_id, customer_id):
    async with SessionLocal() as session:
        favorites = Favorites(car_id=car_id, customer_id=customer_id)
        await add_to_fav(favorites, session)

async def get_favorite_by_car_id_and_customer_id(car_id, customer_id):
    async with SessionLocal() as session:
        return await get_favorite_by_car_id_and_customer_id_orm(session=session, car_id=car_id, customer_id=customer_id)

async def delete_from_favorites(car_id, customer_id):
    async with SessionLocal() as session:
        await delete_from_favorites_orm(car_id=car_id, customer_id=customer_id, session=session)