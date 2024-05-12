from .exceptions import CoreException
from app.schema.models.message import MediaType


async def get_media_type(media_url: str) -> MediaType:
    media_url = media_url.lower()
    if media_url.endswith(".mp4"):
        return MediaType.MP4
    elif media_url.endswith(".mov"):
        return MediaType.MOV
    elif media_url.endswith(".png"):
        return MediaType.PNG
    elif media_url.endswith(".jpg") or media_url.endswith(".jpeg"):
        return MediaType.JPG
    elif media_url.endswith(".gif"):
        return MediaType.GIF
    elif media_url.endswith(".webp"):
        return MediaType.WEBP
    else:
        raise CoreException(msg="Такого типа медиа не существует")
