FROM docker.io/library/python:3.13-slim as base

ENV PATH="/venv/bin:$PATH" \
    VIRTUAL_ENV="/venv" \
    APP_HOME="/home/app"

# Stage: build
# ---------------------------------------------------------
FROM base as build

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT="/venv"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN set -eux; apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN uv venv /venv

WORKDIR $APP_HOME

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --extra test

COPY ./src ./src
COPY ./tests ./tests
COPY ./pyproject.toml ./uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv build --wheel && \
    uv pip install --no-deps dist/*.whl

ENTRYPOINT ["pytest", "-vvv"]