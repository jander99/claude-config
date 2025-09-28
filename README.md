# Claude Config Generator

A simple YAML-to-Markdown templating system for generating Claude Code agent configurations. This project provides specialized agent definitions through a focused build-and-deploy process.

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

This repository implements a **simple templating system** for Claude Code agent configurations. The system provides:

- **YAML Source Format**: Single YAML file per agent with complete definition
- **Template-Based Generation**: Jinja2 templates convert YAML to agent markdown
- **Agent Library**: 28+ specialized agents for software development
- **Build System**: Python CLI with validation, build, and installation
- **Focused Purpose**: Pure agent configuration generation

## Features

### Core Capabilities
- **YAML-to-Template Processing**: Convert YAML definitions to agent markdown
- **Agent Library**: 28+ specialized development agents
- **CLI Tools**: Build, validate, install, and list commands
- **Basic Validation**: YAML syntax and structure checking
- **Simple Installation**: Deploy to ~/.claude/ directory

### Agent System
- **28+ Specialized Agents**: Development, research, and architecture roles
- **Proactive Triggers**: Agents activate based on file patterns and project types
- **Tier-Based Selection**: Haiku (efficiency), Sonnet (balanced), Opus (strategic)
- **Coordination Patterns**: Clear handoff protocols between agents

## Architecture

### Simple Templating System

The architecture uses YAML source files and Jinja2 templates to generate agent configurations:

#### 1. Agent Definitions (`data/personas/`)
Agent specifications in YAML format:
```yaml
# data/personas/python-engineer.yaml
name: python-engineer
display_name: "Python Engineer"
model: sonnet
description: Expert Python developer specializing in web frameworks...

context_priming: |
  You are a senior Python engineer with deep expertise...

responsibilities:
  - Web application development and API design
  - Data processing and automation scripts

expertise:
  - "Web frameworks (Django, FastAPI, Flask)"
  - "Data processing and automation"

proactive_triggers:
  file_patterns: ["*.py", "requirements.txt"]
  project_indicators: ["Flask", "Django"]
```

#### 2. Template System (`src/claude_config/templates/`)
Jinja2 template converts YAML to agent markdown:
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
{% for item in agent.responsibilities %}
- {{ item }}
{% endfor %}
```

#### 3. Build System
Python CLI that processes YAML files through templates to generate agent markdown files.

### Repository Structure

```
claude-config/                     # This repository
├── README.md                      # This documentation
├── CLAUDE.md                      # Global instructions
├── pyproject.toml                 # Python project configuration
├── Makefile                      # Development automation
├── src/
│   └── claude_config/
│       ├── cli.py                # Command-line interface (~100 lines)
│       ├── composer.py           # Template engine (~200 lines)
│       ├── validator.py          # YAML validation (~115 lines)
│       └── templates/            # Jinja2 templates
├── data/
│   └── personas/                # Agent definitions (25+ YAML files)
├── settings.json                 # Claude Code settings
├── tests/                        # Test suite (4 files)
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

This is a simple, focused templating tool for Claude Code configurations:

- **✅ YAML Agent Definitions**: 25+ specialized agents in YAML format
- **✅ Template System**: Jinja2-based YAML-to-Markdown conversion
- **✅ Build System**: Python CLI with essential commands
- **✅ Basic Validation**: YAML syntax and structure checking
- **✅ Installation**: Deploy to ~/.claude/ directory
- **✅ Simplified Architecture**: ~500 lines total, focused on core functionality

### Architecture Focus

**Current State**: Simplified, focused templating tool

**Completed**:
- ✅ YAML agent definitions (25+ agents)
- ✅ Simple template-based generation
- ✅ Basic CLI with essential commands
- ✅ YAML validation and testing
- ✅ Architecture simplification (~500 lines total)

**Current Benefits**:
- 🎯 Simple, focused tool for one purpose
- 📝 25+ development agents in YAML format
- ⚡ Fast, lightweight operation
- 🧹 Clean, maintainable codebase
- ✨ Right-sized for its purpose

## Getting Started

