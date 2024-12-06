from pydantic import BaseModel
from typing import Union

class EmailLiteViewModel(BaseModel):
    id: int
    user_from_id: str
    user_to_id: str
    code: Union[str, None]
    subject: Union[str, None]
    text_message: Union[str, None]
    is_sent: bool
    date_of_add: Union[str, None]
    date_of_sent: Union[str, None]