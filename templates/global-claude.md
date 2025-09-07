# Global Claude Code Configuration Template
# Place this file at: ~/.claude/CLAUDE.md

**GLOBAL AGENT DELEGATION ENFORCEMENT**: This configuration applies to ALL Claude Code sessions across every project on this machine.

## 🌍 UNIVERSAL MANDATORY PROTOCOLS

### Core Global Rules (NON-NEGOTIABLE)

**RULE 1: UNIVERSAL AGENT DELEGATION**
- Claude Code MUST use specialized agents for ALL development work
- Direct coding without agent coordination is PROHIBITED globally
- This rule applies regardless of project type or user request

**RULE 2: GLOBAL SAFETY FIRST**
- Branch protection checks are MANDATORY across all repositories
- Never work directly on main/master branches without permission
- Context verification required before any implementation

**RULE 3: GLOBAL QUALITY GATES**
- ALL development work must coordinate with qa-engineer
- Testing is not optional - it's required for every feature
- Documentation coordination required for user-facing changes

### Global Agent Detection Matrix

```yaml
# These patterns trigger automatic agent delegation in ANY project:

DEVELOPMENT_PATTERNS:
  python: { files: [".py", "requirements.txt"], agent: "python-engineer", critical: true }
  javascript: { files: [".js", ".jsx", ".ts", ".tsx"], agent: "frontend-engineer", critical: true }
  java: { files: [".java", "pom.xml"], agent: "java-engineer", critical: true }
  database: { files: [".sql", "migrations/"], agent: "database-engineer", critical: true }
  infrastructure: { files: ["Dockerfile", ".yml"], agent: "devops-engineer", critical: true }
  blockchain: { files: [".sol"], agent: "blockchain-engineer", critical: true }
  ml_ai: { files: [".ipynb"], keywords: ["torch", "tensorflow"], agent: "ai-engineer", critical: true }

COORDINATION_PATTERNS:
  git_operations: { keywords: ["git", "branch", "commit"], agent: "git-helper", critical: true }
  quality_assurance: { keywords: ["test", "testing", "QA"], agent: "qa-engineer", critical: true }
  documentation: { keywords: ["docs", "API", "guide"], agent: "technical-writer", critical: false }
  research: { keywords: ["research", "analysis"], agent: "ai-researcher", critical: false }
```

### Global Cost Optimization

**Intelligent Global Tier Selection:**
- **Haiku Tier (1x cost)**: git-helper, technical-writer, project-coordinator
- **Sonnet Tier (2-3x cost)**: All standard development agents 
- **Opus Tier (4-5x cost)**: sr-* agents for complex decisions only

**Global Cost Rules:**
- Always start with appropriate tier for task complexity
- Escalate to senior agents only after 3 failed attempts
- Monitor cost patterns across all projects for optimization

### Global Communication Standards

**Universal Response Style:**
- **Maximum 4 lines** unless detail explicitly requested
- **No preamble/postamble** - answer directly
- **Action-oriented** - use tools proactively
- **Professional and concise** - focus on technical solutions

### Global Override Conditions

Agent delegation bypassed ONLY for:
1. **Critical Production Emergencies** (with immediate agent handoff)
2. **Simple Questions** (concept explanations, syntax help)
3. **Explicit User Override** (with acknowledgment of protocol deviation)
4. **System Technical Failure** (temporary bypass until restoration)

## 🔧 GLOBAL INTEGRATION SETTINGS

### MCP Server Configuration

Recommended global MCP servers for agent coordination:
- **Filesystem**: For file operations
- **GitHub**: For repository management  
- **Agent Coordinator**: For delegation enforcement
- **Context7**: For framework documentation
- **Sequential Thinking**: For complex problem solving

### Global Hooks (Optional)

```bash
# ~/.claude/hooks/pre-development.sh
#!/bin/bash
# Verify agent delegation is being used for development tasks
echo "Checking for required agent delegation..."

# ~/.claude/hooks/post-session.sh  
#!/bin/bash
# Generate session summary with agent usage metrics
echo "Session complete - $(date)"
```

## 📊 GLOBAL MONITORING

### Track Across All Projects:
- Agent delegation compliance rate (target: >95%)
- Cost efficiency by tier selection
- Escalation patterns and success rates
- Branch safety protocol adherence
- Quality assurance completion rates

### Global Improvement Areas:
- Identify common delegation failures across projects
- Optimize tier selection accuracy
- Reduce unnecessary escalations
- Improve cost-effectiveness

## 🏠 PERSONAL DEVELOPMENT PREFERENCES

### Your Global Coding Standards:
```yaml
# Customize these based on your preferences:
code_style: "Follow existing project conventions"
testing_approach: "Comprehensive with qa-engineer coordination"
documentation_level: "API docs for user-facing features"
git_workflow: "Feature branches with PR reviews"
deployment_strategy: "Infrastructure as Code with proper CI/CD"
security_approach: "Security-first with regular audits"
```

### Global Shortcuts and Commands:
```bash
# Add to ~/.claude/commands/ directory for global availability:
# security-review.md: "Review this code for security vulnerabilities:"
# optimize-performance.md: "Analyze this code for performance optimization:"
# documentation-update.md: "Update documentation for these API changes:"
```

---

**SCOPE**: Universal - applies to ALL Claude Code sessions
**AUTHORITY**: System-level global configuration  
**OVERRIDE**: Project-specific CLAUDE.md files may extend but not reduce these requirements
**PLACEMENT**: ~/.claude/CLAUDE.md
**LAST UPDATED**: 2025-01-07
**VERSION**: Global v2.0