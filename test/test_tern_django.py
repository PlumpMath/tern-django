from os.path import join, exists
import tern_django


def test_iter_django_applications():
    """Check we can iterate through django applications."""

    assert all([exists(join(app, '__init__.py'))
                for app in tern_django.applications()])


def test_write_tern_project():
    """Check we write tern project in django applications."""

    tern_django.update_tern_projects()
    for app in tern_django.applications():
        has_static = exists(join(app, 'static'))
        has_tern = exists(join(app, tern_django.tern_file))
        assert has_static == has_tern


def test_print_processed_projects(capsys):
    """Check we print names of written tern projects."""

    tern_django.update_tern_projects()
    out, err = capsys.readouterr()
    assert 'Write tern project' in out
