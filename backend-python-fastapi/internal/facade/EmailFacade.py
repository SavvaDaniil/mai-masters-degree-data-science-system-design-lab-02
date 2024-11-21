import uuid
from datetime import datetime

from internal.Entities import Email
from internal.entity.User import User
from internal.dto.EmailDTO import EmailNewDTO
from internal.repository.UserRepository import UserRepository
from internal.repository.EmailRepository import EmailRepository
from internal.custom_exception.EmailCustomException import EmailNotFoundException, EmailUserFromNotFoundException, EmailUserToNotFoundException
from internal.factory.EmailFactory import EmailFactory
from internal.viewmodel.EmailViewModel import EmailLiteViewModel

class EmailFacade:

    def __init__(self):
        self.userRepository: UserRepository = UserRepository()
        self.emailRepository: EmailRepository = EmailRepository()

    def get_by_code(self, email_code: str) -> EmailLiteViewModel:
        email: Email = self.emailRepository.find_by_code(code=email_code)
        if email is None:
            raise EmailNotFoundException()
        
        emailFactory: EmailFactory = EmailFactory()
        return emailFactory.create_lite_viewmodel(email=email)


    def add(self, user_from_id: str, emailNewDTO: EmailNewDTO) -> None:
        userFrom: User = self.userRepository.find_by_id(id=user_from_id)
        if userFrom is None:
            raise EmailUserFromNotFoundException()
        
        userTo: User = self.userRepository.find_by_id(id=emailNewDTO.user_to_id)
        if userTo is None:
            raise EmailUserToNotFoundException()
        
        email: Email = Email()
        email.code = uuid.uuid4()
        email.user_from_id = user_from_id
        email.user_to_id = str(userTo._id)
        email.subject = emailNewDTO.subject
        email.text_message = emailNewDTO.text_message
        email.date_of_add = datetime.now()
        self.emailRepository.add(obj=email)

        if emailNewDTO.is_will_sended:
            #Тут отправка через почтовый сервер

            email.is_sent = 1
            email.date_of_sent = datetime.now()
            self.emailRepository.update(email=email)


