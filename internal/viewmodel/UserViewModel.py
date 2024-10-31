from pydantic import BaseModel
from typing import Union

class UserSearchMicroViewModel(BaseModel):
    id: int
    username: Union[str, None]
    lastname: Union[str, None]
    firstname: Union[str, None]

class UserProfileViewModel(UserSearchMicroViewModel):
    is_active: bool