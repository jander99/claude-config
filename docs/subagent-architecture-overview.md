# Claude Code Subagents: comprehensive architecture and implementation guide

## What are Claude Code Subagents?

Claude Code subagents are **specialized AI assistants defined as markdown files with YAML frontmatter** that can be delegated specific tasks. Each subagent operates with its own isolated context window, customized system prompt, and granular tool permissions - effectively creating an "AI dream team" where specialists handle domain-specific work without context pollution.

The core innovation solves the critical "context reset problem" that plagued previous AI development workflows. As one production user at PubNub noted: *"By using subagents you give each specialist its own dedicated context window, ensuring the quality of each step is preserved."*

## Deliverable 1: Criteria for useful subagents

Based on extensive community feedback analysis across GitHub repositories, Reddit discussions, and production implementations, **useful subagents** meet these essential criteria:

### Must-have characteristics

**Single, clear responsibility** - Each subagent handles one specific domain. Multi-purpose agents become unpredictable and difficult to invoke reliably.

**Non-descriptive naming convention** - Critical finding: Claude overrides custom instructions based on agent names. Use abstract names like "blue-jay" instead of "code-reviewer" to prevent Claude from applying generic presets.

**Specific activation triggers** - Descriptions must include action-oriented phrases like "Use PROACTIVELY after code changes" or "MUST BE USED for security analysis" to enable automatic delegation.

**Minimal necessary tool access** - Follow least-privilege principles. A code reviewer needs Read/Grep/Bash but not Write permissions.

**Detailed system prompts with examples** - Include specific instructions, success criteria, and concrete examples of expected behavior.

### Production-ready standards

**Battle-tested configurations** validated in real workflows, not theoretical constructs. The community consensus: useful subagents solve specific, recurring problems with measurable productivity gains.

**Version control compatibility** - Store in `.claude/agents/` for project-specific agents or `~/.claude/agents/` for global availability. Check into Git for team collaboration.

**Clear success metrics** - Define completion criteria, quality gates, and validation checkpoints.

**Regular maintenance commitment** - Update for Claude model changes, industry best practices evolution, and framework updates.

### Anti-patterns to avoid

- Vague descriptions causing poor automatic delegation
- Overlapping responsibilities between agents
- Over-broad tool permissions creating security risks  
- Missing concrete examples in system prompts
- Creating agents for tasks the main Claude handles well

## Deliverable 2: How Claude Code orchestrates subagents

Claude Code employs sophisticated orchestration through multiple mechanisms:

### Automatic selection algorithm

Claude analyzes tasks using:
1. **Context analysis** - Examines complexity and domain requirements
2. **Description matching** - Routes based on subagent description fields
3. **Tool requirement mapping** - Matches needed capabilities with agent permissions
4. **Workload distribution** - Balances tasks across available specialists

### Execution patterns

**Parallel execution (Fork-Join)** enables multiple agents working simultaneously:
```bash
# Multiple specialists analyzing different aspects
"First analyze the security implications, performance bottlenecks, 
and accessibility issues of this component"
→ Triggers: security-auditor + performance-engineer + accessibility-expert
```

**Serial execution (Pipeline)** creates sequential workflows:
```markdown
Phase 1: product-manager → requirements analysis
Phase 2: system-architect → technical design (receives Phase 1 output)
Phase 3: backend-developer → implementation (receives Phase 2 output)
Phase 4: test-automator → validation (receives Phase 3 output)
```

**Hub-and-spoke orchestration** coordinates complex workflows:
```
Central Orchestrator
├── Research Team (parallel)
│   ├── market-researcher
│   └── competitive-analyst
├── Development Team (parallel)
│   ├── backend-architect → api-developer (serial)
│   └── frontend-architect → ui-developer (serial)
└── Quality Gates (serial)
    ├── security-auditor
    └── performance-validator
```

### Context management

Each subagent receives a **fresh 200k token context window**, preventing cross-contamination between tasks. The Response Awareness Methodology enables agents to receive outputs from previous phases while maintaining clean contexts.

