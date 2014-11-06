#!/usr/bin/env python

from django.apps import apps
import django

tern_file = '.tern_project'
tern_project = {"loadEagerly": ["static/**/*.js"]}


def applications():
    """Collect directories with django applications."""

    django.setup()
    return [app.path for app in apps.get_app_configs()]
