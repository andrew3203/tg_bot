from telegram import Update

from app.utils.exceptions import CoreException
from enum import Enum


class MsgTypes(str, Enum):
    UNDEFINED = "UNDEFINED"
    MSG = "MSG"
    FLY_BTN = "FLY_BTN"


class ParseMessageService:
    def __init__(self) -> None:
        self.msg_type = MsgTypes.UNDEFINED

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
        if update.message is not None:
            self.msg_id = update.message.id
            self.msg_type = MsgTypes.MSG
        elif update.edited_message is not None:
            self.msg_id = update.edited_message.id
        else:
            raise CoreException(msg="Не удалось определить id сообщения")

    async def _set_msq_text(self, update: Update):
        callback = update.callback_query
        if update.message is not None and update.message.text is not None:
            self.msg_text = update.message.text
        elif (
            callback is not None
            and callback.data is not None
            and callback.data.isdigit()
        ):
            self.message_id = int(callback.data)
            self.msg_type = MsgTypes.FLY_BTN
        else:
            raise CoreException(msg="Не удалось определить id сообщения")