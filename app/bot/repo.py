from app.bot.selectors import MessageSelector
from app.bot.services import ParseMessageService, SendMessageService
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
    ) -> None:
        self.session = session

        self.parser = parser
        self.service = service
        self.selector = selector

    async def _process_callback_query(self, update: Update) -> None:
        query = update.callback_query
        if query is not None:
            await query.answer()
            await query.edit_message_reply_markup(reply_markup=None)

    async def process(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.parser.init(update=update)
        await self._process_callback_query(update=update)

        user = await self.selector.get_user(user_id=self.parser.chat_id)
        if self.parser.new_message_id is not None:
            message = await self.selector.get_message(
                user=user, message_id=self.parser.new_message_id
            )
            await self.service.send_message(user_id=user.id, message=message)
        elif self.parser.msg_text is not None:
            message = await self.selector.get_message_by_alias(
                user=user, tg_alias_name=self.parser.msg_text
            )
            await self.service.send_message(user_id=user.id, message=message)

    async def process_error(
        self, update: Update | object, context: ContextTypes.DEFAULT_TYPE
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

        if context.error is not None:
            tb_string = "".join(
                traceback.format_exception(
                    None, context.error, context.error.__traceback__
                )
            )
            update_str = update.to_dict() if isinstance(update, Update) else str(update)
            message = (
                "Возникла ошибка\n"
                f"<pre>{html.escape(tb_string)}</pre>\n\n"
                f"<pre>update: {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
                "</pre>\n\n"
                f"<pre>chat_data: {html.escape(str(context.chat_data))}</pre>\n\n"
            )
            await context.bot.send_message(
                chat_id=settings.LOGS_CHAT_ID,
                text=message,
                parse_mode=ParseMode.HTML,
            )
