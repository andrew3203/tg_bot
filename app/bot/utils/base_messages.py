from enum import Enum
from typing import NamedTuple


class BaseMessage(NamedTuple):
    id: int
    name: str


class BaseMessageNames(BaseMessage, Enum):
    MESSAGE_NOT_FOUND = BaseMessage(name="message_not_found", id=1)
    USER_NOT_FOUND = BaseMessage(name="user_not_found", id=2)
    ERROR_MESSAGE = BaseMessage(name="error_message", id=3)
