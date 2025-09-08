# Troubleshooting Guide

## Table of Contents
- [Common Installation Issues](#common-installation-issues)
- [Build and Validation Problems](#build-and-validation-problems)
- [Agent Configuration Issues](#agent-configuration-issues)
- [CLI Command Problems](#cli-command-problems)
- [Development Environment Issues](#development-environment-issues)
- [Performance and Optimization](#performance-and-optimization)
- [Debugging Tools](#debugging-tools)
- [Getting Help](#getting-help)

---

## Common Installation Issues

### Problem: Package Installation Fails

**Symptoms:**
```bash
$ pip install -e .
ERROR: Could not build wheels for claude-config
```

**Causes & Solutions:**

**Missing Python Development Headers**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip

# CentOS/RHEL
sudo yum install python3-devel python3-pip

# macOS
xcode-select --install
```

**Outdated pip/setuptools**
```bash
pip install --upgrade pip setuptools wheel
pip install -e .
```

**Permission Issues**
```bash
# Use virtual environment instead of system Python
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
pip install -e .
```

### Problem: uv Installation Issues

**Symptoms:**
```bash
$ make dev
uv: command not found
```

**Solution:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv

# Or use homebrew (macOS)
brew install uv
```

### Problem: Claude Code Directory Not Found

**Symptoms:**
```bash
$ make install-to-claude
cp: cannot stat '/home/user/.claude': No such file or directory
```

**Solution:**
```bash
# Create Claude Code directory
mkdir -p ~/.claude/agents
mkdir -p ~/.claude/settings

# Or install to custom location
claude-config install --target /custom/path
```

---

## Build and Validation Problems

### Problem: YAML Syntax Errors

**Symptoms:**
```bash
$ claude-config build
ValidationError: Invalid YAML syntax in python-engineer.yaml
```

**Common YAML Issues & Fixes:**

**Indentation Problems**
```yaml
# ❌ Incorrect indentation
expertise:
- "Python development"
  - "Web frameworks"  # Wrong indentation

# ✅ Correct indentation  
expertise:
- "Python development"
- "Web frameworks"
```

**String Quoting Issues**
```yaml
# ❌ Unescaped quotes
description: He's a Python expert

# ✅ Properly escaped
description: "He's a Python expert"
# or
description: 'He''s a Python expert'
```

**Multi-line String Formatting**
```yaml
# ❌ Incorrect multi-line
context_priming: You are a Python engineer
with extensive experience.

# ✅ Correct multi-line
context_priming: |
  You are a Python engineer
  with extensive experience.
```

**Debug YAML Syntax:**
```bash
# Validate specific file
python -c "import yaml; yaml.safe_load(open('data/personas/python-engineer.yaml'))"

# Or use yq if installed
yq eval . data/personas/python-engineer.yaml
```

### Problem: Template Rendering Failures

**Symptoms:**
```bash
$ claude-config build
TemplateError: Variable 'persona.expertise' not found
```

**Causes & Solutions:**

**Missing Required Fields**
```yaml
# Check your YAML has all required fields
name: python-engineer      # Required
display_name: "Python Engineer"  # Required  
model: sonnet              # Required
description: "..."         # Required
context_priming: |         # Required
  Your mindset...
expertise:                 # Required
- "Python development"
```

**Field Type Mismatches**
```yaml
# ❌ Expertise as string instead of list
expertise: "Python development"

# ✅ Expertise as list
expertise:
- "Python development"
- "Web frameworks"
```

**Debug Template Rendering:**
```bash
# Enable debug mode for detailed error info
claude-config build --debug --agent python-engineer
```

### Problem: Content File References Not Found

**Symptoms:**
```bash
$ claude-config validate
Warning: Referenced content file not found: personas/python-engineer/technical-approach.md
```

**Solution:**
```bash
# Create missing content files
mkdir -p data/content/personas/python-engineer
touch data/content/personas/python-engineer/technical-approach.md

# Or remove reference from YAML if not needed
# Remove content_sections field or specific file reference
```

### Problem: Agent Boundary Conflicts

**Symptoms:**
```bash
$ claude-config validate --check-boundaries
BoundaryConflictError: python-engineer and ai-engineer both handle "API development"
```

**Solution:**
```yaml
# Make boundaries more specific in each agent

# python-engineer.yaml
boundaries:
  do_handle:
  - "Web API development with Django/FastAPI"
  - "General Python application APIs"

# ai-engineer.yaml  
boundaries:
  do_handle:
  - "ML model serving APIs"
  - "AI/ML inference endpoints"
```

---

## Agent Configuration Issues

### Problem: Agent Not Activating Proactively

**Symptoms:**
- Agent doesn't activate when expected file patterns are present
- Manual agent invocation works but proactive doesn't

**Debug Steps:**

**Check File Patterns:**
```yaml
# Make patterns more specific
proactive_triggers:
  file_patterns:
  - "*.py"           # Too broad, conflicts with other agents
  - "**/models.py"   # More specific
  - "**/train_*.py"  # AI-specific patterns
```

**Check Project Indicators:**
```yaml
proactive_triggers:
  project_indicators:
  - "tensorflow"     # Check actual package names
  - "torch"          # Case-sensitive matching
  - "scikit-learn"   # Use exact PyPI names
```

**Test Pattern Matching:**
```bash
# Test if your project matches patterns
claude-config test-triggers --agent ai-engineer --project-path .
```

### Problem: Agent Coordination Not Working

**Symptoms:**
- Agent doesn't coordinate with expected agents
- Missing handoff points in workflows

**Check Coordination Configuration:**
```yaml
boundaries:
  coordinate_with:
  - "qa-engineer: Testing and validation of ML models"
  - "python-engineer: Model serving infrastructure"  # Must match exact agent names
```

**Verify Agent Names:**
```bash
# List all available agents to check exact names
claude-config list-agents
```

### Problem: Quality Criteria Not Being Applied

**Symptoms:**
- Generated agents don't follow specified quality standards
- Standards seem to be ignored

**Make Criteria More Specific:**
```yaml
# ❌ Vague criteria
quality_criteria:
  code_quality:
  - "Write good code"

# ✅ Specific, measurable criteria  
quality_criteria:
  code_quality:
  - "Follow PEP 8 with black formatting and type hints"
  - "90%+ test coverage with meaningful assertions"
  - "Clear docstrings following Google format"
  performance:
  - "API response times <200ms for standard endpoints"
  - "Memory usage <512MB for training jobs"
```

---

## CLI Command Problems

### Problem: Command Not Found

**Symptoms:**
```bash
$ claude-config build
claude-config: command not found
```

**Solutions:**

**Reinstall Package:**
```bash
# Reinstall in development mode
pip install -e .

# Or install normally
pip install .
```

**Check PATH:**
```bash
# Check if CLI script is installed
which claude-config

# If not in PATH, use module form
python -m claude_config build
```

**Virtual Environment Issues:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Or install globally (not recommended)
pip install --user -e .
```

### Problem: Permission Denied When Installing

**Symptoms:**
```bash
$ claude-config install
Permission denied: /home/user/.claude/agents/
```

**Solution:**
```bash
# Create directory with proper permissions
mkdir -p ~/.claude/agents
chmod 755 ~/.claude/agents

# Or install to custom location you own
claude-config install --target ~/my-claude-config
```

### Problem: Build Output Directory Issues

**Symptoms:**
```bash
$ claude-config build
Error: Cannot write to output directory: dist/
```

**Solution:**
```bash
# Create output directory
mkdir -p dist/agents

# Or specify custom output
claude-config build --output-dir /tmp/claude-build

# Check permissions
ls -la dist/
chmod 755 dist/
```

---

## Development Environment Issues

### Problem: Make Commands Failing

**Symptoms:**
```bash
$ make dev
make: *** No rule to make target 'dev'. Stop.
```

**Check Make Installation:**
```bash
# Install make if missing
# Ubuntu/Debian
sudo apt-get install make

# macOS
xcode-select --install

# Windows (use WSL or install make for Windows)
```

**Check Makefile:**
```bash
# Ensure Makefile exists and has proper targets
cat Makefile | grep "^[a-zA-Z].*:"
```

### Problem: Test Failures

**Symptoms:**
```bash
$ make test
FAILED tests/test_composer.py::test_compose_agent - FileNotFoundError
```

**Common Solutions:**

**Missing Test Data:**
```bash
# Ensure test data exists
ls tests/fixtures/
ls data/personas/

# Create minimal test data if missing
mkdir -p tests/fixtures/personas
cp data/personas/python-engineer.yaml tests/fixtures/personas/
```

**Import Errors:**
```bash
# Reinstall package in development mode
pip install -e .

# Or add src to Python path for tests
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

**Database/File Permissions:**
```bash
# Fix permissions on test files
chmod -R 755 tests/
chmod -R 755 data/
```

### Problem: Linting Failures

**Symptoms:**
```bash
$ make lint
black --check src/
would reformat src/claude_config/cli.py
```

**Auto-fix Formatting:**
```bash
# Auto-format code
make format

# Or run formatters directly
black src/ tests/
isort src/ tests/
```

**Fix Specific Issues:**
```bash
# Check what needs formatting
black --diff src/

# Fix imports
isort --diff src/

# Type checking issues
mypy src/ --show-error-codes
```

---

## Performance and Optimization

### Problem: Slow Build Times

**Symptoms:**
- `claude-config build` takes >10 seconds for small configurations
- High CPU usage during builds

**Optimization Steps:**

**Use Specific Agent Builds:**
```bash
# Build only changed agents instead of all
claude-config build --agent python-engineer

# Or use incremental builds (future feature)
claude-config build --incremental
```

**Profile Build Performance:**
```bash
# Enable timing information
claude-config build --profile

# Use verbose mode to see bottlenecks
claude-config build --verbose
```

**Optimize YAML Processing:**
```bash
# Install faster YAML parser
pip install PyYAML[fast]
```

### Problem: Large Memory Usage

**Symptoms:**
- Build process consumes >1GB RAM
- System becomes unresponsive during builds

**Memory Optimization:**

**Process Agents Incrementally:**
```bash
# Build agents one at a time
for agent in $(claude-config list-agents); do
    claude-config build --agent $agent
done
```

**Limit Concurrent Operations:**
```bash
# Set environment variable to limit memory usage
export CLAUDE_CONFIG_MAX_WORKERS=2
claude-config build
```

### Problem: Disk Space Issues

**Symptoms:**
```bash
$ claude-config build
Error: No space left on device
```

**Clean Up Build Artifacts:**
```bash
# Clean build directory
make clean

# Or manually remove
rm -rf dist/
rm -rf build/
rm -rf *.egg-info/
```

**Optimize Output Size:**
```bash
# Build only needed agents
claude-config build --agent-list python-engineer,git-helper

# Remove unused content files
find data/content -name "*.md" -size 0 -delete
```

---

## Debugging Tools

### Enable Debug Mode

```bash
# Enable debug logging for all commands
export CLAUDE_CONFIG_LOG_LEVEL=DEBUG
claude-config build

# Or use debug flag
claude-config build --debug
```

### Validate Configuration Step by Step

```bash
# Schema validation only
claude-config validate --schema-only

# Check specific agent
claude-config validate --agent python-engineer --verbose

# Test template rendering
claude-config build --agent python-engineer --dry-run
```

### Inspect Generated Output

```bash
# Build without installing to inspect output
claude-config build --output-dir /tmp/debug-build
ls -la /tmp/debug-build/agents/

# Check generated agent content
head -50 /tmp/debug-build/agents/python-engineer.md
```

### Profile Performance

```bash
# Time individual operations
time claude-config validate
time claude-config build --agent python-engineer

# Use Python profiler
python -m cProfile -o profile.stats -m claude_config.cli build
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

### Check System Dependencies

```bash
# Verify Python environment
python --version
pip --version
which python

# Check installed packages
pip list | grep -E "(pydantic|jinja2|click|rich)"

# Check file permissions
ls -la ~/.claude/
ls -la dist/
```

---

## Getting Help

### Self-Diagnosis Commands

```bash
# System status check
claude-config status

# List configuration
claude-config list-agents --verbose
claude-config validate --summary

# Check installation
pip show claude-config
```

### Collect Debug Information

```bash
# Create debug bundle
claude-config debug-info > debug-info.txt

# Or manually collect
echo "System Info:" > debug.txt
python --version >> debug.txt
pip --version >> debug.txt
pip show claude-config >> debug.txt
echo -e "\nValidation:" >> debug.txt
claude-config validate >> debug.txt 2>&1
```

### Community Resources

**Documentation:**
- [README.md](../README.md) - Main project documentation
- [API Reference](api-reference.md) - Detailed API documentation
- [Examples Collection](examples.md) - Practical examples

**Issue Reporting:**
When reporting issues, include:
1. **System Information**: OS, Python version, package versions
2. **Error Messages**: Complete error output with stack traces
3. **Configuration**: Relevant YAML configuration files
4. **Steps to Reproduce**: Exact commands and file structure
5. **Expected vs Actual**: What should happen vs what happens

**Debug Information Template:**
```
Environment:
- OS: [Linux/macOS/Windows version]
- Python: [version]
- claude-config: [version]
- Installation method: [pip/uv/development]

Issue Description:
[Clear description of the problem]

Steps to Reproduce:
1. [First step]
2. [Second step]  
3. [Where error occurs]

Error Output:
```
[Complete error message with stack trace]
```

Configuration:
[Relevant YAML files or configuration]

Expected Behavior:
[What should happen]

Actual Behavior:
[What actually happens]
```

### Advanced Debugging

**Enable All Debugging:**
```bash
# Maximum verbosity
export CLAUDE_CONFIG_LOG_LEVEL=DEBUG
export PYTHONPATH="${PWD}/src"
claude-config build --debug --verbose 2>&1 | tee debug.log
```

**Test Individual Components:**
```python
# Test YAML parsing
import yaml
with open('data/personas/python-engineer.yaml') as f:
    config = yaml.safe_load(f)
    print(config)

# Test template rendering
from claude_config.composer import AgentComposer
composer = AgentComposer('data/personas', 'src/claude_config/templates')
result = composer.compose_agent('python-engineer')
print(result[:500])
```

**Check File System Issues:**
```bash
# Check for file system corruption
fsck -f /dev/sda1  # Linux
diskutil verifyDisk disk0  # macOS

# Check permissions recursively
find . -type f -name "*.yaml" -exec ls -la {} \;

# Test write permissions
touch ~/.claude/test-write && rm ~/.claude/test-write
```

This troubleshooting guide covers the most common issues users encounter when working with claude-config. If you encounter an issue not covered here, please refer to the Getting Help section for community resources and issue reporting guidelines.