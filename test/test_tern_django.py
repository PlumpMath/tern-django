from __future__ import absolute_import
from datetime import timedelta
from json import dumps
from os import getcwd, unlink
from os.path import join, exists
from time import time

import pytest

import tern_django


project_dir = join(getcwd(), '.project')
tern_django.database_file = join(getcwd(), 'tern-django.sqlite')


@pytest.fixture
def no_tern_projects():
    """Remove all created tern projects before test run."""

    for app in tern_django.applications():
        project = join(app, tern_django.tern_file)
        if exists(project):
            unlink(project)


def test_iter_django_applications():
    """Check we can iterate through django applications."""

    assert all([exists(join(app, '__init__.py'))
                for app in tern_django.applications()])


# Tern project creation.


def test_write_tern_project(no_tern_projects):
    """Check we write tern project in django applications."""

    tern_django.init_cache()
    tern_django.update_tern_projects()
    for app in tern_django.applications():
        has_static = exists(join(app, 'static'))
        has_tern = exists(join(app, tern_django.tern_file))
        assert has_static == has_tern


def test_print_processed_projects(capsys, no_tern_projects):
    """Check we print names of written tern projects."""

    app2_project = join(project_dir, 'app2', tern_django.tern_file)
    message = 'Write tern project to {0}'.format(app2_project)
    tern_django.init_cache()
    tern_django.update_tern_projects()
    out, err = capsys.readouterr()
    assert message in out


def test_does_not_modify_existed_files(capsys, no_tern_projects):
    """Check we doesn't overwrite up to date tern projects."""

    app1_project = join(project_dir, 'app1', tern_django.tern_file)
    with open(app1_project, 'w') as project:
        project.write(dumps(tern_django.default_tern_project))
    tern_django.init_cache()
    tern_django.update_tern_projects()
    out, err = capsys.readouterr()
    assert app1_project not in out


# Templates analyze.


def test_find_static_files_from_other_application():
    """Check we can search in templates static files include."""

    project = {'libs': [], 'loadEagerly': []}
    app1_static_file = join(project_dir, 'app1', 'static', 'app1', 'app1.js')
    app2 = join(project_dir, 'app2')
    tern_django.analyze_templates(project, app2)
    assert project == {'libs': [], 'loadEagerly': [app1_static_file]}


def test_find_static_predefined_libraries():
    """Check we can detect predefined libraries in templates files."""

    project = {'libs': [], 'loadEagerly': []}
    jquery_app = join(project_dir, 'jquery_app')
    tern_django.analyze_templates(project, jquery_app)
    assert project == {'libs': ['jquery'], 'loadEagerly': []}


def test_meaningful_template():
    """Test if we need process specified template."""

    assert tern_django.meaningful_template('<script>function () {};</script>')
    assert not tern_django.meaningful_template('<body></body>')


def test_needs_to_be_rendered():
    """Test if we need render specified template."""

    assert tern_django.needs_to_be_rendered('<h1>{% load staticfiles %}</h1>')
    assert not tern_django.needs_to_be_rendered('<body></body>')


# Sql cache.


def test_create_cache_file():
    """Check we create database file."""

    tern_django.connect()
    assert exists(tern_django.database_file)


def test_connect_multiple_times():
    """Check that we can safely connect and disconnect to the cache."""

    tern_django.connect()
    one = tern_django.database_cursor
    tern_django.connect()
    two = tern_django.database_cursor
    assert one is two


def test_disconnect_multiple_times():
    """Check we can safely disconnect from cache many times."""

    tern_django.disconnect()
    tern_django.disconnect()
    assert not tern_django.database_connection
    assert not tern_django.database_cursor


def test_database_table_operations():
    """Check we can create, read and write to cache table."""

    tern_django.init_cache()
    html_file = '/test/file.html'
    html_args = (1415483694.061135, '["jquery"]', '')
    tern_django.set_cache(html_file, *html_args)
    obtained = tern_django.get_cache(html_file)
    assert obtained == html_args


def test_database_insert_or_update():
    """Check that set_cache will insert record if missed and update record
    if it already present.
    """

    tern_django.init_cache()
    file_name = '/test/me/twice.html'
    params = (1415483694.061135, '["underscore"]', '')
    tern_django.set_cache(file_name, *params)
    tern_django.set_cache(file_name, *params)
    assert params == tern_django.get_cache(file_name)


# Cache integration with templates analyze.


def test_skip_already_analyzed_template():
    """Check we will ignore templates analyzed earlier."""

    project = {'libs': [], 'loadEagerly': []}
    app = join(project_dir, 'app_for_cache')
    template = join(app, 'templates', 'app_for_cache', 'underscore_app.html')
    tern_django.init_cache()
    tern_django.set_cache(template, time(), '["jquery"]', '')
    tern_django.analyze_templates(project, app)
    assert project == {'libs': ['jquery'], 'loadEagerly': []}


def test_save_analyzed_template_data():

    project = {'libs': [], 'loadEagerly': []}
    app = join(project_dir, 'app_for_cache')
    template = join(app, 'templates', 'app_for_cache', 'underscore_app.html')
    timestamp = time() - timedelta(hours=1).total_seconds()
    tern_django.init_cache()
    tern_django.set_cache(template, timestamp, '["jquery"]', '')
    tern_django.analyze_templates(project, app)
    _, libs, _ = tern_django.get_cache(template)
    assert '["underscore"]' == libs
