from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class CustomerPayment(Base):
    """customer_payments table"""
    __tablename__ = 'customer_payments'

    pid = Column(Integer, primary_key=True, index=True)

    cid = Column(Integer, ForeignKey("customers.cid"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    payment_type = Column(String(20))

    customer = relationship("Customer", back_populates="payments")
