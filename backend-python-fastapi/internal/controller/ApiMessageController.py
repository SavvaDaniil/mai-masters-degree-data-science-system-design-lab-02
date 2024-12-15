from fastapi import APIRouter, Request, Response
from logging import Logger, getLogger
from confluent_kafka import Producer

from internal.abstracts.NotCriticalExceptionAbstract import NotCriticalExceptionAbstract
from internal.dto.MessageDTO import MessageNewDTO
from internal.configuration.KafkaConfiguration import kafka_producer_configuration
from internal.facade.KafkaFacade import KafkaFacade
from internal.viewmodel.BaseResponse import BaseResponse

routerMessage: APIRouter = APIRouter()

logger: Logger = getLogger()

producer: Producer = Producer(**kafka_producer_configuration)
kafkaFacade: KafkaFacade = KafkaFacade(producer=producer)


@routerMessage.api_route(path="", response_model=BaseResponse, methods=["PUT"])
def add(request: Request, response: Response, messageNewDTO: MessageNewDTO):
    """Добавление контента сообщения в очередь Kafka"""
    try:
        kafkaFacade.add_to_topic(messageNewDTO=messageNewDTO)
        response.status_code = 201
        return BaseResponse()
    except NotCriticalExceptionAbstract as e:
        response.status_code = 400
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("PUT /api/message Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")