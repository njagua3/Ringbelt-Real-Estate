from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database import Base

class Landlord(Base):
    __tablename__ = "landlords"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, unique=True, nullable=False)  # Name of the landlord
    properties = relationship("Property", back_populates="landlord")  # Relationship to properties


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, nullable=False)  # Name of the tenant
    age = Column(Integer, nullable=False)  # Age of the tenant
    rent_balance = Column(Float, nullable=False, default=0.0)  # Tenant's rent balance including bills
    property_id = Column(Integer, ForeignKey("properties.id"))  # Foreign key linking to properties
    property = relationship("Property")  # Relationship to Property


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, unique=True, nullable=False)  # Name of the property
    rent_amount = Column(Float, nullable=False)  # Rent amount for the property
    landlord_id = Column(Integer, ForeignKey("landlords.id"))  # Foreign key linking to landlords
    landlord = relationship("Landlord", back_populates="properties")  # Relationship to Landlord
