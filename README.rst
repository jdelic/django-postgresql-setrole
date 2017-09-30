django-postgresql-setrole
=========================

A Django application that executes `SET ROLE` on every connection to PostgreSQL
opened by Django. This is useful if you're using external authentication
managers like `Hashicorp Vault <http://vaultproject.io/>`__\ .

PostgreSQL's user model ("roles") assigns every object created in a database/
tablespace/schema an "owner". Said owner is the *only* user that can modify or
drop the object. This means that user credentials leased from Vault which
expire after some time, can't be used to create or migrate tables unless you
use the same user name every time (which would defeat the purpose).

The solution is to create an "owner role". In layman's terms "a group that has
all necessary permissions on the database and the INHERIT attribute and will
act as the 'sudo' user for leased users from the authentication manager". All
users created by the authentication manager will then be assigned this group
and when they connect to the database execute "SET ROLE <owner role>", thereby
making all objects created owned by the owner role.


How do I use this Django application?
-------------------------------------
Add `postgresql_setrole` to `INSTALLED_APPS`. Then in `settings.DATABASES` add

.. code-block:: python

    DATABASES = {
        "default": {
            ...,  # other settings
            "SET_ROLE": "mydatabaseowner",
        }.
    }


Why is SET ROLE necessary?
--------------------------
The `INHERIT` attribute is not bidirectional. So if a (user) role is assigned
a (group) role it inherits the group's permissions, but the group does not
gain any rights on objects created by the user role.

So what you want is the (group) owner role to own everything.


How do I set this up?
---------------------
On your shell as the `postgres` superuser:

.. code-block:: shell

    # --- create an admin role for Vault
    # no create database
    # encrypt password
    # do not inherit rights
    # can create roles
    # not a superuser
    createuser -D -E -I -l -r -S vaultadmin

    # --- create an owner role for your database
    # no create database
    # encrypt password
    # do not inherit rights
    # can't create roles
    # not a superuser
    createuser -D -E -I -L -R -S mydatabaseowner
    createdb -E utf8 -O mydatabaseowner mydatabase

Then configure Vault to create roles like this:

.. code-block:: shell

    $ vault mount -path=postgresql database
    $ vault write postgresql/config/mydatabase \
                      plugin_name=postgresql-database-plugin \
                      allowed_roles="mydatabase_fullaccess" \
                      connection_url="postgresql://mydatapaseowner:[mydatabasepassword]@localhost:5432/"
    $ vault write postgresql/roles/mydatabase_fullaccess -
    {
        "db_name": "mydatabase",
        "default_ttl": "10m",
        "max_ttl": "1h",
        "creation_statements": "CREATE ROLE \"{{name}}\" WITH LOGIN ENCRYPTED PASSWORD '{{password}}' VALID UNTIL '{{expiration}}' IN ROLE \"mydatabaseowner\" INHERIT NOCREATEROLE NOCREATEDB NOSUPERUSER NOREPLICATION NOBYPASSRLS;",
        "revocation_statements": "DROP ROLE \"name\";"
    }

Then users created by Vault when they log in must run

.. code-block:: sql

    SET ROLE "mydatabaseowner";

This ensures that all created tables and other objects belong to
`mydatabaseowner`.


License
=======

Copyright (c) 2016-2017, Jonas Maurus
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
