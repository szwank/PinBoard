.PHONY: help install run list

.DEFAULT: help
help:
	@echo "make install_dev"
	@echo "       installs all things required to run application using dev configuration"
	@echo "start_services"
	@echo "       start required services"
	@echo "run_dev"
	@echo "       start application with dev configuration"
	@echo "run_prod"
	@echo "       start application with prod configuration"

start_services:
	@echo "Starting services"
	docker-compose up -d

install_dev: start_services
	@echo "Migrating database"
	python manage.py migrate --settings PinBoard.settings.dev

run_dev: start_services
	python manage.py runserver --settings PinBoard.settings.dev

run_prod: start_services
	python manage.py runserver --settings PinBoard.settings.prod

createsuperuser:
	python manage.py createsuperuser --noinput --email admin@admin.com --username szwank
