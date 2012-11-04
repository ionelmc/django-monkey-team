# -*- encoding: utf8 -*-
from setuptools import setup, find_packages

import os

setup(
    name = "django-monkey-team",
    version = "0.2",
    url = 'https://github.com/ionelmc/django-prefetch',
    download_url = '',
    license = 'BSD',
    description = "Django middleware that displays debug tracebacks on production sites (where you would have `DEBUG = False`) only to developers.",
    long_description = file(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author = 'Ionel Cristian Mărieș',
    author_email = 'contact@ionelmc.ro',
    packages = find_packages('src'),
    package_dir = {'':'src'},
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'PyCrypto',
        'Django>=1.3',
    ]
)
