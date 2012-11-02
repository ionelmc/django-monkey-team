===========================
    django-monkey-team
===========================

This is a middleware that displays debug tracebacks on production sites (where
you would have `DEBUG = False`) only to developers. Developers have to install a
special userscript to decode the traceback data. AES with CBC mode is used to
encrypt the traceback. The decode key is a hash of your SECRET_KEY.

Google Chrome and Firefox are supported. If you want to use something else you
have to find a way to install the userscript yourself.

It looks like this: |monkey-dispatch|

.. |monkey-dispatch| image:: https://github.com/ionelmc/django-monkey-team/raw/master/docs/monkey-dispatch.png

Installation guide
==================

Install it::

    pip install django-monkey-team

Change your Django project settings to have::

    INSTALLED_APPS += (
        'monkey_team',
    )
    MIDDLEWARE_CLASSES += (
        'monkey_team.middleware.MonkeyTeamMiddleware',
    )



Requirements
============

The project has been tested on Django 1.1, 1.2, 1.3, 1.4 and trunk with Python
2.6 and 2.7.

|status|_

.. |status| image:: http://travis-ci.org/ionelmc/django-monkey-team.png
.. _status: http://travis-ci.org/ionelmc/django-monkey-team
