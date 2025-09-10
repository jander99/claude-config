# CLAUDE.md

This file provides project-specific guidance to Claude Code when working with this configuration repository.

## Repository Purpose

This is a simple YAML-to-Markdown templating tool that generates Claude Code agent configurations. The system processes YAML agent definitions through Jinja2 templates to create agent markdown files, then installs them to `${HOME}/.claude/` directory. This is a focused templating tool (~500 lines total) that does one thing well: convert YAML agent specs to Claude Code configurations.

## Architecture Overview

This repository uses YAML source files and Jinja2 templates to generate agent markdown files. The system consists of:

- **YAML Agent Definitions** (`data/personas/`) - 25+ agent specifications
- **Template Engine** (`src/claude_config/composer.py`) - ~200 lines of templating logic
- **Basic CLI** (`src/claude_config/cli.py`) - ~100 lines with build, validate, install, list-agents commands
- **YAML Validation** (`src/claude_config/validator.py`) - ~115 lines of basic validation
- **Jinja2 Template** (`src/claude_config/templates/`) - Converts YAML to agent markdown

### Agent Library

The system generates 25+ specialized agents organized by role:

**Core Development:** `ai-engineer`, `python-engineer`, `java-engineer`, `data-engineer`, `blockchain-engineer`, `mobile-engineer`, `frontend-engineer`, `devops-engineer`, `security-engineer`, `database-engineer`

**Research & Strategy:** `ai-researcher`, `sr-ai-researcher`, `product-manager`, `business-analyst`, `quant-analyst`, `sr-quant-analyst`

**Quality & Architecture:** `qa-engineer`, `performance-engineer`, `sr-architect`, `integration-architect`, `technical-writer`, `ui-ux-designer`

**Specialized:** `prompt-engineer`, `git-helper`, `customer-success`, `project-coordinator`, `agent-architect`

All agents are defined in YAML format in `data/personas/` and converted to markdown via template processing.

### Build Process

The system follows a simple templating workflow:

1. **YAML Agent Definitions** - Each agent specified in `data/personas/{agent}.yaml` 
2. **Template Processing** - Jinja2 template converts YAML to agent markdown
3. **Basic Validation** - YAML syntax and structure checking
4. **Agent Generation** - Complete agent markdown files created in `dist/agents/`
5. **Installation** - Generated agents deployed to `~/.claude/agents/`


### Core Components

**CLI Commands:**
- `claude-config build` - Process YAML through templates to generate agents
- `claude-config validate` - Check YAML syntax and structure
- `claude-config install` - Deploy generated agents to ~/.claude/
- `claude-config list-agents` - List available agent definitions
- `claude-config --help` - Show usage information

**Template System:**
- Single Jinja2 template at `src/claude_config/templates/agent.md.j2`
- Converts YAML agent specifications to complete markdown
- Simple variable substitution and basic control flow

**Validation:**
- Basic YAML syntax checking
- Required field validation (name, model, description, etc.)
- Structure verification for consistent agent format

## Directory Structure

### This Repository (Development)
- `data/personas/` - YAML agent definitions (25+ files)
- `src/claude_config/cli.py` - Command-line interface (~100 lines)
- `src/claude_config/composer.py` - Template engine (~200 lines)
- `src/claude_config/validator.py` - YAML validation (~115 lines)
- `src/claude_config/templates/` - Jinja2 template for agent generation
- `tests/` - Test suite (4 files covering core functionality)
- `README.md` - Repository documentation
- `CLAUDE.md` - This project guide

### Production Directory (`${HOME}/.claude/`)
Generated and deployed from this repository:
- `agents/` - Generated agent markdown files
- `settings.json` - Claude Code configuration
- `CLAUDE.md` - Global instructions
- `[runtime directories]` - Claude Code operational files

## Simple Configuration

- **Agent Definitions**: YAML files in `data/personas/` define each agent
- **Template**: Single Jinja2 template generates agent markdown
- **Settings**: Basic `settings.json` for Claude Code preferences
- **Build & Deploy**: CLI processes YAML → markdown → installation



## Agent YAML Structure

Each agent is defined in a YAML file with this basic structure:
```yaml
name: agent-name
display_name: "Agent Name"
model: sonnet|opus|haiku
description: Brief description of agent purpose

context_priming: |
  Agent mindset and thought patterns

responsibilities:
  - Primary responsibility
  - Secondary responsibility

expertise:
  - "Technical expertise area"

proactive_triggers:
  file_patterns: ["*.ext"]
  project_indicators: ["Framework"]
```

## Working with This Repository

1. **Modify Agents**: Edit YAML files in `data/personas/` to update agent behavior
2. **Add New Agents**: Create new YAML files following the established format
3. **Build Agents**: Run `claude-config build` to process YAML through templates
4. **Validate**: Use `claude-config validate` to check YAML syntax
5. **Install**: Deploy with `claude-config install` to ~/.claude/
6. **Test**: Use `pytest tests/` to run the test suite


## Repository Standards

- All agents defined in YAML format with consistent structure
- Use specific file patterns and project indicators for activation
- Follow naming conventions (kebab-case for agent names)
- Include context priming, responsibilities, and expertise for each agent
- Validate YAML before committing changes


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

The agent ecosystem consists of **25 specialized agents** organized into three performance tiers based on complexity and cost requirements.

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

**agent-architect** `model: opus`
- Meta-level agent system design and coordination protocol development
- Agent ecosystem optimization and capability gap analysis
- Proactive on: Agent system design requests, ecosystem improvements

## Agent Coordination Patterns

Agents follow a hierarchical coordination model with clear handoff protocols and escalation chains:

### Primary Coordination Flows

**Development Workflow Pattern:**
1. **Feature Development**: Specialist agents (python-engineer, frontend-engineer, etc.) implement features
2. **Quality Gates**: qa-engineer validates functionality and performance
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
6. qa-engineer: End-to-end testing across the stack
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
6. qa-engineer: Model testing and validation pipelines
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

