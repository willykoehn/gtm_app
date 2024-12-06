from sqlalchemy import Column, Integer, String, Float
from gtm.models.base import Base

class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    user_ratings_total = Column(Integer, nullable=True)
    google_place_id = Column(String, unique=True, nullable=False)
    business_status = Column(String, nullable=True)
    place_type = Column(String, nullable=True)

