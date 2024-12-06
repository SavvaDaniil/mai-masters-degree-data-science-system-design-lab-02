from internal.data.ApplicationRedisDbContext import ApplicationRedisDbContext
from internal.Entities import Email
from internal.custom_exception.EmailCustomException import EmailCodeEmptyException
from internal.model.EmailModel import EmailRedisCache
from internal.factory.EmailFactory import EmailFactory
from internal.util.LoggerUtil import LoggerUtil

from typing import Union
from redis import Redis
import json
from logging import Logger

class EmailRedisRepository():
    """Класс для взаимодействия с сущностью Email в базе данных Redis"""

    def __init__(self):
        self.logger: Logger = LoggerUtil.get_logger()
        self.applicationRedisDbContext: ApplicationRedisDbContext = ApplicationRedisDbContext()
        self.emailFactory: EmailFactory = EmailFactory()

    def __get_key_by_email_code(self, email_code: str) -> str:
        """Генерация ключа для хранения сущности Email в кэше базы данных Redis"""
        if email_code is None or len(email_code) == 0:
            raise EmailCodeEmptyException()
        return f'email:{email_code}'
    
    def find_in_cache_by_code(self, email_code: str) -> Union[EmailRedisCache, None]:
        """Поиск сущности Email по коду в кэше базы данных Redis"""
        cache_key: str = self.__get_key_by_email_code(email_code=email_code)
        redis_client: Redis[str] = self.applicationRedisDbContext.get_client()
        if not redis_client.exists(cache_key):
            return None
        
        cached_email_json_str: str = redis_client.get(cache_key)
        #self.logger.error(f'find_in_cache_by_code cached_email_json_str: {cached_email_json_str}')
        return self.emailFactory.parse_redis_cache_from_redis_json(json_str=cached_email_json_str)

    def save_in_cache(self, email: Email) -> None:
        """Сохранение данных сущности Email в кэше базы данных Redis"""
        emailRedisCache: EmailRedisCache = self.emailFactory.create_redis_cache_viewModel(email=email)
        email_cache_json = dict()
        for key in emailRedisCache.__dict__:
            if key != '_sa_instance_state':
                email_cache_json[key] = emailRedisCache.__dict__[key]

        cache_key: str = self.__get_key_by_email_code(email_code=email.code)
        redis_client: Redis[str] = self.applicationRedisDbContext.get_client()
        #self.logger.error(f'save_in_cache email_cache_json: {email_cache_json}')
        redis_client.set(cache_key, json.dumps(email_cache_json), ex = 60 * 3)
    
