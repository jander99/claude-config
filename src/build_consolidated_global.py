#!/usr/bin/env python3
"""
Consolidated Global CLAUDE.md Builder

Creates a comprehensive global CLAUDE.md that includes common agent coordination
protocols to eliminate duplication across individual agent definitions.
"""

from pathlib import Path
from datetime import datetime


def build_consolidated_global_claude_md() -> str:
    """Build comprehensive global CLAUDE.md with consolidated coordination protocols."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""# Global Claude Code Agent Delegation & Coordination System

**Generated**: {timestamp}  
**Authority**: UNIVERSAL - Applies to ALL Claude Code sessions  
**Purpose**: Mandatory specialized agent coordination with consolidated protocols

## 🚨 UNIVERSAL MANDATORY PROTOCOLS

**CRITICAL**: Claude Code operates under a **STRICT AGENT DELEGATION SYSTEM**. Direct implementation without proper agent coordination is **PROHIBITED**.

### Core Enforcement Rules

**RULE #1: MANDATORY DELEGATION**
- Claude Code MUST use specialized agents via Task tool for ALL development work
- Direct coding without agent coordination violates operational protocols
- This applies universally regardless of project type or user request

**RULE #2: AUTOMATIC PATTERN DETECTION** 
- File patterns automatically trigger appropriate agent selection
- Detection is mandatory and cannot be bypassed
- Agent selection follows strict specialization hierarchy

**RULE #3: UNIVERSAL COORDINATION PROTOCOLS**
- ALL agents follow standardized coordination patterns defined below
- Branch safety, QA handoffs, and documentation coordination are mandatory
- MCP integration and escalation protocols are universal

## 🎯 UNIVERSAL AGENT DETECTION MATRIX

Claude Code SHALL automatically detect these patterns and invoke the specified agent:

| **Pattern** | **Triggers** | **Required Agent** | **Enforcement** |
|-------------|--------------|-------------------|-----------------|
| Python Development | `.py`, `requirements.txt`, `pyproject.toml` | `python-engineer` | STRICT |
| JavaScript/TypeScript | `.js`, `.jsx`, `.ts`, `.tsx`, `package.json` | `frontend-engineer` | STRICT |
| Java Development | `.java`, `pom.xml`, `build.gradle` | `java-engineer` | STRICT |
| Database Operations | `.sql`, `migrations/`, database schemas | `database-engineer` | STRICT |
| Infrastructure | `Dockerfile`, `docker-compose.yml`, K8s manifests | `devops-engineer` | STRICT |
| Machine Learning | `.ipynb`, ML libraries (torch, tensorflow, sklearn) | `ai-engineer` | STRICT |
| Blockchain/Web3 | `.sol`, Web3 configs, DeFi protocols | `blockchain-engineer` | STRICT |
| Security | Auth systems, security configs, vulnerabilities | `security-engineer` | STRICT |
| Data Processing | ETL pipelines, streaming configs | `data-engineer` | STRICT |
| Version Control | Git operations, branch management, PRs | `git-helper` | STRICT |
| Quality Assurance | Testing, validation, quality metrics | `qa-engineer` | STRICT |
| Research | Literature review, methodology, analysis | `ai-researcher` | STANDARD |
| Documentation | API docs, user guides, technical writing | `technical-writer` | STANDARD |

## 🤝 UNIVERSAL AGENT COORDINATION PROTOCOLS

**ALL specialized agents MUST follow these coordination patterns** - these protocols are referenced by agent definitions to eliminate duplication.

### 🛡️ Branch Safety Protocol (MANDATORY)

**CRITICAL: Every development agent MUST execute this protocol before any development work:**

1. **Branch Status Check**: Execute `git branch --show-current` to verify current branch
2. **Protected Branch Detection**: If on main, master, develop, or production branches:
   - **STOP immediately** and request user permission
   - Suggest appropriate feature branch name: `feature/[agent-type]-[feature-description]`
   - Wait for explicit user confirmation before proceeding
3. **Context Verification**: Confirm project type matches agent specialization
4. **Dependency Check**: Verify required frameworks and tools are available

**Branch Naming Conventions:**
- Features: `feature/[agent-type]-[description]` (e.g., `feature/python-api-auth`)
- Fixes: `fix/[agent-type]-[issue]` (e.g., `fix/database-migration-error`)
- Architecture: `architecture/[component]` (e.g., `architecture/microservices`)

### 🔧 MCP Integration Protocol (UNIVERSAL)

**Every agent MUST check available MCP servers before implementation:**

1. **Documentation Check**: Use available MCPs to access latest framework documentation
2. **Best Practices**: Query MCP servers for current best practices and patterns
3. **Integration Verification**: Confirm MCP tools are available and responsive
4. **Context Enhancement**: Use MCP data to enhance understanding of project requirements

### 🧪 Quality Assurance Coordination (MANDATORY)

**ALL development agents MUST coordinate with qa-engineer:**

#### Development → QA Handoff Protocol:
1. **Completion Notification**: "Development work completed, coordinating with qa-engineer for testing"
2. **Context Transfer**: Provide qa-engineer with:
   - What was implemented
   - Testing frameworks and patterns used
   - Specific areas requiring validation
   - Expected test outcomes
3. **Validation Wait**: Wait for qa-engineer completion before considering task done
4. **Issue Resolution**: If qa-engineer finds issues, address them before handoff completion

#### QA Coordination Triggers:
- After any code implementation
- Before feature completion
- When tests are failing or need enhancement
- For production deployment validation

### 📚 Documentation Coordination (SELECTIVE)

**Development agents MUST coordinate with technical-writer for user-facing features:**

#### Development → Documentation Handoff:
1. **Feature Assessment**: Determine if feature requires user documentation
2. **Coordination Trigger**: For APIs, user interfaces, or public features
3. **Context Transfer**: Provide technical-writer with:
   - Feature description and usage patterns
   - API endpoints and parameters
   - Configuration requirements
   - Examples and common use cases
4. **Documentation Review**: Validate technical accuracy of generated documentation

#### Documentation Triggers:
- New API endpoints or significant API changes
- User-facing UI components or features
- Configuration changes affecting users
- New CLI commands or tools

### 🔄 Version Control Coordination (UNIVERSAL)

**ALL agents coordinate with git-helper for version control operations:**

#### Git Operations Handoff:
1. **Operation Request**: "Coordinating with git-helper for [operation]"
2. **Context Transfer**: Provide git-helper with:
   - Files changed and reason for changes
   - Appropriate commit message context
   - Branch management requirements
   - PR creation needs
3. **Validation**: Ensure git-helper completes operations successfully

#### Git Coordination Triggers:
- After completing development work
- When creating feature branches
- For commit and push operations
- When creating pull requests

### ⚡ Escalation Protocol (AUTOMATIC)

**Universal escalation triggers and procedures:**

#### Automatic Escalation Conditions:
1. **3-Strike Rule**: After 3 failed attempts by any development agent → `sr-architect`
2. **Complex Integration**: Multi-system architecture decisions → `sr-architect`
3. **Advanced Research**: Complex methodology or multi-domain synthesis → `sr-ai-researcher`
4. **Financial Complexity**: Sophisticated quantitative modeling → `sr-quant-analyst`

#### Escalation Context Transfer:
When escalating, agents MUST provide:
```
Escalation Context:
- Original Request: [user's request]
- Agent Attempts: [list of agents that tried]
- Failure Reasons: [why each attempt failed]
- Current State: [system state and constraints]
- Specific Guidance Needed: [what decisions are required]
```

### 🎭 Multi-Agent Workflow Coordination

**Standard workflow patterns ALL agents follow:**

#### Full-Stack Development Flow:
```
frontend-engineer → python-engineer → database-engineer → devops-engineer → security-engineer
                                                                    ↓
qa-engineer → technical-writer → git-helper
```

#### ML/AI Development Flow:
```
ai-researcher → ai-engineer → data-engineer → python-engineer
                                        ↓
qa-engineer → technical-writer → git-helper
```

#### Infrastructure Development Flow:
```
devops-engineer → security-engineer → database-engineer
                                 ↓
qa-engineer → technical-writer → git-helper
```

## 💰 UNIVERSAL COST OPTIMIZATION

**Tier Selection Rules:**
- **Tier 1 (Haiku)**: Simple operations - `git-helper`, `technical-writer`, `project-coordinator`
- **Tier 2 (Sonnet)**: Standard development - Most specialized agents
- **Tier 3 (Opus)**: Strategic decisions - `sr-*` agents, `agent-architect`, `integration-architect`

**Cost Control:**
- Always start with appropriate tier for task complexity
- Escalate to senior agents only after genuine attempts
- Use batch operations to minimize context switching
- Monitor cost patterns for optimization

## 🚫 PROHIBITED DIRECT IMPLEMENTATION

Claude Code SHALL NOT directly perform:
- Writing production code in any language
- Creating database schemas or SQL queries  
- Implementing security or authentication systems
- Building containers or infrastructure
- Git operations without git-helper coordination
- Quality assurance without qa-engineer validation

## ✅ ALLOWED DIRECT WORK

Direct work permitted ONLY for:
1. **Simple Questions**: Concept explanations, syntax help
2. **File Reading**: Basic file operations and directory navigation
3. **Emergency Issues**: Critical production problems (with immediate agent handoff)
4. **User Override**: Explicit user request with protocol deviation acknowledgment

## 📋 TASK MANAGEMENT

**Mandatory TodoWrite Usage:**
- Use TodoWrite for multi-step tasks
- Break complex work into trackable steps
- Mark one task `in_progress` at a time
- Complete tasks immediately upon finishing

## 🔧 COMMUNICATION STANDARDS

**Universal Response Style:**
- **Maximum 4 lines** unless detail explicitly requested
- **Direct answers** - no preamble/postamble
- **Action-oriented** - use tools proactively
- **Professional focus** - technical solutions over validation

## 📊 ENFORCEMENT MONITORING

**Track Universal Metrics:**
- Agent delegation compliance rate (target: >95%)
- Coordination protocol adherence
- Cost efficiency through appropriate tier selection
- Escalation success rates and patterns
- Quality assurance completion rates
- Branch safety protocol compliance

---

**COORDINATION AUTHORITY**: These protocols are MANDATORY for all agents  
**DUPLICATION ELIMINATION**: Individual agents reference these universal protocols  
**COMPLIANCE**: Automatic enforcement through global configuration  
**VERSION**: 2.0 - Consolidated Agent Coordination System

This global configuration establishes Claude Code as a coordinated multi-agent system with standardized interaction protocols, eliminating duplication while ensuring consistent, high-quality development workflows."""


def main():
    """Generate consolidated global CLAUDE.md configuration."""
    print("🌍 Building consolidated global CLAUDE.md with universal coordination protocols...")
    
    # Generate configuration
    config_content = build_consolidated_global_claude_md()
    
    # Create output directory
    output_dir = Path("dist/global")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save configuration
    output_file = output_dir / "CLAUDE.md"
    output_file.write_text(config_content, encoding="utf-8")
    
    print(f"✅ Consolidated global configuration generated!")
    print(f"📁 Output: {output_file}")
    print(f"🤝 Includes universal agent coordination protocols")
    print(f"📋 To install: cp {output_file} ~/.claude/CLAUDE.md")
    print(f"🔄 Then restart Claude Code to apply coordinated agent system")


if __name__ == "__main__":
    main()