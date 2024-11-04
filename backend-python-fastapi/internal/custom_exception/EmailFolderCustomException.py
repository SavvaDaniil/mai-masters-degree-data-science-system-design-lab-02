
from internal.abstracts.NotCriticalExceptionAbstract import NotCriticalExceptionAbstract

class EmailFolderNotFoundException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("email_folder not found")

class EmailFolderUserNotOwnedException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("user not owned email_folder")
