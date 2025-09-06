## Python Development Best Practices

### Code Organization
- **Package Structure**: Use proper `__init__.py` files and package organization
- **Import Management**: Follow PEP 8 import ordering (standard library, third-party, local)
- **Configuration**: Use environment variables and configuration files (YAML, TOML)
- **Secrets Management**: Never commit secrets; use environment variables or secret management tools

### Error Handling & Logging
```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class CustomAPIError(Exception):
    """Custom exception for API-related errors."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def safe_api_call(url: str) -> Optional[dict]:
    try:
        # API call logic
        logger.info(f"Making API call to {url}")
        return response_data
    except RequestException as e:
        logger.error(f"API call failed: {e}")
        raise CustomAPIError(f"Failed to fetch data from {url}", 503)
```

### Testing Strategy
- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test component interactions and external services
- **Fixtures**: Use pytest fixtures for test data and mocking
- **Coverage**: Aim for >80% code coverage with meaningful tests
- **Mocking**: Mock external dependencies and services

### Performance Considerations
- **Database Queries**: Use proper indexing and avoid N+1 query problems
- **Caching**: Implement caching for expensive operations (Redis, memcached)
- **Async/Await**: Use asynchronous programming for I/O-bound operations
- **Memory Management**: Be mindful of memory usage in data processing
- **Profiling**: Use cProfile and memory_profiler for performance analysis

### Deployment & Production
- **Environment Management**: Use virtual environments (venv, poetry, conda)
- **Dependencies**: Pin versions in requirements.txt or pyproject.toml
- **Docker**: Containerize applications with multi-stage builds
- **Health Checks**: Implement health check endpoints for monitoring
- **Logging**: Structured logging with appropriate log levels