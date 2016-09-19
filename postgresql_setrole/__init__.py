# -* encoding: utf-8 *-
from django.apps import AppConfig
from django.db.backends.postgresql.base import DatabaseWrapper as PostgreSQLDatabaseWrapper
from django.db.backends.signals import connection_created


def setrole_connection(sender: PostgreSQLDatabaseWrapper, connection: 'psycopg2._psycopg.connection') -> None:
    if "options" in sender.settings_dict and "set_role" in sender.settings_dict["options"]:
        connection.cursor().execute("SET ROLE %s",
                                    (sender.settings_dict["options"]["set_role"],))


class DjangoPostgreSQLSetRoleApp(AppConfig):
    def ready(self) -> None:
        connection_created.connect(setrole_connection, sender=PostgreSQLDatabaseWrapper)


default_app_config = 'postgresql_setrole.DjangoPostgreSQLSetRoleApp'
