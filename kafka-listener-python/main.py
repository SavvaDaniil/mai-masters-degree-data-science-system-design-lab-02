from confluent_kafka import Consumer, KafkaError
from logging import Logger

from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.configuration.KafkaConfiguration import kafka_consumer_configuration, kafka_topic_messages_name
from internal.facade.MessageFacade import MessageFacade
from internal.util.LoggerUtil import LoggerUtil

consumer: Consumer = Consumer(kafka_consumer_configuration)
consumer.subscribe([kafka_topic_messages_name])

logger: Logger = LoggerUtil.get_logger()
messageFacade: MessageFacade = MessageFacade()

try:
    ApplicationDbContext.init_db()
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logger.error(f"Kafka Consumer msg.error(): {msg.error()}")
                break

        messageFacade.add_from_queue(queue_message=msg.value().decode('utf-8'))

except KeyboardInterrupt:
    pass
except Exception as e:
    logger.error(f"Kafka Consumer Exception: {e}")
finally:
    # Закрытие Consumer
    consumer.close()