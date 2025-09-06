# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a Claude Code user configuration repository that generates customized configurations for Claude Code's behavior through specialized agent definitions, settings, and project configurations. This repository builds and deploys to the user's `${HOME}/.claude/` directory. This is not a traditional software development project but rather a configuration repository that enhances Claude Code's capabilities through a build-then-deploy system.

## Architecture Overview

This repository contains a collection of specialized agent specifications for Claude Code's proactive agent system. Each agent is defined in a markdown file with specific expertise areas and coordination patterns.

### Agent Ecosystem

The agent system is organized around several specialized roles:

**Core Development Agents:**
- `ai-engineer.md` - ML/AI development with PyTorch, transformers, and data science
- `python-engineer.md` - Web frameworks, data processing, and general Python development  
- `java-engineer.md` - Spring Boot/Framework and JUnit/Mockito testing
- `data-engineer.md` - Data pipelines, ETL processes, and streaming systems
- `blockchain-engineer.md` - Smart contracts, DeFi protocols, and Web3 development
- `git-helper.md` - Version control operations and GitHub CLI workflows

**Research & Strategy:**
- `ai-researcher.md` - Literature review and methodology guidance
- `sr-ai-researcher.md` - Advanced research with multi-domain synthesis
- `product-manager.md` - Agile methodology and user story creation
- `quant-analyst.md` - Financial metrics and market data analysis
- `sr-quant-analyst.md` - Advanced quantitative modeling and risk management

**Quality & Architecture:**
- `qa-engineer.md` - Test automation across multiple languages/frameworks
- `sr-architect.md` - System design and technical escalation resolution
- `technical-writer.md` - API documentation, user guides, and developer tutorials

**Experimental & Enhancement:**
- `prompt-engineer.md` - EXPERIMENTAL prompt preprocessing and context enhancement

### Agent Coordination Patterns

Agents follow a hierarchical coordination model:

1. **Proactive Activation** - Agents auto-activate based on project detection (file patterns, dependencies)
2. **Prompt Enhancement** - prompt-engineer preprocesses vague requests to add context and clarity
3. **Branch Safety Checks** - All development agents must check branch status before work
4. **Testing Handoffs** - Development agents coordinate with qa-engineer for validation
5. **Escalation Chains** - Complex issues escalate to senior agents after 3 failed attempts
6. **Cross-Domain Coordination** - AI work flows between ai-researcher → ai-engineer → qa-engineer

### Key Integration Points

**AI/ML Workflow:**
- ai-researcher provides methodology guidance
- ai-engineer implements models with comprehensive metrics
- data-engineer builds ML data pipelines and feature stores
- python-engineer handles serving infrastructure
- qa-engineer validates across the pipeline
- technical-writer documents ML models and API usage

**Prompt Enhancement Workflow:**
- prompt-engineer analyzes vague/incomplete user requests
- Adds codebase context, error details, and routing suggestions
- Maintains transparency with bypass options for users

**Data & Blockchain Workflows:**
- data-engineer builds scalable data pipelines and ETL processes
- blockchain-engineer implements DeFi protocols and smart contracts
- Both coordinate with quant-analyst agents for financial data analysis
- Cross-integration for on-chain data analytics and traditional finance

**Documentation & Quality Assurance:**
- All development work coordinates with qa-engineer for testing
- technical-writer creates comprehensive documentation after feature completion
- sr-architect handles complex technical escalations
- Branch protection enforced through git-helper workflows

## Directory Structure

### This Repository (Development)
- `agents/` - Specialized agent definitions (.md files with YAML frontmatter)
- `docs/` - Documentation and guides  
- `data/` - Configuration generation system (planned)
- `CLAUDE.md` - Global instructions and coordination guide
- `README.md` - Repository documentation

### Production Directory (`${HOME}/.claude/`)
Generated and deployed from this repository:
- `agents/` - Specialized agent definitions
- `settings.json` - Claude Code configuration (model preferences, etc.)
- `projects/` - Project-specific configurations and contexts
- `todos/` - Task management and agent coordination state
- `ide/`, `local/`, `shell-snapshots/`, `statsig/` - Claude Code runtime directories

