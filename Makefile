build: stop
	pip freeze > requirements.txt
	docker-compose build --progress=tty
	docker image prune --force

stop:
	docker-compose down

start:
	docker-compose up -d

run: start
	docker exec baseproject alembic -c app/alembic.ini upgrade head

migrate-test: start
	docker exec -e ENVIRONMENT=test -e DATABASE_URL="sqlite+aiosqlite:///test_db.sqlite3" baseproject alembic -c app/alembic.ini upgrade head

test: migrate-test
	docker exec -e ENVIRONMENT=test -e DATABASE_URL="sqlite+aiosqlite:///test_db.sqlite3" baseproject pytest tests --asyncio-mode=strict

coverage: migrate-test
	docker exec -e ENVIRONMENT=test -e DATABASE_URL="sqlite+aiosqlite:///test_db.sqlite3" baseproject coverage run --branch --concurrency=thread,greenlet --source=app -m pytest --asyncio-mode=strict
	docker exec -e ENVIRONMENT=test -e DATABASE_URL="sqlite+aiosqlite:///test_db.sqlite3" baseproject coverage report -m

report: coverage
	docker exec -e ENVIRONMENT=test -e DATABASE_URL="sqlite+aiosqlite:///test_db.sqlite3" baseproject coverage html
	open htmlcov/index.html

lint: start
	docker exec -e ENVIRONMENT=test -e DATABASE_URL="sqlite+aiosqlite:///test_db.sqlite3" baseproject pylint app
	