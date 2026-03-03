from app.db.car_orm_query import create_car, get_cars_by
from app.db.db import AsyncSession
from app.db.models import Car, Model
from app.service.models_service import get_models_by_brand


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
