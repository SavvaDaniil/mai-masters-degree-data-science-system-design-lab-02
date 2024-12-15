
from logging import Logger
from datetime import datetime

from internal.util.LoggerUtil import LoggerUtil
from internal.dto.MessageDTO import MessageFromQueueDTO
from internal.factory.MessageFactory import MessageFactory
from internal.repository.MessageRepository import MessageRepository
from internal.Entities import Message

class MessageFacade:
    
    def __init__(self):
        self.logger: Logger = LoggerUtil.get_logger()
        self.messageFactory: MessageFactory = MessageFactory()
        self.messageRepository: MessageRepository = MessageRepository()

    def add_from_queue(self, queue_message: str) -> None:
        """Добавление сообщения в таблицу базы данных из очереди Kafka"""
        
        messageFromQueueDTO: MessageFromQueueDTO = self.messageFactory.create_dto_from_json_message_from_queue(json_str=queue_message)
        
        #self.logger.error(f"Received message data: {messageFromQueueDTO}")
        message: Message = Message()
        message.content = messageFromQueueDTO.content
        message.date_of_created = datetime.strptime(messageFromQueueDTO.creation_date, "%Y-%m-%d %H:%M:%S") if messageFromQueueDTO.creation_date is not None else None
        message.date_of_add = datetime.now()

        self.messageRepository.add(obj=message)

