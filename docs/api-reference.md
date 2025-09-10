# API Reference Documentation

## Table of Contents
- [Python Package API](#python-package-api)
- [CLI Command Reference](#cli-command-reference)
- [Configuration Schema](#configuration-schema)
- [Template System](#template-system)

## Python Package API

### Core Modules

#### `claude_config.composer`

**Class: `AgentComposer`**
Core templating engine for processing YAML agent definitions through Jinja2 templates.

```python
class AgentComposer:
    """Simple templating engine for converting YAML to agent markdown."""
    
    def __init__(self, config_path: str, template_path: str) -> None:
        """Initialize composer with YAML and template paths."""
    
    def generate_agent(self, agent_name: str) -> str:
        """Generate agent markdown from YAML definition via template.
        
        Args:
            agent_name: Name of agent to generate
            
        Returns:
            Agent markdown as string
            
        Raises:
            AgentNotFoundError: If YAML file doesn't exist
            ValidationError: If YAML is invalid
        """
    
    def list_available_agents(self) -> List[str]:
        """Return list of available agents from YAML files."""
```

**Usage Example:**
```python
from claude_config.composer import AgentComposer

composer = AgentComposer(
    config_path="data/personas",
    template_path="src/claude_config/templates"
)

# Generate agent markdown
agent_markdown = composer.generate_agent("python-engineer")

# List available agents  
agents = composer.list_available_agents()
print(f"Available agents: {agents}")
```

#### `claude_config.validator`

**Class: `ConfigValidator`**
Basic YAML syntax and structure validation.

```python
class ConfigValidator:
    """Basic YAML validation for agent configurations."""
    
    def __init__(self) -> None:
        """Initialize validator."""
    
    def validate_agent_yaml(self, yaml_path: str) -> ValidationResult:
        """Validate agent YAML syntax and required fields.
        
        Args:
            yaml_path: Path to YAML file
            
        Returns:
            ValidationResult with basic errors
        """
    
    def validate_required_fields(self, config: Dict[str, Any]) -> List[str]:
        """Check for required fields in agent configuration."""
```

**Usage Example:**
```python
from claude_config.validator import ConfigValidator

validator = ConfigValidator()

# Validate agent YAML file
result = validator.validate_agent_yaml("data/personas/python-engineer.yaml")
if result.is_valid:
    print("YAML is valid")
else:
    for error in result.errors:
        print(f"Error: {error}")
```

#### `claude_config.exceptions`

**Custom Exception Classes**

```python
class ClaudeConfigError(Exception):
    """Base exception for claude-config package."""

class AgentNotFoundError(ClaudeConfigError):
    """Raised when requested agent YAML file doesn't exist."""

class ValidationError(ClaudeConfigError):
    """Raised when YAML syntax or structure is invalid."""
    
class TemplateError(ClaudeConfigError):
    """Raised when template rendering fails."""
```

### Data Models

#### `claude_config.models`

**Basic Models for YAML Configuration**

```python
from typing import List, Dict, Optional

class AgentConfig:
    """Basic YAML agent configuration."""
    
    def __init__(self, yaml_data: Dict):
        self.name = yaml_data['name']
        self.display_name = yaml_data['display_name']
        self.model = yaml_data['model']
        self.description = yaml_data['description']
        self.context_priming = yaml_data['context_priming']
        self.responsibilities = yaml_data.get('responsibilities', [])
        self.expertise = yaml_data.get('expertise', [])
        self.proactive_triggers = yaml_data.get('proactive_triggers', {})

class ValidationResult:
    """Result of basic YAML validation."""
    
    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []
```

---

## CLI Command Reference

### Installation Commands

```bash
# Install claude-config package
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Using uv (recommended)
uv pip install -e .
```

### Build Commands

```bash
# Build all agent configurations
claude-config build

# Build specific agent
claude-config build --agent python-engineer
```

### Validation Commands

```bash
# Validate all YAML files
claude-config validate

# Validate specific agent
claude-config validate --agent python-engineer
```

### List Commands

```bash
# List all available agents
claude-config list-agents
```

### Installation Commands

```bash
# Install to ~/.claude/ directory
claude-config install
```

### Help Commands

```bash
# Show usage information
claude-config --help

# Show command-specific help
claude-config build --help
```

---

## Configuration Schema

### Agent Configuration Schema

**File Location**: `data/personas/{agent-name}.yaml`

```yaml
# Required fields
name: string                    # Agent identifier (kebab-case)
display_name: string           # Human-readable name
model: haiku|sonnet|opus       # Claude model tier
description: string            # Agent purpose and capabilities

# Core agent definition
context_priming: |             # Multi-line string with agent mindset
  You are a [role] with [experience]. Your mindset:
  - "[thought pattern 1]"
  - "[thought pattern 2]"

responsibilities:              # List of what agent handles
- "Primary responsibility"
- "Secondary responsibility"

expertise:                     # List of technical expertise areas
- "Technology 1 with specific frameworks"
- "Technology 2 with specific tools"

# Optional fields
proactive_triggers:            # Auto-activation patterns
  file_patterns:
  - "*.py"
  - "requirements.txt"
  project_indicators:
  - "Django"
  - "FastAPI"
```



---

## Template System

### Jinja2 Template

**Template Location**: `src/claude_config/templates/agent.md.j2`

Single template that converts YAML to agent markdown:

```jinja2
---
name: {{ agent.name }}
model: {{ agent.model }}
---

# {{ agent.display_name }}

{{ agent.description }}

## Context Priming

{{ agent.context_priming }}

## Responsibilities

{% for responsibility in agent.responsibilities %}
- {{ responsibility }}
{% endfor %}

## Expertise

{% for item in agent.expertise %}
- {{ item }}
{% endfor %}

{% if agent.proactive_triggers %}
## Proactive Triggers

### File Patterns
{% for pattern in agent.proactive_triggers.file_patterns %}
- `{{ pattern }}`
{% endfor %}

### Project Indicators
{% for indicator in agent.proactive_triggers.project_indicators %}
- {{ indicator }}
{% endfor %}
{% endif %}
```

#### Basic Template Functions

**Available in Templates**:

```jinja2
# Basic string formatting
{{ value | title }}          # Title Case
{{ value | upper }}          # UPPERCASE  
{{ value | lower }}          # lowercase

# List operations
{{ items | join(", ") }}     # Join list with separator

# Conditional rendering
{% if condition %}
Content when true
{% endif %}

# Loop over lists
{% for item in list %}
- {{ item }}
{% endfor %}
```

---

### Basic Validation

#### Validation Rules
- **YAML Syntax**: Must be valid YAML
- **Required Fields**: name, display_name, model, description must be present
- **Model Tier**: Must be one of haiku, sonnet, opus
- **Template Variables**: All variables must be resolvable

#### Validation Commands

```bash
# Validate all agents
claude-config validate

# Validate specific agent
claude-config validate --agent python-engineer
```

#### Validation Output Example

```
✅ YAML syntax validation passed (25/25 agents)
❌ Required field validation failed:
  - mobile-engineer.yaml: Missing 'responsibilities' field
  - data-engineer.yaml: Empty 'expertise' field

Validation Summary:
- 23 agents valid
- 2 agents with errors
```

---

## Error Handling

### Common Errors and Solutions

#### `AgentNotFoundError`
**Cause**: Requested agent YAML file doesn't exist
**Solution**: Check available agents with `claude-config list-agents`

#### `ValidationError`
**Cause**: YAML syntax or required fields invalid
**Solution**: Run `claude-config validate --agent <name>` for specific errors

#### `TemplateError`  
**Cause**: Template rendering failed due to missing variables
**Solution**: Check YAML fields match template expectations

This API reference documents the simplified claude-config templating tool for generating Claude Code agent configurations.