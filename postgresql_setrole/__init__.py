# -* encoding: utf-8 *-
import warnings

from django.apps import AppConfig
from django.db.backends.postgresql.base import DatabaseWrapper as PostgreSQLDatabaseWrapper
from django.db.backends.signals import connection_created
from typing import Any, Type


def setrole_connection(*, sender: Type[PostgreSQLDatabaseWrapper],
                       connection: PostgreSQLDatabaseWrapper, **kwargs: Any) -> None:
    if "OPTIONS" in connection.settings_dict:
        role = None
        if "set_role" in connection.settings_dict["OPTIONS"]:
            role = connection.settings_dict["OPTIONS"]["set_role"]
        elif "SET_ROLE" in connection.settings_dict["OPTIONS"]:
            role = connection.settings_dict["OPTIONS"]["SET_ROLE"]

        if role:
            connection.cursor().execute("SET ROLE %s", (role,))
        else:
            warnings.warn("postgresql_setrole app is installed, but no SET_ROLE vaule is in database OPTIONS")
    else:
        warnings.warn("postgresql_setrole app is installed, but no OPTIONS dict is in database settings")

class DjangoPostgreSQLSetRoleApp(AppConfig):
    name = "postgresql_setrole"

    def ready(self) -> None:
        connection_created.connect(setrole_connection, sender=PostgreSQLDatabaseWrapper)


default_app_config = 'postgresql_setrole.DjangoPostgreSQLSetRoleApp'
