# Git Troubleshooting and Problem Resolution

## Overview

Git issues can range from simple conflicts to complex repository corruption. This comprehensive troubleshooting guide provides systematic approaches to diagnose, resolve, and prevent common Git problems.

## Common Issue Categories

### 1. Merge and Conflict Issues

#### Merge Conflicts
**Symptoms**: Merge fails with conflict messages
```bash
# Error messages:
Auto-merging file.js
CONFLICT (content): Merge conflict in file.js
Automatic merge failed; fix conflicts and then commit the result.
```

**Diagnosis**:
```bash
# Check conflict status
git status
git diff  # Shows conflict markers

# Identify conflicted files
git diff --name-only --diff-filter=U
```

**Resolution**:
```bash
# Method 1: Manual resolution
# Edit files to remove conflict markers (<<<<<<, ======, >>>>>>)
git add resolved-file.js
git commit -m "Resolve merge conflict in file.js"

# Method 2: Use merge tool
git mergetool
git commit

# Method 3: Choose one side entirely
git checkout --ours conflicted-file.js    # Keep current branch version
git checkout --theirs conflicted-file.js  # Accept incoming changes
git add conflicted-file.js
git commit

# Method 4: Abort merge and restart
git merge --abort
# Fix underlying issues, then retry merge
```

#### Failed Rebase
**Symptoms**: Rebase stops with conflicts or fails to apply commits
```bash
# Error message:
error: could not apply abc123d... commit message
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue"
```

**Resolution**:
```bash
# Continue rebase after fixing conflicts
git add fixed-file.js
git rebase --continue

# Skip problematic commit
git rebase --skip

# Abort and return to original state
git rebase --abort

# Interactive rebase to edit history
git rebase -i HEAD~5
# Edit/squash/reorder commits as needed
```

### 2. Branch and Remote Issues

#### Branch Tracking Problems
**Symptoms**: Push/pull fails or behaves unexpectedly
```bash
# Common errors:
fatal: The current branch feature has no upstream branch.
fatal: refusing to merge unrelated histories
```

**Diagnosis**:
```bash
# Check branch tracking
git branch -vv
git remote -v
git status
```

**Resolution**:
```bash
# Set upstream branch
git push -u origin feature-branch
git branch --set-upstream-to=origin/feature-branch

# Fix unrelated histories
git pull --allow-unrelated-histories
git merge --allow-unrelated-histories origin/main

# Reset branch tracking
git branch --unset-upstream
git push -u origin HEAD
```

#### Remote Synchronization Issues
**Symptoms**: Remote branches out of sync, missing branches
```bash
# Issues:
- Remote branches not showing locally
- Deleted remote branches still appear
- Unable to fetch/push to remote
```

**Resolution**:
```bash
# Update remote information
git remote update
git fetch --all --prune

# Clean up remote tracking branches
git remote prune origin

# Re-add remote if corrupted
git remote remove origin
git remote add origin https://github.com/user/repo.git
git fetch origin

# Force push (dangerous - use carefully)
git push --force-with-lease origin branch-name
```

### 3. Commit and History Issues

#### Incorrect Commits
**Symptoms**: Wrong files committed, bad commit messages
```bash
# Problems:
- Committed sensitive data
- Wrong files in commit
- Typo in commit message
```

**Resolution**:
```bash
# Fix last commit message
git commit --amend -m "Corrected commit message"

# Add files to last commit
git add forgotten-file.js
git commit --amend --no-edit

# Remove file from last commit
git reset HEAD~ -- unwanted-file.js
git commit --amend

# Completely undo last commit (keep changes staged)
git reset --soft HEAD~1

# Completely undo last commit (discard changes)
git reset --hard HEAD~1

# Remove sensitive data from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch sensitive-file.txt' \
  --prune-empty --tag-name-filter cat -- --all
```

#### Lost Commits or Branches
**Symptoms**: Commits disappeared after reset, branch deleted accidentally
```bash
# Find lost commits
git reflog
git reflog show branch-name

# Recover deleted branch
git branch recovered-branch commit-hash

# Recover specific commit
git cherry-pick lost-commit-hash

# Find all unreachable commits
git fsck --lost-found
```

### 4. Repository Corruption Issues

#### Corrupted Objects
**Symptoms**: Git operations fail with object errors
```bash
# Error messages:
error: object file .git/objects/ab/cdef123... is empty
fatal: loose object abc123def... is corrupt
```

**Diagnosis**:
```bash
# Check repository integrity
git fsck --full --strict

# Identify corrupted objects
git cat-file -p corrupted-object-hash
```

**Resolution**:
```bash
# Method 1: Recover from remote
git fetch origin
git reset --hard origin/main

# Method 2: Manual object recovery
# Find backup of object in .git/objects
# Or recover from another clone

# Method 3: Repository rebuild
cd ..
git clone https://github.com/user/repo.git repo-backup
cd repo-backup
# Copy work from corrupted repo
```

#### Index Corruption
**Symptoms**: Staging area corrupted, git add/status fails
```bash
# Error messages:
error: bad index file sha1 signature
fatal: index file corrupt
```

**Resolution**:
```bash
# Remove and rebuild index
rm .git/index
git reset

# Or force checkout to rebuild
git checkout -f HEAD
```

## Diagnostic Tools and Techniques

### Repository Health Check

