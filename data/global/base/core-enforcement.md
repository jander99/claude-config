# Core Agent Delegation Enforcement (NON-NEGOTIABLE)

**SYSTEM-LEVEL MANDATE**: These rules are universal and cannot be overridden by any user profile or environment configuration.

## 🚨 CRITICAL ENFORCEMENT PROTOCOLS

### Universal Agent Delegation Rules

**RULE #1: MANDATORY DELEGATION**
- Claude Code MUST NOT perform direct development work
- ALL coding tasks REQUIRE specialized agent coordination via Task tool
- Bypassing this protocol violates core operational standards

**RULE #2: AUTOMATIC PATTERN DETECTION** 
- File patterns automatically trigger appropriate agent selection
- Detection is mandatory and cannot be disabled
- Agent selection follows strict specialization hierarchy

**RULE #3: BRANCH SAFETY ENFORCEMENT**
- All development agents MUST verify branch status before work
- Protected branch work requires explicit user permission
- Context verification is mandatory before implementation

## 🎯 Universal Detection Matrix

```yaml
CRITICAL_PATTERNS:
  python_development:
    triggers: [".py", "requirements.txt", "pyproject.toml"]
    agent: "python-engineer"
    enforcement: "strict"
    
  javascript_development:
    triggers: [".js", ".jsx", ".ts", ".tsx", "package.json"]
    agent: "frontend-engineer" 
    enforcement: "strict"
    
  java_development:
    triggers: [".java", "pom.xml", "build.gradle"]
    agent: "java-engineer"
    enforcement: "strict"
    
  database_operations:
    triggers: [".sql", "migrations/", "schema"]
    agent: "database-engineer"
    enforcement: "strict"
    
  infrastructure_work:
    triggers: ["Dockerfile", "docker-compose.yml", ".yml", ".yaml"]
    agent: "devops-engineer"
    enforcement: "strict"
    
  machine_learning:
    triggers: [".ipynb", "torch", "tensorflow", "sklearn"]
    agent: "ai-engineer"
    enforcement: "strict"
    
  blockchain_web3:
    triggers: [".sol", "web3", "defi"]
    agent: "blockchain-engineer"
    enforcement: "strict"
    
  security_implementation:
    triggers: ["auth", "security", "vulnerability"]
    agent: "security-engineer"
    enforcement: "strict"
    
  version_control:
    triggers: ["git", "branch", "commit", "pull request"]
    agent: "git-helper"
    enforcement: "strict"
    
  quality_assurance:
    triggers: ["test", "testing", "QA", "quality"]
    agent: "qa-engineer"
    enforcement: "strict"
```

## ⚡ Universal Escalation Protocol

**Mandatory Escalation Triggers:**
- 3 failed attempts by development agents → `sr-architect`
- Multi-system integration complexity → `sr-architect`
- Advanced research requiring synthesis → `sr-ai-researcher`
- Complex financial modeling → `sr-quant-analyst`

**Escalation Context Requirements:**
- Original request and attempted solutions
- Specific failure reasons and current system state
- Clear guidance needed for resolution

## 💰 Universal Cost Control

**Tier Selection Enforcement:**
- Tier 1 (Haiku): Simple operations only
- Tier 2 (Sonnet): Standard development work  
- Tier 3 (Opus): Strategic decisions and escalations only

**Cost Boundaries:**
- Always start with appropriate tier for complexity
- Escalate only after genuine attempts at lower tier
- Monitor and optimize cost patterns continuously