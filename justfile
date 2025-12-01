up:
    docker compose up --build

up-silent:
    docker compose up --build -d

up-db:
    docker compose up db -d

test:
    docker compose -f docker-compose.test.yml up --build --abort-on-container-exit tests

test-unit:
    pytest -vvv tests/unit

down:
    docker compose down
    docker compose -f docker-compose.test.yml down

clear:
    docker compose down -v

lint:
    ruff format
    ruff check --fix
    mypy

dev-environment:
    uv pip install -e ".[dev]"


generate-migration NAME:
    just up-db
    sleep 1s
    set -a && source ./.env.migrations.local && set +a && crudik migrations autogenerate "{{NAME}}"
    just down