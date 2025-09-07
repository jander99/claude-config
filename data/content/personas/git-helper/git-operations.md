# Advanced Version Control and Git Operations

## Overview

Mastery of Git's advanced features enables efficient version control, sophisticated branching strategies, and robust project history management. This guide covers advanced Git operations, repository management, and version control best practices.

## Repository Management

### Repository Initialization and Configuration

```bash
# Initialize repository with optimal settings
git init --initial-branch=main
git config --local user.name "Team Name"
git config --local user.email "team@company.com"

# Configure line ending handling
git config --local core.autocrlf false  # Unix/Linux
git config --local core.autocrlf true   # Windows

# Set up gitignore from start
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore

# Configure merge strategy
git config --local merge.ours.driver true
git config --local merge.tool vimdiff
```

### Remote Repository Management

```bash
# Add multiple remotes for different purposes
git remote add origin https://github.com/company/main-repo.git
git remote add upstream https://github.com/original/repo.git
git remote add deploy git@deploy-server.com:app/repo.git

# Configure remote tracking
git config --local remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git config --local remote.upstream.fetch "+refs/heads/main:refs/remotes/upstream/main"

# Set up push defaults
git config --local push.default current
git config --local push.followTags true

# Manage remote URLs
git remote set-url origin git@github.com:company/main-repo.git
git remote set-url --push origin git@github.com:company/main-repo.git
```

## Advanced Commit Management

### Commit Crafting and History Editing

```bash
# Interactive staging for precise commits
git add -p  # Stage changes in hunks
git add -i  # Interactive staging menu

# Commit with detailed message
git commit -m "feat: implement user authentication system

- Add JWT token generation and validation
- Implement password hashing with bcrypt
- Add session management middleware
- Include rate limiting for login attempts

Breaking Changes:
- Authentication headers now required for API calls
- Session cookie name changed from 'session' to 'auth_token'

Closes #123, #456
Co-authored-by: Alice Smith <alice@company.com>"

# Amend commits
git commit --amend --no-edit  # Add staged changes to last commit
git commit --amend -m "Updated commit message"

# Interactive rebase for history editing
git rebase -i HEAD~5

# Rebase actions:
# pick   - use commit as is
# reword - use commit but edit message
# edit   - use commit but stop for amending
# squash - combine with previous commit
# fixup  - like squash but discard commit message
# drop   - remove commit
```

### Selective History Management

```bash
# Cherry-pick commits with modifications
git cherry-pick --no-commit abc123def
# Make additional changes
git add .
git commit -m "Cherry-picked and modified: original feature + fixes"

# Apply patch from commit
git format-patch -1 abc123def  # Create patch file
git apply 0001-commit-name.patch  # Apply patch

# Create commits from stash
git stash
git stash apply
git add -A
git commit -m "Applied stashed changes: work in progress"
git stash drop
```

## Branch Operations and Management

### Advanced Branching Techniques

```bash
# Create branch from specific commit
git branch feature/new-work abc123def

# Create orphan branch (no history)
git checkout --orphan gh-pages
git rm -rf .
echo "# GitHub Pages" > README.md
git add README.md
git commit -m "Initial GitHub Pages commit"

# Track remote branch with different name
git checkout -b local-feature origin/remote-feature-name

# Create branch from tag
git checkout -b hotfix/v1.2.1-fix v1.2.1

# Branch from merge base
git checkout -b feature/shared-base $(git merge-base main feature/other)
```

### Branch Synchronization and Updates

```bash
# Update branch with upstream changes
git checkout feature/my-branch
git fetch origin
git rebase origin/main

# Handle rebase conflicts
# 1. Fix conflicts in files
# 2. Stage resolved files
git add resolved-file.js
# 3. Continue rebase
git rebase --continue

# Alternative: merge strategy
git checkout feature/my-branch
git merge origin/main

# Update feature branch with specific commits
git checkout feature/target-branch
git cherry-pick commit1 commit2 commit3

# Sync fork with upstream
git remote add upstream https://github.com/original/repo.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Advanced Merging Strategies

### Merge Options and Strategies

```bash
# No fast-forward merge (preserves branch structure)
git merge --no-ff feature/branch-name

# Squash merge (combines all commits into one)
git merge --squash feature/branch-name
git commit -m "Complete feature: user authentication system

This commit includes all work from feature/branch-name:
- Authentication middleware
- Password hashing
- Session management
- Rate limiting
- Comprehensive tests"

# Octopus merge (multiple branches)
git merge branch1 branch2 branch3

# Custom merge strategies
git merge -X ours feature/branch-name     # Prefer current branch
git merge -X theirs feature/branch-name   # Prefer incoming changes
git merge -X ignore-space-change feature/branch-name
```

### Conflict Resolution

```bash
# Advanced conflict resolution
git config merge.tool kdiff3  # Configure merge tool

# Manual conflict resolution workflow
git status  # See conflicted files
git diff    # View conflicts

# Edit conflicted files, then:
git add resolved-file.js
git commit  # Complete merge

# Abort merge if needed
git merge --abort

# Use specific file version during merge
git checkout --ours conflicted-file.js    # Use current branch version
git checkout --theirs conflicted-file.js  # Use incoming version
git add conflicted-file.js
```

## History Analysis and Navigation

### Advanced Log Analysis

```bash
# Detailed history with branching visualization
git log --oneline --graph --decorate --all

