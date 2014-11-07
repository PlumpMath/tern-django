#!/usr/bin/env python

from json import dumps
from os.path import dirname, exists, join
import django


django_version = django.get_version()
tern_file = '.tern-project'


def applications():
    """Collect directories with django applications."""

    if django_version >= '1.7':
        from django.apps import apps
        django.setup()
        return [app.path for app in apps.get_app_configs()]
    else:
        from django.conf import settings
        from django.utils.importlib import import_module
        from django.utils._os import upath
        directories = []
        apps = settings.INSTALLED_APPS
        for app in apps:
            mod = import_module(app)
            mod_path = dirname(upath(mod.__file__))
            directories.append(mod_path)
        return directories


def update_tern_projects():
    """Update tern projects in each django application."""

    for app in applications():
        if exists(join(app, 'static')):
            tern_project = {'loadEagerly': ['static/**/*.js']}
            with open(join(app, tern_file), 'w') as project:
                project.write(dumps(tern_project))
