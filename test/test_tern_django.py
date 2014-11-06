from os.path import join, exists
import tern_django


def test_iter_django_applications():
    """Check we can iterate through django applications."""

    assert all([exists(join(app, '__init__.py'))
                for app in tern_django.applications()])
