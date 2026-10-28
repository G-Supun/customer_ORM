from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class Customer(Base):
    """Blueprint for customers table"""
    __tablename__ = 'customers'

    cid = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    mobile = Column(String(15))
    address = Column(String(255))

    payments = relationship("CustomerPayment", back_populates="customer",cascade="all, delete-orphan")
    adeona_tables = relationship("AdeonaTables", back_populates="customer",cascade="all, delete-orphan")