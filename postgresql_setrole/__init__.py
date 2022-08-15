# -* encoding: utf-8 *-
import warnings

import django
from postgresql_setrole.apps import DjangoPostgreSQLSetRoleApp


if django.VERSION < (3, 2):
    default_app_config = 'postgresql_setrole.DjangoPostgreSQLSetRoleApp'
