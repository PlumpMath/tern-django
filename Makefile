DJANGO_ADMIM = ${BINDIR}/django-admin.py

default: project

project: $(PWD)/.project/project/settings.py

$(PWD)/.project:
	mkdir -p $(PWD)/.project

$(PWD)/.project/project/settings.py: $(PWD)/.project
	$(DJANGO_ADMIM) startproject project $(PWD)/.project
