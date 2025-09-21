# CLAUDE.md

This file provides project-specific guidance to Claude Code when working with this configuration repository.

## Repository Purpose

This is an advanced YAML-to-Markdown templating system with hybrid trait architecture that generates Claude Code agent configurations. The system processes YAML agent definitions through enhanced Jinja2 templates with trait imports to create comprehensive agent markdown files, then installs them to `${HOME}/.claude/` directory. This is a sophisticated template-based system (~2,000 lines) with trait-based duplication elimination that generates industry-leading agent depth while maintaining consistency.

## Architecture Overview

This repository uses YAML source files and Jinja2 templates to generate agent markdown files. The system consists of:

- **YAML Agent Definitions** (`data/personas/`) - 28 agent specifications with trait imports
- **Hybrid Trait System** (`src/claude_config/traits/`) - 10 reusable traits eliminating 72% duplication
- **Enhanced Template Engine** (`src/claude_config/composer.py`) - ~500 lines with trait processing
- **Advanced CLI** (`src/claude_config/cli.py`) - Build, validate, install commands with trait support
- **YAML Validation** (`src/claude_config/validator.py`) - Enhanced validation with trait verification
- **Jinja2 Templates** (`src/claude_config/templates/`) - Advanced templates with trait integration

### Agent Library

The system generates 28 specialized agents organized by role with hybrid trait coordination:

**Core Development:** `ai-engineer`, `python-engineer`, `java-engineer`, `data-engineer`, `blockchain-engineer`, `mobile-engineer`, `frontend-engineer`, `devops-engineer`, `security-engineer`, `database-engineer`

**Research & Strategy:** `ai-researcher`, `sr-ai-researcher`, `product-manager`, `business-analyst`, `quant-analyst`, `sr-quant-analyst`

**Quality & Architecture:** `qa-engineer`, `performance-engineer`, `sr-architect`, `integration-architect`, `technical-writer`, `ui-ux-designer`

**Specialized:** `prompt-engineer`, `git-helper`, `systems-engineer`, `platform-engineer`, `site-reliability-engineer`, `subagent-generator`

All agents are defined in YAML format in `data/personas/` and converted to markdown via template processing.

### Build Process

The system follows an advanced hybrid trait templating workflow:

1. **YAML Agent Definitions** - Each agent in `data/personas/{agent}.yaml` with trait imports
2. **Trait Processing** - TraitProcessor loads and merges reusable trait content
3. **Template Processing** - Enhanced Jinja2 templates render agents with trait integration
4. **Advanced Validation** - YAML syntax, structure, and trait dependency checking
5. **Agent Generation** - Comprehensive agent markdown files in `dist/agents/` (6,000-12,000 lines each)
6. **Installation** - Generated agents deployed to `~/.claude/agents/`


### Core Components

**CLI Commands:**
- `make build` - Process YAML through enhanced templates with trait integration
- `make install` - Deploy generated agents to ~/.claude/
- `make validate` - Check YAML syntax, structure, and trait dependencies
- `claude-config list-agents` - List available agent definitions
- `claude-config --help` - Show usage information

**Hybrid Trait Template System:**
- Enhanced Jinja2 template at `src/claude_config/templates/agent.md.j2`
- TraitProcessor class for loading and merging trait content
- 10 reusable traits: 4 coordination, 3 tool stacks, 3 compliance/security/performance
- Advanced template rendering with trait imports and custom overrides

**Enhanced Validation:**
- YAML syntax and structure checking
- Required field validation with trait import support
- Trait dependency verification and content validation
- Code example syntax checking and quality gates

## Directory Structure

### This Repository (Development)
- `data/personas/` - YAML agent definitions (28 files with trait imports)
- `src/claude_config/traits/` - Hybrid trait system (10 reusable traits)
- `src/claude_config/cli.py` - Enhanced command-line interface
- `src/claude_config/composer.py` - Advanced template engine with trait processing
- `src/claude_config/validator.py` - Enhanced validation with trait support
- `src/claude_config/templates/` - Advanced Jinja2 templates with trait integration
- `tests/` - Comprehensive test suite covering trait system
- `README.md` - Repository documentation
- `CLAUDE.md` - This project guide
- `DEVELOPMENT_PLAN.md` - Unified enhancement roadmap

