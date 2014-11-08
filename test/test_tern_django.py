from json import dumps
from os.path import join, exists
from os import getcwd, unlink
import tern_django
import pytest


project_dir = join(getcwd(), '.project')


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


def test_write_tern_project(no_tern_projects):
    """Check we write tern project in django applications."""

    tern_django.update_tern_projects()
    for app in tern_django.applications():
        has_static = exists(join(app, 'static'))
        has_tern = exists(join(app, tern_django.tern_file))
        assert has_static == has_tern


def test_print_processed_projects(capsys, no_tern_projects):
    """Check we print names of written tern projects."""

    app2_project = join(project_dir, 'app2', tern_django.tern_file)
    message = 'Write tern project to {0}'.format(app2_project)
    tern_django.update_tern_projects()
    out, err = capsys.readouterr()
    assert message in out


def test_does_not_modify_existed_files(capsys, no_tern_projects):
    """Check we doesn't overwrite up to date tern projects."""

    app1_project = join(project_dir, 'app1', tern_django.tern_file)
    with open(app1_project, 'w') as project:
        project.write(dumps(tern_django.default_tern_project))
    tern_django.update_tern_projects()
    out, err = capsys.readouterr()
    assert app1_project not in out