## Configuration

- **Model Selection**: `settings.json` controls default model preferences (`opusplan`, `sonnet`, `haiku`)
- **Agent Activation**: Agents auto-activate based on project detection patterns
- **Global Instructions**: This CLAUDE.md file provides context to all Claude Code sessions

## Agent Specifications Structure

Each agent file follows this format:
```yaml
---
name: agent-name
description: Brief description with proactive triggers
model: sonnet|opus|haiku
---
```

Followed by detailed sections on:
- Core Responsibilities
- Context Detection & Safety (branch checks, project verification)
- Technical Approach & Expertise
- Coordination Patterns with other agents
- Example Workflows
- Proactive Suggestions

## Working with This Configuration Repository

1. **Modifying Agent Behavior**: Edit agent .md files to refine coordination patterns and triggers
2. **Adding New Agents**: Create new .md files following the established YAML frontmatter pattern  
3. **Updating Global Instructions**: Modify this CLAUDE.md file to change how Claude Code behaves
4. **Configuration Changes**: Update settings.json for model preferences and global settings
5. **Version Control**: Use standard git workflows to track configuration changes

## Repository Standards

- Agent specifications use YAML frontmatter for metadata
- Coordination patterns clearly define handoff points between agents  
- Branch safety checks are mandatory for all development agents
- Testing coordination follows established patterns (3 retry attempts before escalation)
- All agents include proactive activation triggers and project detection logic


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

The agent ecosystem consists of **20 specialized agents** organized into three performance tiers based on complexity and cost requirements.

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

**product-manager** `model: sonnet`
- Agile methodology, user story creation, and product requirements
- Feature planning and stakeholder coordination
- Proactive on: Product planning requests, user story needs

**quant-analyst** `model: sonnet`
- Financial metrics, market data analysis, and quantitative modeling
- Trading algorithms and risk assessment
- Proactive on: Financial data, trading strategies, risk models

#### Quality & Enhancement Agents
**qa-engineer** `model: sonnet`
- Test automation across multiple languages and frameworks
- Quality assurance workflows and testing strategies
- Proactive on: Test files, quality assurance requests

**prompt-engineer** `model: sonnet`
- EXPERIMENTAL: Prompt preprocessing and context enhancement
- Vague request clarification and routing optimization
- Proactive on: Unclear or incomplete user requests

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

**agent-architect** `model: opus`
- Meta-level agent system design and coordination protocol development
- Agent ecosystem optimization and capability gap analysis
- Proactive on: Agent system design requests, ecosystem improvements

---

## Agent Coordination Patterns

### Hierarchical Coordination Model

The agent system follows a structured coordination approach with clear handoff points and escalation paths.

#### 1. Proactive Activation
Agents automatically activate based on project detection patterns:

```
File Pattern Detection → Agent Activation → Context Verification → Work Execution
```

**Example Detection Patterns:**
- `package.json` with React dependencies → **frontend-engineer**
- `Dockerfile` or `docker-compose.yml` → **devops-engineer**
- `.py` files with ML libraries → **ai-engineer**
- `.sol` files or Web3 configs → **blockchain-engineer**
- Database schemas or migrations → **database-engineer**

#### 2. Branch Safety Protocol
**CRITICAL**: All development agents must verify branch status before starting work:

```bash
git branch --show-current
```

If on `main`, `master`, or `develop`:
- Agent asks: "You're currently on [branch]. Should I create a feature branch?"
- Suggests appropriate branch names based on work type
- Waits for user confirmation before proceeding

#### 3. Development Workflow Coordination

```
Request → Prompt Enhancement → Development Agent → QA Testing → Documentation
```

**Standard Development Flow:**
1. **prompt-engineer** (optional): Enhances vague requests with context
2. **Development Agent**: Implements solution with branch safety checks
3. **qa-engineer**: Validates implementation with appropriate tests
4. **technical-writer**: Creates documentation for user-facing features
5. **git-helper**: Manages version control and PR creation

