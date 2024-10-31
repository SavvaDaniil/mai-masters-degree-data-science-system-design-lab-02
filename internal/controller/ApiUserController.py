from fastapi import APIRouter, Request, Response
from logging import Logger, getLogger

from internal.abstracts.NotCriticalExceptionAbstract import NotCriticalExceptionAbstract
from internal.viewmodel.BaseResponse import BaseResponse
from internal.middleware.UserMiddleware import UserMiddleware
from internal.dto.UserDTO import UserRegistrationDTO, UserLoginDTO, UserSearchByUsernameDTO, UserSearchDTO
from internal.facade.UserFacade import UserFacade
from internal.custom_exception.UserCustomException import UserLoginFailedException, UsernameAlreadyExistsException, UserNotFoundException

routerUser: APIRouter = APIRouter()

logger: Logger = getLogger()
userMiddleware: UserMiddleware = UserMiddleware()
userFacade: UserFacade = UserFacade()

@routerUser.api_route('/search/username', response_model=BaseResponse, methods=["POST"])
def search_by_username(request: Request, response: Response, userSearchByUsernameDTO: UserSearchByUsernameDTO):
    """Поиск пользователя по логину"""
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 403
        return BaseResponse(error="not_auth")
    
    try:
        return BaseResponse(userProfileViewModel=userFacade.get_by_username(userSearchByUsernameDTO=userSearchByUsernameDTO))
    except UserNotFoundException as e:
        response.status_code = 404
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("POST /api/user/search/username Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")

@routerUser.api_route('/search', response_model=BaseResponse, methods=["POST"])
def search(request: Request, response: Response, userSearchDTO: UserSearchDTO):
    user_id: int = userMiddleware.get_current_user_id(request=request)
    if user_id == 0:
        response.status_code = 403
        return BaseResponse(error="not_auth")
    
    try:
        return BaseResponse(userSearchMicroViewModels=userFacade.search(userSearchDTO=userSearchDTO))
    except Exception as e:
        logger.error("POST /api/user/search Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")


@routerUser.api_route(path='', response_model=BaseResponse, methods=["PUT"])
def add(request: Request, response: Response, userRegistrationDTO: UserRegistrationDTO):
    """Создание нового пользователя"""
    try:
        access_token: str = userFacade.registration(response=response, userRegistrationDTO=userRegistrationDTO)
        return BaseResponse(is_auth=True, access_token=access_token)
    except UsernameAlreadyExistsException as e:
        response.status_code = 409
        return BaseResponse(error=str(e))
    except NotCriticalExceptionAbstract as e:
        response.status_code = 400
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("PUT /api/user Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")


@routerUser.api_route(path='/login', response_model=BaseResponse, methods=["POST"])
def login(request: Request, response: Response, userLoginDTO: UserLoginDTO):
    try:
        access_token: str = userFacade.login(response=response, userLoginDTO=userLoginDTO)
        return BaseResponse(is_auth=True, access_token=access_token)
    except UserLoginFailedException as e:
        response.status_code = 401
        return BaseResponse(error=str(e))
    except Exception as e:
        logger.error("POST /api/user/login Exception: " + str(e))
        response.status_code = 400
        return BaseResponse(error="unknown")
