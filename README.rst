===========================
    django-monkey-team
===========================

.. image:: https://secure.travis-ci.org/ionelmc/django-monkey-team.png
    :alt: Build Status
    :target: http://travis-ci.org/ionelmc/django-monkey-team

.. image:: https://coveralls.io/repos/ionelmc/django-monkey-team/badge.png?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/django-monkey-team

.. image:: https://badge.fury.io/py/django-monkey-team.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/django-monkey-team

This is a middleware that displays debug tracebacks on production sites (where
you would have `DEBUG = False`) only to developers. Developers have to install a
special userscript to decode the traceback data. AES-256 (CBC mode) is used to
encrypt the traceback. The decode key and client key are hashes of your
SECRET_KEY with salts so your SECRET_KEY is safe even if your userscript gets in
the wrong place.

Google Chrome and Firefox are supported. If you want to use something else you
have to find a way to install the userscript yourself.

There's also a decode page in the admin in case you get user reports with the
encrypted data.

The error page and decrypt flow looks like this:

.. image:: https://github.com/ionelmc/django-monkey-team/raw/master/docs/monkey-dispatch.png
    :alt: Sample error page
    :target: https://github.com/ionelmc/django-monkey-team/raw/master/docs/monkey-dispatch.png


Installation guide
==================

Install it::

    pip install django-monkey-team

Change your Django project settings to have:

.. code-block:: python

    INSTALLED_APPS += (
        'monkey_team',
    )
    MIDDLEWARE_CLASSES += (
        'monkey_team.middleware.MonkeyTeamMiddleware',
    )
    DEBUG = False

Note, that if you want ``DEBUG = True`` and still have the middleware on you need to set:

.. code-block:: python

    MONKEY_FORCE_ACTIVE = True

Then go to django admin and install the userscript. The setup page looks like
this:


.. image:: https://github.com/ionelmc/django-monkey-team/raw/master/docs/monkey-admin.png
    :alt: Userscript install page
    :target: https://github.com/ionelmc/django-monkey-team/raw/master/docs/monkey-admin.png

Requirements
============

:OS: Any
:Runtime: Python 2.6, 2.7
:Packages: PyCrypto, Django>=1.3 (up to 1.6)
