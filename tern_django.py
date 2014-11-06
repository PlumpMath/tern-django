#!/usr/bin/env python

import django
import os

django_version = django.get_version()

tern_file = '.tern_project'
tern_project = {"loadEagerly": ["static/**/*.js"]}


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
            mod_path = os.path.dirname(upath(mod.__file__))
            directories.append(mod_path)
        return directories
