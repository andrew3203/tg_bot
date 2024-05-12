import logging
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
import logging.config
from app.bot.repo import Repository
from config.settings import settings
from app.bot.services import SendMessageService, ParseMessageService, ActionService
from app.bot.selectors import MessageSelector

from app.database import get_async_session


application: Application


logging.config.fileConfig(settings.LOGGING_CONF_PATH, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async for session in get_async_session():
        repo = Repository(
            session=session,
            parser=ParseMessageService(),
            service=SendMessageService(bot=application.bot),
            selector=MessageSelector(session=session),
            action_service=ActionService(session=session),
        )
        await repo.process(update=update, context=context)


async def query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async for session in get_async_session():
        repo = Repository(
            session=session,
            parser=ParseMessageService(),
            service=SendMessageService(bot=application.bot),
            selector=MessageSelector(session=session),
            action_service=ActionService(session=session),
        )
        await repo.process(update=update, context=context)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
    async for session in get_async_session():
        repo = Repository(
            session=session,
            parser=ParseMessageService(),
            service=SendMessageService(bot=application.bot),
            selector=MessageSelector(session=session),
            action_service=ActionService(session=session),
        )
        await repo.process_error(update=update, context=context)


def add_handlers(application: Application) -> None:
    application.add_handler(MessageHandler(filters.COMMAND, message_handler))
    application.add_handler(CallbackQueryHandler(query_handler))

    application.add_error_handler(error_handler)


async def process_event(payload: dict, application: Application) -> None:
    update = Update.de_json(payload, application.bot)
    await application.process_update(update)


async def setup_webhook(application: Application) -> None:
    await application.bot.set_webhook(
        "https://" + settings.SITE_DOMAIN + "/bot/webhook",
        secret_token=settings.TELEGRAM_BOT_WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES,
    )
    await application.start()


def setup_application(is_webhook: bool = False) -> Application:
    application_builder = Application.builder().token(settings.TELEGRAM_BOT_TOKEN)

    if is_webhook:
        application_builder.updater(None)

    global application
    application = application_builder.build()
    add_handlers(application)

    return application


def run_polling(application: Application) -> None:
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        timeout=60,
        read_timeout=10,
        connect_timeout=10,
    )
