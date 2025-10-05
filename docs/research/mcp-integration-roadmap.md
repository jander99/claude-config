# MCP Integration Roadmap

**Status**: Research & Planning Phase
**Last Updated**: 2025-10-05

## Overview

This document outlines the planned integration of Model Context Protocol (MCP) servers into the claude-config toolkit, enabling subagents to access external tools and knowledge sources.

## Vision

Future subagents will be **MCP-aware**, allowing them to leverage specialized MCP servers for enhanced capabilities:

- **Research agents** → Use context7, deepwiki, arxiv for literature access
- **Data agents** → Use server-memory for persistent data storage
- **Development agents** → Use filesystem, github, git tools
- **Analysis agents** → Use time, web-search for temporal and web data

## Planned MCP Integration Points

### 1. Agent-Level MCP Awareness

**Goal**: Subagents automatically know which MCP servers are available and when to use them.

**Mechanism**:
```yaml
# Example agent YAML with MCP awareness
name: research-engineer
mcp_capabilities:
  preferred_servers:
    - context7        # For library documentation
    - deepwiki        # For comprehensive research
    - server-memory   # For data persistence

  usage_patterns:
    documentation_search: "context7"
    research_synthesis: "deepwiki"
    data_storage: "server-memory"
```

### 2. Master CLAUDE.md Orchestration

**Goal**: The master CLAUDE.md file will include instructions for all agents on MCP server usage.

**Current Implementation**: Global CLAUDE.md already includes MCP integration patterns
**Enhancement Needed**: Project-specific CLAUDE.md with agent-specific MCP guidance

### 3. Path-Specific MCP Configuration

**Goal**: Different directories/projects can have different MCP server configurations.

**Mechanism**:
```
project/
├── .claude/
│   └── mcp-config.json     # Project-specific MCP servers
├── CLAUDE.md               # Project-specific agent instructions
└── [project files]
```

## MCP Server Categories

### Research & Documentation
- **context7**: Library documentation and API reference
- **deepwiki**: Comprehensive project documentation
- **arxiv**: Academic paper search and retrieval

### Data & Memory
- **server-memory**: Knowledge graph for persistent data
- **filesystem**: File operations and management
- **sqlite**: Database operations

### Development Tools
- **github**: Repository operations and code search
- **git**: Version control operations
- **sequential-thinking**: Complex problem solving

### Time & Web
- **time**: Timezone and temporal operations
- **web-search**: Real-time web information
- **web-fetch**: URL content retrieval

## Implementation Phases

### Phase 1: Research & Documentation (Current)
- ✅ Document MCP integration vision
- ✅ Identify key MCP servers for agent categories
- ⏳ Design agent YAML schema for MCP awareness

### Phase 2: Agent Template Enhancement
- ⏳ Add MCP capability fields to agent YAML schema
- ⏳ Update Jinja2 templates to include MCP instructions
- ⏳ Create examples of MCP-aware agents

### Phase 3: CLAUDE.md Integration
- ⏳ Enhance master CLAUDE.md with MCP orchestration
- ⏳ Create project-specific CLAUDE.md templates
- ⏳ Document MCP usage patterns for each agent type

### Phase 4: Path-Specific Configuration
- ⏳ Design path-specific MCP config schema
- ⏳ Implement config loading and merging logic
- ⏳ Create CLI commands for MCP management

## Example: Research Agent with MCP

**Future YAML Definition**:
```yaml
name: ai-researcher
display_name: AI Researcher
model: sonnet
description: AI research specialist with MCP-enabled literature access

mcp_awareness:
  required_servers:
    - server-memory    # For storing research findings

  preferred_servers:
    - context7         # For ML library documentation
    - deepwiki         # For comprehensive research

  usage_instructions: |
    When conducting research:
    1. Use context7 for library API documentation
    2. Use deepwiki for project-specific deep dives
    3. Store findings in server-memory for future reference
    4. Use sequential-thinking for complex analysis

proactive_triggers:
  user_intent_patterns:
    keywords:
      - "research this library"
      - "find documentation for"
      - "what does the research say"
```

**Generated Agent Instructions** (future):
```markdown
## MCP Server Integration

This agent has access to the following MCP servers:

**Required**:
- `server-memory`: Store research findings for future reference

**Preferred**:
- `context7`: Library documentation and API references
- `deepwiki`: Comprehensive project research

### Usage Patterns

When conducting research:
1. Use `mcp__context7__get-library-docs` for API documentation
2. Use `mcp__deepwiki__deepwiki_fetch` for deep research
3. Store findings with `mcp__server-memory__create_entities`
4. Use `mcp__sequentialthinking__sequentialthinking` for analysis
```

## Custom Command Library Integration

Future enhancement: Agents should be able to reference custom slash commands defined in `.claude/commands/`.

**Example**:
```yaml
name: test-engineer
custom_commands:
  - /run-tests      # Trigger comprehensive test suite
  - /coverage       # Generate coverage report
  - /lint           # Run linting checks
```

## Open Questions

1. **MCP Server Discovery**: How do agents discover available MCP servers at runtime?
2. **Fallback Behavior**: What should agents do when preferred MCP servers are unavailable?
3. **Cost Optimization**: How to balance MCP tool usage with token costs?
4. **Security**: How to control which agents can access which MCP servers?

## References

- [MCP Server Documentation](https://github.com/anthropics/mcp)
- Current MCP servers in use: github, time, filesystem, server-memory, ide, context7, deepwiki, sequential-thinking

---

**This is a living document** - Update as MCP integration progresses.
