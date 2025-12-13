# Crudik (stands for "cute CRUD" in Russian)

A universal application **template** that follows the principles of a clean architecture and contains everything you need to get started quickly.

## Motivation

We're all familiar with the problem of the "Blank Slate" where we have an idea but don't even know where to start, a typical application includes a lot of fundamental things that are implemented in almost every project and you still have to write them over and over again every time, from project to project. **In order for you to focus only on business logic and not think about secondary things, this template was created.** Template implements a simple backend application, but you can actually use it for a CLI, telegram bot, or GUI, thanks to the extensible architecture of the project and the focus on fundamental concepts.

## Features

-   **Clean Architecture**. The template follows the principles of Clean Architecture, that is designed to simplify the process of developing, refactoring, and testing your application.
-   **Testing.** The template provides a ready-made framework for integration testing of your application, including things like cleaning up the database to isolate tests, as well as an example of writing tests for a backend application.
-   **Working with the database.** The template uses SQLAlchemy in an imperative style to work with the database, and there is also a database migration system using alembic.
-   **User management and authentication.** The template provides two useful endpoints for creating a user of your application and reading it, as well as authenticating users.
-   **Authentication.** The template shows an example of using [OAuth2-Proxy](https://oauth2-proxy.github.io/oauth2-proxy/) along with a self-hosted [Keycloak](https://www.keycloak.org/) for user authentication, as well as an example of integrating this into your application, and shows the nginx configuration so that each outgoing request is authenticated first.
-   **Logging.** The template uses structlog for logs in JSON format, showing how to configure the [Vector](https://vector.dev), [Loki](https://grafana.com/docs/loki/latest/) and [Grafana](https://grafana.com/docs/loki/latest/) stack to process, store and visualize your application's logs.
-   **Infrastructure.** The template shows how to write a [Docker](https://docker.com) image for your application, how to configure [Docker-Compose](https://docs.docker.com/compose/) to run the service in development mode or in test mode with all the necessary infrastructure including [Redis](https://redis.io), [PostgreSQL](https://www.postgresql.org/), [OAuth2-Proxy](https://oauth2-proxy.github.io/oauth2-proxy/), [Keycloak](https://www.keycloak.org/), and [Nginx](https://nginx.org/).
-   **Code quality.** The quality of the code in your project will be ensured by the tools built into this template, such as [mypy](https://www.mypy-lang.org/) (with **strict** mode, of course) for static type analysis and [ruff](https://astral.sh/ruff) as a linter with many rules and [import-linter](https://import-linter.readthedocs.io/en/stable/) that enforces dependency-rule.
-   **CI/CD.** The template will provide you with [Github-Actions](https://docs.github.com/en/actions) already configured for linting the code, testing it, and deploying it. Docker image building inside the pipeline, their semantic versioning, and sending to [Github Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) have been implemented.
-   **Backend.** The backend part is implemented using [FastAPI](https://fastapi.tiangolo.com/), showing application error handling, loading a TOML config, and using [Dishka](https://dishka.readthedocs.io/) for dependency injection.

## Quickstart

### Prerequisites

-   [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed
-   [Just](https://github.com/casey/just) command runner

### Running the Application

1. **Start all services**:

    ```bash
    just up
    ```

    To run in detached mode:

    ```bash
    just up-silent
    ```

2. **Access the application**:

    - **API**: `http://localhost/`
    - **API Documentation**: `http://localhost/docs`
    - **Grafana** (logs visualization): `http://localhost:3000`

3. **Stop all services**:

    ```bash
    just down
    ```

### Available Commands

The project uses [Just](https://github.com/casey/just) for command management. Here are the most useful commands:

-   `just up` - Start all services in development mode
-   `just up-silent` - Start all services in detached mode
-   `just up-db` - Start only the database
-   `just down` - Stop all services
-   `just clear` - Stop all services and remove volumes (cleans database)
-   `just test` - Run integration tests
-   `just lint` - Run code linters (ruff, mypy, import-linter)
-   `just dev-environment` - Install development dependencies locally
-   `just generate-migration <name>` - Generate a new database migration
-   `just cookie-secret` - Generate OAuth2-Proxy cookie secret

### API Endpoints

Once the application is running, you can access:

-   `GET /internal/alive` - Liveness probe
-   `GET /internal/ready` - Readiness probe
-   `POST /users/` - Create a new user (requires authentication)
-   `GET /users/{user_id}` - Get user by ID (requires authentication)
-   `GET /docs` - Interactive API documentation (Swagger UI)

### Running Tests

Run integration tests:

```bash
just test
```

This will:

-   Start test environment (API, database)
-   Run all integration tests
-   Clean up and stop services

### Database Migrations

Generate a new migration:

```bash
just generate-migration "Add new table"
```

Migrations are applied automatically in docker-compose on startup.

## Project Structure

<p align="center">
  <img width="300" height="200" alt="Clean Architecture scheme" src="https://github.com/user-attachments/assets/5fb796c5-467d-41b3-9cbd-181e0cef5f15" />
</p>

```
crudik/
├── src/crudik/                    # Main package (following src-layout)
│   ├── entities/                  # Domain entities
│   │   ├── base.py               # Base entity class
│   │   ├── user.py               # User entity
│   │   └── common/               # Common domain utilities
│   │       ├── identifiers.py    # Type-aliases to identifiers (UserId, etc.)
│   │       └── config.py         # Common configuration class decorator
│   │
│   ├── application/               # Application layer (use cases)
│   │   ├── common/               # Common application interfaces (ports)
│   │   │   ├── interactor.py    # Base interactor decorator
│   │   │   ├── uow.py           # Unit of Work pattern interface
│   │   │   ├── auth_provider.py # Authentication provider interface
│   │   │   └── gateway/         # Database gateway interfaces
│   │   ├── user/                 # User-related interactors
│   │   │   ├── create.py        # Create user interactor
│   │   │   └── read.py          # Read user interactor
│   │   └── errors/              # Application-specific errors
│   │
│   ├── adapters/                 # Adapters (infrastructure) layer
│   │   ├── db/                   # Database adapters
│   │   │   ├── config.py        # Database configuration
│   │   │   ├── models/          # SQLAlchemy models
│   │   │   ├── gateway/         # Database gateway implementations
│   │   │   └── alembic/         # Database migrations
│   │   ├── auth/                 # Authentication adapters
│   │   │   ├── auth_provider.py # Auth provider implementation
│   │   │   ├── idp/             # Identity provider implementations
│   │   │   └── common/          # Common auth interfaces (ports)
│   │   ├── api_client.py        # API client for project (used in tests)
│   │   └── errors/              # Adapter-specific errors
│   │
│   ├── presentation/             # Presentation sub-layer
│   │   └── fast_api/            # FastAPI-specific
│   │       ├── routers/         # API route handlers
│   │       │   ├── user.py      # User endpoints
│   │       │   └── root.py      # Root endpoints
│   │       └── error_handlers.py # Global error handlers
│   │
│   └── bootstrap/                # Application initialization
│       ├── fast_api.py          # FastAPI app factory
│       ├── cli.py               # CLI entry point
│       ├── config/              # Configuration loading
│       ├── di/                  # Dependency injection setup
│       └── logs.py              # Logging configuration
│
├── tests/                        # Test suite
│   └── integration/             # Integration tests
│       ├── conftest.py          # Pytest fixtures
│       └── user/                # User-related tests
│
├── .config/                      # Configuration files
│   ├── config.toml              # Main application configuration
│   ├── .env                     # Application environment variables
│   ├── .env.kc                  # Keycloak environment variables
│   ├── .env.migrations          # Database migrations environment variables
│   ├── .env.oauthproxy          # OAuth2-Proxy environment variables
│   ├── .env.pg                  # PostgreSQL environment variables
│   ├── .env.tests               # Tests environment variables
│   ├── nginx.conf               # Nginx reverse proxy configuration
│   ├── loki.yaml                # Loki log aggregation configuration
│   ├── vector.yaml              # Vector log processing configuration
│   ├── init-db.sql              # PostgreSQL initialization script
│   └── grafana/                  # Grafana provisioning
│       └── provisioning/
│           ├── dashboards/      # Dashboard definitions
│           └── datasources/     # Data source configurations
│
├── docker/                       # Docker configuration
│   ├── Dockerfile               # Main application image
│   ├── tests.Dockerfile         # Tests image
│   ├── grafana.Dockerfile       # Grafana image
│   ├── loki.Dockerfile          # Loki image
│   ├── vector.Dockerfile        # Vector image
│   ├── docker-compose.yml       # Development environment
│   ├── docker-compose.tests.yml # Tests environment
│   └── docker-compose.base.yml  # Base docker-compose template
│
├── keycloak/                     # Keycloak configuration
│   └── clients/                 # Client configs
```

### Layer Responsibilities

-   **entities** - Contains domain entities representing core business objects.

-   **application** - Implements interactors that orchestrate business logic. This layer defines interfaces (ports) that adapters must implement, following the Dependency Inversion Principle.

-   **adapters** - Provides concrete implementations mostly of interfaces defined in the application layer. Includes database access (SQLAlchemy) and authentication logic.

-   **presentation** - Sub-layer of **adapters** layer. Handles HTTP requests and responses using FastAPI.

-   **bootstrap** - Responsible for application initialization, dependency injection container setup, configuration loading, logging setup and CLI interface.

## Authentication

The application uses a multi-layer authentication architecture with **Keycloak** as the identity provider, **OAuth2-Proxy** as the authentication proxy, and **Nginx** as the reverse proxy that enforces authentication on all requests.

### Architecture Overview

```
Client → Nginx → OAuth2-Proxy → Keycloak (OIDC)
                ↓
            (if authenticated)
                ↓
            Application API
```

### Authentication Flow

1. **Request Interception**: When a client makes a request to the application, Nginx intercepts it using the `auth_request` directive.

2. **OAuth2-Proxy Validation**: Nginx forwards the authentication check to OAuth2-Proxy at `/oauth2/auth`. OAuth2-Proxy validates the session cookie:

    - If valid session exists → returns 200 with user information headers
    - If no valid session → returns 401, triggering redirect to Keycloak

3. **Keycloak Authentication**: If unauthenticated, OAuth2-Proxy redirects the user to Keycloak's OIDC login page. After successful login, Keycloak redirects back to OAuth2-Proxy with an authorization code.

4. **Session Creation**: OAuth2-Proxy exchanges the code for tokens, creates a session, stores it in Redis, and sets a secure HTTP-only cookie.

5. **Header Propagation**: Once authenticated, OAuth2-Proxy sets response header containing keycloak user id.

6. **Nginx Header Forwarding**: Nginx extracts these header and forwards them to the application

7. **Application User Resolution**: The application extracts the auth user ID from the configured header. The header name is configurable to match what Nginx forwards. It then looks up the corresponding `AuthUser` record in the database and retrieves the associated application `User` entity.

### Components

#### Keycloak

-   **Role**: Identity Provider (IdP) using OpenID Connect (OIDC)
-   **Configuration**: Client configuration stored in `keycloak/clients/`
-   **Environment**: Configured via `.config/.env.kc`

#### OAuth2-Proxy

-   **Role**: Authentication proxy that handles OAuth2/OIDC flow
-   **Session Storage**: Redis
-   **Configuration**: `.config/.env.oauthproxy`

#### Nginx

-   **Role**: Reverse proxy that enforces authentication
-   **Configuration**: `.config/nginx.conf`
-   **Key Features**:
    -   `auth_request /oauth2/auth`: Validates every request through OAuth2-Proxy
    -   `error_page 401 =403 /oauth2/sign_in`: Redirects unauthenticated users to login
    -   Header forwarding: Passes user information to the backend application

### User Creation and Linking

When a new user is created via the application API:

1. **User Entity Creation**: A new `User` entity is created with a generated UUID.

2. **Auth User Linking**: The `AuthProvider.setup_auth()` method:

    - Extracts the current auth user ID from the request header
    - Creates an `AuthUser` record linking the Keycloak user ID to the application user ID
    - Stores this mapping in the database

3. **Database Schema**: The `AuthUser` table maintains the relationship:
    - `auth_user_id`: Keycloak user identifier (string)
    - `user_id`: Application user identifier (UUID)
    - Foreign key relationship to `User` entity

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. The workflow is defined in `.github/workflows/lint_test_deploy.yml` and runs on every push and pull request.

### Workflow Overview

The pipeline consists of four main jobs that run in sequence:

1. **lint** - Code quality checks
2. **test** - Tests running in docker-compose.
3. **bump_version** - Semantic versioning (only on `master` branch)
4. **build_and_push** - Docker image building and publishing (only on `master` and `dev` branches)

### Jobs Details

#### Lint Job

-   **Triggers**: Runs on every push and pull request
-   **Purpose**: Ensures code quality and consistency
-   **Steps**:
    -   Runs **Ruff** for code linting
    -   Runs **Mypy** for static type checking
    -   Runs **Import-linter** for dependency rule validation

#### Test Job

-   **Triggers**: Runs on every push and pull request
-   **Purpose**: Validates application functionality
-   **Steps**:
    -   Sets up Docker Compose
    -   Runs integration tests using `docker-compose.tests.yml`
    -   Tests execute in isolated containers with database

#### Bump Version Job

-   **Triggers**: Only runs on `master` branch after successful lint and test
-   **Purpose**: Automatically increments version and creates Git tag
-   **Steps**:
    -   Uses `anothrNick/github-tag-action` for semantic versioning
    -   Default bump: `patch`
    -   Creates version tag with `v` prefix (e.g., `v0.0.1`)
    -   Saves version to artifact for use in build job

#### Build and Push Job

-   **Triggers**: Runs on `master` and `dev` branches after successful lint and test
-   **Purpose**: Builds and publishes Docker images to GitHub Container Registry
-   **Versioning Strategy**:
    -   **master branch**: Uses bumped version from previous job (e.g., `v0.0.1`)
    -   **dev branch**: Uses bumped version with `-dev` suffix (e.g., `v0.0.1-dev`)
    -   Each image is tagged with both version tag and `latest` (or `latest-dev` for dev branch)
-   **Images Built**:
    -   Main application image (`ghcr.io/<repo>/<version>`)
    -   Grafana image (`ghcr.io/<repo>-grafana/<version>`)
    -   Vector image (`ghcr.io/<repo>-vector/<version>`)
    -   Loki image (`ghcr.io/<repo>-loki/<version>`)

### Workflow Conditions

-   **Lint and Test**: Always run on push and pull requests
-   **Version Bump**: Only on `master` branch merges
-   **Build and Push**: Only on `master` and `dev` branches when lint and test succeed

### Docker Registry

All images are published to [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) (ghcr.io)

## AI Usage

The AI in this project was only used to cover the code with docstrings, as well as to write some parts of README (under my strict control)

## Author
**lubaskinc0de**

## License
**MIT**

## Contributions
Contributions are welcome