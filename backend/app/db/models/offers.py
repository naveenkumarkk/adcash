from sqlalchemy import Column, String, Text,Boolean,Enum as SAEnum,Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base
from app.core.enums import PayoutType

class Offer(Base):
    __tablename__ = "offers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    is_active=Column(Boolean,default=True)
    image_url=Column(String, nullable=True)
    payout_type = Column(
        SAEnum(PayoutType, name="payout_type_enum"),
        nullable=False,
        default="CPA"
    )
    cpa_amount=Column(Float,default=0.0)
    fixed_amount=Column(Float,default=0.0)
    influencer_custom_payouts = relationship(
        "InfluencerCustomPayouts",
        back_populates="offer"
    )

    offer_categories = relationship(
        "OfferCategories",
        back_populates="offer",
        cascade="all, delete-orphan"
    )