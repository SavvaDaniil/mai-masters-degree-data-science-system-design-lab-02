

kafka_topic_messages_name: str = "messages_topic"
kafka_consumer_configuration: dict = {
    'bootstrap.servers': 'kafka1:9092',  # Адрес Kafka брокера
    'group.id': kafka_topic_messages_name,  # ID группы потребителей
    'auto.offset.reset': 'earliest'  # Начинать с самого раннего сообщения
}
