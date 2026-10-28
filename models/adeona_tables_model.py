from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class AdeonaTables(Base):
    """customer_salary table"""
    __tablename__ = 'adeona_tables'

    sid = Column(Integer, primary_key=True, index=True)

    cid = Column(Integer, ForeignKey("customers.cid"), nullable=False)

    salary = Column(Numeric(10, 2), nullable=False)
    

    customer = relationship("Customer", back_populates="adeona_tables")