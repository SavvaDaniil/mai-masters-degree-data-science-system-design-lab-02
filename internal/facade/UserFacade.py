from fastapi import Response

from passlib.context import CryptContext
from datetime import datetime
from typing import List

from internal.dto.UserDTO import UserRegistrationDTO, UserLoginDTO, UserForgetDTO, UserSearchByUsernameDTO, UserSearchDTO
from internal.repository.UserRepository import UserRepository
from internal.Entities import User
from internal.middleware.UserMiddleware import UserMiddleware
from internal.util.RandomUtil import RandomUtil
from internal.custom_exception.UserCustomException import UserLoginFailedException, UsernameAlreadyExistsException, UserNotFoundException
from internal.viewmodel.BaseResponse import BaseResponse
from internal.viewmodel.UserViewModel import UserProfileViewModel, UserSearchMicroViewModel

class UserFacade:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self):
        self.userRepository: UserRepository = UserRepository()
        self.userMiddleware: UserMiddleware = UserMiddleware()

    def get_by_username(self, userSearchByUsernameDTO: UserSearchByUsernameDTO) -> UserProfileViewModel:
        """Поиск пользователя по логину"""

        user: User = self.userRepository.find_by_username(username=userSearchByUsernameDTO.username)
        if user is None:
            raise UserNotFoundException()
        
        return UserProfileViewModel(
            id=user.id,
            username=user.username,
            is_active=True if user.is_active == 1 else False,
            lastname=user.lastname,
            firstname=user.firstname
        )

    def search(self, userSearchDTO: UserSearchDTO) -> List[UserSearchMicroViewModel]:
        """Поиск пользователя по маске имя и фамилии, а также по логину"""

        query_strs: List[str] = []
        if userSearchDTO.query_string is not None and userSearchDTO.query_string != "":
            query_strs = userSearchDTO.query_string.split(" ")
        users: List[User] = self.userRepository.search(skip=userSearchDTO.skip, take=20, query_strs=query_strs)

        userSearchMicroViewModels: List[UserSearchMicroViewModel] = []
        if users is not None and len(users) > 0:
            for user in users:
                userSearchMicroViewModels.append(
                    UserSearchMicroViewModel(
                        id=user.id,
                        username=user.username,
                        lastname=user.lastname,
                        firstname=user.firstname
                    )
                )
        
        return userSearchMicroViewModels

    def registration(self, response: Response, userRegistrationDTO: UserRegistrationDTO) -> str:
        """Регистрация нового пользователя"""

        return self.userMiddleware.create_access_token(
            response=response, 
            user_id=self.add(userRegistrationDTO=userRegistrationDTO)
        )
    
    def add(self, userRegistrationDTO: UserRegistrationDTO) -> int:

        if self.userRepository.find_by_username(username=userRegistrationDTO.username) is not None:
            raise UsernameAlreadyExistsException()
        
        user: User = User()
        user.username = userRegistrationDTO.username
        user.lastname = userRegistrationDTO.lastname
        user.firstname = userRegistrationDTO.firstname
        user.auth_key = RandomUtil.get_random_string(32)
        user.password = self.pwd_context.hash(userRegistrationDTO.password)
        user.is_active = 1
        user.date_of_add = datetime.now()
        self.userRepository.add(obj=user)

        return user.id

    def login(self, response:Response, userLoginDTO: UserLoginDTO) -> str:
        
        user: User = self.userRepository.find_by_username(username=userLoginDTO.username)
        if user is None:
            raise UserLoginFailedException()

        if self.pwd_context.verify(userLoginDTO.password, user.password):
            return self.userMiddleware.create_access_token(response, user.id)

        raise UserLoginFailedException()
    

    def forget(self, response:Response, userForgetDTO: UserForgetDTO) -> BaseResponse:
        
        if userForgetDTO.step == 0:
            user: User = self.userRepository.find_by_username(username=userForgetDTO.username)
            if user is None:
                response.status_code = 401
                return BaseResponse(error="wrong", access_token=None)
            
            code: str = RandomUtil.get_random_string_only_numbers(6)

            user.forget_count = 0
            user.forget_code = code
            user.forget_date_of_last_try = None
            self.userRepository.update(user=user)

            #отправка письма
            #self.__forget_send_code_to_username(
            #    user=user,
            #    code=code
            #)

            return BaseResponse(forget_id=user.id)
        
        elif userForgetDTO.step == 1:
            user: User = self.userRepository.find_by_id(id=userForgetDTO.forget_id)
            if user is None:
                response.status_code = 400
                return BaseResponse(error="wrong_forget_id", access_token=None, token_type=None)
            
            if userForgetDTO.code != user.forget_code:
                if user.forget_count > 2:
                    response.status_code = 401
                    return BaseResponse(status="error", error="out_of_limit")
                elif user.forget_count > 1:
                    user.forget_count = 3
                    self.userRepository.update(user=user)
                    response.status_code = 401
                    return BaseResponse(status="error", error="0_left")
                elif user.forget_count > 0:
                    user.forget_count = 2
                    self.userRepository.update(user=user)
                    response.status_code = 401
                    return BaseResponse(status="error", error="1_left")
                else:
                    user.forget_count = 1
                    self.userRepository.update(user=user)
                    response.status_code = 401
                    return BaseResponse(status="error", error="2_left")
            
            randomUtil: RandomUtil = RandomUtil()
            password_new: str = randomUtil.get_random_string(6)
            user.password = self.pwd_context.hash(password_new)
            self.userRepository.update(user=user)

            #отправка письма с новым паролем на почту
            #self.__mail_new_password_to_username(
            #    user=user,
            #    password_new=password_new
            #)
            
            access_token: str = self.userMiddleware.create_access_token(response=response, user_id=user.id)
            return BaseResponse(is_auth=True, access_token=access_token)
        
        response.status_code = 400
        return BaseResponse(error="wrong")
    
    def create_if_not_exists_user_master(self) -> None:
        userRepository: UserRepository = UserRepository()
        user_master: User = userRepository.find_by_username(username="master")
        if user_master is not None:
            return

        self.add(userRegistrationDTO=UserRegistrationDTO(
            username="admin",
            password="secret",
            lastname="Фамилия 1",
            firstname="Имя 1"
        ))