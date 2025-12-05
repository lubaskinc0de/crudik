# CRUDIK

A universal, production-ready application template built with Clean Architecture principles. This boilerplate provides a solid foundation for building **any type of application** - web APIs, CLI tools, Telegram bots, and so on!

## Overview

CRUDIK is a universal application template that demonstrates Clean Architecture principles. **The key advantage of this architecture is that your core business logic is completely independent of the presentation layer**.

The template includes a FastAPI web interface as an example, but you can easily add or replace it with any other presentation layer while keeping all your business logic intact.

**Use this template to:**

-   Start new projects with clean architecture best practices
-   Learn how to build framework-independent business logic
-   Create applications that can switch presentation layers without rewriting core code
-   Build maintainable, testable, and scalable applications
-   Save time on boilerplate setup

The template includes a working example with common user management functionality, but you can supplement it with your own domain logic.

## Architecture

The project follows Clean Architecture principles with clear separation of concerns:

-   **Entities**: Core domain models and business logic (framework-independent)
-   **Application**: Interactors to perform business operations in the system
-   **Adapters**: Infrastructure implementations (database, authentication, external services)
-   **Presentation**: Interface adapters (FastAPI is just one example - you can add CLI, telegram bot, etc.)

### Why This Architecture is Universal

The core principle of Clean Architecture is **dependency inversion**: your business logic (Entities and Application layers) has **zero dependencies** on external frameworks or infrastructure. This means:

-   ✅ Your use cases work the same way whether called from HTTP, CLI, gRPC, telegram bot, etc.
-   ✅ You can add multiple presentation layers (web + CLI + worker) without duplicating business logic
-   ✅ You can test business logic without any web framework, database, or external services
-   ✅ You can swap frameworks (FastAPI → Flask → Django) without touching core code
-   ✅ Your domain logic is portable and reusable across different projects

### Key Design Patterns

-   **Dependency Inversion**: Business logic depends on abstractions, not implementations
-   **Dependency Injection**: Using Dishka for IoC container
-   **Unit of Work**: Transaction management pattern
-   **Gateway**: Data access abstraction
-   **Event-Driven**: Domain events using Bazario

## Technology Stack

### Core Framework

-   **FastAPI** - Modern, fast web framework
-   **Python** 3.13+ - Programming language

### Database & ORM

-   **PostgreSQL** 17 - Primary database
-   **SQLAlchemy** - ORM with async support
-   **asyncpg** - Async PostgreSQL driver
-   **Alembic** - Database migrations

### Infrastructure

-   **Dishka** - Dependency injection container
-   **Bazario** - Event bus for domain events
-   **Adaptix** - Data serialization
-   **aiohttp**- Async HTTP client

### Development Tools

-   **pytest** - Testing framework
-   **pytest-asyncio** - Async test support
-   **ruff** - Fast Python linter and formatter
-   **mypy** - Static type checker
-   **uv** - Fast Python package manager and build backend

### DevOps

-   **Docker** & **Docker Compose** - Containerization
-   **Nginx** 1.29.3 - Reverse proxy
-   **Grafana** 12.1.4 - Monitoring and visualization

## Features

-   ✅ Clean Architecture
-   ✅ Complete example implementation (user management)
-   ✅ Multiple presentation layers support
-   ✅ Domain events with Bazario event bus
-   ✅ Comprehensive error handling
-   ✅ Database migrations with Alembic
-   ✅ Unit and integration tests with pytest
-   ✅ Type safety with mypy (strict mode)
-   ✅ Code quality with ruff
-   ✅ Code secutiry with SonarQube
-   ✅ Docker-based deployment ready
-   ✅ Dependency injection with Dishka

## Getting Started

### Using This Template

1. **Create a new repository from this template** or clone it:

```bash
git clone <repository-url>
cd crudik
```

2. **Customize the project name** (optional):

    - Update `pyproject.toml` - change `name = 'crudik'` to your project name
    - Rename the package directory: `src/crudik/` → `src/your_project/`
    - Update all imports throughout the codebase
    - Update CLI command name in `pyproject.toml` under `[project.scripts]`

