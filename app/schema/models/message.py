from datetime import datetime
from pydantic import Field
from ..base_model import BaseModel


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
