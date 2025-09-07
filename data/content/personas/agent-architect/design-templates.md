# Agent Design Templates and Standards

## Overview

This document provides comprehensive design templates and standards for creating new agents within the Claude Code ecosystem. These templates ensure consistency, quality, and proper integration while maintaining the system's coordination patterns and performance characteristics.

## Design Template Framework

### Core Agent Template

```yaml
---
name: [agent-name]
description: [Brief description with proactive context]. Use [when/why] for [specific scenarios]. [Specialized trait count and context]
model: [haiku|sonnet|opus]
---

[Extended description with proactive activation guidance]. Use PROACTIVELY when working with projects detected by file patterns and project indicators. Coordinates with other agents for validation and specialized tasks. [Required safety protocols].

## Core Responsibilities
- [Primary responsibility 1 - action-oriented]
- [Primary responsibility 2 - specific deliverables]
- [Primary responsibility 3 - coordination aspect]
- [Additional responsibilities - 4-8 total]

## Expertise Areas
- [Technical expertise area 1 with specific technologies]
- [Domain expertise area 2 with methodologies]
- [Integration expertise area 3 with coordination patterns]
- [Additional expertise areas - 4-8 total]

## Proactive Activation
This agent automatically activates when detecting:

**File Patterns:**
- `pattern1.*`
- `directory/`
- `config.type`

**Project Indicators:**
- keyword1
- specific context
- integration pattern
- domain identifier

## [Domain Section 1]

<!-- Content file reference: personas/[agent-name]/[domain-section-1].md -->

## [Domain Section 2]

<!-- Content file reference: personas/[agent-name]/[domain-section-2].md -->

[Additional domain sections as needed]
```

### Model Selection Criteria

**Haiku Model (Tier 1 - Efficiency):**
- Simple, routine operations
- Fast response requirements
- Cost-sensitive frequent tasks
- Clear, well-defined scope

**Usage Examples:**
- File operations and basic git workflows
- Simple documentation generation
- Status checks and quick queries
- Routine maintenance tasks

**Sonnet Model (Tier 2 - Specialist):**
- Standard development work
- Domain-specific expertise
- Balanced performance requirements
- Complex but well-understood domains

**Usage Examples:**
- Feature development across languages
- Code review and testing
- Research and analysis
- Integration and coordination tasks

**Opus Model (Tier 3 - Strategic):**
- Complex strategic decisions
- Cross-domain integration
- Advanced problem-solving
- System-level architecture

**Usage Examples:**
- System architecture and design
- Complex escalation resolution
- Multi-domain synthesis
- Strategic planning and analysis

## Agent Specialization Framework

### Specialization Levels

**Primary Specialists (4-6 traits):**
- Deep domain expertise in specific technology or methodology
- Clear boundaries and well-defined scope
- Standard coordination patterns with other agents
- Moderate complexity handling within domain

**Senior Specialists (3-4 traits):**
- Advanced expertise across multiple related domains
- Complex problem-solving and strategic guidance
- Escalation targets for primary specialists
- Cross-system integration capabilities

**Meta-System Agents (1-2 traits):**
- System-wide coordination and optimization
- Agent ecosystem management
- Cross-cutting concerns and patterns
- High-level strategic guidance

### Trait Definition Standards

**Technical Traits:**
- Language/Framework Proficiency
- Domain-Specific Methodologies
- Tool and Platform Integration
- Performance and Optimization

**Coordination Traits:**
- Inter-Agent Communication Patterns
- Handoff and Escalation Protocols
- Quality Assurance Integration
- Documentation and Knowledge Transfer

**Safety Traits:**
- Branch Management and Git Safety
- Data Protection and Security
- Error Handling and Recovery
- Compliance and Standards

## Content Section Templates

### Domain Expertise Section Template

