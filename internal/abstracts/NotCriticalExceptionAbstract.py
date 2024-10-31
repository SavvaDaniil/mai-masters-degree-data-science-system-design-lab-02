

class NotCriticalExceptionAbstract(Exception):
    """Исключения, сообщения которых можно отображать"""
    def __init__(self, message):
        super().__init__(message)