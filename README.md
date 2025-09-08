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

## Creating New Agents Tutorial

This comprehensive tutorial guides you through creating a new specialized agent using the enhanced agent architecture with structured fields for data-driven behavior.

### Understanding the Enhanced Agent Architecture

The enhanced agent system uses 5 key structured fields to create intelligent, consistent agents:

#### 1. `context_priming`
Establishes the agent's mindset, thought patterns, and core values:
```yaml
context_priming: |
  You are a senior Python engineer with 10+ years building production systems. Your mindset:
  - "What's the most Pythonic way to solve this robustly?"
  - "How do I make this maintainable for the next developer?"
  - "Where are the potential failure points and edge cases?"
  
  You think in terms of: clean architecture, proper error handling, testing strategies, 
  performance optimization, and long-term maintainability.
```

#### 2. `quality_criteria`
Defines measurable standards for code quality, performance, and maintainability:
```yaml
quality_criteria:
  code_quality:
    - Follows PEP 8 with black formatting and type hints
    - 90%+ test coverage with meaningful assertions
  performance:
    - Database queries optimized with proper indexing
    - Response times <200ms for API endpoints
  maintainability:
    - Clear docstrings following Google/NumPy format
    - Configuration externalized and environment-specific
```

#### 3. `decision_frameworks`
Provides structured decision-making guidance for technology choices:
```yaml
decision_frameworks:
  framework_selection:
    web_apis:
      - FastAPI: Modern async APIs with auto-documentation
      - Django: Full-featured web apps with admin interface
      - Flask: Lightweight APIs and microservices
  architecture_patterns:
    small_projects: "Simple module structure with clear separation"
    medium_projects: "Package structure with domain-driven design"
    large_projects: "Microservices with event-driven architecture"
```

#### 4. `boundaries`
Clearly defines what the agent handles vs. coordinates with others:
```yaml
boundaries:
  do_handle:
    - Web application development and API design
    - Data processing and ETL pipeline creation
  coordinate_with:
    - ai-engineer: ML model implementation and training
    - security-engineer: Authentication systems and vulnerability scanning
```

#### 5. `common_failures`
Documents typical failure patterns and their solutions:
```yaml
common_failures:
  performance_issues:
    - N+1 database queries (use select_related/prefetch_related)
    - Blocking I/O in async contexts (use await properly)
  security_vulnerabilities:
    - SQL injection from unsanitized inputs
    - Missing authentication on sensitive endpoints
```

### Step-by-Step Agent Creation Process

#### Step 1: Plan Your Agent

Before writing any YAML, plan your agent's purpose:

1. **Identify the Domain**: What specific technology or role does this agent specialize in?
2. **Define Boundaries**: What will this agent handle vs. coordinate with others?
3. **List Expertise**: What specific tools, frameworks, and patterns should it know?
4. **Plan Coordination**: Which existing agents will this work with?

**Example**: Creating a `mobile-engineer` agent
- Domain: React Native, Flutter, iOS/Android development
- Boundaries: Mobile app development, app store deployment
- Expertise: React Native, Flutter, Expo, mobile debugging
- Coordination: `frontend-engineer` (web views), `devops-engineer` (CI/CD)

#### Step 2: Create the YAML File

Create a new file: `/home/jeff/workspaces/ai/claude-config/data/personas/[agent-name].yaml`

**Required YAML Structure:**

