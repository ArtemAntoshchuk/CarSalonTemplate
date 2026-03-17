from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Photo

async def add_photo(photo: Photo, session: AsyncSession):
    session.add(photo)
    await session.commit()

async def delete_photo_by_id(photo_id: int, session: AsyncSession):
    query = delete(Photo).where(Photo.id == photo_id)
    await session.execute(query)
    await session.commit()

async def get_all_photos_by_car_id(car_id: int, session: AsyncSession):
    query = select(Photo).where(Photo.car_id == car_id)
    result = await session.execute(query)

    return result.scalars().all()

async def get_all_photos(session: AsyncSession):
    query = select(Photo)
    result = await session.execute(query)

    return result.scalars().all()