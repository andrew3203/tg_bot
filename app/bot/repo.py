from app.bot.selectors import MessageSelector
from app.bot.services import ParseMessageService, SendMessageService, ActionService
from sqlmodel.ext.asyncio.session import AsyncSession
from telegram import Update
from telegram.ext import ContextTypes
import traceback
import html
from telegram.constants import ParseMode
import json
from config.settings import settings
from .exceptions import MessageNotFoundException, UserNotFoundException
from .utils import BaseMessageNames


class Repository:
    def __init__(
        self,
        session: AsyncSession,
        parser: ParseMessageService,
        service: SendMessageService,
        selector: MessageSelector,
        action_service: ActionService,
    ) -> None:
        self.session = session

        self.parser = parser
        self.service = service
        self.selector = selector
        self.action_service = action_service

    async def _process_callback_query(self, update: Update) -> None:
        query = update.callback_query
        if query is not None:
            await query.answer()
            await query.edit_message_reply_markup(reply_markup=None)

    async def __get_action_params(self, context: ContextTypes.DEFAULT_TYPE) -> dict:
        params = {
            "bot": context.bot,
            "user_msg_text": self.parser.user_msg_text,
            "user_msg_id": self.parser.user_msg_id,
        }
        if context.args is not None and len(context.args) > 1:
            payload = context.args[1]
            if payload and len(payload) > 0:
                params["portobello_id"] = payload
        return params

    async def process(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.parser.init(update=update)
        await self._process_callback_query(update=update)

        user = await self.selector.get_user(user_id=self.parser.chat_id)

        message, is_last = await self.selector.get_message(
            user=user,
            new_message_id=self.parser.new_message_id,
            user_msg_text=self.parser.user_msg_text,
        )

        if not is_last:
            await self.service.send_message(user_id=user.id, message=message)
            await self.selector.save_last_message(
                user_id=user.id,
                message_id=message.id,
            )

        params = await self.__get_action_params(context=context)
        await self.action_service.process_action(
            message=message,
            user=user,
            **params,
        )

    async def process_error(
        self,
        update: Update | object,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        if isinstance(update, Update):
            if isinstance(context.error, MessageNotFoundException):
                error_message_name = BaseMessageNames.MESSAGE_NOT_FOUND
            elif isinstance(context.error, UserNotFoundException):
                error_message_name = BaseMessageNames.USER_NOT_FOUND
            else:
                error_message_name = BaseMessageNames.ERROR_MESSAGE

            await self.parser.init(update=update)
            await self._process_callback_query(update=update)

            message = await self.selector.get_message_by_id(
                message_id=error_message_name.id
            )
            await self.service.send_message(
                user_id=self.parser.chat_id,
                message=message,
            )
            await self.selector.save_last_message(
                user_id=self.parser.chat_id,
                message_id=message.id,
            )

        if context.error is not None:
            tb_string = "".join(
                traceback.format_exception(
                    None, context.error, context.error.__traceback__
                )
            )
            update_str = update.to_dict() if isinstance(update, Update) else str(update)
            text = (
                "Возникла ошибка\n"
                f"<pre>{html.escape(tb_string)[0:3096]}</pre>\n\n"
                f"<pre>update: {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
                "</pre>\n\n"
                f"<pre>chat_data: {html.escape(str(context.chat_data))}</pre>\n\n"
            )
            await context.bot.send_message(
                chat_id=settings.LOGS_CHAT_ID,
                text=text,
                parse_mode=ParseMode.HTML,
            )
