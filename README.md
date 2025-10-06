# Claude Code Subagent Generator

A powerful toolkit for generating and managing specialized Claude Code agent configurations through YAML-driven templating.

## Overview

Claude Code Subagent Generator is a lightweight, flexible system for creating and managing AI agent configurations. It transforms simple YAML definitions into comprehensive markdown-based agent specifications, enabling rapid development of specialized AI assistants.

## Key Features

- **YAML-Driven Agent Definitions**: Create agents using intuitive YAML format
- **Jinja2 Template Engine**: Convert YAML to markdown agent configurations
- **Extensive Agent Library**: 25+ pre-configured specialized agents
- **Simple CLI Management**: Build, validate, and install agents with ease

## Quick Start

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) or pip
- Basic understanding of YAML

### Installation

```bash
# Clone the repository
git clone <repository-url> claude-config
cd claude-config

# Install dependencies
uv pip install -e .
# Or with pip
pip install -e .
```

### Basic Usage

```bash
# Build all agent configurations
claude-config build

# Install to Claude Code directory
claude-config install

# Validate configurations
claude-config validate
```

## Agent Creation Example

Create a new agent in `data/personas/mobile-engineer.yaml`:

```yaml
name: mobile-engineer
display_name: Mobile Engineer
model: sonnet
description: Expert mobile developer for cross-platform mobile applications

context_priming: |
  You are a senior mobile engineer specializing in cross-platform development

responsibilities:
  - React Native and Flutter development
  - Native iOS and Android development
  - Mobile performance optimization

expertise:
  - "React Native with TypeScript"
  - "Flutter with Dart"
  - "iOS with Swift"
  - "Android with Kotlin"

proactive_triggers:
  file_patterns:
    - "*.tsx"
    - "*.dart"
  project_indicators:
    - "React Native"
    - "Flutter"
```

## Orchestration Features

The toolkit includes advanced orchestration commands for generating master coordination files, validating agent relationships, and visualizing the agent ecosystem.

### Generate Master CLAUDE.md

Generate the master orchestration file that Claude Code uses for agent delegation decisions:

```bash
# Generate to default location (~/.claude/CLAUDE.md)
make generate-claude-md

# Generate to custom location
python -m claude_config.cli generate-claude-md --output dist/CLAUDE.md

# Skip validation (not recommended)
python -m claude_config.cli generate-claude-md --no-validate

# Preview without writing
python -m claude_config.cli generate-claude-md --dry-run
```

**What it does:**
- Loads all agent YAML configurations
- Extracts coordination patterns and relationships
- Validates the coordination graph for cycles and consistency
- Generates optimized CLAUDE.md with delegation rules

### Validate Coordination Patterns

Perform comprehensive validation of agent coordination patterns:

```bash
# Validate all agents
make validate-coordination

# Validate specific agent
python -m claude_config.cli validate-coordination --agent python-engineer

# Attempt to fix common warnings
python -m claude_config.cli validate-coordination --fix-warnings
```

**Validation checks:**
- Circular dependency detection
- Bidirectional coordination consistency
- Unreachable agent detection
- Trait validation
- Entry point verification

### Visualize Coordination Graph

Generate visual representations of the agent coordination graph:

```bash
# Display Mermaid diagram in terminal
make visualize-graph

# Save Mermaid diagram to file
python -m claude_config.cli visualize-graph --output coordination.md

# Generate JSON representation
python -m claude_config.cli visualize-graph --format json --output graph.json

# Limit visualization size
python -m claude_config.cli visualize-graph --max-nodes 20
```

**Output formats:**
- **Mermaid**: Interactive diagrams (default)
- **JSON**: Structured graph data
- **DOT**: Graphviz format (planned)

### Show Agent Coordination

Display detailed coordination information for specific agents:

```bash
# Show coordination for python-engineer
make show-coordination AGENT=python-engineer

# Show coordination for qa-engineer
make show-coordination AGENT=qa-engineer
```

**Displays:**
- Outbound coordination (who this agent coordinates with)
- Inbound coordination (who coordinates with this agent)
- Coordination traits used
- Custom coordination patterns
- Proactive trigger patterns

### Build with Orchestration

Build agents and generate orchestration file in one command:

```bash
# Build all agents and generate CLAUDE.md
make build-with-orchestration

# Build agents separately then orchestration
make build-agents
make generate-claude-md
```

**Workflow integration:**
1. Validates all agent configurations
2. Builds agent markdown files
3. Validates coordination patterns
4. Generates optimized CLAUDE.md

## CLI Reference

### Core Commands

```bash
# Build agent configurations
make build-agents

# Install to ~/.claude/
make install

# Validate YAML configurations
make validate

# List available agents
make list-agents
```

### Orchestration Commands

```bash
# Generate CLAUDE.md orchestration file
make generate-claude-md

# Validate coordination patterns
make validate-coordination

# Visualize coordination graph
make visualize-graph

# Show agent coordination details
make show-coordination AGENT=agent-name

# Build with orchestration
make build-with-orchestration
```

### Advanced Options

For advanced usage with custom options, use the Python module directly:

```bash
# Generate with custom options
python -m claude_config.cli generate-claude-md --output PATH --no-validate

# Validate specific agent
python -m claude_config.cli validate-coordination --agent NAME --fix-warnings

# Visualize with format options
python -m claude_config.cli visualize-graph --format json --max-nodes 20
```

### Common Workflows

**Development workflow:**
```bash
# 1. Modify agent YAML files
vim data/personas/python-engineer.yaml

# 2. Validate changes
make validate

# 3. Validate coordination
make validate-coordination

# 4. Build with orchestration
make build-with-orchestration

# 5. Install to Claude Code
make install
```

**Agent debugging workflow:**
```bash
# 1. Check coordination patterns
make show-coordination AGENT=python-engineer

# 2. Visualize graph
make visualize-graph

# 3. Validate specific agent
python -m claude_config.cli validate-coordination --agent python-engineer
```

**Production deployment:**
```bash
# Build, validate, and generate orchestration
make build-with-orchestration

# Preview installation
python -m claude_config.cli install --dry-run

# Install to production
make install
```

## Roadmap

- Expand agent library
- Enhance template system
- Improve CLI tooling
- Add more advanced validation

## Contributing

1. Fork the repository
2. Create your agent in `data/personas/`
3. Validate with `claude-config validate`
4. Submit a pull request

## License

[Insert License Information]

## Contact

[Insert Contact or Support Information]