### Production Directory (`${HOME}/.claude/`)
Generated and deployed from this repository:
- `agents/` - Generated agent markdown files
- `settings.json` - Claude Code configuration
- `CLAUDE.md` - Global instructions
- `[runtime directories]` - Claude Code operational files

## Simple Configuration

- **Agent Definitions**: YAML files in `data/personas/` with trait import system
- **Trait Library**: 10 reusable traits eliminate 72% duplication across agents
- **Template System**: Enhanced Jinja2 templates with trait integration
- **Settings**: Advanced `settings.json` for Claude Code preferences
- **Build & Deploy**: `make build` processes YAML + traits → comprehensive markdown → installation



## Agent YAML Structure

Each agent is defined in a YAML file with this basic structure:
```yaml
name: agent-name
display_name: "Agent Name"
model: sonnet|opus|haiku
description: Brief description of agent purpose

imports:
  coordination:
    - standard-safety-protocols
    - qa-testing-handoff
  tools:
    - python-development-stack

context_priming: |
  Agent mindset and thought patterns

responsibilities:
  - Primary responsibility
  - Secondary responsibility

expertise:
  - "Technical expertise area"

technology_stack:
  primary_frameworks: []
  essential_tools: []

implementation_patterns: []
professional_standards: []
integration_guidelines: []
performance_benchmarks: []
troubleshooting_guides: []
tool_configurations: []

proactive_triggers:
  file_patterns: ["*.ext"]
  project_indicators: ["Framework"]
```

## Working with This Repository

1. **Modify Agents**: Edit YAML files in `data/personas/` with trait import support
2. **Add New Agents**: Create YAML files using trait imports for consistency
3. **Create Traits**: Add reusable patterns to `src/claude_config/traits/`
4. **Build Agents**: Run `make build` to process YAML + traits through templates
5. **Validate**: Use `make validate` or `claude-config validate` to check syntax and traits
6. **Install**: Deploy with `make install` to ~/.claude/
7. **Test**: Use `pytest tests/` to run comprehensive test suite


## Repository Standards

- All agents defined in YAML format with trait import consistency
- Use trait imports for common patterns (coordination, tools, compliance)
- Follow naming conventions (kebab-case for agent names)
- Include comprehensive content in 7 schema sections for industry-leading depth
- Validate YAML and trait dependencies before committing changes
- Target 6,000-12,000 lines per agent with template-driven consistency

## 📝 INTELLIGENT MARKDOWN FILE CREATION PROTOCOL

**CORE PRINCIPLE**: Create persistent markdown files for substantial content while maintaining terminal efficiency for immediate responses.

### 🎯 FILE CREATION DECISION MATRIX

**CREATE MARKDOWN FILE WHEN:**
- User explicitly requests a "report", "analysis", or "documentation"
- Content exceeds 500 words or contains complex structure/formatting
- Information needs preservation for future reference or sharing
- Multi-section analysis with headers, tables, or code blocks
- Agent workflow artifacts requiring persistence across sessions
- Long test results, logs, or analysis that could lose terminal context
- Multi-agent coordination requiring shared artifact handoffs

**SHOW IN TERMINAL WHEN:**
- Quick answers, explanations, or status updates (<500 words)
- Simple code snippets or configuration examples
- Immediate feedback, confirmations, or error messages
- Interactive workflows requiring immediate user response
- File paths, command outputs, or brief troubleshooting steps

### 📁 SMART DIRECTORY RESOLUTION

**Priority Order for File Placement:**

1. **Detect Existing Patterns** (use project conventions):
   - `./docs/` - If exists with markdown files → **User Reports**
   - `./reports/` - If exists → **Analysis and Reports**
   - `./tmp/` - If exists → **Temporary System Files**
   - `./.claude/` - If exists → **Agent Coordination Files**

