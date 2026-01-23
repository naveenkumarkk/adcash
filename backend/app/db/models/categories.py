from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    offer_categories = relationship(
        "OfferCategories",
        back_populates="category",
        cascade="all, delete-orphan"
    )
