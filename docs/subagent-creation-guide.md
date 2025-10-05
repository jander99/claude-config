# Claude Code Subagent Creation Guide

**Version:** 1.0
**Last Updated:** 2025-10-05

## Overview

This guide provides a comprehensive walkthrough for hand-creating Claude Code subagents using YAML definition files. Learn how to design specialized AI assistants that can automatically detect and respond to specific technical tasks and conversations.

## Table of Contents

1. [YAML Agent Schema Reference](#yaml-agent-schema-reference)
2. [Step-by-Step Creation Process](#step-by-step-creation-process)
3. [Field-by-Field Guide](#field-by-field-guide)
4. [Complete Example Agents](#complete-example-agents)
5. [Testing and Validation](#testing-and-validation)
6. [Best Practices](#best-practices)

## YAML Agent Schema Reference

### Required Fields

Every Claude Code subagent YAML must include these critical fields:

```yaml
name: agent-name                    # Unique, kebab-case identifier
display_name: "Agent Name"          # Human-readable name
model: sonnet|opus|haiku            # Claude model tier
description: Brief description      # One-sentence agent summary

core_responsibilities:              # REQUIRED: At least 1 responsibility
  - Primary responsibility

expertise:                          # REQUIRED: At least 1 expertise area
  - "Expertise area"
```

### Critical Activation Fields

```yaml
when_to_use: |                      # Activation summary
  **AUTOMATIC ACTIVATION when user requests:**
  - Specific use case 1
  - Any conversation involving "keyword1", "keyword2"

proactive_triggers:
  user_intent_patterns:
    keywords:                       # Words/phrases that trigger this agent
      - "action phrase"
      - "technical term"

    task_types:                     # Task categories
      - "Task type description"

    problem_domains:                # Problem areas solved
      - "Problem domain"

  file_patterns:                    # Technical file triggers
    - "*.ext"

  project_indicators:               # Dependency/framework triggers
    - package-name
```

## Step-by-Step Creation Process

### Step 1: Define Agent Purpose and Scope

**Key Questions:**
1. What is the agent's primary role?
2. What problems does it solve?
3. What triggers its activation?
4. How does it differ from existing agents?

**Example Description:**
```yaml
description: Expert Python developer specializing in web frameworks (Django, FastAPI, Flask), data processing (pandas, numpy, scipy), automation scripting, testing frameworks (pytest, unittest), and general Python development with modern best practices.
```

### Step 2: Create Intent-Based Triggers

#### Keywords Strategy

**How to choose keywords:**
- Think: "What would a user type to get help?"
- Include **action phrases** and **technical terms**
- Cover both **direct** and **implicit** triggers

**Example (AI Engineer):**
```yaml
keywords:
  # Direct keywords
  - "train a model"
  - "implement neural network"
  - "fine-tune transformer"

  # Implicit keywords
  - "overfitting"
  - "model not converging"
  - "accuracy too low"
```

#### Task Types and Problem Domains

**Task Types:** Describe categories of work
- Use active voice
- Be specific but not too narrow

```yaml
task_types:
  - "Model architecture design and implementation"
  - "Training loop development and optimization"
```

**Problem Domains:** List types of problems solved
- Consider application areas
- Think about industries or use cases

```yaml
problem_domains:
  - "Computer vision classification tasks"
  - "Natural language processing"
```

### Step 3: Add Context Priming

Set the agent's mindset and thought patterns:

```yaml
context_priming: |
  You are a senior [role] with expertise in [domain]. Your mindset:
  - "How do I [primary concern]?"
  - "What's the best approach for [key decision]?"

  You think in terms of: [concepts], [patterns], [priorities].
```

## Example Agents

### AI Engineer Example

```yaml
name: ai-engineer
display_name: AI Engineer
model: sonnet
description: Expert AI/ML developer specializing in PyTorch, transformers, and data science with production-ready model deployment capabilities.

when_to_use: |
  **AUTOMATIC ACTIVATION when user requests:**
  - Building, training, or fine-tuning machine learning models
  - Implementing neural networks or deep learning architectures
  - Any conversation involving "model", "training", or "AI"

proactive_triggers:
  user_intent_patterns:
    keywords:
      - "train a model"
      - "implement neural network"
      - "optimize hyperparameters"
      - "overfitting"

    task_types:
      - "Model architecture design"
      - "Training loop optimization"

    problem_domains:
      - "Computer vision tasks"
      - "Natural language processing"

  file_patterns:
    - '*.py'
    - '*.ipynb'
    - '*.pt'

  project_indicators:
    - torch
    - pytorch
    - transformers
```

### Git Helper Example

```yaml
name: git-helper
display_name: Git Helper
model: haiku
description: Expert Git and version control specialist with automated workflow optimization.

when_to_use: |
  **AUTOMATIC ACTIVATION when user requests:**
  - Creating, managing, or merging Git branches
  - Resolving merge conflicts
  - Any conversation involving "git", "branch", or "commit"

proactive_triggers:
  user_intent_patterns:
    keywords:
      - "create a branch"
      - "merge this branch"
      - "resolve conflict"

    task_types:
      - "Branch creation and management"
      - "Merge conflict resolution"

    problem_domains:
      - "Team collaboration workflows"
      - "CI/CD pipeline integration"

  file_patterns:
    - ".git/**/*"
    - ".gitignore"

  project_indicators:
    - git
    - gh
```

## Testing and Validation

### Pre-Build Validation

```bash
# Validate YAML syntax
make validate

# Common validation checks:
# - Required fields present
# - Valid model type
# - No duplicate agent names
```

### Runtime Testing

1. **Start Claude Code** in a project
2. **Type trigger phrases** from keywords list
3. **Verify agent activation**

**Test Cases:**
```
Test 1: Direct keyword match
User: "Help me train a model for image classification"
Expected: ai-engineer activates

Test 2: Implicit trigger
User: "My training loss isn't decreasing"
Expected: ai-engineer activates
```

## Best Practices

### Do's
- Start with intent triggers first
- Use clear, specific keywords
- Include problem description keywords
- Balance specificity and coverage

### Don'ts
- Don't copy-paste without customization
- Don't skip `when_to_use`
- Don't use only technical jargon
- Don't create overlapping agents

## Quick Checklist

- [ ] Unique `name` in kebab-case
- [ ] Clear `display_name`
- [ ] Appropriate `model` tier
- [ ] One-sentence `description`
- [ ] Comprehensive `when_to_use`
- [ ] 10-25 `keywords`
- [ ] 5-10 `task_types`
- [ ] 4-8 `problem_domains`
- [ ] YAML validation passes
- [ ] Build generates markdown successfully
- [ ] Tested with conversational prompts

## Troubleshooting

### Agent Not Activating
1. Check `when_to_use` clarity
2. Verify `keywords` match user language
3. Review `task_types` specificity
4. Check file patterns
5. Look for overlapping agents

**Happy subagent creation!**