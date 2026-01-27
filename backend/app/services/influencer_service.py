from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.api.schemas.influencers import InfluencerResponse
from app.db.models.influencers import Influencers



async def get_all_influencers(db: AsyncSession) -> List[InfluencerResponse]:
    result = await db.execute(select(Influencers))
    return result.scalars().all()


async def get_influencer_by_id(db: AsyncSession, influencer_id: UUID) -> Influencers | None:
    result = await db.execute(
        select(Influencers).where(Influencers.id == influencer_id)
    )
    return result.scalar_one_or_none()

