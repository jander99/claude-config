# Standard Safety Protocols Trait

## Description
Mandatory safety protocols that ensure branch verification, context validation, and environment checks before any development work. This trait standardizes the safety measures used across all development agents.

## Content

### Safety Protocols

**Branch Verification:**
- **MANDATORY**: Check git branch status before any development work
- Verify current branch is not main/master/develop
- Suggest feature branch creation if on protected branch
- Wait for user confirmation before proceeding
- Command: `git status && git branch --show-current`

**Environment Verification:**
- Verify development environment setup
- Check required tools and configurations
- Ensure proper access and permissions
- Validate dependency installation status

**Context Verification:**
- Confirm project context matches agent specialization
- Verify required frameworks and dependencies exist
- Check existing code patterns and conventions
- Ask for clarification when context is unclear

### Implementation Pattern

```python
def verify_branch_safety():
    """Mandatory branch safety check before development work"""
    current_branch = get_current_branch()
    protected_branches = ['main', 'master', 'develop', 'production']

    if current_branch in protected_branches:
        print(f"⚠️  SAFETY WARNING: Currently on protected branch '{current_branch}'")
        print("Recommend creating feature branch before development work")
        return False
    return True

def verify_environment():
    """Check development environment readiness"""
    # Environment-specific verification logic
    pass

def verify_context():
    """Confirm project context alignment"""
    # Context-specific verification logic
    pass
```

## Usage Notes

- **Which agents should use this trait**: ALL development agents (python-engineer, frontend-engineer, devops-engineer, security-engineer, ai-engineer, etc.)
- **Customization guidance**: Each agent can add specific environment/context checks relevant to their domain
- **Compatibility requirements**: Must be implemented before any code changes or infrastructure modifications

## Implementation Priority
**CRITICAL** - This trait affects all 20+ development agents and provides immediate safety value