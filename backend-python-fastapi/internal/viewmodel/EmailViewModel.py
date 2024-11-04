from pydantic import BaseModel
from typing import Union

class EmailLiteViewModel(BaseModel):
    user_from_id: int
    user_to_id: int
    code: Union[str, None]
    subject: Union[str, None]
    text_message: Union[str, None]
    is_sent: bool
    date_of_add: Union[str, None]
    date_of_sent: Union[str, None]