from sqlalchemy import Column, String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class OfferCategories(Base):
    __tablename__ = "offer_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    offer_id = Column(ForeignKey("offers.id"), nullable=False)
    category_id = Column(ForeignKey("categories.id"), nullable=True)
    offer = relationship(
        "Offer",
        back_populates="offer_categories"
    )
    category = relationship(
        "Categories",
        back_populates="offer_categories"
    )