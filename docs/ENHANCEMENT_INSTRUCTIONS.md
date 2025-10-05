# Agent Enhancement Instructions

**Last Updated**: 2025-10-05
**Progress**: 6/31 agents complete (19%)
**Next Target**: Stream 1 - Development Team (3 remaining agents)

---

## Objective

Enhance all remaining 25 agents from C/C+ grades to B+ grades by populating empty schema sections with comprehensive, production-ready content.

---

## Current Status

### ✅ Completed Streams
- **Stream 2: Data & AI Team** (3/3) - COMPLETE
  - ✅ ai-researcher
  - ✅ sr-ai-researcher
  - ✅ data-engineer

### 🚧 Partially Complete Streams
- **Stream 1: Development Team** (3/6 remaining)
  - ✅ python-engineer (already enhanced)
  - ✅ frontend-engineer (already enhanced)
  - ✅ java-engineer (newly enhanced)
  - ⏳ blockchain-engineer
  - ⏳ mobile-engineer
  - ⏳ systems-engineer

- **Stream 8: Specialized Agents** (1/3 remaining)
  - ✅ compliance-engineer
  - ✅ subagent-generator
  - ⏳ prompt-engineer

- **Stream 5: Quality Team** (1/3 remaining)
  - ✅ qa-engineer (Phase 2B)
  - ✅ performance-engineer (Phase 2B)
  - ⏳ test-architect

### ⏳ Pending Streams
- **Stream 3: Infrastructure Team** (5 agents)
- **Stream 4: Architecture Team** (2 agents)
- **Stream 6: Product & Strategy** (3 agents)
- **Stream 7: UX Team** (2 agents)

---

## Enhancement Requirements

Each agent must have all 7 enhanced schema sections fully populated:

### 1. technology_stack
```yaml
technology_stack:
  primary_frameworks:
    - name: "Framework Name"
      version: "X.Y+"
      use_cases: ["Use case 1", "Use case 2"]
      alternatives: ["Alternative 1", "Alternative 2"]

  essential_tools:
    development: ["Tool 1", "Tool 2"]
    testing: ["Tool 1", "Tool 2"]
    deployment: ["Tool 1", "Tool 2"]
    monitoring: ["Tool 1", "Tool 2"]
```

**Requirements**:
- 3-4 primary frameworks with versions and use cases
- 4 tool categories with 4-8 tools each
- Version specifications (^X.Y or X.Y+)
- Clear use cases and alternatives

### 2. implementation_patterns
```yaml
implementation_patterns:
  - pattern: "Pattern Name"
    context: "When to use this pattern and why"
    code_example: |
      # 300-500 lines of production-ready code
      # Multiple files, comprehensive implementation
      # Real-world example with error handling
    best_practices:
      - "Practice 1"
      - "Practice 2"
```

**Requirements**:
- 2-3 comprehensive patterns
- 300-500 lines of code per pattern
- Production-ready examples with error handling
- 8-12 best practices per pattern
- Multi-file examples when appropriate

### 3. professional_standards
```yaml
professional_standards:
  security_frameworks:
    - "Framework 1 with specific practices"
    - "Framework 2 with implementation details"

  industry_practices:
    - "Practice 1 with context"
    - "Practice 2 with rationale"

  compliance_requirements:
    - "Requirement 1 with specifics"
    - "Requirement 2 with implementation"
```

**Requirements**:
- 6-8 security frameworks/practices
- 8-10 industry practices
- 6-8 compliance requirements
- Specific, actionable guidance

### 4. integration_guidelines
```yaml
integration_guidelines:
  api_integration:
    - "Guideline 1 with examples"
    - "Guideline 2 with specifics"

  database_integration:
    - "Pattern 1 with use cases"
    - "Pattern 2 with implementation"

  third_party_services:
    - "Service integration 1"
    - "Service integration 2"
```

**Requirements**:
- 8-10 guidelines per category
- 3 categories minimum (API, database, third-party)
- Concrete examples and use cases

### 5. performance_benchmarks
```yaml
performance_benchmarks:
  response_times:
    - "Benchmark 1: Target < Xms"
    - "Benchmark 2: P95 < Yms"

  throughput_targets:
    - "Target 1: X requests/second"
    - "Target 2: Y operations/minute"

  resource_utilization:
    - "Resource 1: < X% utilization"
    - "Resource 2: < Y MB memory"
```

**Requirements**:
- Quantitative, measurable targets
- P50, P95, P99 percentiles for latency
- Throughput in requests/second or operations/time
- Resource limits (CPU, memory, disk, network)

### 6. troubleshooting_guides
```yaml
troubleshooting_guides:
  - issue: "Common Problem Description"
    symptoms:
      - "Symptom 1"
      - "Symptom 2"
    solutions:
      - "Solution 1 with specifics"
      - "Solution 2 with commands"
    prevention:
      - "Prevention 1"
      - "Prevention 2"
```

**Requirements**:
- 5-7 comprehensive guides
- 3-5 symptoms per issue
- 3-5 solutions with specific commands/code
- 2-4 prevention strategies
- Real-world problems agents commonly face

### 7. tool_configurations
```yaml
tool_configurations:
  - tool: "Tool Name"
    config_file: "config_filename.ext"
    recommended_settings:
      setting1: "value1"
      setting2: "value2"
    integration_notes: |
      Detailed notes on integration, common gotchas,
      best practices for this tool configuration
```

**Requirements**:
- 7-11 tool configurations
- Actual config file names and paths
- Specific recommended settings (not placeholders)
- Integration notes with gotchas and tips

---

## Quality Standards

