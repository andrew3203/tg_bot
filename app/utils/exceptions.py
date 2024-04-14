class BaseException(Exception):
    """
    Базовы класс ошибки
    """

    def __init__(self, msg: str, code: int, *args: object) -> None:
        self.msg = msg
        self.code = code
        super().__init__(*args)


class DataExeption(BaseException):
    """
    Ошибка вызываеться если пользователь предоставил
    не верные данные
    """

    def __init__(self, msg: str, code: int = 400, *args: object) -> None:
        super().__init__(msg, code, *args)


class AccessExeption(BaseException):
    """
    Ошибка вызываеться если доступ ресурсу запрещен
    или действие не доступно согласно роли пользователя
    """

    def __init__(self, msg: str, code: int = 403, *args: object) -> None:
        super().__init__(msg, code, *args)


class NotFoundException(BaseException):
    """
    Ошибка вызываеться если чкакие то данные не найдены
    """

    def __init__(self, msg: str, code: int = 404, *args: object) -> None:
        super().__init__(msg, code, *args)


class APIException(BaseException):
    """
    Ошибка вызываеться если произошла с внешним апи
    """

    def __init__(self, msg: str, code: int = 409, *args: object) -> None:
        super().__init__(msg, code, *args)


class CoreException(BaseException):
    """
    Ошибка вызываеться если произошла какая то внутренная ошибка
    """

    def __init__(self, msg: str, code: int = 500, *args: object) -> None:
        super().__init__(msg, code, *args)
