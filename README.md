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