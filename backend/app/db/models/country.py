from sqlalchemy import Column, Integer, String,Float
from app.db.base import Base
from sqlalchemy.orm import relationship

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    cpa_amount = Column(Float, default=0.0)
