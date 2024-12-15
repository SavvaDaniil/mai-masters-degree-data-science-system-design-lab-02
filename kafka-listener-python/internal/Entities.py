from sqlalchemy import Column, Integer, Boolean, String, Date, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Message(Base):
    __tablename__ = "message"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)

    content = Column("content", Text)
    
    date_of_created = Column("date_of_created", DateTime)
    date_of_add = Column("date_of_add", DateTime)