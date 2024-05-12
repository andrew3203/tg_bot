class BotBaseException(Exception):
    """
    Базовы класс ошибки для бота
    """

    def __init__(self, msg: str, code: int, *args: object) -> None:
        self.msg = msg
        self.code = code
        super().__init__(*args)


class NotFoundException(BotBaseException):
    """
    Ошибка вызываеться если какие то данные не найдены
    """

    def __init__(self, msg: str, code: int = 404, *args: object) -> None:
        super().__init__(msg, code, *args)


class UserNotFoundException(NotFoundException):
    """
    Ошибка вызываеться если пользователь не найден
    """

    def __init__(self, msg: str, code: int = 404, *args: object) -> None:
        super().__init__(msg, code, *args)


class MessageNotFoundException(NotFoundException):
    """
    Ошибка вызываеться если сообщение не найдено
    """

    def __init__(self, msg: str, code: int = 404, *args: object) -> None:
        super().__init__(msg, code, *args)


class CoreException(BotBaseException):
    """
    Ошибка вызываеться если произошла ошибка на стороне бота
    """

    def __init__(self, msg: str, code: int = 500, *args: object) -> None:
        super().__init__(msg, code, *args)
