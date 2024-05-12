import logging
import aiohttp
from telegram import Bot
from app.models import Action, Message, User, UserResponse, UserResponseType
from sqlmodel.ext.asyncio.session import AsyncSession
from .click_counter import ClickCounterService
from app.schema.models.action_type import ActionType
from app.bot.exceptions import CoreException
from config.settings import settings
from sqlmodel import select

logger = logging.getLogger(__name__)


class ActionService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self._signup_url = "https://crm.portobello.ru/api/telegram/sign-up"

    async def _process_register(self, message: Message, user: User, **kwargs) -> bool:
        portobello_id: int | None = kwargs.get("portobello_id")
        if portobello_id is None:
            logger.error(f"{user}: `portobello_id` is None")
            return False

        data = {"tg_user_id": user.id, "bd_user_id": portobello_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(self._signup_url, json=data) as response:
                if response.status not in (200, 201, 202, 203, 204):
                    logger.error(
                        f"register faild: {user}, portobello_id:{portobello_id}, status:{response.status}"
                    )
                    return False

        return True

    async def _process_calc_click(self, message: Message, user: User, **kwargs) -> bool:
        click_service = ClickCounterService()
        message = await click_service.count_message_unclick(
            message=message,
            user=user,
        )
        message.click_amount += 1
        self.session.add(message)
        await self.session.commit()
        return True

    async def __validate_params(self, user: User, params: dict) -> None:
        missing_params = [key for key, value in params.items() if value is None]
        if len(missing_params) > 0:
            logger.error(f"{user}: params `{missing_params}` are blank")
            raise CoreException(f"Missing params: {missing_params}")

    async def _process_support(self, message: Message, user: User, **kwargs) -> bool:
        params = {
            "bot": kwargs.get("bot"),
            "user_msg_text": kwargs.get("user_msg_text"),
            "user_msg_id": kwargs.get("user_msg_id"),
        }
        await self.__validate_params(user=user, params=params)

        bot = params["bot"]
        if not isinstance(bot, Bot):
            raise CoreException("bot is not instance of Bot")

        support_message = (
            f"Пользователь: {user.id} ({user.firstname} {user.lastname})\n"
            f"Компания: {user.company}\n"
            f"Текст обращения:\n{params['user_msg_text']}"
        )
        bot.send_message(
            chat_id=settings.SUPPORT_CHAT_ID,
            text=support_message,
        )
        bot.send_message(
            chat_id=user.id,
            reply_to_message_id=params["user_msg_id"],
            text="Сообщение отправлено в службу поддержки.",
        )
        return True

    async def _process_save_response(
        self,
        message: Message,
        user: User,
        **kwargs,
    ) -> bool:
        params = {
            "user_msg_text": kwargs.get("user_msg_text"),
            "user_response_type_name": kwargs.get("user_response_type_name"),
        }
        try:
            await self.__validate_params(user=user, params=params)
        except CoreException as e:
            logger.error(f"response was not saved: {e.msg}")
        result = await self.session.exec(
            select(UserResponseType).where(
                UserResponseType == params["user_response_type_name"]
            )
        )
        user_response_type = result.one()
        if user_response_type is None:
            logger.error(f"{user}: `user_response_type` is None")
            return False

        user_response = UserResponse(
            user_id=user.id,
            message_id=message.id,
            response_type_name=user_response_type.name,
            text=params["user_msg_text"],
        )
        self.session.add(user_response)

        return False

    async def inc_action_click(self, action: Action, result: bool) -> None:
        if result:
            action.succeded_amount += 1
        action.run_amount += 1
        self.session.add(action)

    async def process_action(self, message: Message, user: User, **kwargs) -> None:
        """
        info:
            - REGISTER: need params: `portobello_id`
            - CALC_CLICK: need params: None
            - SUPPORT: need params: `bot`, `user_msg_text`, `user_msg_id`
            - SAVE_RESPONSE: need params: `user_msg_text`, `user_response_type_name`
        """
        action_result = await self.session.exec(
            select(Action).where(Action.message_id == message.id)
        )
        actions = action_result.all()
        if len(actions) == 0:
            return

        actions_dict = {
            ActionType.REGISTER: self._process_register,
            ActionType.CALC_CLICK: self._process_calc_click,
            ActionType.SUPPORT: self._process_support,
            ActionType.SAVE_RESPONSE: self._process_save_response,
        }

        for action in actions:
            add_data = {**kwargs, **action.params}
            action.params
            result = await actions_dict[action.action_type](
                message=message,
                user=user,
                **add_data,
            )
            await self.inc_action_click(action=action, result=result)
        await self.session.commit()
