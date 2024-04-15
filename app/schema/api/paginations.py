from collections.abc import Sequence
from .pagination import PaginatedDataBase
from app.models import (
    User,
    UserResponse,
    UserResponseType,
    Action,
    Admin,
    Broadcast,
    Group,
    Message,
)


class PaginatedUsers(PaginatedDataBase):
    data: Sequence[User]


class PaginatedUserResponse(PaginatedDataBase):
    data: list[UserResponse]


class PaginatedUserResponseType(PaginatedDataBase):
    data: list[UserResponseType]


class PaginatedAction(PaginatedDataBase):
    data: list[Action]


class PaginatedAdmin(PaginatedDataBase):
    data: list[Admin]


class PaginatedBroadcast(PaginatedDataBase):
    data: list[Broadcast]


class PaginatedGroup(PaginatedDataBase):
    data: list[Group]


class PaginatedMessage(PaginatedDataBase):
    data: list[Message]