### Prerequisites

-   Python 3.13+
-   Docker and Docker Compose
-   [uv](https://github.com/astral-sh/uv) package manager
-   [just](https://github.com/casey/just) command runner (optional, for convenience commands)

### Installation

1. Install development dependencies:

```bash
just dev-environment
```

Or manually:

```bash
uv pip install -e ".[dev]"
```

### Configuration

Create configuration files in `.config/` directory:

1. **`.config/.env`** - Main application environment variables

2. **`.config/.env.pg`** - PostgreSQL configuration

3. **`.config/.env.migrations`** - Migration environment variables

4. **`.config/config.toml`** - TOML configuration file

5. **`.config/nginx.conf`** - Nginx configuration

6. **`.config/init-db.sql`** - PostgreSQL initialization script

### Running the Application

#### Using Docker Compose (Recommended)

Start all services:

```bash
just up
```

Or in detached mode:

```bash
just up-silent
```

Start only the database:

```bash
just up-db
```

Stop all services:

```bash
just down
```

Clean volumes:

```bash
just clear
```

The API will be available at `http://localhost`

### Endpoints

#### Health Check

```
GET /api/ping/
```

Returns `"pong"` to verify the service is running.

#### Create User

```
POST /api/users/
```

Creates a new user. Requires X-Auth-User header for auth.

**Response:**

```json
{
    "id": "uuid"
}
```

#### Read User

```
GET /api/users/{user_id}
```

Retrieves user information by ID. Requires X-Auth-User auth header and access to the requested user.

**Response:**

```json
{
    "id": "uuid"
}
```

### Error Responses

All errors follow a consistent format:

```json
{
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "meta": {
        "additional": "context"
    }
}
```

Error codes:

-   `UNAUTHORIZED` (401) - Authentication required
-   `USER_NOT_FOUND` (404) - User does not exist
-   `ACCESS_DENIED` (403) - Insufficient permissions
-   `AUTH_USER_ALREADY_EXISTS` (409) - User already registered
-   `INTERNAL_SERVER_ERROR` (500) - Unexpected error

## Database Migrations

Generate a new migration:

```bash
just generate-migration "Migration description"
```

## Development

### Code Quality

Run linting and type checking:

```bash
just lint
```

This will:

-   Format code with `ruff format`
-   Check and fix issues with `ruff check --fix`
-   Run type checking with `mypy`

### Testing

Run tests:

```bash
just test
```

### Project Structure

```
crudik/
├── src/crudik/
│   ├── entities/          # Domain entities and business logic
│   ├── application/       # Use cases and application services
│   ├── adapters/          # Infrastructure implementations
│   │   ├── db/           # Database adapters (SQLAlchemy)
│   │   ├── auth/         # Authentication adapters
│   │   ├── config/       # Configuration loading
│   │   └── di/           # Dependency injection setup
│   ├── presentation/      # Presentation layer (FastAPI)
│   └── bootstrap/         # Application entry points
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/       # Integration tests
├── docker/                # Docker configuration
└── pyproject.toml         # Project configuration
```

### Key Components

#### Entities (Example)

-   `User` - Your business information about user
-   `AuthUser` - Link between external auth system and application user (not a business entity)

#### Interactors

-   `CreateUser` - Interactor that creates a user and publishes UserCreated domain event
-   `ReadUser` - Interactor that retrieves user data with access control

#### Presentation

-   FastAPI routers for HTTP endpoint
-   Global exception handlers for error responses

## Database Migrations

Migrations are managed with Alembic. The migration files are located in `src/crudik/adapters/db/alembic/migrations/versions/`.

To create a new migration:

1. Make changes to database models in `src/crudik/adapters/db/models/`
2. Generate migration: `just generate-migration "Description"`

## Docker Services

The Docker Compose setup includes:

-   **api** - Main FastAPI application
-   **db** - PostgreSQL database
-   **migrations** - Runs database migrations on startup
-   **nginx** - Reverse proxy and load balancer
-   **grafana** - Monitoring and visualization

## License

See [LICENSE](LICENSE) file for details.
