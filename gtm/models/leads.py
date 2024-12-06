from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
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
    phone_number = Column(String, nullable=True)  # New field for phone number
    email = Column(String, nullable=True)         # New field for email
    website = Column(String, nullable=True)       # New field for website URL
    opening_hours = Column(String, nullable=True) # New field for opening hours (as JSON/text)

    # Foreign key to Domain
    domain_id = Column(Integer, ForeignKey('domains.id'), nullable=True)  
    domain = relationship('Domain', back_populates='leads')  # Relationship to Domain model

