# Collaboration Workflows and Team Coordination

## Overview

Effective git collaboration requires well-defined workflows that balance individual productivity with team coordination. This guide covers collaboration patterns, team coordination strategies, and workflow optimization techniques.

## Core Collaboration Models

### Centralized Workflow
**Best for**: Small teams transitioning from centralized VCS

```
Remote Repository (origin/main)
    ↑ push        ↓ pull
Developer A ←→ Developer B ←→ Developer C
```

**Workflow Steps:**
1. Clone central repository
2. Pull latest changes before starting work
3. Make changes and commit locally
4. Pull again to check for conflicts
5. Push changes to central repository

```bash
# Daily workflow
git pull origin main
# ... make changes ...
git add .
git commit -m "Add user validation feature"
git pull origin main  # Check for new changes
git push origin main
```

### Feature Branch Workflow
**Best for**: Teams practicing continuous integration

```
main (protected)
├── feature/user-auth (Alice)
├── feature/payment-system (Bob)
└── feature/admin-panel (Charlie)
```

**Collaboration Pattern:**
```bash
# Alice starts feature
git checkout main
git pull origin main
git checkout -b feature/user-auth
git push -u origin feature/user-auth

# Bob collaborates on Alice's feature
git fetch origin
git checkout feature/user-auth
git pull origin feature/user-auth
# ... make changes ...
git push origin feature/user-auth

# Alice merges completed feature
git checkout main
git pull origin main
git merge --no-ff feature/user-auth
git push origin main
git branch -d feature/user-auth
```

### Forking Workflow
**Best for**: Open source projects and external contributors

```
Upstream Repository (maintainer)
    ↑ pull request
Fork Repository (contributor)
    ↑ push        ↓ clone
Local Repository (contributor)
```

**Contributor Workflow:**
```bash
# 1. Fork repository on GitHub/GitLab
# 2. Clone your fork
git clone https://github.com/yourusername/project.git
cd project

# 3. Add upstream remote
git remote add upstream https://github.com/original/project.git

# 4. Create feature branch
git checkout -b feature/new-functionality

# 5. Make changes and push to your fork
git push origin feature/new-functionality

# 6. Create pull request to upstream
# 7. Keep fork synchronized
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Pull Request Workflows

### Standard PR Process

```bash
# 1. Create feature branch
git checkout -b feature/api-optimization

# 2. Make commits with clear messages
git commit -m "feat: optimize database queries in user service

- Add connection pooling configuration
- Implement query result caching
- Reduce N+1 queries in user relationships

Performance improvement: 40% faster response times
Test coverage: 95% maintained"