### Prerequisites
- Python 3.8+
- [uv](https://docs.astral.sh/uv/) or pip for package management
- Basic familiarity with YAML and Jinja2 templates

### Installation

#### Development Setup
```bash
# Clone repository
git clone <repository-url> claude-config
cd claude-config/

# Install dependencies
uv pip install -e .

# Or with pip
pip install -e .
```

#### Quick Start
```bash
# Build agent configurations
claude-config build

# Install to Claude Code directory
claude-config install

# Validate configurations
claude-config validate
```

## Development

### Development Workflow

```bash
# Build configurations
claude-config build

# Validate YAML and templates
claude-config validate

# Install to Claude Code
claude-config install

# List available agents
claude-config list-agents

# Run tests
pytest tests/
```

### Architecture Overview

The system is built with:

- **Python Package**: Simple project structure with pyproject.toml
- **CLI Interface**: Basic command-line tools with Click
- **Template Engine**: Jinja2 templates for YAML-to-Markdown conversion
- **Basic Validation**: YAML syntax and structure checking
- **Testing**: Focused test suite covering core functionality

### Key Components

#### CLI (`src/claude_config/cli.py`) - ~100 lines
```bash
claude-config build                    # Build agent configurations
claude-config validate                 # Validate YAML syntax
claude-config list-agents              # List available agents
claude-config install                  # Install to ~/.claude/
claude-config --help                   # Show usage
```

#### Composer (`src/claude_config/composer.py`) - ~200 lines
Core templating engine that processes YAML files through Jinja2 templates.

#### Validator (`src/claude_config/validator.py`) - ~115 lines
Basic YAML syntax and structure validation.

#### Templates (`src/claude_config/templates/`)
Jinja2 template for converting YAML to agent markdown.

## CLI Usage

### Building Configurations
```bash
# Build all agents
claude-config build

# Build specific agent
claude-config build --agent python-engineer
```

### Validation
```bash
# Validate YAML syntax and structure
claude-config validate

# List available agents
claude-config list-agents
```

### Installation
```bash
# Install to ~/.claude/
claude-config install
```

## Configuration

### Configuration System

- **`data/personas/*.yaml`**: Agent definitions in YAML format
- **`src/claude_config/templates/`**: Jinja2 template for generating agent markdown
- **`settings.json`**: Claude Code configuration
- **`CLAUDE.md`**: Global instructions for Claude Code

### Agent Configuration Format

YAML format for agent definitions:

```yaml
name: agent-name
display_name: "Display Name"
model: sonnet|opus|haiku
description: Brief description...

context_priming: |
  You are a senior engineer...

responsibilities:
  - Specific responsibility
  - Another responsibility

expertise:
  - "Domain expertise"

proactive_triggers:
  file_patterns: ["*.py"]
  project_indicators: ["Django"]
```

## Creating New Agents

This guide shows how to create a new agent using the YAML format.

### Agent YAML Structure

Agent definitions use a simple YAML structure:

#### Required Fields

```yaml
name: agent-name                    # Unique identifier
display_name: "Agent Name"          # Human-readable name
model: sonnet|opus|haiku           # LLM model tier
description: Brief description...   # Purpose and capabilities

context_priming: |                  # Agent mindset
  You are a senior engineer...

responsibilities:                   # What agent handles
  - Primary responsibility
  - Secondary responsibility

expertise:                         # Technical expertise
  - "Technology/framework knowledge"

proactive_triggers:                # When agent activates
  file_patterns: ["*.ext"]
  project_indicators: ["Framework"]
```

### Creating an Agent

#### Step 1: Plan the Agent

1. **Define the domain**: What technology does this agent specialize in?
2. **List expertise**: What tools and frameworks should it know?
3. **Set boundaries**: What will it handle directly vs. coordinate on?

#### Step 2: Create the YAML File

Create a new file in `data/personas/[agent-name].yaml`:

```yaml
name: mobile-engineer
display_name: Mobile Engineer
model: sonnet
description: Expert mobile developer for React Native, Flutter, iOS, and Android.

context_priming: |
  You are a senior mobile engineer. You focus on:
  - Cross-platform compatibility
  - Performance optimization
  - Platform-specific requirements

responsibilities:
  - React Native and Flutter development
  - Native iOS and Android development
  - Mobile performance optimization
  - App store deployment

expertise:
  - "React Native with TypeScript"
  - "Flutter with Dart"
  - "iOS with Swift"
  - "Android with Kotlin"

proactive_triggers:
  file_patterns:
    - "*.tsx"
    - "*.dart"
    - "*.swift"
    - "*.kt"
  project_indicators:
    - "React Native"
    - "Flutter"
```

#### Step 3: Validate and Build

Validate the YAML syntax:
```bash
claude-config validate --agent mobile-engineer
```

Build the agent:
```bash
claude-config build --agent mobile-engineer
```

#### Step 4: Test Installation

Install to Claude Code:
```bash
claude-config install
```

The agent will be available in `~/.claude/agents/`.

### Best Practices

- **Context Priming**: Write clear mindset and approach
- **Responsibilities**: Be specific about what agent handles
- **Expertise**: List concrete tools and frameworks
- **Triggers**: Use specific file patterns to avoid conflicts

### Validation

The system provides basic validation:

```bash
# Validate YAML syntax
claude-config validate

# Run tests
pytest tests/
```

### Build Process

The build system:

1. **Validates** YAML syntax
2. **Generates** agent markdown using Jinja2 templates
3. **Installs** to Claude Code directory

```
YAML Definition → Template Rendering → Agent Markdown → Installation
```

### Contributing Agents

1. Create YAML file following the format
2. Validate and test locally
3. Submit pull request
4. Ensure no conflicts with existing agents

## Simplified Architecture

This system provides a focused, lightweight approach to agent configuration:

### Current Architecture
- **Core templating**: ~200 lines
- **CLI interface**: ~100 lines
- **Basic validation**: ~115 lines
- **Tests**: 4 files, focused coverage
- **Total**: ~500-600 lines

### Benefits
- **Focused purpose**: Pure YAML-to-Markdown templating
- **Simple maintenance**: No unnecessary complexity
- **Fast operation**: Minimal overhead and dependencies
- **Clear boundaries**: Does one thing well

## Contributing

### Development Process

1. **Setup**: Clone repository and install dependencies
2. **Changes**: Edit YAML files or Python code as needed
3. **Testing**: Run `claude-config validate` and `pytest tests/`
4. **Submit**: Create PR with clear description

### Areas for Contribution

- **New Agents**: Create agents for additional technologies
- **Template Improvements**: Enhance Jinja2 template
- **Documentation**: Improve guides and examples
- **Basic Tooling**: Small CLI enhancements

### Quality Standards

- YAML must validate (`claude-config validate`)
- Tests must pass (`pytest tests/`)
- Follow existing YAML format for agents
- Update documentation for user-facing changes

---

## Project Status

**Current State**: Simplified, focused templating tool

**Completed**:
- ✅ YAML agent definitions (25+ agents)
- ✅ Simple template-based generation
- ✅ Basic CLI with essential commands
- ✅ YAML validation and testing
- ✅ Architecture simplification (~500 lines total)

**Current State**:
- 🎯 Simple, focused tool for one purpose
- 📝 25+ development agents in YAML format
- ⚡ Fast, lightweight operation
- 🧹 Clean, maintainable codebase
- ✨ Right-sized for its purpose

This system provides a simple, effective way to generate Claude Code agent configurations without unnecessary complexity.