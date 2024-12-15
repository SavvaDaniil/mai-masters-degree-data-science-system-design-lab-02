
from confluent_kafka import Producer
import json

from internal.custom_exception.MessageCustomException import MessageContentIsEmptyException
from internal.viewmodel.MessageViewModel import MessageQueueViewModel
from internal.configuration.KafkaConfiguration import kafka_topic_messages_name

class KafkaService:

    def __init__(self, producer: Producer):
        self.producer = producer

    def add_to_topic(self, messageQueueViewModel: MessageQueueViewModel) -> None:
        """Добавление объекта Message в очередь брокера сообщений"""

        if messageQueueViewModel.content is None or len(messageQueueViewModel.content) == 0:
            raise MessageContentIsEmptyException()
        
        message_json = dict()
        for key in messageQueueViewModel.__dict__:
            if key != '_sa_instance_state':
                message_json[key] = messageQueueViewModel.__dict__[key]
        
        self.producer.produce(
            topic=kafka_topic_messages_name,
            value=json.dumps(message_json),
            callback=self.__delivery_report
        )
    
    def __delivery_report(self, err, msg) -> None:
        """Функция для обработки результатов доставки сообщения"""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')