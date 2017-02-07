# -* encoding: utf-8 *-
import warnings

from django.apps import AppConfig
from django.db.backends.postgresql.base import DatabaseWrapper as PostgreSQLDatabaseWrapper
from django.db.backends.signals import connection_created
from typing import Any, Type


warning_given = False

def setrole_connection(*, sender: Type[PostgreSQLDatabaseWrapper],
                       connection: PostgreSQLDatabaseWrapper, **kwargs: Any) -> None:
    global warning_given
    role = None
    if "set_role" in connection.settings_dict:
        role = connection.settings_dict["set_role"]
    elif "SET_ROLE" in connection.settings_dict:
        role = connection.settings_dict["SET_ROLE"]

    if role:
        connection.cursor().execute("SET ROLE %s", (role,))
    else:
        if not warning_given:
            warnings.warn("postgresql_setrole app is installed, but no SET_ROLE value is in settings.DATABASE")
            warning_given = True  # Once is enough


class DjangoPostgreSQLSetRoleApp(AppConfig):
    name = "postgresql_setrole"

    def ready(self) -> None:
        connection_created.connect(setrole_connection, sender=PostgreSQLDatabaseWrapper)


default_app_config = 'postgresql_setrole.DjangoPostgreSQLSetRoleApp'
