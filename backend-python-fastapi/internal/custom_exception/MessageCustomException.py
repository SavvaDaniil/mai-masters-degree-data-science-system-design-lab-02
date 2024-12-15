from internal.abstracts.NotCriticalExceptionAbstract import NotCriticalExceptionAbstract

class MessageContentIsEmptyException(NotCriticalExceptionAbstract):
    def __init__(self):
        super().__init__("message content is empty")