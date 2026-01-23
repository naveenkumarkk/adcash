from sqlalchemy import Column, ForeignKey, Float, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base


class InfluencerCustomPayouts(Base):
    __tablename__ = "influencer_custom_payouts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    influencer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("influencers.id"),
        nullable=False
    )
    offer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("offers.id"),
        nullable=False
    )

    amount = Column(Float, nullable=False)

    influencer = relationship(
        "Influencers",
        back_populates="influencer_custom_payouts"
    )
    offer = relationship(
        "Offer",
        back_populates="influencer_custom_payouts"
    )
    
    
