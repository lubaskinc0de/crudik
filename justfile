up:
    docker compose -f docker/docker-compose.yml --env-file=./.config/.env up --build

up-silent:
    docker compose -f docker/docker-compose.yml --env-file=./.config/.env up --build -d

up-db:
    docker compose -f docker/docker-compose.yml --env-file=./.config/.env up db -d

test:
    docker compose -f docker/docker-compose.tests.yml --env-file=./.config/.env up --build --abort-on-container-exit tests
    just down

test-unit:
    pytest -vvv tests/unit

down:
    docker compose -f docker/docker-compose.yml --env-file=./.config/.env down
    docker compose -f docker/docker-compose.tests.yml --env-file=./.config/.env down

clear:
    docker compose -f docker/docker-compose.yml --env-file=./.config/.env down -v

lint:
    ruff format
    ruff check --fix
    mypy
    lint-imports

dev-environment:
    uv pip install -e ".[dev]"

generate-migration NAME:
    just up-db
    sleep 1s
    set -a && source ./.config/.env.migrations.local && set +a && crudik migrations autogenerate "{{NAME}}"
    just down

cookie-secret:
    echo "OAUTH2_PROXY_COOKIE_SECRET=$(openssl rand -base64 32)"