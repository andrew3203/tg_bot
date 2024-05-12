from telegram import Update

from app.bot.exceptions import CoreException
from enum import Enum


class MsgTypes(str, Enum):
    UNDEFINED = "UNDEFINED"
    MSG = "MSG"
    FLY_BTN = "FLY_BTN"


class ParseMessageService:
    """
    params:
        - `msg_type` - тип сообщения
        - `chat_id` - id чата (id пользователя)
        - `user_msg_id` - id сообщения телеграм
        - `new_message_id` - id нового сообщения (id внутреннего сообщения)
        - `user_msg_text` - текст сообщения

        Либо `new_message_id` будет пустым либо `user_msg_text`
    """

    def __init__(self) -> None:
        self.msg_type = MsgTypes.UNDEFINED
        self.chat_id: int
        self.user_msg_id: int
        self.new_message_id: int | None = None
        self.user_msg_text: str | None = None

    async def _set_chat_id(self, update: Update):
        callback = update.callback_query
        if update.effective_chat is not None:
            self.chat_id = update.effective_chat.id
        elif update.message is not None:
            self.chat_id = update.message.chat_id
            self.msg_type = MsgTypes.MSG
        elif update.effective_user is not None:
            self.chat_id = update.effective_user.id
        elif (
            callback is not None
            and callback.message is not None
            and callback.message.chat is not None
        ):
            self.chat_id = callback.message.chat.id
            self.msg_type = MsgTypes.FLY_BTN
        else:
            raise CoreException(msg="Не удалось определить чат")
        return self.chat_id

    async def _set_msq_id(self, update: Update):
        query = update.callback_query

        if update.message is not None:
            self.user_msg_id = update.message.id
            self.msg_type = MsgTypes.MSG
        elif update.edited_message is not None:
            self.user_msg_id = update.edited_message.id
        elif (
            query is not None
            and query.message is not None
            and query.message.message_id is not None
        ):
            self.user_msg_id = query.message.message_id
        else:
            raise CoreException(msg="Не удалось определить id сообщения")

    async def _set_msq_text(self, update: Update):
        callback = update.callback_query
        if update.message is not None and update.message.text is not None:
            self.user_msg_text = update.message.text
        elif (
            callback is not None
            and callback.data is not None
            and callback.data.isdigit()
        ):
            self.new_message_id = int(callback.data)
            self.msg_type = MsgTypes.FLY_BTN
        else:
            raise CoreException(msg="Не удалось определить id сообщения")

    async def init(self, update: Update) -> None:
        await self._set_chat_id(update=update)
        await self._set_msq_id(update=update)
        await self._set_msq_text(update=update)
