from telegram import Bot
from app.models import Message, User
from telegram import InputMediaPhoto, InputMediaVideo, InputMedia
from app.schema.models.message import MediaType
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class SendMessageService:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def _get_message_media(self, message: Message) -> list | None:
        if len(message.media) == 0:
            return None

        media: list[InputMedia] = []
        for media_url, media_type in zip(message.media, message.media_types):
            if MediaType(media_type).is_image:
                media.append(InputMediaPhoto(media_url))
            elif MediaType(media_type).is_video:
                media.append(InputMediaVideo(media_url))
        return media

    async def __get_cols_rows_count(self, childrens_count: int) -> tuple[int, int]:
        if childrens_count <= 3:
            return childrens_count, 1

        first_row = childrens_count // 2 + childrens_count % 2
        second_row = childrens_count - first_row
        return first_row, second_row

    async def get_markup(self, message: Message) -> InlineKeyboardMarkup | None:
        childrens_count = len(message.childrens)
        if childrens_count == 0:
            return None

        children_keys = list(message.childrens.keys())
        rows_count, cols_count = await self.__get_cols_rows_count(
            childrens_count=childrens_count
        )
        keyboard: list[list[InlineKeyboardButton]] = []
        for i in range(rows_count):
            keyboard.append([])
            for j in range(cols_count):
                key = children_keys[i * cols_count + j]
                keyboard[i].append(
                    InlineKeyboardButton(text=key, callback_data=message.childrens[key])
                )

        return InlineKeyboardMarkup(keyboard)

    async def send_message(self, message: Message, user: User) -> None:
        media = await self._get_message_media(message)
        if media is not None:
            await self.bot.send_media_group(
                chat_id=user.id,
                media=media,
            )

        reply_markup = await self.get_markup(message)
        await self.bot.send_message(
            chat_id=user.id,
            text=message.text,
            parse_mode="HTML",
            reply_markup=reply_markup,
        )
