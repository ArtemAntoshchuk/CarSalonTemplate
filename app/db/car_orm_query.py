from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Car

# async def get_car_by_id(car_id, session: AsyncSession):
#     car = await session.execute(select(Car).where(Car.id == car_id))
#     car = car.scalar_one_or_none()
#     return car
#
# async def get_cars_by_engine_type(engine_type, session: AsyncSession):
#     car = await session.execute(select(Car).where(Car.engine_type == engine_type))
#     car = car.scalar_one_or_none()
#     return car
#
# async def get_cars_by_engine_gen(engine_gen, session: AsyncSession):
#     car = await session.execute(select(Car).where(Car.engine_gen == engine_gen))
#     car = car.scalar_one_or_none()
#     return car
#
# async def get_cars_by_engine_volume(engine_volume, session: AsyncSession):
#     car = await session.execute(select(Car).where(Car.engine_volume == engine_volume))
#     car = car.scalar_one_or_none()
#     return car
#
# async def get_cars_by_year_produced(year_produced, session: AsyncSession):
#     car = await session.execute(select(Car).where(Car.year_produced == year_produced))
#     car = car.scalar_one_or_none()
#     return car
#
# async def get_car_by_was_in_accident(was_in_acc, session: AsyncSession):
#     car = await session.execute(select(Car).where(Car.was_in_accident == was_in_acc))
#     car = car.scalar_one_or_none()
#     return car
#
async def create_car(car: Car, session: AsyncSession):
    session.add(car)
    await session.commit()

async def delete_car_by_id(car_id, session: AsyncSession):
    query = delete(Car).where(Car.id == car_id)
    await session.execute(query)
    await session.commit()

async def find_all_cars(session: AsyncSession):
    query = select(Car)
    result = await session.execute(query)

    return result.scalars().all()

async def get_cars_by(session: AsyncSession, **filters):
    query = select(Car).filter_by(**filters)
    result = await session.execute(query)

    return result.scalars().all()