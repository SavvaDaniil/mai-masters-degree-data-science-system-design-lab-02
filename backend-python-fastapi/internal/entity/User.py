from dataclasses import dataclass
import datetime
from typing import Union
from bson.objectid import ObjectId


@dataclass
class User():

    _id: Union[ObjectId, None] = None
    
    username: Union[str, None] = None
    password: Union[str, None] = None
    auth_key: Union[str, None] = None
    access_token: Union[str, None] = None
    is_active: int = 0

    lastname: Union[str, None] = None
    firstname: Union[str, None] = None

    date_of_add: Union[datetime.datetime, None] = None

    #emails_from = relationship("Email", back_populates="user_from")
    #emails_to = relationship("Email", back_populates="user_to")

    #email_folders = relationship("EmailFolder", back_populates="user")