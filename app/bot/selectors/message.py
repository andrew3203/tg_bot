from sqlmodel import select
from app.models import Message, User
from sqlmodel.ext.asyncio.session import AsyncSession
from app.utils.exceptions import NotFoundException


class FlowSelector:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user(self, user_id: int):
        result = await self.session.exec(select(User).where(User.id == user_id))
        user = result.one_or_none()
        if user is None:
            raise NotFoundException(msg="Пользователь не найден")

    async def get_message(self, user_id: int, message_id: int):
        user = await self.get_user(user_id=user_id)
        result = await self.session.exec(
            select(Message).where(
                Message.group_id == user.group_id, Message.id == message_id
            )
        )
        message = result.one_or_none()
        if message is None:
            raise NotFoundException(msg="Сообщение не найдено")
        return message
