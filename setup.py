#!/usr/bin/env python
# -* encoding: utf-8 *-
import os
from setuptools import setup

HERE = os.path.dirname(__file__)

try:
    long_description = open(os.path.join(HERE, 'README.rst')).read()
except IOError:
    long_description = None


setup(
    name="django-postgresql-setrole",
    version="1.0.8",
    packages=["postgresql_setrole"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
    ],
    url="https://github.com/jdelic/django-postgresql-setrole/",
    author="Jonas Maurus (@jdelic)",
    author_email="jonas-postgresql-setrole@gopythongo.com",
    maintainer="GoPythonGo.com",
    maintainer_email="info@gopythongo.com",
    description="Execute SET ROLE on every PostgreSQL connection in the Django ORM",
    long_description=long_description,
)
