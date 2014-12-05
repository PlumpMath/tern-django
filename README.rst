.. |travis| image:: https://travis-ci.org/proofit404/tern-django.png
    :target: https://travis-ci.org/proofit404/tern-django
    :alt: Build Status

.. |coveralls| image:: https://coveralls.io/repos/proofit404/tern-django/badge.png
    :target: https://coveralls.io/r/proofit404/tern-django
    :alt: Coverage Status

================================
Tern Django |travis| |coveralls|
================================

Create tern projects for django applications.

Obviously all JavaScript code of application stored in application
static folder.  So we can write standard .tern-project file into
each application root.  We can add custom JavaScript from templates
script html tags.  We can extend default "libs", "loadEagerly" and
"plugins" settings.  Also if template use external library from
internet we can download it to temporary folder and make it
accessible for tern.

``tern-django`` command do following:

* Check if DJANGO_SETTINGS_MODULE was specified
* Run python script in the background
* Parse each template file in each application folder
* Find specified static files in the script html tags
* Save processed result in sqlite3 database
* Write .tern-project file for each application if necessary

Installation
------------

You can install this package from Melpa:
::

    M-x package-install RET tern-django RET

Usage
-----

Drop following line into your .emacs file:

.. code:: lisp

    (add-hook 'after-save-hook 'tern-django)

Setup your project variables:
::

    M-x setenv RET DJANGO_SETTINGS_MODULE RET project.settings
    M-x setenv RET PYTHONPATH RET /home/user/path/to/project/

When you save any file all tern projects will be updated to the
most resent changes in your project.  Only one process running at
the time.  So first run for newly specified project will take some
time.  But next run will be much faster because ``tern-django`` saves
processed result for future reuse.  You can safely ignore both tern
projects and tern ports files in you VCS.
