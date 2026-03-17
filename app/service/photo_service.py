from app.db.db import AsyncSession
from app.db.models import Photo
from app.db.photo_orm_query import add_photo as add_photo_orm_query
from app.db.photo_orm_query import delete_photo_by_id as delete_photo_by_id_orm_query
from app.db.photo_orm_query import get_all_photos_by_car_id as get_all_photos_by_car_id_orm_query
from app.db.photo_orm_query import get_all_photos as get_all_photos_orm_query


async def add_photo(url, car_id):
    async with AsyncSession() as session:
        photo = Photo(url=url, car_id=car_id)

        await add_photo_orm_query(photo=photo, session=session)

async def delete_photo(id):
    async with AsyncSession() as session:
        await delete_photo_by_id_orm_query(photo_id=id, session=session)

async def get_all_photos_by_car_id(car_id):
    async with AsyncSession() as session:
        await get_all_photos_by_car_id_orm_query(car_id=car_id, session=session)

async def get_all_photos():
    async with AsyncSession() as session:
        await get_all_photos_orm_query(session=session)