### Model selection strategy

Claude intelligently assigns models based on task complexity:
- **Opus**: Complex reasoning, architecture decisions (21+ specialized agents)
- **Sonnet**: Standard development tasks (46+ agents) 
- **Haiku**: Simple formatting, quick checks (11+ agents)
- **Inherit**: Maintains consistency with main conversation

## Deliverable 3: Creating new subagents

### Step-by-step creation process

**1. Identify the specific problem** - Focus on repetitive, specialized tasks that benefit from consistent handling. Start with your top 3 recurring challenges.

**2. Define the subagent structure**:
```markdown
---
name: api-security-validator
description: PROACTIVELY validates API endpoints for OWASP vulnerabilities and security best practices
tools: Read, Grep, Bash(curl *)
model: sonnet
---

You are a senior API security specialist with expertise in OWASP API Security Top 10.

## Core Responsibilities
1. Validate authentication and authorization implementations
2. Check for injection vulnerabilities  
3. Verify rate limiting and DDoS protection
4. Ensure proper data exposure controls

## Process
When analyzing an API endpoint:
1. Review authentication middleware
2. Check input validation and sanitization
3. Verify error handling doesn't leak information
4. Test rate limiting configurations
5. Validate CORS and security headers

## Success Criteria
- All OWASP API Security risks addressed
- Authentication properly implemented
- No sensitive data exposure
- Rate limiting configured
- Security headers present

Provide findings organized as:
- 🔴 Critical (must fix immediately)
- 🟡 Warning (should address soon)  
- 🟢 Suggestion (consider improving)
```

**3. Determine appropriate tool permissions**:
- Read-only agents: `Read, Grep, Glob`
- Development agents: `Read, Write, Edit, Bash`
- Testing agents: `Read, Bash(npm test*)`
- Security agents: `Read, Grep, Bash(security-scan*)`

**4. Place in correct directory**:
- Project-specific: `.claude/agents/agent-name.md`
- User-global: `~/.claude/agents/agent-name.md`

**5. Test and iterate**:
- Start with manual invocation: "Use the api-security-validator to check this endpoint"
- Refine description for better automatic selection
- Adjust tool permissions based on actual needs
- Update system prompt based on performance

### Community-proven patterns

**The specialist pattern** - Deep expertise in narrow domain:
```markdown
name: postgres-optimizer
description: Database performance specialist for PostgreSQL optimization
```

**The orchestrator pattern** - Coordinates multiple agents:
```markdown
name: feature-orchestrator  
description: Manages end-to-end feature development workflow
```

**The validator pattern** - Quality gates and checks:
```markdown
name: accessibility-validator
description: WCAG 2.1 compliance and accessibility testing
```

## Deliverable 4: CLAUDE.md configuration for orchestration

### Hierarchical configuration system

Claude Code uses a four-tier configuration hierarchy where each level can override those below:

1. **Enterprise policy** (`/etc/claude-code/managed-settings.json`)
2. **User-global** (`~/.claude/CLAUDE.md`)
3. **Project-level** (`./CLAUDE.md`)
4. **Session overrides** (`--append-system-prompt`)

### Essential CLAUDE.md structure for subagent invocation

```markdown
# Project: E-Commerce Platform

## Project Overview
Multi-tenant SaaS platform for online retail with microservices architecture.

## Tech Stack
- Frontend: Next.js 14, TypeScript, Tailwind CSS
- Backend: Node.js, Express, GraphQL  
- Database: PostgreSQL, Redis
- Infrastructure: AWS, Kubernetes, Terraform

## Subagent Orchestration Strategy

### Automatic Agent Invocation Rules
- Code changes → Trigger code-reviewer IMMEDIATELY
- New endpoints → Invoke api-documenter + security-auditor
- Database changes → Activate postgres-optimizer  
- Performance issues → Deploy performance-engineer
- Before deployment → Run full-stack-validator sequence

### Task Decomposition Patterns
When receiving complex requests:
1. Break into specialized subtasks
2. Identify parallel vs sequential dependencies
3. Delegate to appropriate specialists
4. Synthesize results for coherent solution

### Quality Gates
All code must pass through:
1. syntax-validator (haiku) - Quick syntax check
2. test-runner (sonnet) - Comprehensive testing
3. security-scanner (opus) - Deep vulnerability analysis  
4. performance-profiler (sonnet) - Resource optimization

## Workflow Configurations

### Feature Development Pipeline
```
/feature "User authentication system"
→ product-manager: Requirements gathering
→ system-architect: Technical design
→ Parallel:
  - backend-developer: API implementation
  - frontend-developer: UI components
  - database-engineer: Schema design
