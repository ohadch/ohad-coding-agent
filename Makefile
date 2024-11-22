makemigrations:
	alembic revision --autogenerate -m "$(name)"

migrate:
	alembic upgrade head

rollback:
	alembic downgrade -1

db-up:
	cd .. && docker-compose up -d db
