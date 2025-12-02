FROM python:3.13.9-slim

# installing curl for heatlh-checks
RUN apt-get -qq update && \
    apt-get -qq install -y --no-install-recommends \
    wget && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    apt install -y git curl && \
    rm -rf /var/lib/apt/lists/

# setting working directory
ENV APP_HOME=/home/app
WORKDIR $APP_HOME

# setting required environment variables
ENV VIRTUAL_ENV="$APP_HOME/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV UV_PROJECT_ENVIRONMENT="$VIRTUAL_ENV"

# installing uv and creating virtual environment
RUN pip install uv
RUN uv venv -p 3.13

# copying pyproject.toml and lock file, installing only dependencies and setting up cache
COPY ./pyproject.toml ./uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# copying application source code
COPY ./src $APP_HOME/src

# installing application itself without dependencies
RUN uv pip install --no-deps .