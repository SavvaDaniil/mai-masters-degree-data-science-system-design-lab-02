from sqlalchemy import Column, Integer, Boolean, String, Date, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
class User(Base):
    __tablename__ = "user"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)
    username = Column("username", String(256))
    password = Column("password", String(256))
    auth_key = Column("auth_key", String(32))
    access_token = Column("access_token", String(32))
    is_active = Column("is_active", Integer, nullable=False, default="0")

    lastname = Column("lastname", String(256))
    firstname = Column("firstname", String(256))

    date_of_add = Column("date_of_add", DateTime)

    #emails_from = relationship("Email", back_populates="user_from")
    #emails_to = relationship("Email", back_populates="user_to")

    email_folders = relationship("EmailFolder", back_populates="user")
"""


class Email(Base):
    __tablename__ = "email"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)

    code = Column("code", String(36))

    user_from_id = Column("user_from_id", String(128))
    #user_from_id = Column("user_from_id", Integer, ForeignKey("user.id"))
    #user_from = relationship("User", back_populates="emails_from", lazy="joined", foreign_keys="Email.user_from_id")

    user_to_id = Column("user_to_id", String(128))
    #user_to_id = Column("user_to_id", Integer, ForeignKey("user.id"))
    #user_to = relationship("User", back_populates="emails_to", lazy="joined", foreign_keys="Email.user_to_id")

    subject = Column("subject", String(1024))
    text_message = Column("text_message", Text)
    
    is_sent = Column("is_sent", Integer, nullable=False, default="0")#статус черновика
    date_of_add = Column("date_of_add", DateTime)
    date_of_sent = Column("date_of_sent", DateTime)

    connection_email_to_email_folder_list = relationship("ConnectionEmailToEmailFolder", back_populates="email")

class EmailFolder(Base):
    __tablename__ = "email_folder"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)

    user_id = Column("user_id", String(128))
    #user_id = Column("user_id", Integer, ForeignKey("user.id"))
    #user = relationship("User", back_populates="email_folders", lazy="joined")

    title = Column("title", String(1024))
    
    date_of_add = Column("date_of_add", DateTime)

    connection_email_to_email_folder_list = relationship("ConnectionEmailToEmailFolder", back_populates="email_folder")


class ConnectionEmailToEmailFolder(Base):
    __tablename__ = "connection_email_to_email_folder"
    
    id = Column("id", Integer, primary_key = True, index=True, unique = True)

    email_folder_id = Column("email_folder_id", Integer, ForeignKey("email_folder.id"))
    email_folder = relationship("EmailFolder", back_populates="connection_email_to_email_folder_list", lazy="joined")

    email_id = Column("email_id", Integer, ForeignKey("email.id"))
    email = relationship("Email", back_populates="connection_email_to_email_folder_list", lazy="joined")

    date_of_add = Column("date_of_add", DateTime)


# class Message(Base):
#     __tablename__ = "message"
    
#     id = Column("id", Integer, primary_key = True, index=True, unique = True)
#     content_of_message = Column("content_of_message", Text)
#     date_of_add = Column("date_of_add", DateTime)


