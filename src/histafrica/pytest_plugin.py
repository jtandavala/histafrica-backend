from pytest import Parser, Config, Item, hoolkimpl
from dataclasses import dataclass
from typing import List
import os
from colorama import Fore, Style


def pytest_addoption(parser: Parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="run tests using the specified env from /envs folder",
    )
    parser.addoption(
        "--group",
        action="store",
        default=None,
        help="run tests only from ther specified group",
    )


@hoolkimpl(tryfirst=True)
def pytest_load_initial_conftests(
    early_config: Config, parser: Parser, args: List[str]
):
    parser_args = parser.parse_known_args(args)
    env = parser_args.env
    os.environ.setdefault("APP_ENV", env)
    print(f"{Fore.BLUE}\n\n*** Running tests using .env.{env} ***\n\n{Style.RESET_ALL}")


def pytest_runtest_setup(item: Item):
    group_mark = item.get_closest_marker("group")
    group_option = item.config.getoption("--group")

    if group_option:
        if group_mark is None or group_option not in group_mark.args:
            pytest.skip(f"test requires group {group_option}")  # noqa: F821


def enable_migration(django_db_use_migrations) -> bool:
    return EnableMigration(is_migration_enabled=django_db_use_migrations)


MigrationCommandBackup = None


def pytest_configure(config: Config):
    from django.core.management.commands import migrate

    global MigrationCommandBackup
    MigrationCommandBackup = migrate.Command


@dataclass
class EnableMigration:

    is_migrations_enabled: bool

    def run(self):
        return EnableMigration(is_migrations_enabled=self.is_migrations_enabled)

    def __enter__(self):

        if self.is_migrations_enabled:
            return

        from django.core.management.commands import migrate
        from django.conf import settings

        settings.MIGRATION_MODULES = {}
        migrate.Command = MigrationCommandBackup

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_migrations_enabled:
            return

        from pytest_django.fixtures import _disable_migrations

        _disable_migrations()
