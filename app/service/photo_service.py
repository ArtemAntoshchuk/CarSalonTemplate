from app.db.db import SessionLocal
from app.db.models import Photo
from app.db.photo_orm_query import add_photo as add_photo_orm_query
from app.db.photo_orm_query import delete_photo_by_id as delete_photo_by_id_orm_query
from app.db.photo_orm_query import get_all_photos_by_car_id as get_all_photos_by_car_id_orm_query
from app.db.photo_orm_query import get_all_photos as get_all_photos_orm_query


async def add_photo(photo_tg_id, is_main, car_id):
    async with SessionLocal() as session:
        photo = Photo(photo_tg_id = photo_tg_id, is_main = is_main, car_id = car_id)

        await add_photo_orm_query(photo=photo, session=session)

async def delete_photo(photo_id):
    async with SessionLocal() as session:
        await delete_photo_by_id_orm_query(photo_id=photo_id, session=session)

async def get_all_photos_by_car_id(car_id):
    async with SessionLocal() as session:
        return await get_all_photos_by_car_id_orm_query(car_id=car_id, session=session)

async def get_all_photos():
    async with SessionLocal() as session:
        return await get_all_photos_orm_query(session=session)

async def add_photos(photo_ids: list, car_id: int):
    for photo_id in photo_ids:
        is_main = False
        if photo_ids.index(photo_id) == 0:
            is_main = True
        await add_photo(photo_id, is_main, car_id)

async def get_main_photo_tg_id_by_car_id(car_id):
        photos = await get_all_photos_by_car_id(car_id)
        for i in photos:
            if i.is_main:
                return i.photo_tg_id
        return -1
