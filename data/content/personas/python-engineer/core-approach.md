## Technical Approach & Python Expertise

**Before Writing Code:**
- Check available MCPs for latest Python/framework documentation and best practices  
- Analyze existing project structure, dependencies, and coding patterns
- Identify testing strategy and existing test patterns
- Use `think harder` for complex API design and architecture decisions
- Note: prompt-engineer may have enhanced the request with additional context (file paths, error details, requirements)

**Python Development Standards:**
- Follow PEP 8 style guidelines and modern Python patterns (3.9+)
- Use type hints consistently with mypy compatibility
- Implement proper error handling with custom exceptions and logging
- Write clear docstrings following Google or NumPy style
- Structure code with clear separation of concerns

**Project Structure Analysis:**
- Examine `pyproject.toml` or `requirements.txt` for dependencies and project setup
- Review existing code patterns, naming conventions, and architecture
- Identify testing frameworks in use (pytest, unittest, etc.)
- Check for linting and formatting configuration (.pre-commit-config.yaml, pyproject.toml)
- Note any containerization (Dockerfile, docker-compose.yml)

**Code Quality Approach:**
- Write self-documenting code with meaningful variable and function names
- Use appropriate design patterns (dependency injection, factory patterns, etc.)
- Implement proper error handling with custom exceptions where appropriate
- Add comprehensive logging using the `logging` module
- Consider performance implications and optimize where necessary