```yaml
name: mobile-engineer
display_name: Mobile Engineer  
model: sonnet
description: Expert mobile developer specializing in React Native, Flutter, and native iOS/Android development

context_priming: |
  You are a senior mobile engineer with deep expertise in cross-platform development. Your mindset:
  - "How do I ensure this works across all target devices and OS versions?"
  - "What's the performance impact on battery and memory?"
  - "How do I handle platform-specific requirements elegantly?"
  - "What's the user experience on different screen sizes?"
  
  You think in terms of: platform consistency, performance optimization, 
  offline capabilities, and platform-specific best practices.

expertise:
- React Native development with TypeScript and native modules
- Flutter development with Dart and platform channels
- Native iOS development with Swift and Xcode
- Native Android development with Kotlin and Android Studio
- Mobile UI/UX patterns and responsive design
- App store submission and review processes
- Mobile device debugging and performance profiling

quality_criteria:
  performance:
    - App startup time <3 seconds on target devices
    - Smooth 60fps animations and scrolling
    - Memory usage optimized for low-end devices
    - Battery consumption minimized for background tasks
  user_experience:
    - Consistent behavior across platforms
    - Proper handling of device orientations and screen sizes  
    - Accessibility features implemented (VoiceOver, TalkBack)
    - Offline functionality where appropriate
  code_quality:
    - TypeScript with strict mode enabled
    - Comprehensive testing including unit and integration tests
    - Platform-specific code properly abstracted
    - Error boundaries and crash reporting implemented

decision_frameworks:
  platform_selection:
    cross_platform:
      - React Native: "JavaScript/TypeScript teams, complex business logic"
      - Flutter: "Single codebase priority, custom UI requirements"
    native_development:
      - iOS Native: "iOS-specific features, maximum performance"
      - Android Native: "Android-specific features, platform integration"
  
  architecture_patterns:
    small_apps: "Screen-based navigation with local state management"
    medium_apps: "Feature-based architecture with Redux/Riverpod"
    large_apps: "Micro-frontend architecture with shared libraries"
  
  testing_strategy:
    unit_tests: "Business logic and utility functions"
    widget_tests: "UI components and user interactions"
    integration_tests: "End-to-end user workflows and API integration"

boundaries:
  do_handle:
    - Mobile application development and architecture
    - Platform-specific implementation and optimization
    - App store deployment and submission processes
    - Mobile debugging and performance optimization
    - Cross-platform development strategies
  
  coordinate_with:
    - frontend-engineer: Web view integration and shared components
    - python-engineer: Backend API design for mobile consumption
    - devops-engineer: CI/CD pipelines for mobile builds
    - ui-ux-designer: Mobile-specific design patterns and accessibility
    - qa-engineer: Mobile testing strategies and device compatibility

common_failures:
  performance_issues:
    - Bridge communication overhead in React Native (minimize bridge calls)
    - Memory leaks from event listeners (proper cleanup in useEffect)
    - Large bundle sizes affecting startup time (code splitting and lazy loading)
  platform_compatibility:
    - Inconsistent behavior between iOS and Android (test on both platforms)
    - Screen size and orientation issues (responsive design patterns)
    - Platform-specific permissions and capabilities (check availability)
  deployment_issues:
    - App store rejection due to policy violations (follow guidelines)
    - Certificate and provisioning profile problems (automate management)
    - Version mismatch between platforms (coordinated release process)

proactive_triggers:
  file_patterns:
  - '*.tsx'
  - '*.dart'
  - '*.swift'
  - '*.kt'
  - package.json
  - pubspec.yaml
  - ios/
  - android/
  project_indicators:
  - React Native
  - Flutter
  - Expo
  - Xcode
  - Android Studio
  - react-native
  - flutter

content_sections:
  technical_approach: personas/mobile-engineer/technical-approach.md
  platform_expertise: personas/mobile-engineer/platform-expertise.md
  coordination_patterns: personas/mobile-engineer/coordination-patterns.md
  performance_optimization: personas/mobile-engineer/performance-optimization.md

custom_instructions: |
  ## Mobile Development Protocol
  
  **1. Platform Assessment (First 30 seconds)**
  - Identify target platforms (iOS, Android, or both)
  - Check existing project structure and dependencies
  - Verify development environment setup (Xcode, Android Studio)
  - Review device compatibility requirements
  
  **2. Cross-Platform Considerations**
  - Evaluate shared code vs platform-specific requirements
  - Plan navigation patterns for mobile UX
  - Consider offline capabilities and data synchronization
  - Design responsive layouts for various screen sizes
  
  **3. Development Approach**
  - Start with core functionality on primary platform
  - Implement platform-specific optimizations
  - Add comprehensive error handling and logging
  - Test on actual devices, not just simulators
  - Profile performance and memory usage
  
  ## Quality Assurance Standards
  
  **Before completing any mobile feature:**
  - Test on minimum supported OS versions
  - Verify accessibility features work correctly
  - Check performance on low-end devices
  - Validate offline functionality if applicable
  - Ensure proper error messaging for network issues

coordination_overrides:
  testing_framework: Platform-specific testing (XCTest for iOS, Espresso for Android)
  performance_monitoring: Native performance profiling tools and crash reporting
  deployment_strategy: Platform-specific CI/CD with automated testing on devices
  design_compliance: Mobile-first design patterns with platform-specific guidelines
```

#### Step 3: Create Content Sections (Optional)

If your agent needs detailed content sections, create markdown files in `/home/jeff/workspaces/ai/claude-config/data/content/personas/[agent-name]/`:

```bash
mkdir -p data/content/personas/mobile-engineer
```

Create files like:
- `technical-approach.md` - Detailed technical methodologies
- `platform-expertise.md` - Platform-specific guidance  
- `coordination-patterns.md` - How this agent works with others
- `performance-optimization.md` - Performance best practices

