from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class Influencers(Base):
    __tablename__ = "influencers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    influencer_custom_payouts = relationship(
        "InfluencerCustomPayouts",
        back_populates="influencer",
        cascade="all, delete-orphan"
    )
