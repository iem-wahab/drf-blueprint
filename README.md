# DRF-Starter-Template

DRF-Starter-Template is a tailored Django/DRF project template built as a foundation for rapid development of scalable and maintainable RESTful APIs. The project is structured to ensure a clear separation between presentation, business logic, and data access, which simplifies development and long-term maintenance.

It uses consistent file names, clean code, clear separation for production and development, integrated code formatters and linters (with tests), and focuses on delivering consistent API responses, proper pagination, and robust error handling.

---

## Overview

The project follows a modular architecture designed to promote clarity and scalability. Its structure is organized as follows:

- **Models:**
  All models extend a central `BaseModel` that standardizes features across the project. This includes a UUID primary key, automatic timestamps, and soft-deletion, ensuring consistency and reducing boilerplate code.

- **Views:**
  Each API endpoint is implemented as its own view class (e.g., create, list, detail, update) by extending a custom `BaseAPIView`. This approach enforces a strict separation of concerns, keeping endpoint logic simple and focused.

- **Business Logic:**
  Complex operations and interactions are delegated to dedicated services (for data modifications and triggering side effects) and selectors (for optimized data retrieval). This separation aids in testability and maintainability.

- **Configuration:**
  Settings and dependency definitions are segregated into common, local, and production environments. A CI/CD pipeline provided in the **.github** folder automates testing and deployment processes.

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/SaadRafiq4/DRF-Starter-Template.git
```

### Set Up Your Environment

**Create a Virtual Environment:**

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
py -m venv venv
venv\Scripts\activate
```

**Install Dependencies:**

For local development, run:

```bash
pip install -r requirements/local.txt
```

**Configure Environment Variables:**

Copy and edit the sample environment file:

```bash
cp .env.example .env
```

---

## API Documentation

This project includes automatic API documentation using drf-spectacular. Once the server is running, you can access:

- API Schema: `/schema/`
- Swagger UI: `/schema/swagger/`
- ReDoc: `/schema/redoc/`

The root URL (`/`) redirects to the Swagger UI for convenient API exploration during development.

---

## Developer Tools & Commands

Before committing your code, ensure you run the tests, pre-commit hooks, and Ruff formatter to maintain high code quality.

**Testing:**

Run all tests with:

```bash
pytest
# For specific directories:
pytest path/to/tests_directory
```

Check coverage with:

```bash
coverage run -m pytest
coverage report
```

**Code Quality:**

Use Ruff for linting and formatting:

```bash
ruff check .
ruff check . --fix
```

Pre-commit hooks ensure quality before each commit:

```bash
pre-commit run --all-files
```

---

## Styleguide & Best Practices

**Coding Conventions:**
Use `snake_case` for functions and variables, and `CamelCase` for classes. Maintain a consistent project structure to promote readability and maintainability.

**Views & APIs:**

- Build each endpoint in its own view class to enforce a single responsibility.
- Delegate all business logic to services and selectors.
- Define dedicated serializers (for input, output, filtering, etc.) as inner classes to keep each view self-contained. Use inline serializers only for nested data structures.

**Models:**
Extend from `BaseModel` to benefit from standardized behavior (UUIDs, timestamps, soft deletion) and keep models lean by offloading logic where appropriate.

**Services & Selectors:**

- **Services:** Handle business logic and data manipulation.
- **Selectors:** Centralize and optimize data retrieval. This clear separation supports easier testing and code maintenance.

**Error Handling:**
Raise DRF exception classes (such as `ValidationError`, `NotFound`, and `PermissionDenied`) directly in your code. A centralized error handler provides uniform error responses.