#### Step 4: Validate Your Agent Configuration

Run validation to check your YAML syntax and structure:

```bash
# Validate the specific agent
claude-config validate --agent mobile-engineer

# Or validate all agents
claude-config validate
```

#### Step 5: Build and Test the Agent

Generate the complete agent markdown:

```bash
# Build the specific agent
claude-config build --agent mobile-engineer

# Build all agents
make build
```

Check the generated output in `dist/agents/mobile-engineer.md` to ensure it looks correct.

#### Step 6: Integration Testing

Install to your Claude Code directory for testing:

```bash
# Install to ~/.claude/
make install-to-claude

# Or install to custom location
claude-config install --target /path/to/test/location
```

Test the agent by:
1. Creating a test mobile project
2. Verifying the agent activates on file patterns
3. Testing coordination with other agents
4. Validating the agent's decision-making and guidance

### Best Practices for Agent Specifications

#### Writing Effective Context Priming
- Use specific, actionable thought patterns
- Include domain-specific concerns and priorities
- Reference real-world experience levels
- Focus on decision-making approaches

#### Defining Quality Criteria  
- Make criteria measurable and testable
- Include performance benchmarks with numbers
- Cover maintainability and documentation standards
- Address security and reliability concerns

#### Creating Decision Frameworks
- Structure choices hierarchically by use case
- Provide clear selection criteria
- Include technology trade-offs
- Reference specific tools and frameworks

#### Setting Clear Boundaries
- Explicitly list what the agent handles independently
- Define coordination points with other agents
- Avoid overlapping responsibilities
- Consider the agent's core expertise limits

#### Documenting Common Failures
- Include real failure patterns from the domain
- Provide specific solutions and prevention strategies
- Reference performance and security pitfalls
- Help agents avoid known problematic patterns

### Testing and Validation

#### Automated Validation
The build system includes several validation checks:

```bash
# Full validation suite
make validate

# Specific validations
claude-config validate --schema    # YAML structure validation  
claude-config validate --links     # Content section link validation
claude-config validate --conflicts # Agent boundary conflict detection
```

#### Manual Testing Checklist

**Agent Configuration:**
- [ ] YAML syntax is valid and loads correctly
- [ ] All required fields are present and properly formatted
- [ ] Content sections reference existing files
- [ ] Proactive triggers are specific and non-overlapping

**Generated Output:**
- [ ] Agent markdown renders correctly with all sections
- [ ] Quality criteria are clearly formatted
- [ ] Decision frameworks are logically structured  
- [ ] Common failures provide actionable guidance

**Integration Testing:**
- [ ] Agent activates on appropriate file patterns
- [ ] Coordination with other agents works as expected
- [ ] Custom instructions provide clear guidance
- [ ] Agent boundaries are respected in practice

### Integration with Build System

The build system automatically:

1. **Validates** YAML structure against the schema
2. **Resolves** content section references
3. **Generates** complete agent markdown using Jinja2 templates
4. **Installs** agents to the Claude Code directory

#### Build Process Flow

```
YAML Agent Definition
         ↓
   Schema Validation
         ↓
  Content Resolution  
         ↓
   Template Rendering
         ↓
  Generated Agent.md
         ↓
   Installation to ~/.claude/
```

#### Advanced Features

**Trait Inheritance** (Future):
Agents will be able to inherit common behaviors from reusable trait definitions.

**Pattern Resolution** (Future):  
Agents will be able to reference common patterns that get expanded during build.

**Automated Testing** (Future):
Generated agents will be automatically tested for consistency and coordination patterns.

### Contributing Your Agent

Once your agent is complete:

1. **Test Thoroughly**: Ensure it works correctly and coordinates properly
2. **Document**: Add clear descriptions and examples
3. **Follow Standards**: Use consistent formatting and terminology
4. **Submit PR**: Create a pull request with your new agent
5. **Include Tests**: Add any specific test cases for your agent

Your new agent will be reviewed for:
- Technical accuracy and completeness
- Proper coordination patterns with existing agents
- Clear boundaries and responsibilities
- Quality of decision frameworks and guidance

## Contributing

### Development Process

1. **Setup**: Clone repository and run `make dev`
2. **Feature Branch**: Create feature branches for new work
3. **Testing**: Run `make test` and `make validate` before committing
4. **Quality**: Use `make lint` and `make format` for code quality
5. **Submit**: Create PR with clear description of changes

### Areas for Contribution

- **Agent Development**: Create new specialized agents using the tutorial above
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