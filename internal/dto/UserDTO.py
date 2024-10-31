from pydantic import BaseModel
from typing import Union

class UserSearchByUsernameDTO(BaseModel):
    username: str
    
class UserSearchDTO(BaseModel):
    skip: int
    query_string: Union[str, None]

class UserRegistrationDTO(BaseModel):
    username: str
    password: str
    lastname: Union[str, None]
    firstname: Union[str, None]

class UserForgetDTO(BaseModel):
    step: int
    forget_id: int = 0
    username: Union[str, None]
    code: Union[str, None]

class UserLoginDTO(BaseModel):
    username: str
    password: str