#!/usr/bin/env python

from __future__ import print_function
from json import dumps, loads
from os.path import dirname, basename, exists, join, abspath, expanduser
from os import walk
from django.conf import settings
from django.template import Template, Context
try:
    from html.parser import HTMLParser, HTMLParseError
except ImportError:
    from HTMLParser import HTMLParser, HTMLParseError
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit
import atexit
import copy
import django
import sqlite3


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
        analyze_templates(tern_project, app)
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


def analyze_templates(project, app):
    """Add to project properties grabbed from app templates."""

    templates = join(app, 'templates')
    for root, dirs, files in walk(templates):
        htmls = [join(root, f) for f in files if f.endswith('.html')]
        for html in htmls:
            process_html_template(project, html, app)


def process_html_template(project, html, app):
    """Grab static files from html template."""

    with open(html) as template:
        source = template.read()
    if meaningful_template(source):
        rendered_source = render_if_necessary(source)
        try:
            parser = TemplateParser()
            # Don't move this to TemplateParser init.  Super will not
            # properly work with this class in python2.x
            parser.src = []
            parser.feed(rendered_source)
        except HTMLParseError:
            pass
        analyzer = TemplateAnalyzer(app, parser.src)
        analyzer.find()
        project['libs'].extend(analyzer.libs)
        project['loadEagerly'].extend(analyzer.loadEagerly)


def render_if_necessary(source):
    """Render django template if necessary."""

    if needs_to_be_rendered(source):
        source_template = Template(source)
        source_context = Context({})
        rendered_source = source_template.render(source_context)
        return rendered_source
    else:
        return source


class TemplateParser(HTMLParser):
    """Static files html grabber."""

    def handle_starttag(self, tag, attrs):
        """Process script html tags."""

        if tag == 'script':
            for attr, value in attrs:
                if attr == 'src':
                    self.src.append(value)


class TemplateAnalyzer(object):
    """Analyze static files source."""

    def __init__(self, app, sources):

        self.sources = sources
        self.app = app
        self.libs = []
        self.loadEagerly = []

    def find(self):
        """Find true definitions of each source."""

        for src in self.sources:
            self.handle(src)

    def handle(self, src):
        """Determine and save true src location."""

        if self.is_relative(src):
            self.process_relative_url(src)
        else:
            self.process_absolute_url(src)

    def is_relative(self, src):
        """Check if src specify resource from same domain."""

        return src.startswith('/')

    def process_relative_url(self, uri):
        """Find static file from its uri."""

        file_base = uri.replace(settings.STATIC_URL, '')
        for app in applications():
            path = abspath(join(app, 'static', file_base))
            if exists(path) and not path.startswith(self.app):
                self.loadEagerly.append(path)
                break

    def process_absolute_url(self, url):
        """Find external library.  Download if needed."""

        scheme, netloc, path, query, fragment = urlsplit(url)
        base = basename(path)
        for lib in ['jquery', 'underscore']:
            if base.startswith(lib):
                self.libs.append(lib)
                break


def meaningful_template(template):
    """Check if template is interesting for tern."""

    # Don't close first script tag here.
    return '<script' in template and '</script>' in template


def needs_to_be_rendered(template):
    """Check if template has necessary django tags"""

    return '{% load staticfiles %}' in template

# Sql cache.

database_file = expanduser('~/.emacs.d/tern-django.sqlite')
database_connection = None
database_cursor = None


def connect():
    """Connect to cache database."""

    global database_connection
    global database_cursor
    if database_connection is None or database_cursor is None:
        database_connection = sqlite3.connect(database_file)
        database_cursor = database_connection.cursor()


def disconnect():
    """Disconnect from cache database."""

    global database_connection
    global database_cursor
    if database_cursor is not None:
        database_cursor.close()
    if database_connection is not None:
        database_connection.close()
    database_connection = None
    database_cursor = None


atexit.register(disconnect)


def init_cache():
    """Create cache table if necessary."""

    connect()
    database_cursor.execute("""
    create table if not exists tern_django (
        "id" integer primary key,
        "file_name" text unique not null,
        "mtime" real,
        "libs" text,
        "loadEagerly" text);
    """)
    database_connection.commit()


def get_cache(file_name):
    """Get file name attributes from cache if exists."""

    database_cursor.execute("""
        select "mtime", "libs", "loadEagerly"
        from tern_django
        where file_name=?;
    """, (file_name,))
    return database_cursor.fetchone()


def set_cache(file_name, mtime, libs, loadEagerly):
    """Set file name attributes in cache."""

    if get_cache(file_name):
        query = """
        update tern_django set "mtime"=?, "libs"=?, "loadEagerly"=?
        where "file_name"=?;
        """
        params = (mtime, libs, loadEagerly, file_name)
    else:
        query = """
        insert into tern_django("file_name", "mtime", "libs", "loadEagerly")
        values (?, ?, ?, ?);
        """
        params = (file_name, mtime, libs, loadEagerly)
    database_cursor.execute(query, params)
    database_connection.commit()


if __name__ == '__main__':
    update_tern_projects()
