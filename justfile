up:
    docker compose -f docker/docker-compose.yml up --build

up-silent:
    docker compose -f docker/docker-compose.yml up --build -d

up-db:
    docker compose -f docker/docker-compose.yml up db -d

test:
    docker compose -f docker/docker-compose.tests.yml up --build --abort-on-container-exit tests
    just down

test-unit:
    pytest -vvv tests/unit

down:
    docker compose -f docker/docker-compose.yml down
    docker compose -f docker/docker-compose.tests.yml down

clear:
    docker compose -f docker/docker-compose.yml down -v

lint:
    ruff format
    ruff check --fix
    mypy

dev-environment:
    uv pip install -e ".[dev]"


generate-migration NAME:
    just up-db
    sleep 1s
    set -a && source ./.config/.env.migrations.local && set +a && crudik migrations autogenerate "{{NAME}}"
    just down