```markdown
## [Domain Name]

### Core Methodologies

**[Methodology 1]:**
- **Approach**: [How this methodology is applied]
- **Use Cases**: [When to use this methodology]
- **Integration**: [How it coordinates with other approaches]
- **Validation**: [How to verify successful application]

**[Methodology 2]:**
[Same structure as above]

### Technology Integration

**[Technology/Framework 1]:**
- **Current Version**: [Version and compatibility notes]
- **Best Practices**: [Current recommended approaches]
- **Common Patterns**: [Frequently used implementation patterns]
- **Migration Considerations**: [Upgrade and compatibility guidance]

### Implementation Guidelines

**Development Workflow:**
1. [Step 1 with specific actions]
2. [Step 2 with validation criteria]
3. [Step 3 with coordination requirements]
4. [Additional steps as needed]

**Quality Standards:**
- [Quality criterion 1 with measurable outcomes]
- [Quality criterion 2 with validation methods]
- [Quality criterion 3 with success metrics]

### Coordination Patterns

**With [Agent Type]:**
- [Specific coordination scenario and protocol]
- [Handoff points and required information]
- [Success criteria and validation steps]

**Escalation Triggers:**
- [Condition 1 that requires escalation]
- [Condition 2 with specific escalation path]
- [Resolution criteria and follow-up protocols]
```

### Safety Protocol Template

```markdown
## [Safety Domain] (Safety)

[Brief description of safety concern and protection scope]

## [Safety Domain] Protocol

**CRITICAL: [Primary safety requirement]**

### [Safety Check Category]
1. **[Check Name]**:
   ```bash
   [command or verification step]
   ```

2. **[Protection Action]**:
   - [Specific protection requirement]
   - [User confirmation requirement]
   - [Proceed/halt decision criteria]

3. **[Safety Guidance]**:
   - [Guideline 1 with specific actions]
   - [Guideline 2 with examples]
   - [Guideline 3 with validation steps]

### [Safety Rules Category]
- **[Rule Type]** [specific requirement]
- **[Rule Type]** [confirmation requirement]
- **[Rule Type]** [procedural requirement]
- **[Rule Type]** [validation requirement]

### Coordination Patterns

**[Safety Trigger]**
- Trigger: [specific condition detection]
- Action: [required safety action]
- Required Context: [necessary information for safety decision]

**[Protection Verification]**
- Trigger: [verification requirement condition]
- Action: [verification steps and validation]
- Required Context: [context needed for verification]
```

### Coordination Template

```markdown
## [Coordination Domain] (Coordination)

[Brief description of coordination purpose and integration scope]

## [Coordination Purpose] Protocol

### [Coordination Scenario]

**[Coordination Context]:**

1. **[Coordination Step]**:
   - [Specific coordination action]
   - [Information requirements]
   - [Success criteria]

2. **[Integration Step]**:
   - [Integration action with specific agent]
   - [Context transfer requirements]
   - [Validation and feedback mechanisms]

3. **[Handoff Step]**:
   - [Handoff criteria and information]
   - [Receiving agent requirements]
   - [Follow-up and monitoring needs]

### [Coordination Flow]
```
[Process Step 1] → [Process Step 2] → [Process Step 3] → [Outcome]
```

**Coordination Examples:**
- "[Agent] should [specific action] with [context/criteria]"
- "[Agent] should [specific coordination] for [scenario]"
- "[Agent] should [integration action] with [system/component]"

### Coordination Patterns

**[Pattern Name]**
- Trigger: [activation condition]
- Action: [coordination action with specific agent]
- Required Context: [necessary context for coordination]

**[Integration Pattern]**
- Trigger: [integration requirement condition]
- Action: [integration steps and validation]
- Required Context: [context needed for integration success]
```

## Agent Integration Standards

### Proactive Activation Patterns

**File Pattern Detection:**
- Use specific file extensions and directory structures
- Include configuration files and project markers
- Consider dependency files and framework indicators
- Balance specificity with broad applicability

**Project Indicator Keywords:**
- Domain-specific terminology
- Technology stack indicators  
- Methodology and process keywords
- Integration and coordination terms

**Context Verification Requirements:**
- Confirm project type alignment with agent expertise
- Verify required dependencies and prerequisites
- Check for existing patterns and conventions
- Validate coordination requirements with other agents

### Quality Assurance Integration

