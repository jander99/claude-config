# Claude Config API Reference Documentation

## Table of Contents
- [Overview](#overview)
- [Python Package API](#python-package-api)
- [CLI Command Reference](#cli-command-reference)
- [Configuration Schema](#configuration-schema)
- [Template System](#template-system)

## Overview

Claude Config is a specialized tool for generating and managing agent configurations through YAML-driven templates. It provides a flexible system for defining Claude Code agents with consistent formatting and validation.

## Python Package API

### Core Modules

#### `claude_config.composer`

**Class: `AgentComposer`**
Process YAML agent definitions into markdown documentation.

```python
class AgentComposer:
    """Generates markdown documentation from YAML agent configurations."""

    def __init__(self, config_dir: str, template_dir: str):
        """
        Initialize composer with configuration and template directories.

        Args:
            config_dir: Path to directory containing YAML agent definitions
            template_dir: Path to Jinja2 template directory
        """

    def generate_agent(self, agent_name: str) -> str:
        """
        Generate markdown for a specific agent.

        Args:
            agent_name: Identifier of agent to generate

        Returns:
            Markdown-formatted agent documentation

        Raises:
            AgentNotFoundError: If agent YAML is missing
            ValidationError: If agent configuration is invalid
        """

    def list_available_agents(self) -> List[str]:
        """
        Retrieve list of agent names from YAML configuration directory.

        Returns:
            List of available agent names
        """
```

**Usage Example:**
```python
from claude_config.composer import AgentComposer

# Initialize composer with configuration paths
composer = AgentComposer(
    config_dir="data/personas",
    template_dir="src/claude_config/templates"
)

# Generate markdown for a specific agent
agent_markdown = composer.generate_agent("python-engineer")

# List all available agents
agents = composer.list_available_agents()
```

#### `claude_config.validator`

**Class: `ConfigValidator`**
Validates YAML agent configurations against defined rules.

```python
class ConfigValidator:
    """Validates YAML agent configuration files."""

    def validate_agent_yaml(self, yaml_path: str) -> ValidationResult:
        """
        Validate an agent's YAML configuration.

        Args:
            yaml_path: Path to agent YAML file

        Returns:
            ValidationResult with validation status and errors
        """

    def validate_required_fields(self, config: Dict[str, Any]) -> List[str]:
        """
        Check for presence of required configuration fields.

        Args:
            config: Parsed YAML configuration dictionary

        Returns:
            List of missing or invalid field errors
        """
```

### Exceptions

```python
class ClaudeConfigError(Exception):
    """Base exception for claude-config package."""

class AgentNotFoundError(ClaudeConfigError):
    """Raised when requested agent configuration is missing."""

class ValidationError(ClaudeConfigError):
    """Raised when agent configuration fails validation."""
```

---

## CLI Command Reference

### Package Installation

```bash
# Install package in editable mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Configuration Management

```bash
# List all available agents
claude-config list-agents

# Build agent configurations
claude-config build

# Build specific agent configuration
claude-config build --agent python-engineer

# Validate configurations
claude-config validate

# Validate specific agent configuration
claude-config validate --agent python-engineer
```

### Help and Information

```bash
# Show CLI help
claude-config --help

# Show command-specific help
claude-config build --help
```

---

## Configuration Schema

### Agent Configuration

**Location**: `data/personas/{agent-name}.yaml`

**Required Fields**:
- `name`: Unique kebab-case identifier
- `display_name`: Human-readable name
- `model`: Agent model tier (haiku, sonnet, opus)
- `description`: Purpose and capabilities

**Example Configuration**:
```yaml
name: python-engineer
display_name: Python Engineer
model: sonnet
description: Backend development and Python ecosystem specialist

context_priming: |
  You specialize in Python web frameworks, data processing, and backend architectures.

responsibilities:
- Web API development
- Backend system design
- Python package creation

expertise:
- Django and FastAPI frameworks
- Asynchronous programming
- Microservices architecture
```

---

## Template System

### Jinja2 Template Processing

**Template Location**: `src/claude_config/templates/agent.md.j2`

Converts YAML configurations to markdown documentation using Jinja2 templating.

**Key Template Features**:
- Dynamic section generation
- Conditional rendering
- List iteration
- Basic text transformations

```jinja2
# {{ agent.display_name }}

{{ agent.description }}

## Responsibilities
{% for responsibility in agent.responsibilities %}
- {{ responsibility }}
{% endfor %}
```

---

## Validation Rules

- YAML must be valid syntax
- Required fields must be present
- Model tier must be one of: haiku, sonnet, opus
- All template variables must be resolvable

**Validation Example**:
```
✅ Validation passed: 25/25 agents
❌ Validation errors:
  - mobile-engineer.yaml: Missing 'responsibilities'
  - data-engineer.yaml: Empty 'expertise'
```

---

## Error Handling

### Common Errors

#### `AgentNotFoundError`
- **Cause**: Missing agent YAML configuration
- **Solution**: Verify agent name with `claude-config list-agents`

#### `ValidationError`
- **Cause**: Invalid YAML configuration
- **Solution**: Run `claude-config validate` for detailed errors

## Source Code Reference

For the most up-to-date API details, refer to the source code:
- [GitHub Repository](https://github.com/your-org/claude-config)
- Source files: `src/claude_config/`