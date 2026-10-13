from sqlalchemy import select
from app.db.db import SessionLocal
from app.db.models import ShifterType


async def find_all_shifter_types(session: SessionLocal):
    shifter_types = await session.execute(select(ShifterType))
    shifter_types = shifter_types.scalars().all()
    return shifter_types

async def get_shifter_type_by_id(shifter_type_id: int, session: SessionLocal):
    shifter_type = await session.execute(select(ShifterType).where(ShifterType.id == shifter_type_id))
    return shifter_type.scalar_one_or_none()
