from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from gtm.models.base import Base

class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True)
    domain_name = Column(String, unique=True, nullable=False)
    business_size_category = Column(String, nullable=True)  # SME, Mid-market, Enterprise
    number_of_leads = Column(Integer, default=0, nullable=False)

    # Relationship to Lead model
    leads = relationship("Lead", back_populates="domain", cascade="all, delete-orphan")

    # Uniqueness constraint for safety (additional safeguard)
    __table_args__ = (UniqueConstraint("domain_name", name="uq_domain_name"),)

