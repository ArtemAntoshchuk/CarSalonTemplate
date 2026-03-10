from app.db.car_orm_query import create_car, get_cars_by, find_all_cars
from app.db.db import AsyncSession
from app.db.models import Car, Model
from app.service.models_service import get_models_by_brand, get_model_by_id, get_brand_by_model_id
from app.dto.dto import CarBaseInfoDTO


async def add_car(model: Model,
                  price,
                  vin,
                  mileage,
                  engine_type,
                  engine_gen,
                  description,
                  shifter_type,
                  year_produced,
                  horse_power,
                  color,
                  status,
                  engine_volume,
                  was_in_accident):
    async with AsyncSession() as session:
        car = Car(model_id=model.id,
                  price=price,
                  vin=vin,
                  mileage=mileage,
                  engine_type=engine_type,
                  engine_gen=engine_gen,
                  description=description,
                  shifter_type=shifter_type,
                  year_produced=year_produced,
                  horse_power=horse_power,
                  color=color,
                  status=status,
                  engine_volume=engine_volume,
                  was_in_accident=was_in_accident)

        await create_car(car=car,session=session)



async def get_cars_by_brand(brand_id):
    async with AsyncSession() as session:
        models = await get_models_by_brand(brand_id)
        all_cars = []

        for model in models:
            cars = await get_cars_by_model(model.id)
            all_cars.extend(cars)

        return all_cars


async def get_cars_by_model(model_id):
    async with AsyncSession() as session:
        return await get_cars_by(session, model_id=model_id)

async def get_all_cars_base_dto():
    cars = []
    async with AsyncSession() as session:
        cars = await find_all_cars(session)

    cars_base_dto = []
    for car in cars:
        model = await get_model_by_id(car.model_id)
        brand = await get_brand_by_model_id(car.model_id)

        car_base_info_dto = CarBaseInfoDTO(brand=brand, model=model, year=car.year_produced, price=car.price)
        cars_base_dto.append(car_base_info_dto)

    return cars_base_dto
        #todo create part for creating CarBaseInfoDTO object by car from list