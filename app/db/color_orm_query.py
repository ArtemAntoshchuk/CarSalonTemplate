from sqlalchemy import select, delete
from app.db.db import SessionLocal as AsyncSession

from app.db.models import Color

async def find_all_colors(session: AsyncSession):
    query = select(Color)
    result = await session.execute(query)
    return result.scalars().all()

async def get_color_by_id_orm(color_id: int, session: AsyncSession):
    query = select(Color).where(Color.id == color_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