```bash
#!/bin/bash
# git-health-check.sh

echo "Git Repository Health Check"
echo "=========================="

# Check repository integrity
echo "1. Repository Integrity:"
if git fsck --full --strict 2>/dev/null; then
    echo "   ✓ Repository integrity OK"
else
    echo "   ✗ Repository integrity issues detected"
    git fsck --full --strict
fi

# Check for large files
echo "2. Large Files Check:"
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {if ($3 > 1048576) print $3/1048576 "MB " $4}' | \
  sort -nr | head -5

# Check remote connectivity
echo "3. Remote Connectivity:"
for remote in $(git remote); do
    if git ls-remote --exit-code $remote >/dev/null 2>&1; then
        echo "   ✓ $remote: Connected"
    else
        echo "   ✗ $remote: Connection failed"
    fi
done

# Check for uncommitted changes
echo "4. Working Directory Status:"
if git diff-index --quiet HEAD --; then
    echo "   ✓ No uncommitted changes"
else
    echo "   ! Uncommitted changes detected"
    git status --porcelain
fi

# Check branch status
echo "5. Branch Status:"
git for-each-ref --format='%(refname:short) %(upstream) %(upstream:track)' refs/heads | \
  while read branch upstream track; do
    if [[ -n "$upstream" ]]; then
        echo "   $branch -> $upstream $track"
    else
        echo "   $branch (no upstream)"
    fi
  done
```

### Performance Analysis

```bash
# Repository performance analysis
echo "Repository Size Analysis:"
echo "========================"

# Overall size
echo "Repository size: $(du -sh .git | cut -f1)"

# Object count
git count-objects -v

# Pack file analysis
echo "Pack files:"
ls -lh .git/objects/pack/

# Find largest objects
git verify-pack -v .git/objects/pack/*.idx | \
  sort -k 3 -nr | head -10 | \
  while read sha1 type size rest; do
    echo "$size bytes: $(git rev-list --objects --all | grep $sha1 | cut -d' ' -f2-)"
  done
```

## Environment-Specific Issues

### Windows-Specific Problems

#### Line Ending Issues
```bash
# Configure line endings
git config --global core.autocrlf true    # Windows
git config --global core.autocrlf input   # Unix/Linux
git config --global core.autocrlf false   # Mixed environment

# Fix existing repository
git config core.autocrlf true
git rm --cached -r .
git reset --hard
```

#### Path Length Limitations
```bash
# Enable long path support
git config --system core.longpaths true

# Or use shorter paths
git config --global core.precomposeUnicode true
```

### Network and Proxy Issues

#### Corporate Firewall/Proxy
```bash
# Configure proxy
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy https://proxy.company.com:8080

# Configure for specific repository
git config http.proxy http://proxy.company.com:8080

# Use SSH instead of HTTPS
git remote set-url origin git@github.com:user/repo.git

# Skip SSL verification (not recommended for production)
git config --global http.sslverify false
```

#### SSH Key Issues
```bash
# Test SSH connection
ssh -T git@github.com

# Use specific SSH key
git config core.sshCommand "ssh -i ~/.ssh/specific_key"

# Add key to SSH agent
ssh-add ~/.ssh/id_rsa

# Debug SSH issues
ssh -vT git@github.com
```

## Prevention Strategies

### Pre-commit Validation

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Check for large files
for file in $(git diff-index --name-only --cached HEAD); do
    size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || echo 0)
    if [ $size -gt 10485760 ]; then  # 10MB
        echo "Error: File $file is too large ($(( size / 1048576 ))MB)"
        echo "Consider using Git LFS for large files"
        exit 1
    fi
done

# Check for sensitive data patterns
if git diff --cached | grep -E "(password|secret|key|token)" | grep -E "=.*['\"][^'\"]{8,}['\"]"; then
    echo "Warning: Possible sensitive data detected in commit"
    echo "Please review changes carefully"
    exit 1
fi

# Validate commit doesn't break build
if command -v npm >/dev/null 2>&1; then
    npm test
    if [ $? -ne 0 ]; then
        echo "Tests failed. Commit aborted."
        exit 1
    fi
fi
```

### Repository Maintenance Scripts

```bash
#!/bin/bash
# git-maintenance.sh

# Run weekly maintenance
echo "Running Git maintenance..."

# Garbage collection
git gc --auto

# Repack repository
git repack -ad

# Prune old objects
git prune --expire="2 weeks ago"

# Clean up remote tracking branches
git remote prune origin

# Verify repository integrity
if ! git fsck --full >/dev/null 2>&1; then
    echo "Warning: Repository integrity issues detected"
    git fsck --full
fi

# Repository statistics
echo "Repository statistics:"
git count-objects -vH

echo "Maintenance completed"
```

## Emergency Recovery Procedures

### Complete Repository Recovery

```bash
# When local repository is completely corrupted
cd /path/to/projects

# 1. Backup current state
mv corrupted-repo corrupted-repo-backup

# 2. Fresh clone
git clone https://github.com/user/repo.git

# 3. Restore uncommitted work
cp -r corrupted-repo-backup/src/ repo/src/
cd repo

# 4. Check what needs to be committed
git status
git add .
git commit -m "Restore work after repository corruption"
```

### Data Recovery from Backups

```bash
# Restore from Time Machine (macOS) or similar backup
cp -r /Volumes/Backup/path/to/repo/.git .
git status

# Restore from GitHub/GitLab backup
git remote add backup https://github.com/user/repo-backup.git
git fetch backup
git merge backup/main

# Restore specific files from history
git checkout commit-hash -- path/to/file.js
git checkout branch-name -- path/to/directory/
```

This comprehensive troubleshooting guide provides systematic approaches to diagnose, resolve, and prevent Git issues across different environments and use cases.