# 3. Push and create PR
git push -u origin feature/api-optimization
```

### PR Templates

```markdown
<!-- .github/pull_request_template.md -->
## Description
Brief description of changes and motivation

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Performance testing completed (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is commented where necessary
- [ ] Documentation updated
- [ ] No merge conflicts

## Related Issues
Fixes #123
Closes #456
Related to #789
```

### Review Process

```bash
# Reviewer workflow
git fetch origin
git checkout feature/api-optimization

# Review changes
git log --oneline origin/main..HEAD
git diff origin/main...HEAD

# Test locally
npm install
npm test
npm run lint

# Leave feedback and request changes if needed
# After approval, merge options:

# Option 1: Merge commit (preserves branch history)
git checkout main
git merge --no-ff feature/api-optimization

# Option 2: Squash merge (clean history)
git merge --squash feature/api-optimization
git commit -m "feat: optimize database queries

- Implement connection pooling
- Add query result caching
- Reduce N+1 queries

Performance: 40% improvement in response times"

# Option 3: Rebase merge (linear history)
git checkout feature/api-optimization
git rebase main
git checkout main
git merge feature/api-optimization
```

## Team Coordination Patterns

### Daily Synchronization

```bash
#!/bin/bash
# daily-sync.sh - Run each morning

# 1. Sync main branch
git checkout main
git pull origin main

# 2. Update feature branch
git checkout feature/current-work
git rebase main

# 3. Check for team updates
git fetch origin
git branch -r --merged origin/main | grep -v main

echo "Branches merged since yesterday:"
git log --oneline --since="yesterday" --merges origin/main
```

### Conflict Resolution Strategies

```bash
# Strategy 1: Rebase with conflict resolution
git checkout feature/my-feature
git rebase main

# When conflicts occur:
# 1. Edit conflicted files
# 2. Mark as resolved
git add conflicted-file.js
git rebase --continue

# Strategy 2: Merge with three-way merge
git checkout feature/my-feature
git merge main

# Resolve conflicts and commit
git add .
git commit -m "Resolve merge conflicts with main branch"

# Strategy 3: Interactive rebase for complex conflicts
git rebase -i main

# Use 'edit' for problematic commits
# Fix conflicts for each commit individually
```

### Communication Protocols

```bash
# Commit message conventions (Conventional Commits)
feat: add user authentication system
fix: resolve memory leak in data parser
docs: update API documentation
style: fix code formatting issues
refactor: restructure user service modules
test: add integration tests for payment flow
chore: update dependencies

# Branch naming with context
feature/PROJ-123-user-authentication
fix/BUG-456-memory-leak
hotfix/SECURITY-789-input-validation
refactor/database-optimization
```

## Distributed Team Workflows

### Timezone Coordination

```bash
# Time-based branch naming
feature/2023-12-01-morning-team-user-auth
feature/2023-12-01-evening-team-payment-fix

# Asynchronous handoffs
git checkout feature/shared-component
git pull origin feature/shared-component

# Add handoff notes
git commit -m "WIP: completed authentication flow

TODO for next developer:
- Add error handling for edge cases
- Implement rate limiting
- Add integration tests for token refresh

Progress: 70% complete
Next step: src/auth/middleware.js line 45"

git push origin feature/shared-component
```

### Remote Collaboration Tools

```bash
# Shared development environment
git worktree add ../feature-branch-workspace feature/shared-work
cd ../feature-branch-workspace

# Pair programming via shared commits
git config user.name "Alice & Bob"
git config user.email "team@company.com"
git commit -m "feat: implement shared feature

Co-authored-by: Alice Smith <alice@company.com>
Co-authored-by: Bob Jones <bob@company.com>"
```

## Code Integration Strategies

### Continuous Integration

```yaml
# .github/workflows/pr-validation.yml
name: PR Validation
on:
  pull_request:
    branches: [ main, develop ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0  # Full history for analysis
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      
      - name: Install dependencies
        run: npm install
      
      - name: Run linting
        run: npm run lint
      
      - name: Run tests with coverage
        run: npm run test:coverage
      
      - name: Check test coverage
        run: |
          if [ $(npm run test:coverage | grep "Lines" | awk '{print $3}' | sed 's/%//') -lt 80 ]; then
            echo "Test coverage below 80%"
            exit 1
          fi
      
      - name: Security audit
        run: npm audit --audit-level high
      
      - name: Build project
        run: npm run build

  compatibility:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14, 16, 18]
    steps:
      - uses: actions/checkout@v2
      - name: Test Node ${{ matrix.node-version }}
        uses: actions/setup-node@v2
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm install && npm test
```

### Automated Quality Gates

```bash
# pre-commit hook for quality checks
#!/bin/sh
# .git/hooks/pre-commit

# Check for debugging code
if grep -r "console.log\|debugger\|TODO" src/; then
    echo "Found debugging code or TODOs. Please remove before committing."
    exit 1
fi

# Run linting
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed. Please fix issues before committing."
    exit 1
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed. Please fix before committing."
    exit 1
fi

echo "Pre-commit checks passed!"
```

## Workflow Optimization

### Branch Management Automation

```bash
#!/bin/bash
# branch-cleanup.sh

# Delete merged feature branches
echo "Cleaning up merged branches..."
git branch --merged main | grep -E "feature/|fix/|hotfix/" | xargs -n 1 git branch -d

# Prune remote branches
git remote prune origin

# Update branch information
git fetch origin

# Report branch status
echo "Active feature branches:"
git branch -r | grep -E "feature/|fix/" | grep -v "merged"

echo "Stale branches (no activity in 30 days):"
git for-each-ref --format='%(refname:short) %(committerdate)' refs/remotes/origin | \
awk '$2 <= "'$(date -d '30 days ago' '+%Y-%m-%d')'"' | \
grep -E "feature/|fix/"
```

### Performance Monitoring

```bash
# Repository health check
#!/bin/bash
# repo-health.sh

echo "Repository Statistics:"
echo "====================="

# Repository size
echo "Repository size: $(du -sh .git | cut -f1)"

# Commit activity
echo "Commits this month: $(git log --oneline --since='1 month ago' | wc -l)"
echo "Active contributors: $(git shortlog -sn --since='1 month ago' | wc -l)"

# Branch analysis
echo "Total branches: $(git branch -a | wc -l)"
echo "Active branches: $(git branch -r | grep -v merged | wc -l)"
echo "Merged branches: $(git branch -r --merged main | wc -l)"

# Largest files
echo "Largest files:"
git rev-list --objects --all | \
git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
sed -n 's/^blob //p' | \
sort --numeric-sort --key=2 --reverse | \
head -5

# Most changed files
echo "Most frequently changed files:"
git log --format= --name-only --since='3 months ago' | \
sort | uniq -c | sort -nr | head -10
```

### Team Metrics and Analytics

```bash
# Team productivity analysis
#!/bin/bash
# team-metrics.sh

START_DATE="3 months ago"

echo "Team Collaboration Metrics (since $START_DATE)"
echo "=============================================="

# Commit activity by team member
echo "Commits by team member:"
git shortlog -sn --since="$START_DATE"

# Pull request activity
echo "Pull request statistics:"
gh pr list --state all --limit 100 --json createdAt,author,mergeable | \
jq -r '.[] | "\(.createdAt) \(.author.login) \(.mergeable)"' | \
awk '{print $2}' | sort | uniq -c | sort -nr

# Code review participation
echo "Code review participation:"
gh pr list --state all --limit 50 --json reviews | \
jq -r '.[] | .reviews[].author.login' | \
sort | uniq -c | sort -nr

# Average PR lifetime
echo "Average pull request lifetime:"
gh pr list --state closed --limit 20 --json createdAt,closedAt | \
jq -r '.[] | "\(.createdAt) \(.closedAt)"' | \
while read created closed; do
    echo $(( ($(date -d "$closed" +%s) - $(date -d "$created" +%s)) / 86400 ))
done | awk '{sum+=$1; count++} END {print sum/count " days"}'
```

This comprehensive collaboration framework enables teams to work effectively across different sizes, timezones, and project complexities while maintaining code quality and team productivity.