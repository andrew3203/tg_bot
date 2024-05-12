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
            id=item.id,
            group_id=1,
            parents={},
            childrens={},
            name=item.name,
            tg_alias_name=item.name,
            text=item.name,
            media=[],
            media_types=[],
        )
        for item in BaseMessageNames
    ]

    return result
