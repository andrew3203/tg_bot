from app.models import Group, Message
from .base_messages import BaseMessageNames


def get_group() -> Group:
    group = Group(
        id=1,
        name="General",
        description="General group for all messages and users",
        criterion_field="id",
        criterion_field_type="int",
        criterion_value="-1",
        criterion_value_type="int",
        criterion_rule=">",
    )
    return group


def get_messages() -> list[Message]:
    result = [
        Message(
            id=data.id,
            group_id=1,
            parents={},
            childrens={},
            name=data.name,
            tg_alias_name=data.name,
            text=data.name,
            media=[],
            media_types=[],
        )
        for data in BaseMessageNames
    ]

    return result
