# Version Control Coordination Trait

## Description
Standardized coordination pattern for git-helper integration ensuring proper version control operations, branch management, and PR workflows. This trait provides consistent git operations across all development agents.

## Content

### Git Helper Coordination

**When to coordinate:**
- For all git operations beyond basic status checks
- When creating branches, commits, or pull requests
- For complex merge operations or conflict resolution
- When setting up git hooks or repository configuration

**Coordination Scope:**
- Branch management and feature branch creation
- Commit formatting with conventional commit messages
- Pull request preparation and validation
- Git hooks setup for automated testing
- Repository configuration and best practices

**Boundary Definition:**
- Development agents handle basic git status and branch verification
- git-helper manages all complex git operations
- git-helper coordinates PR creation and merge strategies
- git-helper handles repository setup and configuration

### Coordination Pattern

```yaml
git_helper_coordination:
  basic_operations_self_managed:
    - git_status_checks
    - branch_verification
    - simple_git_log_viewing
    - working_directory_status

  coordinate_with_git_helper:
    - branch_creation_and_switching
    - commit_creation_and_formatting
    - pull_request_preparation
    - merge_operations
    - repository_configuration
    - git_hooks_setup
    - conflict_resolution

  handoff_context:
    - current_branch_status
    - modified_files_list
    - commit_message_context
    - pr_description_requirements
    - target_branch_information
```

### Branch Management Protocol

**Self-Managed Branch Operations:**
```bash
# Check current branch status (agents handle directly)
git status
git branch --show-current

# Verify working directory state
git diff --name-only
git log --oneline -n 5
```

**Coordinate with git-helper:**
```yaml
branch_operations:
  create_feature_branch:
    context: "Feature description and naming context"
    target: "Base branch for new feature"

  commit_changes:
    context: "Changes made and commit message guidance"
    files: "List of modified files"

  create_pull_request:
    context: "PR description and review requirements"
    changes: "Summary of modifications"
```

### Handoff Message Template

```
**Git Helper Coordination Request**

**Operation Type:** [Branch Creation/Commit/Pull Request/Repository Setup]

**Current State:**
- Branch: [current branch name]
- Modified files: [list of changed files]
- Status: [clean/dirty working directory]

**Request Details:**
- [Specific git operation needed]
- [Context for commit messages or branch names]
- [Target branch or merge requirements]

**Additional Context:**
- [Feature description or change summary]
- [Any special requirements or constraints]
```

### Integration with Development Workflow

**Pre-Development:**
1. Verify branch status (self-managed)
2. If on protected branch, coordinate with git-helper for feature branch creation

**During Development:**
1. Continue using basic git status checks (self-managed)
2. Coordinate with git-helper for any branch switching needs

**Post-Development:**
1. Coordinate with git-helper for commit creation
2. Coordinate with git-helper for PR preparation and submission

## Usage Notes

- **Which agents should use this trait**: ALL development agents (python-engineer, frontend-engineer, devops-engineer, security-engineer, ai-engineer, etc.)
- **Customization guidance**: Each agent provides domain-specific context for commits and PRs (e.g., security implications for security-engineer, performance impact for performance-engineer)
- **Compatibility requirements**: Must maintain clear boundaries between self-managed and coordinated git operations

## Implementation Priority
**HIGH** - This trait affects 20+ development agents and provides consistent version control practices