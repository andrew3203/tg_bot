"""add base data

Revision ID: 7ad163b1fc68
Revises: d379ea6810fb
Create Date: 2024-05-12 14:27:29.321410

"""
from alembic import op
import sqlmodel
from sqlmodel import delete
from app.bot.utils import get_group, get_messages
from app.models import Group, Message

# revision identifiers, used by Alembic.
revision = "7ad163b1fc68"
down_revision = "d379ea6810fb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with sqlmodel.Session(bind=op.get_bind()) as session:
        group = get_group() 
        session.add(group)
        session.commit()
        for message in get_messages():
            session.add(message)
        session.commit()


def downgrade() -> None:
    with sqlmodel.Session(bind=op.get_bind()) as session:
        for message in get_messages():
            session.exec(delete(Message).where(Message.id == message.id))
        
        group = get_group() 
        session.exec(delete(Group).where(Group.id == group.id))
        session.commit()