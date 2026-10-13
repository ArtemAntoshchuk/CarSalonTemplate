from app.db.car_orm_query import create_car, get_cars_by, find_all_cars
from app.db.car_orm_query import get_shifter_type_by_car_id as get_shifter_type_by_car_id_orm
from app.db.car_orm_query import get_count_of_cars as get_count_cars
from app.db.db import SessionLocal
from app.db.models import Car, Model
from app.service.brand_service import get_brand_name_by_id
from app.service.engine_service import get_engine_by_id
from app.service.models_service import get_models_by_brand, get_model_by_id, get_brand_by_model_id
from app.dto.dto import CarBaseInfoDTO
from app.service.photo_service import get_main_photo_tg_id_by_car_id
from app.service.shifter_type_service import get_shifter_type_by_id


async def add_car(model_id,
                  price,
                  vin,
                  mileage,
                  description,
                  shifter_type_id,
                  year_produced,
                  color_id,
                  was_in_accident,
                  engine_id):
    async with SessionLocal() as session:
        car = Car(model_id=model_id,
                  price=price,
                  vin=vin,
                  mileage=mileage,
                  description=description,
                  shifter_type_id=shifter_type_id,
                  year_produced=year_produced,
                  color_id=color_id,
                  engine_id=engine_id,
                  was_in_accident=was_in_accident)

        await create_car(car=car,session=session)
        return car.id



async def get_cars_by_brand(brand_id):
    async with SessionLocal() as session:
        models = await get_models_by_brand(brand_id)
        all_cars = []

        for model in models:
            cars = await get_cars_by_model(model.id)
            all_cars.extend(cars)

        return all_cars


async def get_cars_by_model(model_id):
    async with SessionLocal() as session:
        return await get_cars_by(session, model_id=model_id)

async def get_shifter_type_by_car_id(car_id):
    async with SessionLocal() as session:
        return await get_shifter_type_by_car_id_orm(session=session, car_id=car_id)


async def get_all_cars_base_dto():
    cars = []
    async with SessionLocal() as session:
        cars = await find_all_cars(session)

    cars_base_dto = []
    for car in cars:
        id = car.id
        model = await get_model_by_id(car.model_id)
        brand = await get_brand_by_model_id(car.model_id)
        main_photo_tg_id = await get_main_photo_tg_id_by_car_id(car.id)
        shifter_type = await get_shifter_type_by_car_id(car.id)

        engine = await get_engine_by_id(car.engine_id)

        engine_type_id = engine.engine_type_id
        engine_volume = engine.volume

        car_base_info_dto = CarBaseInfoDTO(id=id, brand_name=brand.name, model_name=model.name, year=car.year_produced, price=car.price, main_photo_tg_id=main_photo_tg_id, mileage=car.mileage, shifter_type_name=shifter_type.name, engine_type_id=engine_type_id, engine_volume=engine_volume)
        cars_base_dto.append(car_base_info_dto)
        #todo - finish car_base_info_dto   (in dto.py - engine_volume, etc.)

    return cars_base_dto


async def get_count_of_cars():
    async with SessionLocal() as session:
        return await get_count_cars(session)

async def get_cars_by_engine_id(engine_id):
    async with SessionLocal() as session:
        return await get_cars_by(session, engine_id=engine_id)
