from collections.abc import Sequence
from .pagination import PaginatedDataBase
from app.models import (
    User,
    UserResponse,
    UserResponseType,
    Admin,
    Broadcast,
    Group,
)
from app.schema.models import ActionDataList, MessageDataList


class PaginatedUser(PaginatedDataBase):
    data: Sequence[User]


class PaginatedUserResponse(PaginatedDataBase):
    data: list[UserResponse]


class PaginatedUserResponseType(PaginatedDataBase):
    data: list[UserResponseType]


class PaginatedAction(PaginatedDataBase):
    data: list[ActionDataList]


class PaginatedAdmin(PaginatedDataBase):
    data: list[Admin]


class PaginatedBroadcast(PaginatedDataBase):
    data: list[Broadcast]


class PaginatedGroup(PaginatedDataBase):
    data: list[Group]


class PaginatedMessage(PaginatedDataBase):
    data: list[MessageDataList]
