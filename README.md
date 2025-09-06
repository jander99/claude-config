# Claude Code Agent Configuration Repository

A composable system for Claude Code that enables efficient, specialized AI assistance through intelligent agent compositions for personal development workflows.

## Table of Contents
- [Project Overview](#project-overview)
- [Current Architecture](#current-architecture)
- [Proposed Composable System](#proposed-composable-system)
- [Implementation Phases](#implementation-phases)
- [Getting Started](#getting-started)
- [Technical Architecture](#technical-architecture)
- [Developer Guide](#developer-guide)
- [Scripts and Tools](#scripts-and-tools)
- [Contributing](#contributing)

## Project Overview

This repository contains a comprehensive composition system for Claude Code, featuring **20 specialized agents** and **configuration composition capabilities** that provide expert assistance across software development domains. The system enables proactive, context-aware development workflows with intelligent agent coordination and flexible, secure configuration management.

### Current Capabilities
- **Core Development**: AI/ML, Python, Java, Frontend, DevOps, Data Engineering, Blockchain
- **Research & Strategy**: AI Research, Product Management, Quantitative Analysis  
- **Quality & Architecture**: QA Engineering, System Architecture, Technical Writing
- **Support**: Git Operations, Security, Database Engineering, Prompt Enhancement

### The Composable Vision

We are implementing a **composable system** that transforms how agents are built and maintained:

**Agent Composition:**
- **Eliminate Duplication**: 60%+ code reuse through shared components
- **Consistent Coordination**: Standardized communication patterns across all agents
- **Rapid Innovation**: Build new agents by composing existing personas and traits
- **Maintainable Architecture**: Template-based generation with version control
- **Personal Customization**: Clean configuration system for individual workflows

## Current Architecture

### File Structure
```
${HOME}/.claude/
├── agents/                 # Specialized agent definitions
│   ├── ai-engineer.md          # ML/AI development specialist
│   ├── python-engineer.md      # Web frameworks & data processing
│   ├── java-engineer.md        # Spring Boot & enterprise Java
│   ├── frontend-engineer.md    # React, Vue, Angular development
│   ├── devops-engineer.md      # Kubernetes, Docker, CI/CD
│   ├── data-engineer.md        # Data pipelines & ETL processes
│   ├── blockchain-engineer.md  # Smart contracts & DeFi protocols
│   ├── sr-architect.md         # System design & escalation resolution
│   ├── qa-engineer.md          # Test automation & quality assurance
│   ├── technical-writer.md     # API docs & user guides
│   ├── git-helper.md           # Version control operations
│   ├── security-engineer.md    # Application security & compliance
│   ├── database-engineer.md    # Database design & optimization
│   ├── ai-researcher.md        # Literature review & methodology
│   ├── sr-ai-researcher.md     # Advanced research synthesis
│   ├── product-manager.md      # Agile methodology & user stories
│   ├── quant-analyst.md        # Financial metrics & modeling
│   ├── sr-quant-analyst.md     # Advanced quantitative analysis
│   ├── prompt-engineer.md      # EXPERIMENTAL: Request enhancement
│   └── agent-architect.md      # Meta-level agent system design
```

### Current Agent Format
Each agent uses YAML frontmatter with markdown content:

```yaml
---
name: python-engineer
description: Web frameworks, data processing, and general Python development
model: sonnet
---

# Python Engineer Agent

You are a Python development specialist focused on web frameworks...
```

### Current Limitations

1. **High Duplication**: Branch safety checks, coordination patterns, and boilerplate repeated across agents
2. **Inconsistent Coordination**: Agent handoff patterns vary in implementation
3. **Maintenance Overhead**: Updates require manual changes across multiple files
4. **Limited Extensibility**: No plugin architecture for custom agent development
5. **Version Fragmentation**: Different agents may use incompatible patterns

## Proposed Composable System

### Agent Component Architecture

The agent composition system introduces four core component types:

#### 1. Personas (`data/personas/`)
Domain-specific expertise definitions:
```yaml
# data/personas/python-engineer.yaml
name: python_developer
display_name: "Python Developer"
expertise:
  - "Web frameworks (Django, FastAPI, Flask)"
  - "Data processing with pandas, numpy"
  - "API development and testing"
proactive_triggers:
  file_patterns: ["*.py", "requirements.txt", "pyproject.toml"]
  project_indicators: ["Flask", "Django", "FastAPI"]
```

#### 2. Traits (`data/traits/`)
Reusable behaviors and capabilities:
```yaml
# data/traits/safety/branch-check.yaml
name: branch_safety
category: safety
implementation: |
  ## Branch Safety Protocol
  Before any development work:
  1. Check current branch: `git branch --show-current`
  2. If on protected branch (main/master/develop):
     - Ask: "You're on {{branch}}. Create feature branch?"
     - Suggest: `{{branch_type}}/{{feature_name}}`
```

#### 3. Compositions (`data/personas/`)
Agent definitions built from personas and traits:
```yaml
# data/personas/python-engineer.yaml
name: python-engineer
model: sonnet
persona: python_developer
traits:
  - branch_safety
  - testing_coordination
  - documentation_handoff
  - proactive_detection
custom_instructions: |
  Focus on modern Python practices and performance optimization.
```

#### 4. Scripts (`data/scripts/`)
Automation and composition tools:
```python
# data/scripts/build.py
def compose_agent(composition_file):
    """Build complete agent from composition definition"""
    composition = load_yaml(composition_file)
    persona = load_persona(composition.persona)
    traits = [load_trait(t) for t in composition.traits]
    
    return render_agent_template(persona, traits, composition)
```

### Configuration System

The configuration system uses a single, simple configuration file with clean file inclusion:

**Single config.yaml example**:
```yaml
# data/config.yaml
name: personal-claude-config
output_dir: dist/

# Agent selection
agents:
  - ai-engineer
  - python-engineer  
  - git-helper
  - qa-engineer

# MCP server configuration
mcp_servers:
  - github
  - filesystem
  - docker
  - time

# Global settings
settings:
  secrets_file: .env
  model_preferences:
    default: sonnet
    complex: opus
    simple: haiku

# Custom instructions
global_instructions: |
  Personal preferences and instructions
  that apply to all agents.
```

**Persona Definition Example**:
```yaml
# personas/ai-engineer.yaml  
name: ai-engineer
model: sonnet
content:
  sections:
    core: "content/personas/ai-engineer/core.md"
    coordination: "content/personas/ai-engineer/coordination.md"
    examples: "content/personas/ai-engineer/examples.md"
traits:
  - safety/branch-check
  - coordination/qa-handoff
```

### Directory Structure

#### This Repository (claude-config)
```
claude-config/                 # This repository
├── README.md                      # This documentation
├── CLAUDE.md                      # Global instructions & coordination guide
├── agents/                        # Current agent definitions (.md files)
│   ├── ai-engineer.md
│   ├── python-engineer.md
│   ├── java-engineer.md
│   ├── frontend-engineer.md
│   ├── devops-engineer.md
│   ├── data-engineer.md
│   ├── blockchain-engineer.md
│   ├── sr-architect.md
│   ├── qa-engineer.md
│   ├── technical-writer.md
│   ├── git-helper.md
│   ├── security-engineer.md
│   ├── database-engineer.md
│   ├── ai-researcher.md
│   ├── sr-ai-researcher.md
│   ├── product-manager.md
│   ├── quant-analyst.md
│   ├── sr-quant-analyst.md
│   ├── prompt-engineer.md
│   └── agent-architect.md
├── settings.json                  # Claude Code configuration settings
├── data/                          # Configuration generation system (planned)
│   ├── config.yaml                    # Single configuration file
│   ├── personas/                      # Agent definitions (YAML only)
│   │   ├── ai-engineer.yaml
│   │   ├── python-engineer.yaml
│   │   └── git-helper.yaml
│   ├── traits/                        # Reusable behaviors (YAML only)  
│   │   ├── safety/
│   │   │   ├── branch-check.yaml
│   │   │   └── project-verification.yaml
│   │   └── coordination/
│   │       ├── qa-handoff.yaml
│   │       └── escalation.yaml
│   ├── content/                       # All markdown content
│   │   ├── personas/
│   │   │   ├── ai-engineer/
│   │   │   │   ├── core.md
│   │   │   │   ├── coordination.md
│   │   │   │   └── examples.md
│   │   │   └── python-engineer/
│   │   │       ├── core.md
│   │   │       └── coordination.md
│   │   ├── traits/
│   │   │   ├── safety/
│   │   │   │   └── branch-check.md
│   │   │   └── coordination/
│   │   │       └── qa-handoff.md
│   │   └── shared/                    # Reusable content chunks
│   │       ├── cost-optimization.md
│   │       └── common-workflows.md
│   ├── templates/                     # Jinja2 templates
│   │   ├── agent.md.j2
│   │   └── claude-config.json.j2
│   └── scripts/                       # Build and automation scripts
│       ├── build.py
│       ├── validate.py
│       └── watch.py
└── dist/                          # Generated outputs (gitignored)
    ├── agents/
    ├── settings.json
    └── CLAUDE.md

```

#### Production Directory (${HOME}/.claude/)
Generated and deployed from this repository:
```
${HOME}/.claude/
├── agents/                        # Specialized agent definitions
├── settings.json                  # Claude Code configuration
├── CLAUDE.md                      # Global instructions
├── projects/                      # Project-specific configurations
├── todos/                         # Task management state
└── ide/, local/, shell-snapshots/, statsig/  # Runtime directories
```

## Implementation Phases

### Phase 1: Proof of Concept (4-6 weeks)
**Agent Composition Deliverables:**
- [ ] Python composition engine with Jinja2 templates
- [ ] 3 core personas (Python, AI, Git Helper)
- [ ] 5 essential traits (branch safety, testing, documentation, proactive detection, coordination)
- [ ] 2 complete agent compositions demonstrating the system
- [ ] Makefile-based build system (`make build`)

**Success Criteria:**
- Generated agents functionally equivalent to hand-written versions
- 50%+ reduction in boilerplate code
- Successful composition of new agent variants
- Simple configuration generation without multi-environment complexity

### Phase 2: Core Migration (6-8 weeks)
**Agent Migration Deliverables:**
- [ ] All existing agents migrated to composable system
- [ ] Full trait library covering all current patterns
- [ ] Validation framework ensuring backward compatibility
- [ ] Make-based documentation generation and diff tools
- [ ] Simple configuration system for personal use

**Success Criteria:**
- 100% feature parity with existing agents
- All coordination patterns standardized
- Automated testing validates agent behavior
- Simple, maintainable configuration system

### Phase 3: Advanced Features (4-6 weeks)
**Deliverables:**
- [ ] Agent versioning and dependency management
- [ ] Communication protocol implementation
- [ ] Plugin architecture for custom traits
- [ ] Performance optimization and caching
- [ ] Advanced composition patterns

**Success Criteria:**
- Multiple agent versions supported simultaneously
- Third-party trait integration working
- Sub-second agent composition performance

### Phase 4: Community & Extensibility (2-4 weeks)
**Deliverables:**
- [ ] Comprehensive developer documentation
- [ ] Trait contribution guidelines and templates
- [ ] Community agent registry
- [ ] Integration examples and tutorials
- [ ] Migration tools for legacy patterns

**Success Criteria:**
- External developers can create custom agents
- Community contributions integrated successfully
- Knowledge transfer complete for ongoing maintenance

## Configuration Management

### Simple Configuration System

The configuration system uses a single config.yaml file with optional .env for secrets:

#### Configuration Structure
```yaml
# config.yaml
name: personal-claude-config
output_dir: dist/

# Agent selection
agents:
  - ai-engineer
  - python-engineer  
  - git-helper
  - qa-engineer

# MCP server configuration
mcp_servers:
  - github
  - filesystem
  - docker
  - time

# Global settings
settings:
  secrets_file: .env
  model_preferences:
    default: sonnet
    complex: opus
    simple: haiku

# Custom instructions
global_instructions: |
  Personal preferences and instructions
  that apply to all agents.
```

#### Environment Variables
```bash
# .env (optional, not committed)
GITHUB_TOKEN=ghp_your_token_here
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```


## Getting Started

### Prerequisites
- Python 3.8+ 
- uv (Python package manager)
- Git for version control
- Claude Code CLI access

### Development Setup
```bash
# Install uv (modern Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repository-url> claude-config
cd claude-config/

# Install in development mode with all dependencies
make dev

# Build and install configurations
make build
make install-to-claude
```

### Quick Start Example
```bash
# Development workflow
make dev          # Setup development environment
make build        # Build all agents
make test         # Run tests
make install-to-claude  # Install to ~/.claude/

# Continuous development
make watch        # Watch for changes and rebuild
make validate     # Validate all configurations
make lint         # Check code quality
```

## Technical Architecture

### Composition Engine

The composition engine uses Python with Jinja2 templates to generate complete agent markdown files:

```python
class AgentComposer:
    def __init__(self, template_dir: Path):
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def compose_agent(self, composition: AgentComposition) -> str:
        """Generate complete agent markdown from composition"""
        persona = self.load_persona(composition.persona)
        traits = [self.load_trait(t) for t in composition.traits]
        
        template = self.env.get_template('base_agent.md.j2')
        return template.render(
            persona=persona,
            traits=traits,
            composition=composition
        )
```

### Template System

Jinja2 templates provide flexible agent generation:

```jinja2
{# base_agent.md.j2 #}
---
name: {{ composition.name }}
description: {{ persona.display_name }} with {{ traits|length }} specialized traits
model: {{ composition.model }}
---

# {{ persona.display_name }} Agent

{{ persona.description }}

## Core Responsibilities
{% for responsibility in persona.responsibilities %}
- {{ responsibility }}
{% endfor %}

{% for trait in traits %}
{% include 'traits/' + trait.name + '.md.j2' %}
{% endfor %}

{{ composition.custom_instructions }}
```

### Communication Protocol

Standardized agent communication uses structured messaging:

```yaml
# Communication protocol example
agent_message:
  sender: python-engineer
  recipient: qa-engineer
  message_type: handoff
  context:
    task: "API endpoint testing"
    artifacts: ["tests/test_api.py", "src/api/endpoints.py"]
    requirements: ["integration_tests", "performance_validation"]
  priority: normal
```

### Versioning Strategy

Version management supports multiple agent versions:

```yaml
# Version configuration
agent_version: "2.1.0"
dependencies:
  persona: python_developer >= 1.2.0
  traits:
    - branch_safety >= 1.0.0
    - testing_coordination >= 2.0.0
compatibility:
  claude_code: ">= 1.0.0"
  min_model: sonnet
```

## Developer Guide

### Creating New Personas

Define domain expertise in YAML format:

```yaml
# data/personas/rust-engineer.yaml
name: rust_developer
display_name: "Rust Developer"
version: "1.0.0"
description: "Systems programming specialist focused on memory safety and performance"

expertise:
  - "Memory-safe systems programming"
  - "Concurrent and parallel computing"
  - "WebAssembly development"
  - "Performance optimization"

responsibilities:
  - "Implement high-performance Rust applications"
  - "Ensure memory safety and thread safety"
  - "Optimize for zero-cost abstractions"

proactive_triggers:
  file_patterns: ["*.rs", "Cargo.toml", "Cargo.lock"]
  project_indicators: ["Rust", "Cargo", "rustc"]
  
tools_integration:
  - cargo
  - rustfmt
  - clippy
```

### Developing Reusable Traits

Create modular behaviors:

```yaml
# data/traits/performance/optimization.yaml
name: performance_optimization
category: enhancement
version: "1.0.0"
dependencies: []

description: "Performance analysis and optimization capabilities"

implementation: |
  ## Performance Optimization Protocol
  
  ### Before Implementation
  1. Profile current performance baseline
  2. Identify bottlenecks and critical paths
  3. Set performance targets and metrics
  
  ### During Development  
  1. Use appropriate profiling tools for the language
  2. Implement optimizations incrementally
  3. Measure impact of each optimization
  
  ### Validation
  1. Run performance benchmarks
  2. Compare against baseline metrics
  3. Document optimization decisions and tradeoffs

coordination_patterns:
  - name: performance_handoff
    trigger: "performance issues identified"
    action: "coordinate with appropriate specialist"
    context_required: ["profiling_data", "performance_requirements"]
```

### Composing Agents

Combine personas and traits to create specialized agents:

```yaml
# data/personas/rust-performance-engineer.yaml
name: rust-performance-engineer
version: "1.0.0"
model: sonnet

persona: rust_developer
traits:
  - branch_safety
  - performance_optimization
  - testing_coordination
  - documentation_handoff
  - proactive_detection

custom_instructions: |
  Focus on zero-cost abstractions and compile-time optimizations.
  Prioritize memory safety while achieving C-level performance.
  
  ## Specialized Workflows
  - Use `cargo bench` for performance regression testing
  - Integrate `valgrind` and `perf` for profiling
  - Coordinate with devops-engineer for deployment optimization

coordination_overrides:
  testing_framework: "cargo test with criterion.rs benchmarks"
  documentation_style: "rustdoc with performance notes"
```


### Testing and Validation

Ensure composition correctness:

```python
# tests/test_rust_performance_engineer.py
def test_rust_performance_composition():
    """Validate Rust performance engineer composition"""
    composition = load_composition("rust-performance-engineer.yaml")
    agent = compose_agent(composition)
    
    # Verify persona integration
    assert "memory safety" in agent.content
    assert "performance optimization" in agent.content
    
    # Verify trait inclusion
    assert "Branch Safety Protocol" in agent.content
    assert "Performance Optimization Protocol" in agent.content
    
    # Verify coordination patterns
    assert "cargo bench" in agent.content
    assert "devops-engineer" in agent.coordination_patterns
```

## Scripts and Tools

The Python project includes comprehensive Make targets and a CLI:

### Command Line Interface
```bash
# Core commands
claude-config build              # Build all agent configurations
claude-config build --agent ai-engineer  # Build specific agent
claude-config validate          # Validate all configurations
claude-config list-agents       # List available personas
claude-config list-traits       # List available traits
claude-config install          # Install to ~/.claude/

# Development commands
claude-config build --watch     # Watch for changes and rebuild
claude-config build --validate  # Build with validation
```

### Make Targets
```makefile
# Setup & Installation
make dev                        # Install in development mode
make install                    # Install package
make install-to-claude          # Install generated config to ~/.claude/

# Development
make build                      # Build all agent configurations
make validate                   # Validate all configurations
make test                       # Run test suite
make lint                       # Run code linting
make format                     # Auto-format code
make watch                      # Watch for changes and rebuild

# Maintenance
make clean                      # Clean build artifacts
make list                       # List available agents and traits
```

### Development Workflow

#### Setup New Environment
```bash
git clone <repository-url> claude-config
cd claude-config/
make dev                        # Install dev dependencies and setup
```

#### Daily Development
```bash
make build                      # Build all configurations
make test                       # Run test suite  
make validate                   # Check configuration validity
make install-to-claude          # Deploy to ~/.claude/
```

#### Code Quality
```bash
make format                     # Auto-format Python code
make lint                       # Run linters (black, isort, mypy)
make clean                      # Clean build artifacts
```

#### Continuous Development
```bash
make watch                      # Watch files and rebuild automatically
make test-watch                 # Run tests on file changes
```


## Contributing

### Contribution Areas

**Agent Composition:**
- **Persona Development**: Create expertise definitions for new domains
- **Trait Libraries**: Develop reusable behaviors and coordination patterns  
- **Template Enhancement**: Improve agent generation templates
- **Agent Testing**: Validate compositions and ensure backward compatibility

**Infrastructure & Tooling:**
- **CLI Tool Development**: Build utilities for composition and validation
- **Testing Frameworks**: Develop automated testing for compositions
- **Documentation**: Expand guides, examples, and best practices
- **Configuration System**: Maintain simple, personal configuration management

### Development Workflow

1. **Fork Repository**: Create personal fork for development
2. **Feature Branch**: Use `feature/` prefix for new capabilities
3. **Composition First**: Build agents using the composable system
4. **Test Thoroughly**: Validate generated agents match expected behavior
5. **Document Changes**: Update relevant documentation and examples
6. **Submit PR**: Include before/after comparisons and test results

### Quality Standards

- **Backward Compatibility**: Existing agent behavior must be preserved
- **Performance**: Agent composition should complete in <1 second
- **Documentation**: All new traits and personas require documentation
- **Testing**: Include automated tests for all new components
- **Validation**: Generated agents must pass all existing validation tests

### Getting Help

- **Issues**: Report bugs and request features via GitHub issues
- **Discussions**: Join architectural discussions and planning
- **Documentation**: Refer to `docs/` directory for detailed guides
- **Examples**: Check `docs/examples/` for implementation patterns

---

## Next Steps

This composable system represents a significant evolution in how AI development assistance is structured and delivered. The implementation will:

**Agent Composition Benefits:**
1. **Reduce Maintenance Overhead** by centralizing common patterns
2. **Enable Rapid Innovation** through component reuse and composition  
3. **Improve Consistency** across all agent interactions
4. **Support Extensibility** for custom domain requirements
5. **Simplify Configuration** with clean, personal workflow management

The phased approach ensures stability while enabling continuous improvement. Each phase builds upon previous work, creating a robust foundation for agent development in AI-assisted workflows.

**Current Status**: Planning and Architecture Complete  
**Next Milestone**: Phase 1 Proof of Concept Development  
**Timeline**: 10-14 weeks total implementation

Ready to transform how AI agents are built and maintained in personal development workflows.