→ test-automator: Test suite creation
→ security-auditor: Vulnerability assessment
→ deployment-engineer: Production rollout
```

### Emergency Response Protocol  
```
/incident "High latency in payment service"
→ Parallel (5-min SLA):
  - incident-responder: Initial triage
  - monitoring-specialist: Metrics analysis
  - stability-engineer: Service health check
→ root-cause-analyst: Deep investigation
→ fix-implementer: Resolution deployment
```

## Environment Configuration
NODE_ENV=development
API_URL=http://localhost:3001
ENABLE_SUBAGENTS=true
MAX_PARALLEL_AGENTS=8
CONTEXT_OPTIMIZATION=true

## Instructions for Claude
- Use ultrathink for complex architectural decisions
- ALWAYS delegate specialized tasks to subagents
- Maintain clean handoffs between agents using structured protocols
- Preserve context across agent transitions
- Monitor token budget and optimize when approaching limits
```

### Advanced orchestration configuration

**Parallel execution limits based on resources**:
```json
{
  "orchestration": {
    "maxParallelAgents": 8,
    "contextWindowOptimization": true,
    "tokenBudget": 100000,
    "modelAllocation": {
      "criticalTasks": "opus",
      "standardTasks": "sonnet",
      "simpleTasks": "haiku"
    }
  }
}
```

**Hook system for automated workflows**:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "subagent",
        "agent": "code-reviewer",
        "automatic": true
      }]
    }]
  }
}
```

**MCP server integration for external tools**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
    }
  }
}
```

## Key insights and best practices

### Start small, scale gradually
The community strongly emphasizes beginning with 1-2 focused agents solving your most painful repetitive tasks before building comprehensive agent libraries. Success correlates with incremental adoption rather than attempting to create dozens of agents upfront.

### The context isolation revolution
Subagents fundamentally solve the context pollution problem by providing each specialist with a fresh 200k token window. This enables longer development sessions without degradation and allows true parallel processing of complex tasks.

### Non-descriptive naming is critical
Perhaps the most important technical finding: Claude's name-based inference will override your custom prompts. Always use abstract names (wildlife, colors, mythology) rather than functional names to maintain full control over agent behavior.

### Production patterns over experimentation
Focus on battle-tested configurations from companies like PubNub rather than experimental "awesome lists." Their production pipeline (`pm-spec → architect-review → implementer-tester`) demonstrates real-world effectiveness.

### Invest in orchestration infrastructure
The most successful implementations use sophisticated orchestration patterns - hub-and-spoke models, quality gates with hooks, and structured handoff protocols between agents. This infrastructure investment pays dividends in reliability and maintainability.

### Model selection impacts cost and performance
Strategic model assignment (Haiku for simple tasks, Opus for complex reasoning) can reduce token consumption by 40-60% while maintaining quality. The "inherit" option ensures consistency when needed.

## Conclusion

Claude Code subagents represent a paradigm shift from monolithic AI assistance to specialized, orchestrated AI teams. Success requires thoughtful implementation focusing on clear agent boundaries, sophisticated orchestration patterns, and continuous refinement based on production feedback. The community has demonstrated that well-implemented subagent systems can transform development workflows, but warns against complexity for complexity's sake - every agent should solve a real, recurring problem with measurable impact.