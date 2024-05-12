from sqlmodel import select
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CommandHandler,
)
from app.models import User, Message
from config.settings import settings
from app.bot.services.send_message import SendMessageService
from app.bot.services.parse_message import ParseMessageService
from app.database import get_async_session

application: Application


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с встроенной клавиатурой при команде /start."""
    parser = ParseMessageService()
    await parser.init(update=update)
    service = SendMessageService(bot=application.bot)

    async for session in get_async_session():
        usr_result = await session.exec(select(User).where(User.id == parser.chat_id))
        user = usr_result.one()
        message_result = await session.exec(select(Message).where(Message.id == 1))
        message = message_result.one()
        await service.send_message(user=user, message=message)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает CallbackQuery."""
    query = update.callback_query
    if query is not None:
        await query.answer()
        await query.edit_message_text(text=f"Выбрана опция: {query.data}")

    parser = ParseMessageService()
    await parser.init(update=update)
    service = SendMessageService(bot=application.bot)

    async for session in get_async_session():
        usr_result = await session.exec(select(User).where(User.id == parser.chat_id))
        user = usr_result.one()
        message_result = await session.exec(
            select(Message).where(Message.id == parser.message_id)
        )
        message = message_result.one()
        await service.send_message(user=user, message=message)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if update.message is not None and update.message.text is not None:
        await update.message.reply_text(update.message.text)


def add_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


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
