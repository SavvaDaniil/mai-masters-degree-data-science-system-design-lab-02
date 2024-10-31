from fastapi import APIRouter, Request, Response
from logging import Logger, getLogger

from internal.abstracts.NotCriticalExceptionAbstract import NotCriticalExceptionAbstract
from internal.viewmodel.BaseResponse import BaseResponse
from internal.middleware.UserMiddleware import UserMiddleware
from internal.facade.EmailFacade import EmailFacade
from internal.dto.EmailDTO import EmailNewDTO
from internal.custom_exception.EmailCustomException import EmailUserFromNotFoundException, EmailUserToNotFoundException
from internal.viewmodel.EmailViewModel import EmailLiteViewModel

routerEmail: APIRouter = APIRouter()

logger: Logger = getLogger()
userMiddleware: UserMiddleware = UserMiddleware()
emailFacade: EmailFacade = EmailFacade()


@routerEmail.api_route(path='', response_model=BaseResponse, methods=["PUT"])
def add(request: Request, response: Response, emailNewDTO: EmailNewDTO):
    """Создание нового письма"""

    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 403
        return BaseResponse(error="not_auth")
    
    try:
        emailFacade.add(user_from_id=user_id, emailNewDTO=emailNewDTO)
        return BaseResponse()
    except NotCriticalExceptionAbstract as e:
        response.status_code = 400
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("PUT /api/email Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")



@routerEmail.api_route(path='/code/{email_code}', response_model=BaseResponse, methods=["GET"])
def get_by_code(request: Request, response: Response, email_code: str):
    """Получение письма по коду"""

    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 403
        return BaseResponse(error="not_auth")
    
    try:
        emailLiteViewModel: EmailLiteViewModel = emailFacade.get_by_code(email_code=email_code)
        return BaseResponse(emailLiteViewModel=emailLiteViewModel)
    except NotCriticalExceptionAbstract as e:
        response.status_code = 400
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("GET /api/email/code/<email_code> Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")