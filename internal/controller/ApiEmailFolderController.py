from fastapi import APIRouter, Request, Response
from logging import Logger, getLogger
from typing import List

from internal.abstracts.NotCriticalExceptionAbstract import NotCriticalExceptionAbstract
from internal.viewmodel.BaseResponse import BaseResponse
from internal.middleware.UserMiddleware import UserMiddleware
from internal.facade.EmailFolderFacade import EmailFolderFacade
from internal.dto.EmailFolderDTO import EmailFolderNewDTO
from internal.dto.ConnectionEmailToEmailFolder import ConnectionEmailToEmailFolderNewDTO
from internal.custom_exception.UserCustomException import UserNotFoundException
from internal.custom_exception.EmailFolderCustomException import EmailFolderNotFoundException, EmailFolderUserNotOwnedException
from internal.viewmodel.EmailFolderViewModel import EmailFolderPreviewViewModel
from internal.viewmodel.EmailViewModel import EmailLiteViewModel

routerEmailFolder: APIRouter = APIRouter()

logger: Logger = getLogger()
userMiddleware: UserMiddleware = UserMiddleware()
emailFolderFacade: EmailFolderFacade = EmailFolderFacade()


@routerEmailFolder.api_route(path='', response_model=BaseResponse, methods=["PUT"])
def add_by_user(request: Request, response: Response, emailFolderNewDTO: EmailFolderNewDTO):
    """Создание нового почтовой папки пользователем"""

    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 403
        return BaseResponse(error="not_auth")
    
    try:
        emailFolderFacade.add_by_user(user_id=user_id, emailFolderNewDTO=emailFolderNewDTO)
        return BaseResponse()
    except NotCriticalExceptionAbstract as e:
        response.status_code = 400
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("PUT /api/email_folder Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")

@routerEmailFolder.api_route(path='/email', response_model=BaseResponse, methods=["PUT"])
def add_email_to_email_folder(request: Request, response: Response, connectionEmailToEmailFolderNewDTO: ConnectionEmailToEmailFolderNewDTO):
    """Добавления письма в папку"""

    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 403
        return BaseResponse(error="not_auth")
    
    try:
        emailFolderFacade.add_email_to_email_folder(user_id=user_id, connectionEmailToEmailFolderNewDTO=connectionEmailToEmailFolderNewDTO)
        return BaseResponse()
    except NotCriticalExceptionAbstract as e:
        response.status_code = 400
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("PUT /api/email_folder/email Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")

@routerEmailFolder.api_route(path='/{email_folder_id_str}/email_list', response_model=BaseResponse, methods=["GET"])
def list_of_emails(request: Request, response: Response, email_folder_id_str: str):
    """Получение всех писем в папке"""

    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 403
        return BaseResponse(error="not_auth")
    
    try:
        email_folder_id = int(email_folder_id_str)
        emailLiteViewModels: List[EmailLiteViewModel] = emailFolderFacade.email_lite_list_by_email_folder_id(user_id=user_id, email_folder_id=email_folder_id)
        return BaseResponse(emailLiteViewModels=emailLiteViewModels)
    except NotCriticalExceptionAbstract as e:
        response.status_code = 400
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("GET /api/email_folder/<email_folder_id_str>/email_list Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")
    

@routerEmailFolder.api_route(path='/list_all', response_model=BaseResponse, methods=["GET"])
def get_list_by_user(request: Request, response: Response):
    """Получение перечня всех папок пользователя"""

    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 403
        return BaseResponse(error="not_auth")
    
    try:
        emailFolderPreviewViewModels: List[EmailFolderPreviewViewModel] = emailFolderFacade.get_list_by_user(user_id=user_id)
        return BaseResponse(emailFolderPreviewViewModels=emailFolderPreviewViewModels)
    except NotCriticalExceptionAbstract as e:
        response.status_code = 400
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("GET /api/email_folder/list_all Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")
    

@routerEmailFolder.api_route(path='/{email_folder_id_str}', response_model=BaseResponse, methods=["DELETE"])
def delete_by_id_by_user(request: Request, response: Response, email_folder_id_str: str):
    """Удаление почтовой папки пользователем"""

    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 403
        return BaseResponse(error="not_auth")

    try:
        email_folder_id = int(email_folder_id_str)
        emailFolderFacade.delete_by_id_by_user(user_id=user_id, email_folder_id=email_folder_id)
        return BaseResponse()
    except NotCriticalExceptionAbstract as e:
        response.status_code = 400
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("DELETE /api/email_folder/<email_folder_id_str> Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")
