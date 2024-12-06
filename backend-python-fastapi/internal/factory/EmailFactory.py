
from internal.Entities import Email
from internal.viewmodel.EmailViewModel import EmailLiteViewModel
from internal.model.EmailModel import EmailRedisCache
from internal.util.LoggerUtil import LoggerUtil
import json
from datetime import datetime

from logging import Logger

class EmailFactory:

    def __init__(self):
        self.logger: Logger = LoggerUtil.get_logger()

    def redis_cache_to_lite_viewmodel(self, emailRedisCache: EmailRedisCache) -> EmailLiteViewModel:
        return EmailLiteViewModel(
            id=emailRedisCache.id,
            user_from_id=emailRedisCache.user_from_id,
            user_to_id=emailRedisCache.user_to_id,
            code=emailRedisCache.code,
            subject=emailRedisCache.subject,
            text_message=emailRedisCache.text_message,
            is_sent=True if emailRedisCache.is_sent == 1 else False,
            date_of_add=emailRedisCache.date_of_add_str,
            date_of_sent=emailRedisCache.date_of_sent_str,
        )

    def create_redis_cache_viewModel(self, email: Email) -> EmailRedisCache:
        """Создание модели для хранения данных сущности Email в кэше базы данных Redis"""
        return EmailRedisCache(
            id=email.id,
            code=email.code,
            user_from_id=email.user_from_id,
            user_to_id=email.user_to_id,
            subject=email.subject,
            text_message=email.text_message,
            is_sent=email.is_sent,
            date_of_add_str=email.date_of_add.strftime("%Y-%m-%d %H:%M:%S") if email.date_of_add is not None else None,
            date_of_sent_str=email.date_of_sent.strftime("%Y-%m-%d %H:%M:%S") if email.date_of_sent is not None else None,
        )

    def parse_redis_cache_from_redis_json(self, json_str: str) -> EmailRedisCache:
        """Получение модели из хранящихся данных в формате JSON сущности Email из базы данных Redis"""

        json_data = json.loads(json_str)
        return EmailRedisCache(
            id=int(json_data["id"]),
            user_from_id=json_data["user_from_id"],
            user_to_id=json_data["user_to_id"],
            code=json_data["code"],
            subject=json_data["subject"],
            text_message=json_data["text_message"],
            is_sent=int(json_data["is_sent"]),
            date_of_add_str=json_data["date_of_add_str"],
            date_of_sent_str=json_data["date_of_sent_str"],
        )

    def create_lite_viewmodel(self, email: Email) -> EmailLiteViewModel:
        return EmailLiteViewModel(
            id=email.id,
            user_from_id=email.user_from_id,
            user_to_id=email.user_to_id,
            code=email.code,
            subject=email.subject,
            text_message=email.text_message,
            is_sent=True if email.is_sent == 1 else False,
            date_of_add=email.date_of_add.strftime("%Y-%m-%d %H:%M:%S") if email.date_of_add is not None else None,
            date_of_sent=email.date_of_sent.strftime("%Y-%m-%d %H:%M:%S") if email.date_of_sent is not None else None,
        )