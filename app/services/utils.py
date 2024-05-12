from app.models import Group
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config.settings import settings

from app.json import json

sync_engine = create_engine(
    str(settings.SYNC_DATABASE_URL),
    echo=False,
    future=True,
    json_serializer=json.dumps,
    json_deserializer=json.loads,
    pool_size=30,
    pool_timeout=10,
)


def apply_group_criteria(group: Group):
    if group.criterion_value_type == "int":
        criterion_expression = f"{group.criterion_field} {group.criterion_rule} {int(group.criterion_value)}"
    elif group.criterion_value_type == "float":
        criterion_expression = f"{group.criterion_field} {group.criterion_rule} {float(group.criterion_value)}"
    elif group.criterion_value_type == "bool":
        criterion_expression = f"{group.criterion_field} {group.criterion_rule} {bool(group.criterion_value)}"
    elif group.criterion_value_type == "datetime":
        criterion_expression = (
            f"{group.criterion_field} {group.criterion_rule} '{group.criterion_value}'"
        )
    else:
        criterion_expression = (
            f"{group.criterion_field} {group.criterion_rule} '{group.criterion_value}'"
        )

    query = text(
        f"UPDATE public.user SET group_id = :group_id WHERE {criterion_expression}"
    )

    with Session(sync_engine) as session:
        session.execute(query, {"group_id": group.id})
        session.commit()
