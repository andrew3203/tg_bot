from datetime import datetime
from pydantic import Field
from ..base_model import BaseModel
from enum import Enum


class MediaType(str, Enum):
    MP4 = "mp4"
    MOV = "mov"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    GIF = "gif"
    WEBP = "webp"

    @property
    def is_video(self):
        return self in [MediaType.MP4, MediaType.MOV]

    @property
    def is_image(self):
        return self in [
            MediaType.PNG,
            MediaType.JPG,
            MediaType.JPEG,
            MediaType.GIF,
            MediaType.WEBP,
        ]


class MessageDataList(BaseModel):
    id: int = Field(description="Id")
    name: str = Field(description="Message name")
    group_id: int = Field(description="Group id")
    group_name: str = Field(description="Group name")
    tg_alias_name: str = Field(description="Tg alias name")
    click_amount: int = Field(description="Click amount")
    uclick_amount: int = Field(description="Unique click amount")
    created_at: datetime = Field(description="Created at")
    updated_at: datetime | None = Field(description="Updated at")
