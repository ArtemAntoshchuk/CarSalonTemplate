
from app.db.customer_orm_query import get_customer_by_tg_id, create_customer
from app.db.db import AsyncSession
from app.db.models import Customer


async def register_customer(telegram_id,
                      first_name,
                      last_name,
                      phone_number):
    async with AsyncSession() as session:
        if not await customer_is_registered(telegram_id) :
            customer = Customer(telegram_id=telegram_id,
                                first_name=first_name,
                                last_name=last_name,
                                phone_number=phone_number)
            await create_customer(customer, session)

async def customer_is_registered(telegram_id):
    async with AsyncSession() as session:
        customer = await get_customer_by_tg_id(telegram_id, session)
        return customer is not None
