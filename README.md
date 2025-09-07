# Claude Config Generator

A composable system for generating Claude Code agent configurations through YAML-based composition. This project transforms how Claude Code agents are built and maintained by enabling component reuse, consistent coordination patterns, and rapid agent development through composition rather than duplication.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Development](#development)
- [CLI Usage](#cli-usage)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Project Overview

This repository implements a **composable agent system** for Claude Code that eliminates duplication and enables rapid agent development through component reuse. Instead of maintaining 20+ individual agent files with repeated patterns, the system uses:

- **Personas**: Domain expertise definitions (YAML)
- **Traits**: Reusable behaviors and coordination patterns (YAML)
- **Templates**: Jinja2 templates for generating complete agent markdown
- **Compositions**: Agent definitions built by combining personas and traits
- **CLI Tools**: Python-based build system for generation and validation

## Features

### Core Capabilities
- **Composable Architecture**: Build agents from reusable personas and traits
- **Template-Based Generation**: Jinja2 templates generate complete agent markdown
- **YAML Configuration**: Clean, maintainable configuration files
- **CLI Tools**: Full command-line interface for building and validation
- **Testing Framework**: Automated validation of generated agents
- **Development Workflow**: Watch mode, linting, and quality checks

### Agent System
- **20+ Specialized Agents**: Comprehensive coverage of development domains
- **Consistent Coordination**: Standardized patterns across all agents
- **Branch Safety**: Mandatory safety checks before development work
- **Quality Assurance**: Integrated testing and documentation workflows
- **Escalation Protocols**: Senior agent routing for complex issues

## Architecture

### Component System

The composable architecture uses four main component types:

#### 1. Personas (`data/personas/`)
Domain expertise definitions in YAML:
```yaml
# data/personas/python-engineer.yaml
name: python_developer
display_name: "Python Developer" 
expertise:
  - "Web frameworks (Django, FastAPI, Flask)"
  - "Data processing and automation"
proactive_triggers:
  file_patterns: ["*.py", "requirements.txt"]
  project_indicators: ["Flask", "Django"]
```

#### 2. Traits (`data/traits/`)
Reusable behaviors and coordination patterns:
```yaml
# data/traits/safety/branch-check.yaml
name: branch_safety
category: safety
implementation: |
  ## Branch Safety Protocol
  Before development work:
  1. Check current branch with `git branch --show-current`
  2. Create feature branch if on protected branch
```

#### 3. Templates (`src/claude_config/templates/`)
Jinja2 templates for agent generation:
```jinja2
---
name: {{ composition.name }}
model: {{ composition.model }}
---

# {{ persona.display_name }}

{{ persona.description }}

{% for trait in traits %}
{{ trait.implementation }}
{% endfor %}
```

#### 4. Build System
Python-based CLI with validation and generation tools.

### Repository Structure

```
claude-config/                     # This repository
├── README.md                      # This documentation
├── CLAUDE.md                      # Global instructions & coordination guide
├── pyproject.toml                 # Python project configuration
├── uv.lock                       # Dependency lock file
├── Makefile                      # Development automation
├── src/
│   └── claude_config/
│       ├── __init__.py
│       ├── cli.py                # Command-line interface
│       ├── composer.py           # Agent composition engine
│       ├── validator.py          # Configuration validation
│       ├── exceptions.py         # Custom exceptions
│       └── templates/            # Jinja2 templates
├── data/                         # Configuration source (planned)
│   ├── config.yaml              # Main configuration
│   ├── personas/                # Agent expertise definitions
│   ├── traits/                  # Reusable behaviors
│   └── content/                 # Markdown content
├── agents/                       # Current agent definitions
│   ├── ai-engineer.md
│   ├── python-engineer.md
│   ├── [18 more agents...]
│   └── agent-architect.md
├── settings.json                 # Claude Code settings
├── tests/                        # Test suite
├── docs/                         # Documentation
├── dist/                         # Generated outputs (gitignored)
└── .claude/                      # Local development target
```

### Deployment Structure

Generated configurations are installed to `${HOME}/.claude/`:
```
${HOME}/.claude/
├── agents/                       # Generated agent definitions
├── settings.json                 # Claude Code configuration
├── CLAUDE.md                     # Global instructions
└── [runtime directories...]
```

## Development Status

This is an active development project implementing a composable agent system:

- **✅ Core Infrastructure**: Python package with CLI, composition engine, and validation
- **✅ Build System**: Make-based development workflow with testing and linting
- **✅ Agent Library**: 20+ specialized agents for comprehensive development coverage
- **🔄 Template System**: Implementing Jinja2-based generation (in progress)
- **📋 Data Layer**: YAML-based personas and traits system (planned)
- **📋 Migration**: Converting existing agents to composable system (planned)

### Next Steps

1. **Template Implementation**: Complete Jinja2 template system for agent generation
2. **Data Layer Setup**: Create YAML personas and traits structure
3. **Agent Migration**: Convert existing agents to composable format
4. **Testing Framework**: Expand test coverage for generated agents
5. **Documentation**: Complete developer guides and examples


## Getting Started

### Prerequisites
- Python 3.8+
- [uv](https://docs.astral.sh/uv/) (recommended Python package manager)
- Git for version control

### Installation

#### Development Setup
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone <repository-url> claude-config
cd claude-config/

# Setup development environment
make dev
```

#### Quick Start
```bash
# Build agent configurations
make build

# Install to Claude Code directory
make install-to-claude

# Run tests
make test
```

## Development

### Development Workflow

```bash
# Setup development environment
make dev                       # Install dependencies and setup pre-commit

# Daily development
make build                     # Build all configurations
make test                      # Run test suite
make validate                  # Validate configurations
make install-to-claude         # Install to ~/.claude/

# Code quality
make format                    # Format Python code
make lint                      # Run linters (black, isort, mypy)

# Continuous development
make watch                     # Watch for changes and rebuild
make clean                     # Clean build artifacts
```

### Architecture Overview

The system is built with:

- **Python Package**: Structured as a proper Python project with `pyproject.toml`
- **CLI Interface**: Rich command-line tools built with Click and Rich
- **Composition Engine**: Jinja2-based template system for agent generation
- **Validation Framework**: Pydantic models and validation rules
- **Testing**: Pytest-based test suite with coverage reporting
- **Development Tools**: Pre-commit hooks, linting, and formatting

### Key Components

#### CLI (`src/claude_config/cli.py`)
```bash
claude-config build                    # Build agent configurations
claude-config validate                 # Validate configurations
claude-config list-agents              # List available agents
claude-config install                  # Install to ~/.claude/
```

#### Composer (`src/claude_config/composer.py`)
Handles agent composition and generation from YAML configurations.

#### Validator (`src/claude_config/validator.py`)
Validates YAML configurations and ensures consistency.

#### Templates (`src/claude_config/templates/`)
Jinja2 templates for generating agent markdown files.


## CLI Usage

### Building Configurations
```bash
# Build all agents
claude-config build

# Build specific agent
claude-config build --agent python-engineer

# Build with validation
claude-config build --validate
```

### Validation and Testing
```bash
# Validate all configurations
claude-config validate

# List available agents
claude-config list-agents

# List available traits
claude-config list-traits
```

### Installation
```bash
# Install to default Claude Code directory
claude-config install

# Install to custom location
claude-config install --target /custom/path

# Dry run to see what would be installed
claude-config install --dry-run
```

## Configuration

### Current Configuration Files

- **`CLAUDE.md`**: Global instructions and coordination guide for all agents
- **`settings.json`**: Claude Code configuration (model preferences, MCP servers)
- **`agents/*.md`**: Individual agent definitions with YAML frontmatter

### Future Configuration System

Planned YAML-based configuration system:

```yaml
# data/config.yaml
name: personal-claude-config
output_dir: dist/

agents:
  - ai-engineer
  - python-engineer
  - git-helper

settings:
  model_preferences:
    default: sonnet
    complex: opus
    simple: haiku
```

## Contributing

### Development Process

1. **Setup**: Clone repository and run `make dev`
2. **Feature Branch**: Create feature branches for new work
3. **Testing**: Run `make test` and `make validate` before committing
4. **Quality**: Use `make lint` and `make format` for code quality
5. **Submit**: Create PR with clear description of changes

### Areas for Contribution

- **Agent Development**: Create new specialized agents
- **Template System**: Improve Jinja2 templates and generation
- **Testing**: Expand test coverage and validation rules
- **Documentation**: Improve guides and examples
- **Tooling**: Enhance CLI and development workflows

### Quality Standards

- All code must pass linting (`make lint`)
- Tests must pass (`make test`) 
- Configurations must validate (`make validate`)
- Documentation should be updated for user-facing changes
- Follow existing code style and patterns

---

## Project Status

**Current State**: Active development of composable agent system

**Completed**:
- ✅ Python package structure with CLI
- ✅ Build system and development workflow
- ✅ 20+ specialized agent definitions
- ✅ Configuration validation framework

**In Progress**:
- 🔄 Template-based agent generation
- 🔄 YAML persona and trait system
- 🔄 Migration from static to composable agents

**Planned**:
- 📋 Complete composable architecture
- 📋 Comprehensive testing framework
- 📋 Advanced coordination patterns
- 📋 Plugin system for custom agents

This system aims to eliminate duplication in agent definitions while maintaining the comprehensive coverage and intelligent coordination that makes Claude Code effective for software development workflows.