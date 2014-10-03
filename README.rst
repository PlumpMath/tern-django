.. |travis| image:: https://travis-ci.org/proofit404/tern-django.png
    :target: https://travis-ci.org/proofit404/tern-django
    :alt: Build Status

====================
Tern Django |travis|
====================

Create tern projects for django applications.

Obviously all JavaScript code of application stored in application
static folder.  So we can write standard .tern-project file into
each application root.  We can add custom JavaScript from templates
script tags.  So we can extend default "libs", "loadEagerly" and
"plugins" settings.  Also if template use external library from
internet we can download it to temporary folder and make it
accessible for tern.

``django-tern`` command do following:

* Check if DJANGO_SETTINGS_MODULE was specified
* Call python script
* For each application parse each file in templates directory
* Look in script tags for specified static files
* Save parse result with file modification date in sqlite3 database
* Write .tern-project file if necessary

Installation
------------

You can install this package from Melpa:
::

    M-x package-install RET relative-buffers RET

Usage
-----

Drop following line into your .emacs file:

.. code:: lisp

    (add-hook 'after-save-hook 'tern-django)

Setup your project variables:
::

    M-x setenv RET DJANGO_SETTINGS_MODULE RET project.settings
    M-x setenv RET PYTHONPATH RET /home/user/path/to/project/

When you save any file all tern-project settings will be updated to
the most resent changes.
