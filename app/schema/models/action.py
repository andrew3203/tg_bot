from datetime import datetime
from pydantic import Field
from ..base_model import BaseModel


class ActionDataList(BaseModel):
    id: int = Field(description="Id")
    name: str = Field(description="Action name")
    run_amount: int = Field(description="Run amount")
    succeded_amount: int = Field(description="Succeded amount")
    message_name: str = Field(description="Message name")
    message_id: int = Field(description="Message id")
    created_at: datetime = Field(description="Created at")
    updated_at: datetime | None = Field(description="Updated at")
