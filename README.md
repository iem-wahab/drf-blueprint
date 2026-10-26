# DRF Blueprint

A reusable Django REST Framework starter for building REST APIs with a consistent, maintainable structure.

I built this template because I kept repeating the same setup whenever I started a new Django API project. Instead of rebuilding the foundations each time, I wanted one place for the conventions and tools I regularly use: clear separation of concerns, consistent API responses, testing, and code quality checks.

## What's included

- **Service-selector architecture** — Keep API views focused on requests and responses, business logic in services, and database queries in selectors.
- **Reusable base classes** — A `BaseModel` with UUID primary keys, timestamps, and soft deletion, plus a custom `BaseAPIView` for consistent API behavior.
- **Consistent APIs** — Shared patterns for pagination, responses, and exception handling.
- **Environment-specific settings** — Separate common, local, and production configuration.
- **API documentation** — Automatically generated OpenAPI schema, Swagger UI, and ReDoc using drf-spectacular.
- **Developer tooling** — Pytest, coverage, Ruff, pre-commit hooks, and GitHub Actions configuration.

## Project structure

The template is organized so each layer has a clear responsibility:

| Layer | Responsibility |
| --- | --- |
| **Models** | Define data structures and share common fields and behavior through `BaseModel`. |
| **API views** | Handle HTTP requests and responses. Endpoints use focused view classes extending `BaseAPIView`. |
| **Serializers** | Validate input and shape API output. |
| **Services** | Handle business logic, data modifications, and side effects. |
| **Selectors** | Centralize data retrieval and reusable queries. |
| **Configuration** | Keep settings and dependencies organized by environment. |

This approach helps keep endpoints readable and makes business logic easier to test and reuse.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/iem-wahab/drf-blueprint.git
cd drf-blueprint
```

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```powershell
py -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements/local.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Update `.env` with the settings required for your local environment. Check the environment-specific configuration before running the application.

### 5. Run the project

```bash
python manage.py migrate
python manage.py runserver
```

## API documentation

Once the development server is running, the API documentation is available at:

| Documentation | Path |
| --- | --- |
| OpenAPI schema | `/schema/` |
| Swagger UI | `/schema/swagger/` |
| ReDoc | `/schema/redoc/` |

The root URL (`/`) redirects to Swagger UI.

## Tests and code quality

**Run tests**

```bash
pytest
```

**Check test coverage**

```bash
coverage run -m pytest
coverage report
```

**Lint and format with Ruff**

```bash
ruff check .
ruff format .
```

**Run pre-commit checks**

```bash
pre-commit run --all-files
```

## Conventions

- Keep views small and focused on HTTP concerns.
- Put business rules and data changes in **services**.
- Put reusable read queries in **selectors**.
- Use dedicated serializers for input, output, and filtering where appropriate.
- Extend `BaseModel` for common model behavior.
- Raise DRF exceptions such as `ValidationError`, `NotFound`, and `PermissionDenied` so errors follow the shared response format.

## Why this project exists

This isn't intended to be a framework for every possible Django application. It's a starting point based on patterns I've found useful when working on API-driven products. The goal is to spend less time setting up a new project and more time building what matters.
