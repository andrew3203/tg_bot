import importlib
import os
import uuid
from collections import defaultdict, namedtuple
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

from faker import Faker
from sqlalchemy_utils import create_database, drop_database
from yarl import URL

from alembic.config import Config


# faker as one instance of class Faker
faker = Faker("ru_RU")
# reproducible randomness for faker
faker.random.seed(42)


def __get_project_path() -> Path:
    path = Path(__file__).parent.resolve()
    return path.parents[1]


PROJECT_PATH: Path = __get_project_path()


def make_alembic_config(
    cmd_opts: SimpleNamespace, base_path: Path = PROJECT_PATH
) -> Config:
    # Replace path to alembic.ini file to absolute
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(str(base_path), cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)  # type: ignore

    # Replace path to alembic folder to absolute
    alembic_location = config.get_main_option("script_location")
    if not os.path.isabs(alembic_location):  # type: ignore
        config.set_main_option("script_location", os.path.join(base_path, alembic_location))  # type: ignore

    if cmd_opts.test_db_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.test_db_url)
        config.set_main_option("test_db_url", cmd_opts.test_db_url)

    return config


def alembic_config_from_url(test_db_url: str | None = None) -> Config:
    """
    Provides Python object, representing alembic.ini file.
    """
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        test_db_url=test_db_url,
    )

    return make_alembic_config(cmd_options)


# Represents test for 'data' migration.
# Contains revision to be tested, it's previous revision, and callbacks that
# could be used to perform validation.
MigrationValidationParamsGroup = namedtuple(  # type: ignore
    "MigrationData", ["rev_base", "rev_head", "on_init", "on_upgrade", "on_downgrade"]
)


def load_migration_as_module(file: str):
    """
    Allows to import alembic migration as a module.
    """
    return importlib.machinery.SourceFileLoader(
        file, os.path.join(PROJECT_PATH, "alembic", "versions", file)
    ).load_module()


def make_validation_params_groups(*migrations) -> list[MigrationValidationParamsGroup]:
    """
    Creates objects that describe test for data migrations.
    See examples in testsdata_migrations/migration_*.py.
    """
    data = []
    for migration in migrations:
        # Ensure migration has all required params
        for required_param in ["rev_base", "rev_head"]:
            if not hasattr(migration, required_param):
                raise RuntimeError(
                    f"{required_param} not specified for {migration.__name__}"
                )

        # Set up callbacks
        callbacks = defaultdict(lambda: lambda *args, **kwargs: None)  # type: ignore
        for callback in ["on_init", "on_upgrade", "on_downgrade"]:
            if hasattr(migration, callback):
                callbacks[callback] = getattr(migration, callback)

        data.append(
            MigrationValidationParamsGroup(
                rev_base=migration.rev_base,
                rev_head=migration.rev_head,
                on_init=callbacks["on_init"],
                on_upgrade=callbacks["on_upgrade"],
                on_downgrade=callbacks["on_downgrade"],
            )
        )

    return data


@contextmanager
def tmp_database_url(
    db_url: URL, suffix: str = "", **kwargs
) -> Generator[str, None, None]:
    tmp_db_name = ".".join([uuid.uuid4().hex, "app", suffix])
    tmp_db_url = str(db_url.with_path(tmp_db_name))
    create_database(tmp_db_url, **kwargs)

    try:
        yield tmp_db_url
    finally:
        drop_database(tmp_db_url)


def from_sync_to_async_url_connection(sunc_url: str) -> str:
    res = sunc_url.split("://")
    if len(res) == 2:
        url = res[0] + "+asyncpg://" + res[1]
        return url
    return sunc_url
