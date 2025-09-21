# Python Development Stack Trait

## Description
Comprehensive Python development toolchain configuration including testing, formatting, type checking, and dependency management. This trait standardizes Python development environments across agents.

## Content

### Python Development Tools

**Development Tools:**
- Poetry ^1.7.0 - Dependency management and packaging with pyproject.toml configuration
- Black ^23.11.0 - Code formatting with 88-character line length and Python 3.11 target
- MyPy ^1.7.0 - Static type checking with strict mode and comprehensive error detection
- Pre-commit ^3.6.0 - Git hooks for automated code quality enforcement
- Ruff ^0.1.0 - Fast Python linter and formatter, replacing flake8 and isort

**Testing Tools:**
- Pytest ^7.4.0 - Testing framework with fixtures, parametrization, and coverage integration
- Factory Boy ^3.3.0 - Test data generation with realistic fake data using Faker
- pytest-asyncio ^0.21.0 - Async testing support for FastAPI and async Python code
- pytest-mock ^3.12.0 - Simplified mocking and patching for unit tests
- Hypothesis ^6.88.0 - Property-based testing for edge case discovery

**Deployment Tools:**
- Uvicorn ^0.24.0 - ASGI server for FastAPI with hot reloading and production settings
- Gunicorn ^21.2.0 - WSGI server for Django/Flask with worker process management
- Docker - Containerization with multi-stage builds and Alpine Linux base images
- docker-compose - Local development environment orchestration

**Monitoring Tools:**
- Sentry ^1.38.0 - Error tracking, performance monitoring, and release tracking
- Prometheus + Grafana - Metrics collection and visualization for production systems
- Structlog ^23.2.0 - Structured logging with JSON output for better observability

### Tool Configurations

**Pytest Configuration (pyproject.toml):**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--disable-warnings",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov",
    "--cov-fail-under=90"
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests"
]
```

**Black Configuration (pyproject.toml):**
```toml
[tool.black]
line-length = 88
target-version = ["py311"]
include = "\\.pyi?$"
extend-exclude = "/(migrations|venv|build)/"
```

**MyPy Configuration (pyproject.toml):**
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
```

**Pre-commit Configuration (.pre-commit-config.yaml):**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
```

### Testing Execution Strategy

**Pytest Projects:**
- Detection: Look for pytest.ini, pyproject.toml with pytest config, or pytest in requirements
- Primary command: `pytest --cov=src --cov-report=term-missing`
- XML output: `pytest --junit-xml=test-results.xml`
- Verbose mode: `python -m pytest -v --tb=short`
- Coverage HTML: `pytest --cov=src --cov-report=html:htmlcov`

**Unittest Fallback:**
- Command: `python -m unittest discover`
- Verbose: `python -m unittest discover -v`

**Quality Gates:**
- Unit test coverage: > 90% for critical business logic
- Integration coverage: All API endpoints and database operations
- Mutation testing: > 75% for core functionality
- Type checking: mypy --strict passing
- Code quality: flake8, black, isort, bandit passing
- Security scans: No high/critical vulnerabilities in dependencies

### Development Workflow

**Setup Commands:**
```bash
# Install pre-commit hooks
pre-commit install

# Run all pre-commit hooks on all files
pre-commit run --all-files

# Install dependencies with Poetry
poetry install --with dev,test

# Activate virtual environment
poetry shell
```

**Development Commands:**
```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Lint code
ruff check src/ tests/
```

## Usage Notes

- **Which agents should use this trait**: python-engineer, ai-engineer, data-engineer, any agent working with Python code
- **Customization guidance**: Framework-specific tools can be added (e.g., Django-specific testing tools for Django projects)
- **Compatibility requirements**: Python 3.9+ with modern dependency management practices

## Implementation Priority
**MEDIUM-HIGH** - This trait affects 8+ Python-focused agents and provides comprehensive development environment standardization