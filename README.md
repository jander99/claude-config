# Claude Code Subagent Generator

An advanced YAML-to-Markdown templating system with hybrid trait architecture for generating Claude Code agent configurations.

## Overview

Claude Code Subagent Generator is a sophisticated templating system that transforms YAML agent definitions through Jinja2 templates into comprehensive markdown agent specifications (6,000-12,000 lines each). It enables a multi-agent ecosystem with intelligent task delegation across three performance tiers, using a hybrid trait system to eliminate duplication.

## Key Features

- **YAML-Driven Agent Definitions**: Define agents using intuitive YAML format with Pydantic validation
- **Hybrid Trait System**: 10 reusable traits eliminate 72% duplication across agents
- **Three-Tier Agent Architecture**: Cost-optimized model selection (Haiku/Sonnet/Opus)
- **Jinja2 Template Engine**: Generate comprehensive 6,000-12,000 line agent configurations
- **Extensive Agent Library**: 36 pre-configured specialized agents across development, research, and quality roles
- **Advanced Coordination**: Cycle detection, consistency validation, and graph optimization
- **Rich CLI**: Beautiful terminal output with progress indicators and validation reporting

## Architecture

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| CLI | `src/claude_config/cli.py` | Rich CLI with Click framework |
| Composer | `src/claude_config/composer.py` | Template engine with Pydantic models |
| Validator | `src/claude_config/validator.py` | YAML and trait validation |
| TraitProcessor | `src/claude_config/composer.py` | Loads and merges reusable trait content |
| Coordination | `src/claude_config/coordination/` | Cycle detection, consistency, optimization |
| Generator | `src/claude_config/generator/` | Master CLAUDE.md generation |

### Agent Tiers

| Tier | Model | Cost | Use Cases |
|------|-------|------|-----------|
| 1 | Haiku | Low | git-helper, technical-writer |
| 2 | Sonnet | Medium | 30+ specialists (python-engineer, frontend-engineer, etc.) |
| 3 | Opus | High | sr-architect, sr-ai-researcher, integration-architect |

## Project Structure

```
claude-config/
├── data/
│   └── personas/           # 36 agent YAML definitions
├── src/claude_config/
│   ├── cli.py              # Rich CLI interface
│   ├── composer.py         # Template engine + TraitProcessor
│   ├── validator.py        # YAML validation
│   ├── coordination/       # Cycle detection, consistency, optimization
│   ├── generator/          # CLAUDE.md generator
│   ├── templates/          # Jinja2 templates
│   └── traits/             # 10 reusable trait modules
├── tests/                  # Comprehensive test suite
├── dist/                   # Generated output (gitignored)
│   └── agents/             # Built agent markdown files
├── Makefile                # Build commands
└── pyproject.toml          # Project configuration
```

## Trait System

The hybrid trait system provides reusable modules that agents can import, eliminating duplication across the agent library.

### Trait Categories

```
src/claude_config/traits/
├── coordination/           # Agent handoff patterns
│   ├── standard-safety-protocols.md
│   ├── qa-testing-handoff.md
│   ├── documentation-handoff.md
│   └── version-control-coordination.md
├── tools/                  # Technology stack configurations
│   ├── python-development-stack.md
│   ├── javascript-frontend-stack.md
│   └── docker-kubernetes-stack.md
├── compliance/
│   └── enterprise-compliance-frameworks.md
├── security/
│   └── security-audit-protocols.md
└── performance/
    └── performance-benchmarking-standards.md
```

### Using Traits in Agents

```yaml
# In data/personas/python-engineer.yaml
imports:
  coordination:
    - standard-safety-protocols
    - qa-testing-handoff
  tools:
    - python-development-stack
```

## Quick Start

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) or pip
- Basic understanding of YAML

### Dependencies

The project uses these Python packages (automatically installed):

- `click>=8.0.0` - CLI framework
- `jinja2>=3.0.0` - Template engine
- `pyyaml>=6.0` - YAML parsing
- `pydantic>=2.0.0` - Data validation
- `rich>=13.0.0` - Terminal formatting
- `watchdog>=3.0.0` - File watching

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
make build-agents

# Build global CLAUDE.md orchestration file
make build-claude

# Install to Claude Code directory (~/.claude/)
make install

# Validate YAML configurations and traits
make validate

# List available agents
claude-config list-agents
```

## Agent YAML Schema

Agents support the following fields:

```yaml
name: mobile-engineer
display_name: Mobile Engineer
model: sonnet  # haiku | sonnet | opus
description: Expert mobile developer for cross-platform applications

# Trait imports (reduces duplication)
imports:
  coordination:
    - standard-safety-protocols
  tools:
    - javascript-frontend-stack

context_priming: |
  You are a senior mobile engineer specializing in cross-platform development

responsibilities:
  - React Native and Flutter development
  - Native iOS and Android development

expertise:
  - "React Native with TypeScript"
  - "Flutter with Dart"

# Proactive activation triggers
proactive_triggers:
  file_patterns: ["*.tsx", "*.dart", "*.swift"]
  project_indicators: ["React Native", "Flutter"]
  dependency_patterns: ["react-native", "flutter"]
  user_intent_keywords: ["mobile app", "iOS", "Android"]

# Coordination patterns
coordination:
  triggers:
    outbound:
      - trigger: code_complete
        agents: [qa-engineer]
        mode: automatic
  relationships:
    parallel: [frontend-engineer]
    delegates_to: [security-engineer]

# Additional optional fields
technology_stack:
  primary_frameworks: []
  essential_tools: []
implementation_patterns: []
professional_standards: []
integration_guidelines: []
performance_benchmarks: []
troubleshooting_guides: []
tool_configurations: []
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
claude-config list-agents
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

- [ ] MCP server integration for external tool access
- [ ] Enhanced multi-agent workflow orchestration
- [ ] Additional trait categories (testing, observability)
- [ ] DOT/Graphviz visualization format
- [ ] Agent capability gap analysis tooling
- [ ] Automated trait extraction from existing agents

## Contributing

1. Fork the repository
2. Create your agent in `data/personas/`
3. Add trait imports for common patterns
4. Validate with `make validate` and `make validate-coordination`
5. Submit a pull request

## License

[Insert License Information]

## Contact

[Insert Contact or Support Information]
