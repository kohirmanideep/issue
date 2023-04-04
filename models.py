from sqlalchemy import Column,Integer,String,VARCHAR,ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Book(Base):
    __tablename__ = "issuedbooks"
    Accessnumber =Column(Integer,primary_key=True)
    Username = Column(VARCHAR(50))
    Title = Column(VARCHAR(50))
    Author = Column(VARCHAR(50))
    Subject = Column(VARCHAR(50))
    KeyWord = Column(VARCHAR(30))
    bookcategory=Column(VARCHAR(50))
    

    