**Testing Coordination Requirements:**
- All development agents MUST coordinate with qa-engineer
- Provide comprehensive context about implemented features
- Specify testing frameworks and validation requirements
- Include edge cases and integration testing needs

**Documentation Integration:**
- User-facing features require technical-writer coordination
- Provide implementation context and usage patterns
- Include API specifications and integration guides
- Specify target audience and documentation type

### Branch Safety Integration

**Universal Requirements:**
- All development agents MUST check branch status
- Protected branch detection and user confirmation
- Appropriate branch naming suggestions
- Wait for user approval before proceeding

**Branch Naming Standards:**
- `feature/[agent-type]-[feature-name]`
- `fix/[agent-type]-[issue-description]`
- `architecture/[system-component]`
- `refactor/[component-name]`

## Validation and Testing Standards

### Agent Functionality Validation

**Core Function Testing:**
- Verify proactive activation on expected patterns
- Test coordination handoffs with other agents
- Validate safety protocol enforcement
- Confirm escalation trigger conditions

**Integration Testing:**
- Cross-agent coordination workflows
- Handoff information completeness
- Error handling and recovery procedures
- Performance under typical usage patterns

**Performance Validation:**
- Response time within acceptable thresholds
- Resource utilization monitoring
- Cost efficiency relative to model tier
- Success rate for typical task completion

### Content Quality Standards

**Technical Accuracy:**
- Current best practices and methodology alignment
- Framework and technology version compatibility
- Security and compliance requirement coverage
- Integration pattern correctness

**Usability Standards:**
- Clear, actionable guidance
- Appropriate detail level for target users
- Logical organization and navigation
- Consistent terminology and conventions

**Maintenance Requirements:**
- Regular content review and updates
- Technology stack evolution tracking
- Performance metric monitoring
- User feedback integration

## Deployment and Lifecycle Management

### Agent Deployment Process

1. **Design Validation**: Template compliance and integration review
2. **Content Creation**: Complete all required content sections
3. **Testing Phase**: Functionality and integration testing
4. **Documentation**: User guides and coordination documentation
5. **Production Deployment**: Staged rollout with monitoring
6. **Performance Monitoring**: Success metrics and optimization

### Lifecycle Maintenance

**Regular Review Cycles:**
- Monthly performance and usage analysis
- Quarterly content and methodology updates
- Annual architecture and integration review
- Event-driven updates for major technology changes

**Optimization Opportunities:**
- Usage pattern analysis for model tier optimization
- Coordination efficiency improvements
- Content gap identification and resolution
- Cross-agent collaboration enhancement

### Retirement and Evolution

**Retirement Criteria:**
- Technology obsolescence or replacement
- Coordination pattern changes
- Performance degradation below thresholds
- User adoption below minimum viable levels

**Evolution Pathways:**
- Capability expansion and new domain integration
- Model tier optimization based on usage patterns
- Coordination pattern enhancement
- Specialization refinement and focus areas

## Best Practices Summary

### Design Principles
1. **Single Responsibility**: Each agent has clear, focused expertise
2. **Coordination First**: Design for seamless inter-agent workflows
3. **Safety Integration**: Built-in safety protocols and validations
4. **Performance Optimization**: Appropriate model tier selection
5. **Extensibility**: Design for future capability expansion

### Implementation Guidelines
1. **Follow Templates**: Use established patterns for consistency
2. **Complete Content**: Ensure all sections have comprehensive coverage
3. **Test Thoroughly**: Validate functionality and integration
4. **Document Clearly**: Provide clear usage and coordination guidance
5. **Monitor Performance**: Track success metrics and optimization opportunities

### Coordination Standards
1. **Proactive Activation**: Clear triggers and context verification
2. **Handoff Protocols**: Complete information transfer
3. **Safety Enforcement**: Universal safety protocol compliance
4. **Quality Integration**: Mandatory testing and documentation coordination
5. **Escalation Management**: Clear paths and context requirements

This template framework ensures consistent, high-quality agent development while maintaining the system's coordination excellence and performance optimization characteristics.