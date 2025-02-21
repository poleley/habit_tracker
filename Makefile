run:
	uvicorn app.main:app --reload --port 8000

install:
	pip install poetry
	poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

linter:
	pylint app/

black:
	python -m black .

cleanimports:
	isort .
	autoflake -r -i --remove-all-unused-imports --ignore-init-module-imports --exclude "db" .

al:
	alembic -c db/migrations/alembic.ini revision --autogenerate -m"$(comment)"

upgrade:
	alembic -c db/migrations/alembic.ini upgrade head

rundocker_b:
	docker compose up --build

rundocker:
	docker compose up

db:
	docker run --env-file .env_postgres -p 5400:5432 postgres:16
