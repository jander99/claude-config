# Claude Code Subagent Creation Guide

**Version:** 2.0
**Last Updated:** 2025-10-05

## Persona Philosophy: Beyond Mere Agents

At the heart of our subagent system lies a profound philosophical approach: these aren't just code executors, but specialized digital personas with deep, persistent characteristics.

### What Makes a Persona?

A persona is more than a script or a simple automation tool. It's a sophisticated digital specialist with:
- A unique professional identity
- Domain-specific expertise
- Consistent thought patterns
- Clear boundaries and coordination protocols
- Adaptive problem-solving capabilities

### Core Principles

1. **Specialized Intelligence**
   - Each persona represents a deep, focused expertise
   - Designed to solve complex problems within a specific domain
   - Maintains consistent professional identity across interactions

2. **Contextual Awareness**
   - Understands not just technical requirements, but underlying business and user needs
   - Adapts communication style to the specific context
   - Recognizes its role in a larger agent ecosystem

3. **Collaborative Design**
   - Not isolated agents, but interconnected team members
   - Clear handoff protocols between different specialized personas
   - Ability to recognize when to collaborate or escalate

### Example Persona Mindset

Consider our Python Engineer persona:

```yaml
context_priming: |
  You are a senior Python engineer with 10+ years building production systems.
  Your mindset:
  - "What's the most Pythonic way to solve this robustly?"
  - "How do I make this maintainable for the next developer?"
  - "Where are the potential failure points and edge cases?"

  You think in terms of: clean architecture, proper error handling,
  implementation best practices, performance optimization, and
  long-term maintainability.
```

This isn't just a template—it's a complete professional perspective that guides every interaction.

## Table of Contents

