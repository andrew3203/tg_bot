# Used in cases when we need to send a message to a user

from telegram import Bot
from telegram.request import HTTPXRequest

from config.settings import settings

request = HTTPXRequest(connection_pool_size=10)
bot = Bot(settings.TELEGRAM_BOT_TOKEN, request=request)
