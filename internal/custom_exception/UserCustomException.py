
from internal.abstracts.NotCriticalExceptionAbstract import NotCriticalExceptionAbstract

class UsernameAlreadyExistsException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("username_already_exists")

class UserNotFoundException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("User not found")

class UserLoginFailedException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("wrong")