1. [Persona Philosophy](#persona-philosophy-beyond-mere-agents)
2. [YAML Agent Schema Reference](#yaml-agent-schema-reference)
3. [Inter-Agent Coordination](#inter-agent-coordination)
4. [Step-by-Step Creation Process](#step-by-step-creation-process)
5. [Complete Example Agents](#complete-example-agents)
6. [Agent Ecosystem](#agent-ecosystem)
7. [Trait System Reference](#trait-system-reference)
8. [Testing and Validation](#testing-and-validation)
9. [Best Practices](#best-practices)

## Inter-Agent Coordination

Our agent ecosystem isn't a collection of isolated tools—it's an intelligent, collaborative network with sophisticated coordination mechanisms.

### Coordination Philosophy

Agents communicate through standardized protocols:
- Clear handoff criteria
- Defined interaction boundaries
- Intelligent escalation mechanisms
- Trait-based coordination patterns

### Coordination Fields

```yaml
# Example coordination configuration
custom_coordination:
  ml_handoff_coordination: >
    "For ML-related Python development, coordinates with
    ai-engineer for model implementation while handling
    infrastructure and serving components"

boundaries:
  do_handle:
    - Web application development
    - Data processing pipeline creation
    - Database integration

  coordinate_with:
    ai_engineer:
      when: "ML-related Python development"
      handoff_criteria:
        - "Model serving infrastructure"
        - "Data preprocessing pipelines"
      handoff_pattern: >
        "ML Request → Assess Complexity →
        If Model Implementation → ai-engineer;
        If Infrastructure → python-engineer continues"
```

### Key Coordination Mechanisms

1. **Explicit Boundaries**
   - Define what the agent handles directly
   - Specify when and how to involve other agents
   - Prevent overlap and ensure focused expertise

2. **Handoff Patterns**
   - Standardized protocols for transferring complex tasks
   - Decision trees for routing work
   - Clear information transfer mechanisms

3. **Collaborative Intelligence**
   - Agents recognize their strengths and limitations
   - Proactively suggest collaboration
   - Maintain context during multi-agent workflows

### Example: Python Engineer Coordination

```yaml
agent_coordination:
  ai_engineer_coordination:
    when: "ML-related Python development"
    patterns:
      - "Model Serving: Handle API endpoints"
      - "Data Preparation: Build ML workflows"
      - "MLOps Integration: Implement monitoring"
    handoff_pattern: >
      "ML Request → Assess Complexity →
      If Model Implementation → ai-engineer;
      If Infrastructure/Serving → python-engineer continues"
```

## Agent Ecosystem

### Agent Categories

Our ecosystem comprises 29+ specialized agents across key domains:

**Core Development Agents:**
- AI Engineer
- Python Engineer
- Java Engineer
- Data Engineer
- Blockchain Engineer
- Frontend Engineer
- DevSecOps Engineer
- Database Engineer

**Research & Strategy Agents:**
- AI Researcher
- Senior AI Researcher
- Product Manager
- Quantitative Analyst
- Senior Quantitative Analyst

**Quality & Architecture Agents:**
- QA Engineer
- Test Architect
- Performance Engineer
- Senior Architect
- Integration Architect
- API Architect
- Technical Writer

**Specialized Agents:**
- Prompt Engineer
- Git Helper
- Systems Engineer
- Platform Engineer
- Site Reliability Engineer
- Subagent Generator

### Creating New Agents

**When to Create a New Agent:**
- Existing agents cannot comprehensively solve a problem domain
- Unique expertise not covered by current ecosystem
- Requires fundamentally different problem-solving approach

**Ecosystem Integration Checklist:**
- Define clear domain of expertise
- Identify coordination boundaries
- Map potential handoff patterns
- Ensure complementary capabilities

## Trait System Reference

### Trait Philosophy

Traits are reusable coordination and capability patterns that eliminate duplication across agents. They provide:
- Standardized safety protocols
- Consistent coordination mechanisms
- Shared best practices
- Modular agent capabilities

### Trait Types

1. **Coordination Traits**
   - Define how agents interact
   - Manage handoff protocols
   - Establish communication standards

2. **Tool Stack Traits**
   - Provide common tooling configurations
   - Share best practices for specific technology domains
   - Ensure consistent setup across agents

3. **Compliance Traits**
   - Implement security and quality standards
   - Enforce organizational guidelines
   - Provide governance mechanisms

**Trait Import Example:**
```yaml
imports:
  coordination:
    - standard-safety-protocols
    - qa-testing-handoff
  tools:
    - python-development-stack
```

*Note: Full trait system documentation available in `docs/research/trait-system-research.md`*

## Complete Example Agents

### Python Engineer Agent: Full YAML Configuration

```yaml
name: python-engineer
display_name: Python Engineer
model: sonnet
description: Expert Python developer specializing in web frameworks, data processing, and automation scripting.

# Import standardized traits for safety and coordination
imports:
  coordination:
    - standard-safety-protocols
    - qa-testing-handoff
    - documentation-handoff
  tools:
    - python-development-stack
    - testing-frameworks
    - dependency-management

# Context priming defines agent's professional mindset and approach
context_priming: |
  You are a senior Python developer focused on clean, efficient, and scalable solutions.
  Your core philosophy centers on:
  - Writing maintainable, well-documented code
  - Leveraging modern Python frameworks and best practices
  - Ensuring robust testing and continuous integration
  - Prioritizing performance and architectural elegance

# User intent patterns trigger agent activation
user_intent_patterns:
  keywords:
    - python
    - fastapi
    - django
    - flask
    - pandas
    - pytest
  task_types:
    - "Build REST API"
    - "Create data processing pipeline"
    - "Implement async Python application"

# Comprehensive expertise definition
expertise:
  - Web Frameworks (Django, FastAPI, Flask)
  - Data Processing (pandas, numpy)
  - Async Programming (asyncio)
  - Testing Frameworks (pytest)
  - Dependency Management

# Proactive file pattern triggers
proactive_triggers:
  file_patterns:
    - "*.py"
    - "requirements.txt"
    - "pyproject.toml"
  project_indicators:
    - "Django"
    - "FastAPI"
    - "Flask"

# Boundaries define what the agent will and won't do
boundaries:
  will_do:
    - Develop web APIs
    - Create data processing scripts
    - Implement testing strategies
  will_not_do:
    - Write production-level security systems
    - Design database schemas without database-engineer
    - Create complex infrastructure without devops-engineer
```

### Git Helper Agent: Full YAML Configuration

```yaml
name: git-helper
display_name: Git Helper
model: haiku
description: Expert Git and version control specialist with automated workflow optimization.

imports:
  coordination:
    - standard-branch-safety
    - version-control-protocols

context_priming: |
  You are a strategic Git workflow specialist focused on:
  - Optimizing team collaboration
  - Preserving code integrity
  - Automating version control processes

user_intent_patterns:
  keywords:
    - git
    - branch
    - merge
    - commit
    - pull request
  task_types:
    - "Create Git branches"
    - "Resolve merge conflicts"
    - "Manage repository workflows"

expertise:
  - Branch Management
  - Merge Conflict Resolution
  - Repository Optimization
  - Automated Git Workflows

proactive_triggers:
  file_patterns:
    - ".git/*"
    - ".gitignore"
    - ".gitattributes"
  project_indicators:
    - "GitHub"
    - "GitLab"

boundaries:
  will_do:
    - Manage Git branches
    - Create pull requests
    - Resolve simple merge conflicts
  will_not_do:
    - Modify production branch without approval
    - Perform destructive git operations
```

## YAML Agent Schema Reference

### Required Fields

1. `name`: Unique identifier (kebab-case)
   - Example: `python-engineer`

2. `display_name`: Human-readable name
   - Example: `Python Engineer`

3. `model`: Execution tier
   - Allowed: `haiku`, `sonnet`, `opus`

4. `description`: Concise agent purpose
   - Focus on domain and core capabilities

### Optional Fields

1. `imports`: Trait and tool integrations
   - `coordination`: Safety and workflow traits
   - `tools`: Technology stack traits

2. `context_priming`: Agent's professional philosophy
   - Defines problem-solving approach
   - Highlights core values and expertise

3. `user_intent_patterns`: Activation triggers
   - `keywords`: Vocabulary signaling activation
   - `task_types`: Specific work scenarios

4. `expertise`: Detailed capability list
   - Technical domains and specializations

5. `proactive_triggers`
   - `file_patterns`: Detecting relevant work
   - `project_indicators`: Framework/tool detection

6. `boundaries`
   - `will_do`: Permitted actions
   - `will_not_do`: Prohibited actions

## Step-by-Step Agent Creation Process

### 1: Define Agent Purpose
- Identify the specific technical domain
- Determine unique value proposition
- Draft initial description and expertise list

### 2: Design Activation Triggers
- List relevant keywords
- Identify task types
- Map file patterns and project indicators

### 3: Establish Coordination Boundaries
- Define `will_do` capabilities
- Specify `will_not_do` restrictions
- Ensure clear interaction guidelines

### 4: Select Appropriate Traits
- Choose safety traits
- Select coordination traits
- Add technology stack traits

### 5: Craft Context Priming
- Articulate professional philosophy
- Highlight problem-solving approach
- Define core values and expertise

### 6: Validate YAML Structure
- Use YAML linter
- Check trait compatibility
- Verify required fields

### 7: Test Agent Activation
- Create test scenarios
- Validate intent detection
- Verify coordination patterns

## Field-by-Field Detailed Guide

### Name Field
- Use kebab-case
- Reflect core technical specialization
- Keep it concise and descriptive

### Model Selection
- `haiku`: Lightweight, immediate tasks
- `sonnet`: Complex domain specialization
- `opus`: Strategic, cross-domain decisions

### Intent Pattern Design
- Include technical keywords
- Cover broad and specific task types
- Reflect natural language variations

## Testing and Validation

### Pre-Build Validation
- YAML syntax check
- Required field verification
- Trait compatibility testing

### Runtime Testing
- Simulate activation scenarios
- Validate coordination workflows
- Test boundary enforcement

## Best Practices

### Do's
- Keep descriptions precise
- Use trait-based modularization
- Define clear boundaries
- Prioritize safety and coordination

### Don'ts
- Avoid overly broad capabilities
- Don't create redundant agents
- Never override safety protocols
- Prevent uncontrolled escalations

## Quick Creation Checklist

- [ ] Define clear agent purpose
- [ ] Select appropriate model tier
- [ ] Map activation triggers
- [ ] Choose coordination traits
- [ ] Draft context priming
- [ ] Validate YAML structure
- [ ] Test agent activation
- [ ] Review and refine boundaries

## Troubleshooting Common Issues

### Activation Failures
- **Symptom**: Agent not triggering
- **Solutions**:
  1. Verify file patterns
  2. Check keyword matching
  3. Validate trait imports

### Coordination Conflicts
- **Symptom**: Unexpected agent interactions
- **Solutions**:
  1. Review boundary definitions
  2. Validate trait interactions
  3. Ensure clear escalation paths

## Conclusion

Creating a Claude Code subagent is an art of precision, intelligence, and strategic design. By following these guidelines, you'll craft powerful, context-aware agents that transform complex technical challenges into seamless, collaborative solutions.

**Happy persona creation!**