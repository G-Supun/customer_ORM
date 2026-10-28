from sqlalchemy import Column, Integer, String
from config.database import Base

class MobileNumber(Base):
    __tablename__ = 'mobile_numbers'

    nid = Column(Integer, primary_key=True)  
    mobile = Column(String(15), nullable=False)
  