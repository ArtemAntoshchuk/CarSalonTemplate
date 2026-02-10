from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Customer


async def get_customer_by_tg_id(tg_id, session:AsyncSession):
    customer = await session.execute(select(Customer).where(Customer.telegram_id == tg_id))
    customer = customer.scalar_one_or_none()
    return customer

async def create_customer(customer:Customer, session:AsyncSession):
    session.add(customer)
    await session.commit()
