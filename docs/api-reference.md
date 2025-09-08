# API Reference Documentation

## Table of Contents
- [Python Package API](#python-package-api)
- [CLI Command Reference](#cli-command-reference)
- [Configuration Schema](#configuration-schema)
- [Template API](#template-api)
- [Validation Framework](#validation-framework)

## Python Package API

### Core Modules

#### `claude_config.composer`

**Class: `AgentComposer`**
Main class for composing agents from YAML configurations and templates.

```python
class AgentComposer:
    """Agent composition engine for generating agents from YAML configurations."""
    
    def __init__(self, config_path: str, template_path: str) -> None:
        """Initialize composer with configuration and template paths."""
    
    def compose_agent(self, agent_name: str) -> str:
        """Generate complete agent markdown from YAML configuration.
        
        Args:
            agent_name: Name of agent to compose
            
        Returns:
            Complete agent markdown as string
            
        Raises:
            AgentNotFoundError: If agent configuration doesn't exist
            ValidationError: If YAML configuration is invalid
        """
    
    def list_available_agents(self) -> List[str]:
        """Return list of available agent names from configurations."""
    
    def validate_agent_config(self, agent_name: str) -> bool:
        """Validate agent YAML configuration against schema."""
```

**Usage Example:**
```python
from claude_config.composer import AgentComposer

composer = AgentComposer(
    config_path="data/personas",
    template_path="src/claude_config/templates"
)

# Generate agent
agent_markdown = composer.compose_agent("python-engineer")

# List available agents  
agents = composer.list_available_agents()
print(f"Available agents: {agents}")
```

#### `claude_config.validator`

**Class: `ConfigValidator`**
Validates YAML configurations and ensures consistency across agents.

```python
class ConfigValidator:
    """Validation framework for agent configurations."""
    
    def __init__(self, schema_path: str) -> None:
        """Initialize validator with schema definitions."""
    
    def validate_persona_config(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate persona YAML configuration.
        
        Args:
            config: Parsed YAML configuration dictionary
            
        Returns:
            ValidationResult with errors and warnings
        """
    
    def validate_trait_config(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate trait YAML configuration."""
    
    def check_agent_boundaries(self, agents: List[Dict]) -> List[BoundaryConflict]:
        """Check for overlapping agent responsibilities."""
    
    def validate_proactive_triggers(self, triggers: Dict) -> List[ValidationError]:
        """Validate proactive trigger patterns for conflicts."""
```

**Usage Example:**
```python
from claude_config.validator import ConfigValidator
import yaml

validator = ConfigValidator("data/schemas")

# Load and validate persona config
with open("data/personas/python-engineer.yaml") as f:
    config = yaml.safe_load(f)

result = validator.validate_persona_config(config)
if result.is_valid:
    print("Configuration is valid")
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
    """Raised when requested agent configuration doesn't exist."""

class ValidationError(ClaudeConfigError):
    """Raised when YAML configuration fails validation."""
    
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message)

class TemplateError(ClaudeConfigError):
    """Raised when template rendering fails."""

class BoundaryConflictError(ClaudeConfigError):
    """Raised when agent boundaries overlap inappropriately."""
```

### Data Models

#### `claude_config.models`

**Pydantic Models for Configuration**

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class PersonaConfig(BaseModel):
    """Schema for persona YAML configuration."""
    
    name: str = Field(..., description="Agent identifier")
    display_name: str = Field(..., description="Human-readable name")
    model: Literal["haiku", "sonnet", "opus"] = Field(..., description="Claude model tier")
    description: str = Field(..., description="Agent purpose and capabilities")
    
    context_priming: str = Field(..., description="Mindset and thought patterns")
    expertise: List[str] = Field(..., description="Technical expertise areas")
    quality_criteria: Dict[str, List[str]] = Field(..., description="Quality standards")
    decision_frameworks: Dict[str, Dict] = Field(..., description="Decision guidance")
    boundaries: Dict[str, List[str]] = Field(..., description="Responsibility boundaries")
    common_failures: Dict[str, List[str]] = Field(..., description="Known failure patterns")
    
    proactive_triggers: Optional[ProactiveTriggers] = Field(None, description="Auto-activation patterns")
    content_sections: Optional[Dict[str, str]] = Field(None, description="Content file references")
    custom_instructions: Optional[str] = Field(None, description="Additional instructions")
    coordination_overrides: Optional[Dict[str, str]] = Field(None, description="Coordination customizations")

class ProactiveTriggers(BaseModel):
    """Proactive activation patterns."""
    
    file_patterns: List[str] = Field(default_factory=list, description="File glob patterns")
    project_indicators: List[str] = Field(default_factory=list, description="Project detection keywords")
    dependency_patterns: List[str] = Field(default_factory=list, description="Package.json/requirements.txt patterns")

class ValidationResult(BaseModel):
    """Result of configuration validation."""
    
    is_valid: bool = Field(..., description="Overall validation status")
    errors: List[str] = Field(default_factory=list, description="Critical validation errors")
    warnings: List[str] = Field(default_factory=list, description="Non-critical warnings")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
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

# Build with validation enabled
claude-config build --validate

# Build to custom output directory
claude-config build --output-dir /custom/path

# Verbose build output
claude-config build --verbose

# Clean build (remove existing outputs)
claude-config build --clean
```

### Validation Commands

```bash
# Validate all configurations
claude-config validate

# Validate specific agent
claude-config validate --agent python-engineer

# Schema validation only
claude-config validate --schema-only

# Check for agent boundary conflicts
claude-config validate --check-boundaries

# Validate proactive trigger patterns
claude-config validate --check-triggers

# Detailed validation output
claude-config validate --verbose
```

### List Commands

```bash
# List all available agents
claude-config list-agents

# List agents by model tier
claude-config list-agents --tier sonnet

# List agents with descriptions
claude-config list-agents --verbose

# List available traits (future)
claude-config list-traits

# List content sections for agent
claude-config list-content --agent python-engineer
```

### Installation Commands

```bash
# Install to default Claude Code directory (~/.claude/)
claude-config install

# Install to custom directory
claude-config install --target /custom/path

# Dry run installation (show what would be installed)
claude-config install --dry-run

# Install with backup of existing files
claude-config install --backup

# Force installation (overwrite without confirmation)
claude-config install --force
```

### Development Commands

```bash
# Watch for changes and rebuild
claude-config watch

# Start development server (future)
claude-config serve

# Generate documentation
claude-config docs

# Check system status
claude-config status
```

---

## Configuration Schema

### Persona Configuration Schema

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

expertise:                     # List of technical expertise areas
- "Technology 1 with specific frameworks"
- "Technology 2 with specific tools"

quality_criteria:              # Nested dictionary of quality standards
  code_quality:
  - "Standard 1 with measurable criteria"
  - "Standard 2 with specific requirements"
  performance:
  - "Performance metric with target"
  maintainability:
  - "Maintainability requirement"

decision_frameworks:           # Nested decision guidance
  category_name:
    option_1: "When to use option 1"
    option_2: "When to use option 2"
  architecture_patterns:
    small_projects: "Guidance for small projects"
    large_projects: "Guidance for large projects"

boundaries:                    # Clear responsibility boundaries
  do_handle:
  - "Responsibility 1"
  - "Responsibility 2"
  coordinate_with:
  - "other-agent: What to coordinate on"

common_failures:               # Known failure patterns and solutions
  failure_category:
  - "Failure pattern (solution approach)"
  - "Another failure (prevention strategy)"

# Optional fields
proactive_triggers:            # Auto-activation patterns
  file_patterns:
  - "*.py"
  - "requirements.txt"
  project_indicators:
  - "Django"
  - "FastAPI"
  dependency_patterns:
  - "flask"
  - "django"

content_sections:              # External content file references
  section_name: personas/{agent-name}/section-file.md

custom_instructions: |         # Additional specific instructions
  ## Custom Protocol
  
  Specific instructions that override defaults.

coordination_overrides:        # Override default coordination patterns
  testing_framework: "Custom testing approach"
  deployment_strategy: "Custom deployment approach"
```

### Trait Configuration Schema (Future)

**File Location**: `data/traits/{category}/{trait-name}.yaml`

```yaml
name: string                   # Trait identifier
category: string               # Trait category (safety, coordination, enhancement)
display_name: string           # Human-readable name
description: string            # Trait purpose

implementation: |              # Multi-line implementation details
  ## Trait Implementation
  
  Detailed implementation guidance.

dependencies:                  # Other traits this depends on
- trait-name-1
- trait-name-2

conflicts:                     # Traits that conflict with this one
- conflicting-trait

parameters:                    # Configurable parameters
  parameter_name:
    type: string|boolean|integer
    default: value
    description: "Parameter description"
```

---

## Template API

### Jinja2 Template System

**Template Location**: `src/claude_config/templates/`

#### Main Agent Template

**File**: `agent.md.j2`

```jinja2
---
name: {{ persona.name }}
model: {{ persona.model }}
---

# {{ persona.display_name }}

{{ persona.description }}

## Context Priming

{{ persona.context_priming }}

## Expertise

{% for item in persona.expertise %}
- {{ item }}
{% endfor %}

## Quality Criteria

{% for category, criteria in persona.quality_criteria.items() %}
### {{ category | title }}
{% for criterion in criteria %}
- {{ criterion }}
{% endfor %}
{% endfor %}

## Decision Frameworks

{% for framework, options in persona.decision_frameworks.items() %}
### {{ framework | title }}
{% for option, guidance in options.items() %}
**{{ option }}**: {{ guidance }}
{% endfor %}
{% endfor %}

## Boundaries

### Direct Responsibilities
{% for responsibility in persona.boundaries.do_handle %}
- {{ responsibility }}
{% endfor %}

### Coordination Points
{% for coordination in persona.boundaries.coordinate_with %}
- {{ coordination }}
{% endfor %}

## Common Failures

{% for category, failures in persona.common_failures.items() %}
### {{ category | title }}
{% for failure in failures %}
- {{ failure }}
{% endfor %}
{% endfor %}

{% if persona.proactive_triggers %}
## Proactive Triggers

### File Patterns
{% for pattern in persona.proactive_triggers.file_patterns %}
- `{{ pattern }}`
{% endfor %}

### Project Indicators
{% for indicator in persona.proactive_triggers.project_indicators %}
- {{ indicator }}
{% endfor %}
{% endif %}

{% if persona.content_sections %}
## Extended Content

{% for section, file_path in persona.content_sections.items() %}
### {{ section | title }}

{% include file_path %}
{% endfor %}
{% endif %}

{% if persona.custom_instructions %}
{{ persona.custom_instructions }}
{% endif %}
```

#### Template Functions

**Available Functions in Templates**:

```jinja2
# String formatting
{{ value | title }}          # Title Case
{{ value | upper }}          # UPPERCASE  
{{ value | lower }}          # lowercase
{{ value | kebab_case }}     # kebab-case
{{ value | snake_case }}     # snake_case

# List operations
{{ items | join(", ") }}     # Join list with separator
{{ items | length }}         # Get list length
{{ items | sort }}           # Sort list

# Conditional rendering
{% if condition %}
Content when true
{% endif %}

{% for item in list %}
- {{ item }}
{% endfor %}

# Template inheritance
{% extends "base.md.j2" %}
{% block content %}
Agent-specific content
{% endblock %}

# Including other templates
{% include "common/safety-protocols.md.j2" %}
```

---

## Validation Framework

### Validation Rules

#### Schema Validation
- **YAML Syntax**: Must be valid YAML
- **Required Fields**: All required fields must be present
- **Field Types**: Fields must match expected types (string, list, dict)
- **Model Tier**: Must be one of haiku, sonnet, opus
- **Name Format**: Agent names must be kebab-case

#### Content Validation  
- **File References**: Content section files must exist
- **Template Variables**: All template variables must be resolvable
- **Markdown Syntax**: Generated markdown must be valid

#### Semantic Validation
- **Boundary Conflicts**: Agents shouldn't have overlapping responsibilities
- **Trigger Conflicts**: File patterns shouldn't conflict between agents
- **Coordination Integrity**: Referenced agents in coordination must exist
- **Quality Criteria**: Must be specific and measurable

### Validation Commands

```bash
# Run full validation suite
make validate

# Individual validation types
claude-config validate --schema              # YAML structure only
claude-config validate --content             # Content file existence
claude-config validate --semantic            # Boundary and trigger conflicts
claude-config validate --template            # Template rendering
```

### Validation Output Example

```
✅ Schema validation passed (25/25 agents)
✅ Content validation passed (all referenced files exist)  
❌ Semantic validation failed:
  - Boundary conflict: python-engineer and ai-engineer both handle "API development"
  - Trigger conflict: *.py pattern matches both python-engineer and ai-engineer
⚠️  Template warnings:
  - mobile-engineer.yaml: Referenced content file not found: platform-expertise.md

Validation Summary:
- 23 agents valid
- 2 agents with conflicts  
- 1 agent with warnings
- 0 critical errors
```

### Custom Validation Rules

**Extending Validation**:

```python
from claude_config.validator import ConfigValidator, ValidationRule

class CustomRule(ValidationRule):
    """Custom validation rule example."""
    
    def validate(self, config: Dict) -> List[ValidationError]:
        errors = []
        
        # Custom validation logic
        if "custom_field" in config and not config["custom_field"]:
            errors.append(ValidationError("Custom field cannot be empty"))
            
        return errors

# Register custom rule
validator = ConfigValidator()
validator.add_rule(CustomRule())
```

---

## Error Handling

### Common Errors and Solutions

#### `AgentNotFoundError`
**Cause**: Requested agent configuration file doesn't exist
**Solution**: Check available agents with `claude-config list-agents`

#### `ValidationError`
**Cause**: YAML configuration doesn't match schema
**Solution**: Run `claude-config validate --agent <name>` for specific errors

#### `TemplateError`  
**Cause**: Template rendering failed due to missing variables
**Solution**: Check template variables match configuration fields

#### `BoundaryConflictError`
**Cause**: Multiple agents claim the same responsibilities
**Solution**: Run `claude-config validate --check-boundaries` to identify conflicts

### Debug Mode

```bash
# Enable detailed error output
claude-config build --debug

# Enable verbose logging
export CLAUDE_CONFIG_LOG_LEVEL=DEBUG
claude-config build
```

This API reference provides comprehensive documentation for all aspects of the claude-config system, enabling developers to effectively use, extend, and contribute to the project.