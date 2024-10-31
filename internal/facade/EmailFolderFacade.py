
from datetime import datetime
from typing import List

from internal.Entities import Email, User, EmailFolder, ConnectionEmailToEmailFolder
from internal.dto.EmailFolderDTO import EmailFolderNewDTO
from internal.dto.ConnectionEmailToEmailFolder import ConnectionEmailToEmailFolderNewDTO
from internal.repository.EmailRepository import EmailRepository
from internal.repository.EmailFolderRepository import EmailFolderRepository
from internal.repository.ConnectionEmailToEmailFolderRepository import ConnectionEmailToEmailFolderRepository
from internal.repository.UserRepository import UserRepository
from internal.custom_exception.UserCustomException import UserNotFoundException
from internal.custom_exception.EmailCustomException import EmailNotFoundException, EmailUserNotOwnedException
from internal.custom_exception.EmailFolderCustomException import EmailFolderNotFoundException, EmailFolderUserNotOwnedException
from internal.factory.EmailFactory import EmailFactory
from internal.viewmodel.EmailFolderViewModel import EmailFolderPreviewViewModel
from internal.viewmodel.EmailViewModel import EmailLiteViewModel

class EmailFolderFacade:

    def __init__(self):
        self.userRepository: UserRepository = UserRepository()
        self.emailRepository: EmailRepository = EmailRepository()
        self.emailFolderRepository: EmailFolderRepository = EmailFolderRepository()
        self.connectionEmailToEmailFolderRepository: ConnectionEmailToEmailFolderRepository = ConnectionEmailToEmailFolderRepository()

    def add_by_user(self, user_id: int, emailFolderNewDTO: EmailFolderNewDTO) -> None:
        """Создание нового почтовой папки пользователем"""
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        emailFolder: EmailFolder = EmailFolder()
        emailFolder.user = user
        emailFolder.title = emailFolderNewDTO.title
        emailFolder.date_of_add = datetime.now()

        self.emailFolderRepository.add(obj=emailFolder)

    def add_email_to_email_folder(self, user_id: int, connectionEmailToEmailFolderNewDTO: ConnectionEmailToEmailFolderNewDTO) -> None:
        """Добавления письма в папку"""
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        email: Email = self.emailRepository.find_by_id(id=connectionEmailToEmailFolderNewDTO.email_id)
        if email is None:
            raise EmailNotFoundException()
        
        if email.user_from_id != user_id:
            raise EmailUserNotOwnedException()
        
        emailFolder: EmailFolder = self.emailFolderRepository.find_by_id(id=connectionEmailToEmailFolderNewDTO.email_folder_id)
        if emailFolder is None:
            raise EmailFolderNotFoundException()
        
        if emailFolder.user_id != user_id:
            raise EmailFolderUserNotOwnedException()
        
        connectionEmailToEmailFolder: ConnectionEmailToEmailFolder = self.connectionEmailToEmailFolderRepository.find_by_email_id_with_email_folder_id(
            email_id=connectionEmailToEmailFolderNewDTO.email_id, 
            email_folder_id=connectionEmailToEmailFolderNewDTO.email_folder_id
        )
        if connectionEmailToEmailFolder is not None:
            return
        
        connectionEmailToEmailFolder = ConnectionEmailToEmailFolder()
        connectionEmailToEmailFolder.email = email
        connectionEmailToEmailFolder.email_folder = emailFolder
        connectionEmailToEmailFolder.date_of_add = datetime.now()
        self.connectionEmailToEmailFolderRepository.add(obj=connectionEmailToEmailFolder)

    
    def get_list_by_user(self, user_id: int) -> List[EmailFolderPreviewViewModel]:
        """Получение перечня всех папок пользователем"""
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        emailFolders: List[EmailFolder] = self.emailFolderRepository.list_by_user_id(user_id=user_id)
        emailFolderPreviewViewModels: List[EmailFolderPreviewViewModel] = []
        if emailFolders is not None:
            for emailFolder in emailFolders:
                emailFolderPreviewViewModels.append(
                    EmailFolderPreviewViewModel(
                        id=emailFolder.id,
                        title=emailFolder.title,
                        date_of_add=emailFolder.date_of_add.strftime("%Y-%m-%d %H:%M:%S") if emailFolder.date_of_add is not None else None,
                    )
                )
        
        return emailFolderPreviewViewModels
    
    def email_lite_list_by_email_folder_id(self, user_id: int, email_folder_id: int) -> List[EmailLiteViewModel]:
        """Получение всех писем в папке пользователем"""
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        emailFolder: EmailFolder = self.emailFolderRepository.find_by_id(id=email_folder_id)
        if emailFolder is None:
            raise EmailFolderNotFoundException()
        
        if emailFolder.user_id != user_id:
            raise EmailFolderUserNotOwnedException()
        
        connectionEmailToEmailFolders: List[ConnectionEmailToEmailFolder] = self.connectionEmailToEmailFolderRepository.list_by_email_folder_id(email_folder_id=email_folder_id)

        emailFactory: EmailFactory = EmailFactory()
        emailLiteViewModels: List[EmailLiteViewModel] = []
        for connectionEmailToEmailFolder in connectionEmailToEmailFolders:
            emailLiteViewModels.append(emailFactory.create_lite_viewmodel(email=connectionEmailToEmailFolder.email))
        
        return emailLiteViewModels
        


    def delete_by_id_by_user(self, user_id: int, email_folder_id: int) -> None:
        """Удаление почтовой папки пользователем"""
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()

        emailFolder: EmailFolder = self.emailFolderRepository.find_by_id(id=email_folder_id)
        if emailFolder is None:
            raise EmailFolderNotFoundException()
    
        if emailFolder.user_id != user.id:
            raise EmailFolderUserNotOwnedException()
        
        self.emailFolderRepository.delete(obj=emailFolder)