django-postgresql-setrole
=========================

A Django application that executes `SET ROLE` on every connection to PostgreSQL
opened by Django. This is useful if you're using external authentication
managers like `Hashicorp Vault <http://vaultproject.io/>`__\ .

PostgreSQL's user model ("roles") assigns every object created in a database/
tablespace/schema an "owner". Said owner is the *only* user that can modify or
drop the object. This means that using a user leased from Vault that expires
after a while can't be used to create or migrate tables unless you use the same
user every time.

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

    # no create database
    # encrypt password
    # does not inherit rights
    # can't create roles
    # not a superuser
    createuser -D -E -I -L -R -S mydatabaseowner
    createdb -E utf8 -O mydatabaseowner mydatabase

Then configure Vault to create roles like this:

.. code-block:: shell

    $ vault mount -path=mydatabase-auth postgresql
    $ vault write vault write mydatabase-auth/roles/fullaccess sql=-
    CREATE ROLE "{{name}}" WITH LOGIN PASSWORD '{{password}}' VALID
    UNTIL '{{expiration}}' IN ROLE "mydatabaseowner" INHERIT NOCREATEROLE
    NOCREATEDB NOSUPERUSER NOREPLICATION NOBYPASSRLS;

Then users created by Vault when they log in must run

.. code-block:: sql

    SET ROLE "mydatabaseowner";

This ensures that all created tables and other objects belong to
`mydatabaseowner`.
