DJANGO_ADMIM = ${BINDIR}/django-admin.py
PROJECT_DIR = $(PWD)/.project
SETTINGS = $(PROJECT_DIR)/project/settings.py
APP1 = $(PROJECT_DIR)/project/app1/models.py

project: $(SETTINGS) $(APP1)

$(PROJECT_DIR):
	mkdir -p $@

$(SETTINGS): DJANGO_SETTINGS_MODULE=
$(SETTINGS): $(PROJECT_DIR)
	$(DJANGO_ADMIM) startproject project $<

$(APP1): $(PROJECT_DIR)
	$(DJANGO_ADMIM) startapp app1 $<

clean:
	rm -rf $(PROJECT_DIR)