#### 4. Cross-Domain Integration Patterns

**Full-Stack Web Application:**
```
frontend-engineer → python-engineer → database-engineer → devops-engineer → security-engineer
    ↓
qa-engineer → technical-writer → git-helper
```

**AI/ML Pipeline:**
```
ai-researcher → ai-engineer → data-engineer → python-engineer
    ↓
qa-engineer → technical-writer
```

**Blockchain DeFi Application:**
```
blockchain-engineer → security-engineer → frontend-engineer
    ↓  
qa-engineer → technical-writer
```

#### 5. Escalation Chains

When standard approaches fail (3 retry attempts), agents escalate to senior specialists:

```
Development Agent Failures → sr-architect
Research Complexity → sr-ai-researcher  
Financial Complexity → sr-quant-analyst
```

---

## Agent Tier Selection Guide

### When to Use Each Tier

#### Tier 1 (Haiku): Quick Operations
**Use for:**
- Simple git operations and branch management
- Basic documentation generation
- Straightforward file operations
- Quick status checks and simple queries

**Cost Impact:** Lowest cost, fastest response
**Typical Tasks:** git commits, README updates, simple documentation

#### Tier 2 (Sonnet): Primary Development
**Use for:**
- All standard development work
- Feature implementation across languages
- Code review and testing
- Research and analysis tasks
- Most day-to-day development activities

**Cost Impact:** Balanced cost-performance ratio
**Typical Tasks:** Building features, writing tests, API development, data analysis

#### Tier 3 (Opus): Complex Strategy
**Use for:**
- Architectural decisions requiring deep analysis
- Complex multi-system integration problems
- Advanced research requiring synthesis
- System design and strategic planning
- Escalations after multiple failures

**Cost Impact:** Highest cost, maximum capability
**Typical Tasks:** System architecture, complex problem solving, strategic guidance

### Decision Matrix

| Task Complexity | Recommended Tier | Example Agents |
|-----------------|------------------|----------------|
| Simple/Routine | Tier 1 (Haiku) | git-helper, technical-writer |
| Standard Development | Tier 2 (Sonnet) | python-engineer, ai-engineer, qa-engineer |
| Strategic/Complex | Tier 3 (Opus) | sr-architect, sr-ai-researcher, agent-architect |

---

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

---

## Cost Optimization Strategy

### Multi-Tier Cost Management

The three-tier system provides intelligent cost optimization through appropriate agent selection:

#### Cost Multipliers (Approximate)
- **Haiku (Tier 1)**: 1x baseline cost
- **Sonnet (Tier 2)**: ~2-3x Haiku cost  
- **Opus (Tier 3)**: ~4-5x Haiku cost

#### Optimization Strategies

**1. Start with Appropriate Tier**
- Use Tier 1 for simple operations
- Default to Tier 2 for standard development
- Reserve Tier 3 for strategic decisions

**2. Escalate Only When Necessary**
- Let Tier 2 agents attempt solutions first
- Escalate to Tier 3 after 3 failed attempts
- Use escalation data to improve agent selection

**3. Batch Related Work**
- Coordinate multiple agents in parallel when possible
- Minimize context switching between tiers
- Plan work to reduce overall agent interactions

**4. Leverage Agent Specialization**
- Use the most specialized agent for each task
- Avoid using senior agents for tasks junior agents can handle
- Maintain clear agent boundaries and responsibilities

### Cost Examples by Project Type

**Small Project** (Simple CRUD app):
- 2-3 Sonnet agents + 1 Haiku agent
- Cost: ~5-7x Haiku baseline

**Medium Project** (Full-stack application):
- 5-7 Sonnet agents + 1-2 Haiku agents  
- Cost: ~11-16x Haiku baseline

**Large Project** (Enterprise system):
- 1 Opus + 8-10 Sonnet + 2 Haiku agents
- Cost: ~20-25x Haiku baseline

