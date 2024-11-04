
from internal.abstracts.NotCriticalExceptionAbstract import NotCriticalExceptionAbstract

class EmailNotFoundException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("email not found")

class EmailUserFromNotFoundException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("user from not found")

class EmailUserToNotFoundException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("user to not found")

class EmailUserNotOwnedException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("user not owned email")

class EmailSendFailedException(NotCriticalExceptionAbstract):
    def __init__(self, e: Exception):
        super().__init__("email not send, error: " + str(e))

class EmailAlreadySentException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("email already sent")