2. **Create Directory Strategy**:
   - **User Reports**: `./docs/` (create if needed)
   - **System Files**: `./tmp/` (create if needed)
   - **Agent Artifacts**: `./.claude-temp/` (create if needed)

3. **Fallback Chain**: `./docs/` → `./reports/` → `./tmp/` → `./` (current directory)

### 🏷️ FILE NAMING CONVENTIONS

**User Reports** (descriptive, date-stamped):
```
project-analysis-2024-01-15.md
security-audit-report-2024-01-15.md
performance-review-2024-01-15.md
```

**System Files** (timestamped, purpose-prefixed):
```
claude-context-20240115-143022.md
claude-test-results-20240115-144530.md
claude-workflow-state-20240115-145000.md
```

**Agent Coordination** (agent-specific, task-oriented):
```
qa-engineer-test-strategy-20240115-150000.md
technical-writer-docs-draft-20240115-151000.md
multi-agent-handoff-20240115-152000.md
```

**Conflict Resolution**: Append `-{n}` for duplicates (e.g., `report-2024-01-15-2.md`)

### 🤝 AGENT INTEGRATION PROTOCOLS

**Coordination Patterns:**
- **User-Facing Reports** → Trigger `coordination/documentation-handoff` to technical-writer for review
- **New Documentation** → Trigger `coordination/version-control-coordination` with git-helper for tracking
- **Multi-Agent Artifacts** → Use `./.claude-temp/` for workflow handoffs between agents
- **Long-Running Tasks** → Create progress files for context preservation across sessions

### 💬 USER COMMUNICATION STANDARDS

**File Creation Notifications:**
```
✅ Report created: ./docs/security-analysis-2024-01-15.md
✅ Analysis saved: ./tmp/claude-context-20240115-143022.md for reference
✅ Multi-agent workflow artifacts: ./.claude-temp/ (3 files)
✅ Documentation draft: ./docs/api-guide-2024-01-15.md (ready for technical-writer review)
```

### 🛠️ ERROR HANDLING & FALLBACKS

**Permission Issues:**
- Try alternative directories in fallback chain
- If all directories fail → display in terminal with warning message
- Suggest `mkdir docs` or permission fixes to user

**Git Integration Conflicts:**
- Check if target directory is gitignored
- For user reports → prefer tracked directories
- For system files → prefer gitignored or temporary directories
- Coordinate with git-helper for appropriate placement

### 📋 IMPLEMENTATION EXAMPLES

**Example 1 - User Report Request:**
```
User: "Give me a security analysis report of this codebase"
→ CREATE: ./docs/security-analysis-2024-01-15.md
→ NOTIFY: "✅ Security analysis report: ./docs/security-analysis-2024-01-15.md"
→ COORDINATE: Trigger documentation-handoff to technical-writer
```

**Example 2 - System Context Preservation:**
```
Multi-agent workflow with long analysis
→ CREATE: ./.claude-temp/context-preservation-20240115-143022.md
→ NOTIFY: "✅ Workflow context saved: ./.claude-temp/ for session continuity"
→ NO COORDINATION: Internal system file
```

**Example 3 - Quick Answer:**
```
User: "How do I install this package?"
→ TERMINAL: Display pip install command directly
→ NO FILE: Simple, immediate answer doesn't warrant persistence
```

### 🎯 QUALITY GATES

**Before File Creation:**
- Verify content substance and structure warrant file creation
- Check directory permissions and available space
- Ensure appropriate naming convention for content type
- Confirm integration needs (agent coordination, git tracking)

**After File Creation:**
- Provide clear file location with absolute path
- Trigger appropriate coordination workflows (documentation-handoff, version-control)
- Log file creation for session context and debugging
- Verify file was created successfully with expected content

---

**ENFORCEMENT TARGET**: 90% appropriate file creation decisions with seamless directory resolution and clear user communication.

