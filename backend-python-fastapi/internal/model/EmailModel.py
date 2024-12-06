from pydantic import BaseModel
from typing import Union
from datetime import datetime

class EmailRedisCache(BaseModel):
    """Модели для хранения данных сущности Email в кэше базы данных Redis"""
    
    id: int

    code: Union[str, None]

    user_from_id: Union[str, None]

    user_to_id: Union[str, None]

    subject: Union[str, None]
    text_message: Union[str, None]
    
    is_sent: int
    date_of_add_str: Union[str, None]
    date_of_sent_str: Union[str, None]