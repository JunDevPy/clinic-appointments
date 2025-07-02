.PHONY: lint test up down logs clean migrate

lint:
	black .
	isort .
	flake8 .

test:
	pytest -v

up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

migrate:
	docker-compose exec api python -c "from api.database import engine; from api.models import Base; Base.metadata.create_all(bind=engine)"