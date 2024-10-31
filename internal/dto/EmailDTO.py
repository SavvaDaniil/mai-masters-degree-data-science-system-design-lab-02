from pydantic import BaseModel

class EmailNewDTO(BaseModel):
    user_to_id: int
    subject: str
    text_message: str

    is_will_sended: bool