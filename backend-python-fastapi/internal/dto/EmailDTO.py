from pydantic import BaseModel

class EmailNewDTO(BaseModel):
    user_to_id: str
    subject: str
    text_message: str

    is_will_sended: bool