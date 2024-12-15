
from confluent_kafka import Producer
from datetime import datetime

from internal.dto.MessageDTO import MessageNewDTO
from internal.custom_exception.MessageCustomException import MessageContentIsEmptyException
from internal.viewmodel.MessageViewModel import MessageQueueViewModel
from internal.service.KafkaService import KafkaService

class KafkaFacade():

    def __init__(self, producer: Producer):
        self.producer: Producer = producer
        self.kafkaService: KafkaService = KafkaService(producer=producer)

    def add_to_topic(self, messageNewDTO: MessageNewDTO) -> None:
        """Добавление объекта Message в очередь брокера сообщений"""

        if messageNewDTO.content is None or len(messageNewDTO.content) == 0:
            raise MessageContentIsEmptyException()
        
        messageQueueViewModel: MessageQueueViewModel = MessageQueueViewModel(
            content=messageNewDTO.content,
            creation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self.kafkaService.add_to_topic(messageQueueViewModel=messageQueueViewModel)