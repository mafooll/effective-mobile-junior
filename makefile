.PHONY: run migrate makemigrations shell cleanup tests createsuperuser

run:
	docker-compose up --build web

migrate:
	docker-compose run --rm web uv run python manage.py migrate

makemigrations:
	docker-compose run --rm web uv run python manage.py makemigrations

shell:
	docker-compose run --rm web uv run python manage.py shell

cleanup:
	docker-compose down --volumes --remove-orphans

tests:
	docker-compose exec web uv run pytest

createsuperuser:
	docker-compose run --rm web uv run python manage.py createsuperuser
