from sqlalchemy import Column, Integer, String, Text, Boolean
from config.database import Base

class Message(Base):
    __tablename__ = "classified_messages"

    mid = Column(Integer, primary_key=True) 
    mobile = Column(String(15), nullable=False)
    message = Column(Text, nullable=False)
    is_transactional = Column(Boolean, nullable=False)
    
    def __repr__(self):
        return(
            f"<Message mid={self.mid}"
            f"mobile={self.mobile}"
            f"is_transactional={self.is_transactional}>"
        )


    