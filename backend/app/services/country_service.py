from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.models.country import Country


async def get_all_countries(db: AsyncSession) -> List[Country]:
    result = await db.execute(select(Country))
    return result.scalars().all()


async def get_country_by_id(db: AsyncSession, country_id: int) -> Country | None:
    result = await db.execute(select(Country).where(Country.id == country_id))
    return result.scalar_one_or_none()


async def get_country_by_code(db: AsyncSession, code: str) -> Country | None:
    result = await db.execute(select(Country).where(Country.code == code))
    return result.scalar_one_or_none()
