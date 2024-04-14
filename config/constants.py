"""
Contains general constats of the project
"""

from enum import Enum

DB_NAMING_CONVENTION = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__" "%(referred_table_name)s"),
    "pk": "pk__%(table_name)s",
}


class Stage(str, Enum):
    """
    Describes project stages (LOCAL, STAGING, TESTING, PRODUCTION)
    """

    LOCAL = "LOCAL"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        """Check if current setting in LOCAL, STAGING or TESTING mode"""
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        """Check if current setting in TESTING mode"""
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        """Check if current setting in STAGING or PRODUCTION mode"""
        return self == self.PRODUCTION