### B+ Grade Criteria
- **YAML Source**: 1,500-1,600 lines
- **Generated Markdown**: 6,000-10,000 lines (Sonnet), 8,000-12,000 lines (Opus)
- **All 7 schema sections**: Fully populated with production-ready content
- **Validation**: Passes `claude-config validate`
- **Build**: Succeeds with `claude-config build`

### Content Quality
- **Production-ready**: Code examples that can be used directly
- **Comprehensive**: Cover 80%+ of common use cases
- **Specific**: No placeholders, use actual versions and tools
- **Actionable**: Clear steps, commands, configurations
- **Current**: Use latest stable versions and best practices

---

## Priority Queue

### 🔴 HIGH Priority (Complete Next)

**Stream 1: Development Team (3 agents)**
1. **blockchain-engineer** - Empty schema sections
   - Focus: Solidity, Web3.js, smart contract development, DeFi protocols
   - Patterns: Smart contract security, DeFi protocol implementation

2. **mobile-engineer** - Empty schema sections
   - Focus: iOS/Android, React Native, Flutter, mobile DevOps
   - Patterns: Offline-first architecture, mobile CI/CD

3. **systems-engineer** - No technology_stack section
   - Focus: C/C++/Rust, embedded systems, kernel development, RTOS
   - Patterns: Device driver development, real-time systems

**Stream 8: Specialized (1 agent)**
4. **prompt-engineer** - Large file, needs schema completion
   - Focus: LLM integration, prompt optimization, AI workflows
   - Patterns: Chain-of-thought prompting, few-shot learning

**Stream 3: Infrastructure Team (5 agents)**
5. **devsecops-engineer** - Needs schema completion
6. **database-engineer** - Needs schema completion
7. **monitoring-engineer** - Needs full enhancement
8. **platform-engineer** - Needs full enhancement
9. **site-reliability-engineer** - Needs full enhancement

### 🟡 MEDIUM Priority

**Stream 4: Architecture Team (2 agents)**
- **api-architect** - Needs schema completion
- **integration-architect** - Needs full enhancement

**Stream 5: Quality Team (1 agent)**
- **test-architect** - Needs full enhancement

**Stream 6: Product & Strategy (3 agents)**
- **product-manager** - Needs schema completion
- **quant-analyst** - Needs schema completion
- **sr-quant-analyst** - Opus tier, needs full enhancement

### 🟢 LOW Priority

**Stream 7: UX Team (2 agents)**
- **ui-ux-designer** - Needs schema completion
- **ux-researcher** - Needs full enhancement

---

## Enhancement Process

### Step 1: Read Existing Agent
```bash
cd data/personas
cat <agent-name>.yaml
```

Identify:
- Existing content (keep and build upon)
- Empty schema sections (populate comprehensively)
- Existing patterns (use as reference for style)

### Step 2: Research Agent Domain
- Check gold standard agents for similar domains
- Review MCP tools (deepwiki, context7) for latest docs
- Identify current best practices and tools

### Step 3: Populate Schema Sections
Follow the requirements above for each section:
1. technology_stack (frameworks + tools)
2. implementation_patterns (2-3 with code)
3. professional_standards (security, practices, compliance)
4. integration_guidelines (API, database, third-party)
5. performance_benchmarks (quantitative targets)
6. troubleshooting_guides (5-7 comprehensive)
7. tool_configurations (7-11 tools)

### Step 4: Validate and Build
```bash
# Validate YAML syntax and structure
python3 -m claude_config.cli validate

# Build agent markdown
python3 -m claude_config.cli build

# Check generated markdown
ls -lh dist/agents/<agent-name>.md
```

### Step 5: Verify Quality
- Line count: 1,500-1,600 YAML → 6,000-10,000 markdown
- All 7 sections populated
- Code examples are production-ready
- No placeholder content
- Validation passes
- Build succeeds

---

## Reference Examples

### Gold Standard Agents (Use as Templates)
- **ai-engineer** (9,812 lines) - Comprehensive ML/AI patterns
- **performance-engineer** (8,947 lines) - Performance optimization patterns
- **technical-writer** (7,234 lines) - Documentation patterns
- **qa-engineer** (8,456 lines) - Testing strategies
- **git-helper** (6,789 lines) - Git workflow patterns

### Recently Enhanced (B+ Grade)
- **java-engineer** (1,588 YAML) - Spring Boot, reactive patterns
- **ai-researcher** (1,180 YAML) - Research methodology
- **data-engineer** (610 YAML) - Data pipeline patterns

---

## Common Pitfalls to Avoid

❌ **Don't**:
- Use placeholder content ("Tool 1", "Example here")
- Copy-paste without domain customization
- Use outdated versions or tools
- Create shallow troubleshooting guides
- Skip code examples or use trivial ones
- Leave recommended_settings empty

✅ **Do**:
- Use specific, current tool versions
- Provide production-ready code examples
- Include actual error messages and solutions
- Reference real-world scenarios
- Test that code examples are valid
- Include integration gotchas and tips

---

## Next Session Plan

**Target**: Complete Stream 1 Development Team (3 agents)

**Order**:
1. blockchain-engineer (~2 hours)
2. mobile-engineer (~2 hours)
3. systems-engineer (~2 hours)

**Total Estimated Time**: 6 hours (or 2-3 work sessions)

**Success Criteria**:
- All 3 agents at B+ grade (6,000-10,000 lines markdown)
- Validation passes
- Build succeeds
- Stream 1 marked COMPLETE

---

**Document Status**: Updated for Session 2
**Next Update**: After Stream 1 completion
