
from internal.dto.MessageDTO import MessageFromQueueDTO
import json

class MessageFactory:

    def create_dto_from_json_message_from_queue(self, json_str: str) -> MessageFromQueueDTO:
        message_data = json.loads(json_str)
        return MessageFromQueueDTO(
            content=message_data["content"],
            creation_date=message_data["creation_date"]
        )