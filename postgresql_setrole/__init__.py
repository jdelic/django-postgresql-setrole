# -* encoding: utf-8 *-
from django.apps import AppConfig
from django.db.backends.postgresql.base import DatabaseWrapper as PostgreSQLDatabaseWrapper
from django.db.backends.signals import connection_created
from typing import Any, Type


def setrole_connection(*, sender: Type[PostgreSQLDatabaseWrapper],
                       connection: PostgreSQLDatabaseWrapper, **kwargs: Any) -> None:
    if "options" in connection.settings_dict and "set_role" in connection.settings_dict["options"]:
        connection.cursor().execute("SET ROLE %s",
                                    (sender.settings_dict["options"]["set_role"],))


class DjangoPostgreSQLSetRoleApp(AppConfig):
    name = "postgresql_setrole"

    def ready(self) -> None:
        connection_created.connect(setrole_connection, sender=PostgreSQLDatabaseWrapper)


default_app_config = 'postgresql_setrole.DjangoPostgreSQLSetRoleApp'
