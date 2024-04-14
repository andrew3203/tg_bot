"""
Test can find cases, when you've changed something in migration and forgot
about models for some reason (or vice versa).

Test can find forgotten downgrade methods, undeleted data types in downgrade
methods, typos and many other errors.

Does not require any maintenance - you just add it once to check 80% of typos
and mistakes in migrations forever.
"""

import pytest
from sqlalchemy.engine.base import Engine
from sqlmodel import SQLModel

from alembic.autogenerate.api import compare_metadata
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import Script, ScriptDirectory
from app.tests.utils import alembic_config_from_url


def test_migrations_up_to_date(alembic_config: Config, postgres_engine: Engine):
    upgrade(alembic_config, "head")

    migration_ctx = MigrationContext.configure(postgres_engine.connect())
    diff = compare_metadata(migration_ctx, SQLModel.metadata)
    assert not diff


def get_revisions():
    # Create Alembic configuration object
    # (we don't need database for getting revisions list)
    config = alembic_config_from_url()

    # Get directory object with Alembic migrations
    revisions_dir = ScriptDirectory.from_config(config)

    # Get & sort migrations, from first to last
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)

    # We need -1 for downgrading first migration (its down_revision is None)
    downgrade(alembic_config, revision.down_revision or "-1")  # type: ignore
    upgrade(alembic_config, revision.revision)
