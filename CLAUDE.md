# CLAUDE.md - Flights Service Guidelines

## Build/Test Commands
- Run tests: `pytest`
- Run a single test: `pytest path/to/test_file.py::test_function_name`
- Start server: `uvicorn flights_service.app:app --reload`
- Run type checking: `mypy flights_service`
- Launch shell: `python -m flights_service.shell`

## Code Style Guidelines

### Structure
- Domain-driven design with models, repositories, schemas, services
- Repository pattern for data access
- Adapter pattern for external integrations

### Typing
- Use strict typing throughout with Python 3.12+ type annotations
- Return type annotations on all methods (including `-> None`)
- All parameters must have type annotations
- Use `TypedDict` for structured dictionary types
- Use domain-specific types (e.g., `Currency` from pydantic_extra_types)

### Naming/Imports
- Classes: PascalCase (e.g., `OfferSchema`, `SearchService`)
- Methods/functions/variables: snake_case
- Group imports: stdlib → third-party → local
- Explicit imports (no wildcards)

### Error Handling
- Use domain-specific exceptions
- Document expected exceptions in docstrings
- Prefer explicit error handling to implicit exception propagation