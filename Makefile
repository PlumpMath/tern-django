DJANGO_ADMIM = ${BINDIR}/django-admin.py
PROJECT_DIR = $(PWD)/.project
SETTINGS = $(PROJECT_DIR)/project/settings.py

project: $(SETTINGS)

$(PROJECT_DIR):
	mkdir -p $@

$(SETTINGS): $(PROJECT_DIR)
	$(DJANGO_ADMIM) startproject project $<

clean:
	rm -rf $(PROJECT_DIR)
