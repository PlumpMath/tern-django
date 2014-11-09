#!/usr/bin/env python

from __future__ import print_function
from json import dumps, loads
from os.path import dirname, exists, join, abspath
from os import walk
from django.conf import settings
from django.template import Template, Context
try:
    from html.parser import HTMLParser, HTMLParseError
except ImportError:
    from HTMLParser import HTMLParser, HTMLParseError
import copy
import django


django_version = django.get_version()
tern_file = '.tern-project'

default_tern_project = {
    'loadEagerly': ['static/**/*.js'],
    'libs': ['browser', 'ecma5']
}


def applications():
    """Collect directories with django applications."""

    if django_version >= '1.7':
        from django.apps import apps
        django.setup()
        return [app.path for app in apps.get_app_configs()]
    else:
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
        update_application(app)


def update_application(app):
    """Update tern project in specified django application."""

    static = join(app, 'static')
    if exists(static):
        project_file = join(app, tern_file)
        tern_project = copy.deepcopy(default_tern_project)
        # analyze_templates(tern_project, app)
        save_tern_project(tern_project, project_file)


def save_tern_project(tern_project, project_file):
    """Save tern project to specified file if necessary."""

    if not exists(project_file):
        write_tern_project(tern_project, project_file)
        return
    with open(project_file) as project:
        written_project = loads(project.read())
    if written_project != tern_project:
        write_tern_project(tern_project, project_file)


def write_tern_project(tern_project, project_file):
    """Save tern project."""

    print('Write tern project to', project_file)
    with open(project_file, 'w') as project:
        project.write(dumps(tern_project))


def analyze_templates(project, app_directory):
    """Add to project properties grabbed from app templates."""

    templates = join(app_directory, 'templates')
    for root, dirs, files in walk(templates):
        htmls = [join(root, f) for f in files if f.endswith('.html')]
        for html in htmls:
            process_html_template(project, html, app_directory)


def process_html_template(project, html, app_directory):
    """Grab static files from html template."""

    with open(html) as template:
        source = template.read()
    source_template = Template(source)
    source_context = Context({})
    rendered_source = source_template.render(source_context)
    try:
        parser = StaticFilesParser(app_directory)
        parser.feed(rendered_source)
    except HTMLParseError:
        pass
    project['libs'].extend(parser.libs)
    project['loadEagerly'].extend(parser.loadEagerly)


class StaticFilesParser(HTMLParser):
    """Static files html grabber."""

    def __init__(self, app_directory):

        super(StaticFilesParser, self).__init__()
        self.app_directory = app_directory
        self.libs = []
        self.loadEagerly = []

    def handle_starttag(self, tag, attrs):
        """Process script html tags."""

        if tag == 'script':
            for attr, value in attrs:
                if attr == 'src':
                    self.handle_src_value(value)

    def handle_src_value(self, value):
        """Save src attribute value in parser properties."""

        location = self.locate_static(value)
        if location and not location.startswith(self.app_directory):
            self.loadEagerly.append(location)

    def locate_static(self, uri):
        """Find static file from its uri."""

        file_base = uri.replace(settings.STATIC_URL, '')
        for app in applications():
            path = abspath(join(app, 'static', file_base))
            if exists(path):
                return path


if __name__ == '__main__':
    update_tern_projects()