# Search commit messages and content
git log --grep="authentication" --oneline
git log -S "function loginUser" --oneline  # Search for code changes

# Show commits affecting specific file
git log --follow --patch -- path/to/file.js

# Time-based history
git log --since="2023-01-01" --until="2023-12-31" --author="alice@company.com"
git log --since="2 weeks ago" --oneline

# Show merge commits only
git log --merges --oneline

# Find commits that introduced bugs
git log --grep="fix\|bug" --oneline --since="1 month ago"
```

### Blame and Attribution

```bash
# Line-by-line file history
git blame src/auth/login.js

# Ignore whitespace changes in blame
git blame -w src/auth/login.js

# Show commit details for specific line
git blame -L 10,20 src/auth/login.js

# Find when line was changed
git log -L 15,25:src/auth/login.js

# Show original author of moved/copied lines
git blame -M -C src/auth/login.js
```

## Data Recovery and Maintenance

### Recovery Operations

```bash
# Recover deleted branch
git reflog  # Find branch commit hash
git branch recovered-branch abc123def

# Recover deleted commits
git reflog show HEAD
git cherry-pick lost-commit-hash

# Recover from hard reset
git reflog
git reset --hard HEAD@{2}  # Go back to previous state

# Find lost commits
git fsck --lost-found
git show lost-commit-hash

# Recover deleted files
git checkout HEAD~1 -- deleted-file.js
git checkout branch-name -- deleted-file.js
```

### Repository Maintenance

```bash
# Clean up repository
git gc --prune=now  # Garbage collect immediately
git repack -ad      # Repack objects for efficiency

# Remove untracked files and directories
git clean -fd       # Remove files and directories
git clean -fX       # Remove only ignored files
git clean -fx       # Remove ignored and untracked files

# Verify repository integrity
git fsck --full --strict

# Repository size analysis
git count-objects -vH  # Show repository statistics
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '/^blob/ {print substr($0,6)}' | sort --numeric-sort --key=2 --reverse | head -20

# Large file detection and removal
git filter-branch --tree-filter 'rm -rf path/to/large/file' HEAD
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now
```

## Hooks and Automation

### Git Hooks Implementation

```bash
# Pre-commit hook example
#!/bin/sh
# .git/hooks/pre-commit

# Check for merge conflicts markers
if grep -r "<<<<<<< HEAD\|>>>>>>> \|=======" src/; then
    echo "Error: Merge conflict markers found in staged files"
    exit 1
fi

# Run linting
npm run lint
if [ $? -ne 0 ]; then
    echo "Error: Linting failed"
    exit 1
fi

# Check commit message format (commit-msg hook)
#!/bin/sh
# .git/hooks/commit-msg

commit_regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format!"
    echo "Format: type(scope): description"
    echo "Example: feat(auth): add user login functionality"
    exit 1
fi

# Post-receive hook for deployment
#!/bin/sh
# hooks/post-receive

while read oldrev newrev refname; do
    if [[ $refname == "refs/heads/main" ]]; then
        echo "Deploying to production..."
        cd /var/www/app
        git --git-dir=/var/www/app/.git --work-tree=/var/www/app pull origin main
        npm install --production
        npm run build
        systemctl restart app-service
        echo "Deployment completed"
    fi
done
```

### Workflow Automation Scripts

```bash
#!/bin/bash
# daily-workflow.sh

# Update main branch
git checkout main
git pull origin main

# Clean up merged branches
git branch --merged main | grep -v "main\|develop" | xargs -n 1 git branch -d

# Prune remote branches
git remote prune origin

# Show status of current work
echo "Current branches:"
git branch

echo "Recent activity:"
git log --oneline --since="yesterday" --all --author="$(git config user.email)"

echo "Outstanding pull requests:"
gh pr list --state open --author="@me"
```

## Advanced Git Configuration

### Global Configuration Optimization

```bash
# Performance optimizations
git config --global core.preloadindex true
git config --global core.fscache true
git config --global gc.auto 256

# Better diff and merge tools
git config --global diff.algorithm histogram
git config --global merge.conflictstyle diff3

# Enhanced push settings
git config --global push.default current
git config --global push.followTags true
git config --global push.autoSetupRemote true

# Useful aliases
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
git config --global alias.type 'cat-file -t'
git config --global alias.dump 'cat-file -p'
git config --global alias.hist 'log --pretty=format:"%h %ad | %s%d [%an]" --graph --date=short'

# Security settings
git config --global user.signingkey GPG_KEY_ID
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

### Repository-Specific Configuration

```bash
# Per-repository settings
git config --local core.autocrlf false
git config --local core.filemode false
git config --local branch.autosetupmerge always
git config --local branch.autosetuprebase always

# Custom merge drivers
echo "*.generated merge=ours" >> .gitattributes
git config merge.ours.driver true

# LFS configuration for large files
git lfs track "*.zip"
git lfs track "*.tar.gz"
git lfs track "*.bin"
echo ".lfsconfig" >> .gitignore
```

This comprehensive version control framework provides the foundation for managing complex project histories, enabling efficient collaboration, and maintaining repository health across development lifecycles.