# Claude Agent Ecosystem Coordination Guide

This document serves as the definitive guide for understanding and coordinating the specialized agent ecosystem within Claude Code. It provides comprehensive information about all available agents, their coordination patterns, and how to effectively leverage the multi-tier system for optimal cost and performance.

## Table of Contents
1. [Available Specialized Agents](#available-specialized-agents)
2. [Agent Coordination Patterns](#agent-coordination-patterns)
3. [Agent Tier Selection Guide](#agent-tier-selection-guide)
4. [Agent Usage Examples](#agent-usage-examples)
5. [Cost Optimization Strategy](#cost-optimization-strategy)
6. [Safety and Branch Management](#safety-and-branch-management)
7. [Escalation Protocols](#escalation-protocols)

---

## Available Specialized Agents

The agent ecosystem consists of **28 specialized agents** organized into three performance tiers based on complexity and cost requirements, enhanced with hybrid trait coordination.

### Tier 1: Efficiency Agents (Haiku - Fast & Cost-Effective)

**git-helper** `model: haiku`
- Version control operations and GitHub CLI workflows
- Branch management, commit formatting, and PR creation
- Proactive on: `.git` directories, GitHub operations

**technical-writer** `model: haiku`  
- API documentation, user guides, and developer tutorials
- Documentation generation after development completion
- Proactive on: Documentation requests, API changes


### Tier 2: Specialist Agents (Sonnet - Balanced Performance)

#### Core Development Agents
**ai-engineer** `model: sonnet`
- ML/AI development with PyTorch, transformers, and data science
- Model training, deployment, and MLOps workflows
- Proactive on: Python ML files, model training scripts, Jupyter notebooks

**python-engineer** `model: sonnet`
- Web frameworks (Django, FastAPI), data processing, general Python development
- Backend APIs, automation scripts, and Python applications
- Proactive on: Python files, requirements.txt, Flask/Django projects

**java-engineer** `model: sonnet`
- Spring Boot/Framework development and JUnit/Mockito testing
- Enterprise Java applications and microservices
- Proactive on: Java files, Maven/Gradle configs, Spring projects

**data-engineer** `model: sonnet`
- Data pipelines, ETL processes, and streaming systems
- Apache Spark, Airflow, and data warehouse operations
- Proactive on: Data pipeline configs, SQL files, streaming setups

**blockchain-engineer** `model: sonnet`
- Smart contracts, DeFi protocols, and Web3 development
- Solidity, Web3.js, and blockchain integrations
- Proactive on: Solidity files, Web3 projects, DeFi protocols

**mobile-engineer** `model: sonnet`
- iOS (Swift/SwiftUI), Android (Kotlin/Jetpack Compose), React Native, Flutter
- Mobile architecture patterns, app store optimization, offline-first design
- Proactive on: Mobile project files, device-specific optimizations, app deployment

**frontend-engineer** `model: sonnet`
- React, Vue, Angular, and modern JavaScript/TypeScript development
- UI components, state management, and progressive web applications
- Proactive on: package.json, JSX/TSX files, frontend frameworks

**devops-engineer** `model: sonnet`
- Kubernetes, Docker, CI/CD pipelines, and infrastructure as code
- Container orchestration, automation, and cloud deployments
- Proactive on: Dockerfiles, K8s configs, CI/CD pipelines

**security-engineer** `model: sonnet`
- Application security, vulnerability assessments, and secure coding
- Security audits, penetration testing, and compliance
- Proactive on: Security configs, auth systems, vulnerability reports

**database-engineer** `model: sonnet`
- Database design, optimization, and data architecture
- SQL/NoSQL databases, performance tuning, and migrations
- Proactive on: Database schemas, SQL files, migration scripts

#### Research & Strategy Agents
**ai-researcher** `model: sonnet`
- Literature review, methodology guidance, and research planning
- Academic paper analysis and experimental design
- Proactive on: Research requests, methodology questions

**business-analyst** `model: sonnet`
- Market research, competitive analysis, and business intelligence
- ROI optimization and product development strategy
- Proactive on: Market research, business intelligence, ROI analysis

**product-manager** `model: sonnet`
- Agile methodology, user story creation, and product requirements
- Feature planning and stakeholder coordination
- Proactive on: Product planning requests, user story needs

**quant-analyst** `model: sonnet`
- Financial metrics, market data analysis, and quantitative modeling
- Trading algorithms and risk assessment
- Proactive on: Financial data, trading strategies, risk models

#### Quality & Enhancement Agents

**performance-engineer** `model: sonnet`
- Application performance monitoring, load testing, and scalability planning
- Cost optimization and resource rightsizing for high-performance systems
- Proactive on: Performance testing, optimization, monitoring, scalability

**qa-engineer** `model: sonnet`
- Test automation across multiple languages and frameworks
- Quality assurance workflows and testing strategies
- Proactive on: Test files, quality assurance requests

**ui-ux-designer** `model: sonnet`
- Interface optimization, accessibility, design systems, and conversion optimization
- User research and usability testing for digital products
- Proactive on: UI design, user experience, accessibility, design systems

**prompt-engineer** `model: sonnet`
- LLM integration, prompt optimization, and AI workflow design
- API integration patterns, model selection, and cost optimization
- Proactive on: LLM configs, prompt templates, AI integration projects

**systems-engineer** `model: sonnet`
- Low-level programming (C/C++/Rust), embedded systems, kernel programming
- Real-time systems, hardware-software interfaces, performance optimization
- Proactive on: Systems programming, embedded projects, performance-critical code

**platform-engineer** `model: sonnet`
- Internal developer tooling, platform-as-a-service development, developer experience
- Kubernetes operators, CI/CD platforms, self-service infrastructure
- Proactive on: Platform tooling, developer productivity, internal tools

**site-reliability-engineer** `model: sonnet`
- Production system reliability, observability, incident response, chaos engineering
- SLO/SLI management, monitoring systems, reliability automation
- Proactive on: Production monitoring, reliability requirements, incident procedures

### Tier 3: Senior Agents (Opus - Advanced & Strategic)

**sr-architect** `model: opus`
- System design, technical escalation resolution, and architectural decisions
- Cross-domain technical guidance and conflict resolution
- Escalation target: After 3 failed attempts by development agents

**sr-ai-researcher** `model: opus`
- Advanced research with multi-domain synthesis and complex methodology
- Senior-level research guidance and academic leadership
- Escalation target: For complex research questions

**sr-quant-analyst** `model: opus`
- Advanced quantitative modeling, risk management, and regulatory compliance
- Complex financial engineering and institutional-grade analysis
- Escalation target: For sophisticated financial modeling

**integration-architect** `model: opus`
- Third-party API strategy, enterprise integration patterns, and legacy system modernization
- Vendor evaluation and microservices communication patterns
- Proactive on: API integration, enterprise integration, legacy modernization

**subagent-generator** `model: opus`
- Meta-level agent system design and coordination protocol development
- Agent ecosystem optimization and capability gap analysis
- Proactive on: Agent system design requests, ecosystem improvements

## Agent Coordination Patterns

Agents follow a hierarchical coordination model with clear handoff protocols and escalation chains:

### Primary Coordination Flows

**Development Workflow Pattern:**
1. **Feature Development**: Specialist agents (python-engineer, frontend-engineer, etc.) implement features with language-specific unit testing
2. **Integration & Strategy**: qa-engineer provides test strategy, integration testing, and cross-cutting quality concerns
3. **Documentation**: technical-writer creates user guides and API docs
4. **Version Control**: git-helper manages branches, merges, and releases

**AI/ML Pipeline Pattern:**
1. **Research Phase**: ai-researcher provides methodology and literature review
2. **Implementation**: ai-engineer builds models with data-engineer for pipelines
3. **Integration**: python-engineer handles serving infrastructure
4. **Optimization**: performance-engineer monitors and optimizes systems

**Cross-Platform Coordination:**
- **mobile-engineer** coordinates with backend teams for API integration
- **frontend-engineer** and **mobile-engineer** align on design systems
- **security-engineer** reviews all authentication and data protection
- **devops-engineer** manages deployment across web and mobile platforms

## Agent Usage Examples

### Example 1: Full-Stack Web Application Development

**Scenario**: Building a modern e-commerce platform with React frontend, Python backend, and PostgreSQL database.

**Agent Coordination Flow:**
```
1. frontend-engineer: React components and state management
2. python-engineer: FastAPI backend with authentication  
3. database-engineer: PostgreSQL schema design and optimization
4. security-engineer: Authentication security and data protection
5. devops-engineer: Docker containerization and deployment
6. qa-engineer: Integration testing strategy and cross-stack validation
7. technical-writer: API documentation and user guides
8. git-helper: Branch management and PR workflows
```

**Cost Optimization**: 
- 7 Sonnet agents + 1 Haiku agent
- No Opus escalation needed for standard development
- Total cost: ~8-10x Haiku baseline

### Example 2: Machine Learning Research Project

**Scenario**: Developing a new transformer model for financial sentiment analysis.

**Agent Coordination Flow:**
```
1. ai-researcher: Literature review and methodology design
2. data-engineer: Financial data pipeline and preprocessing
3. ai-engineer: Model architecture and training implementation
4. quant-analyst: Financial metrics integration and validation
5. python-engineer: Model serving infrastructure
6. qa-engineer: ML testing strategy and validation pipeline design
7. technical-writer: Model documentation and API guides
```

**Potential Escalation**:
- If model performance issues persist → **sr-ai-researcher**
- If financial modeling becomes complex → **sr-quant-analyst**

**Cost Optimization**:
- 6 Sonnet agents standard flow
- Opus escalation only if needed
- Total cost: ~6-8x Haiku baseline (12-16x if escalated)

### Example 3: Blockchain DeFi Protocol

**Scenario**: Creating a decentralized lending protocol with smart contracts and web interface.

**Agent Coordination Flow:**
```
1. blockchain-engineer: Smart contract development and testing
2. security-engineer: Security audit and vulnerability assessment
3. frontend-engineer: DApp interface with Web3 integration
4. quant-analyst: Risk modeling and tokenomics
5. qa-engineer: Comprehensive testing including security tests
6. devops-engineer: Deployment infrastructure and monitoring
7. technical-writer: Protocol documentation and user guides
```

**Cost Optimization**:
- 7 Sonnet agents for comprehensive development
- High-quality output without Opus escalation
- Total cost: ~7-9x Haiku baseline

### Example 4: Enterprise System Architecture

**Scenario**: Designing microservices architecture for enterprise application modernization.

**Direct Opus Engagement:**
```
1. sr-architect: System architecture design and technology selection
2. Multiple Sonnet agents: Implementation across services
3. qa-engineer: Integration testing strategy
4. devops-engineer: Orchestration and deployment
5. technical-writer: Architecture documentation
```

**Cost Optimization**:
- Strategic Opus use for architecture decisions
- Sonnet agents for implementation
- Total cost: ~1 Opus + 4-5 Sonnet = ~3-4x Haiku baseline

### Example 5: Mobile Application Development

**Scenario**: Building a cross-platform mobile app with React Native, backend API, and cloud deployment.

**Agent Coordination Flow:**
```
1. mobile-engineer: React Native development and platform-specific optimizations
2. python-engineer: FastAPI backend with mobile-optimized endpoints
3. database-engineer: Mobile-friendly data synchronization and offline storage
4. security-engineer: Mobile authentication and data security
5. devops-engineer: App store deployment and backend infrastructure
6. qa-engineer: Cross-platform testing and performance validation
7. technical-writer: Mobile app documentation and API guides
```

**Cost Optimization**:
- 7 Sonnet agents for comprehensive mobile development
- Focus on mobile-first performance and offline capabilities
- Total cost: ~7-9x Haiku baseline