**Research Project** (Novel ML approach):
- 1-2 Opus + 4-6 Sonnet + 1 Haiku
- Cost: ~15-22x Haiku baseline

---

## Safety and Branch Management

### Universal Safety Protocols

All development agents follow consistent safety patterns:

#### 1. Branch Status Verification
```bash
# Required check before any development work
git branch --show-current

# If on protected branch:
# - Ask user for permission to create feature branch
# - Suggest appropriate branch name
# - Wait for confirmation
```

#### 2. Project Context Verification
- Confirm project type matches agent specialization
- Verify required dependencies and configurations exist  
- Check for existing code patterns and conventions
- Ask for clarification if project context is unclear

#### 3. MCP Tool Integration
- Use available MCP tools for current documentation
- Check for latest framework patterns and best practices
- Integrate with external tools and services appropriately
- Maintain tool usage consistency across agents

### Branch Naming Conventions

Agents suggest consistent branch naming patterns:

- **Features**: `feature/[agent-type]-[feature-name]`
  - `feature/frontend-user-dashboard`
  - `feature/api-authentication`
  - `feature/ml-sentiment-model`

- **Bug Fixes**: `fix/[agent-type]-[issue-description]`  
  - `fix/database-migration-error`
  - `fix/security-auth-vulnerability`

- **Architecture**: `architecture/[system-component]`
  - `architecture/microservices-design`
  - `architecture/data-pipeline`

---

## Escalation Protocols

### When to Escalate

#### Automatic Escalation Triggers
1. **Development Agent Failure**: After 3 failed testing attempts
2. **Complex Architecture Decisions**: Cross-domain integration problems
3. **Research Complexity**: Advanced methodology or multi-domain synthesis needed
4. **Financial Modeling**: Sophisticated quantitative analysis requirements

#### Manual Escalation Requests
Users can directly request senior agent involvement for:
- Strategic architectural decisions
- Complex problem analysis requiring deep expertise
- Cross-system integration planning
- Advanced research guidance

### Escalation Paths

```
Standard Development Issues → sr-architect
Research Complexity → sr-ai-researcher
Financial Modeling → sr-quant-analyst
Agent System Design → agent-architect
```

### Escalation Context

When escalating, agents provide:
- **Original Task**: What was the user trying to accomplish?
- **Attempts Made**: What approaches were tried and why did they fail?
- **Current State**: What is the system state and constraints?
- **Specific Questions**: What decisions or guidance is needed?

### Post-Escalation Workflow

After senior agent guidance:
1. **Implementation**: Appropriate Sonnet agents execute the solution
2. **Validation**: qa-engineer verifies the implementation
3. **Documentation**: technical-writer documents the solution
4. **Knowledge Capture**: Patterns are incorporated into agent knowledge

---

## Best Practices Summary

### For Users
1. **Let agents activate proactively** based on file patterns and project context
2. **Start with appropriate tier** - don't over-engineer simple requests
3. **Trust the escalation process** - let agents try before requesting senior help
4. **Maintain consistent branch practices** - work in feature branches
5. **Leverage agent specialization** - let each agent focus on their expertise

### For Agent Coordination
1. **Follow branch safety protocols** - always check before development work
2. **Coordinate with qa-engineer** - ensure testing validation for all features  
3. **Use appropriate escalation paths** - escalate after genuine attempts
4. **Maintain context consistency** - share relevant information between agents
5. **Document significant decisions** - ensure knowledge transfer through technical-writer

### Cost Management
1. **Default to Sonnet tier** for most development work
2. **Use Haiku tier** for simple operations and documentation
3. **Reserve Opus tier** for genuinely complex strategic decisions
4. **Batch related work** to minimize context switching costs
5. **Monitor escalation patterns** to optimize agent selection over time

---

This coordination guide provides the foundation for effective multi-agent development workflows. The 20-agent ecosystem offers comprehensive coverage of modern software development needs while maintaining cost efficiency through intelligent tier selection and coordination patterns.