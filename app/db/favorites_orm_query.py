from sqlalchemy import select, delete, and_
from app.db.db import SessionLocal as AsyncSession

from app.db.models import Favorites

async def add_to_fav(favorites: Favorites, session: AsyncSession):
    session.add(favorites)
    await session.commit()

async def get_favorite_by_car_id_and_customer_id(session: AsyncSession, car_id: int, customer_id: int):
    # query = select(Favorites).where(and_(Favorites.car_id == car_id, Favorites.customer_id == customer_id))
    query = select(Favorites).where(Favorites.car_id == car_id and Favorites.customer_id == customer_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def delete_from_favorites(car_id: int, customer_id: int, session: AsyncSession):
    query = delete(Favorites).where(Favorites.car_id == car_id and Favorites.customer_id == customer_id)
    await session.execute(query)
    await session.commit()