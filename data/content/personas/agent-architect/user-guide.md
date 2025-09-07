# User Guide for Claude Agent System Navigation

## Getting Started with the Agent Ecosystem

### Understanding the Three-Tier Agent System

#### Tier 1: Efficiency Agents (Haiku)
**Purpose**: Fast, cost-effective solutions for routine operations
- **When to Use**: Simple tasks like version control, basic documentation
- **Response Time**: Under 2 seconds for most operations
- **Cost**: Most economical option (~1x baseline cost)
- **Examples**: `git-helper` for commits and PRs, `technical-writer` for basic documentation

**Best Use Cases:**
- Creating git commits and managing branches
- Generating basic README files and documentation
- Simple file operations and status checks
- Quick configuration changes
- Basic project setup tasks

#### Tier 2: Specialist Agents (Sonnet)
**Purpose**: Professional-level expertise for development and analysis
- **When to Use**: Feature development, code analysis, research, testing
- **Response Time**: 5-15 seconds for typical development work
- **Cost**: Balanced performance (~2-3x baseline cost)
- **Examples**: All development agents, research agents, QA specialists

**Best Use Cases:**
- Implementing new features and functionality
- Code review and optimization
- Research and analysis tasks
- Testing and quality assurance
- Database design and optimization
- Security implementation
- Performance optimization

#### Tier 3: Strategic Agents (Opus)
**Purpose**: Advanced analysis and complex decision-making
- **When to Use**: Architecture decisions, complex problems, strategic guidance
- **Response Time**: 15-45 seconds for comprehensive analysis
- **Cost**: Premium performance (~4-5x baseline cost)
- **Examples**: `sr-architect`, `sr-ai-researcher`, `agent-architect`

**Best Use Cases:**
- System architecture decisions
- Complex problem resolution after multiple failed attempts
- Strategic planning and guidance
- Multi-domain integration challenges
- Crisis resolution and system recovery
- Advanced research requiring deep analysis

### How Agents Are Automatically Selected

#### Proactive Agent Detection
The system automatically detects which agent to use based on:
- **File Patterns**: `.py` files → python-engineer, `package.json` → frontend-engineer
- **Project Structure**: React components → frontend-engineer, Docker files → devops-engineer
- **Task Content**: ML libraries → ai-engineer, database schemas → database-engineer
- **Keywords**: "test" → qa-engineer, "security" → security-engineer

#### Manual Agent Selection
You can explicitly request specific agents:
```
"Have the python-engineer help me implement authentication"
"Ask the sr-architect to review this system design"
"Use the security-engineer to audit this code"
```

### Understanding Agent Coordination

#### Standard Workflow Patterns
Most tasks follow predictable patterns:
1. **Detection**: System identifies the right agent for your request
2. **Implementation**: Specialist agent performs the work
3. **Quality Check**: qa-engineer validates the output (for development tasks)
4. **Documentation**: technical-writer creates user-facing docs (when needed)
5. **Version Control**: git-helper manages commits and PRs

#### Multi-Agent Workflows
Complex tasks may involve multiple agents working together:
- **Sequential**: One agent completes work, hands off to another
- **Parallel**: Multiple agents work simultaneously on different components
- **Coordinated**: Project-coordinator manages complex multi-agent workflows

## Working Effectively with Agents

### Providing Clear Context

#### Essential Information to Include
- **What you want to accomplish**: Clear goal statement
- **Current project context**: What you're working on
- **Constraints**: Time limits, requirements, limitations
- **Quality expectations**: Performance requirements, standards
- **Integration needs**: How this fits with existing code

#### Context Examples

**Good Context:**
```
"I need to add user authentication to my FastAPI project. The project already uses PostgreSQL and has a User model. I need JWT token-based auth with login/logout endpoints and middleware for protected routes."
```

**Poor Context:**
```
"Add authentication to my app"
```

**Great Context for Complex Tasks:**
```
"I'm building a React e-commerce frontend that needs to integrate with our existing Python/FastAPI backend. The backend has user authentication and product APIs. I need to create a shopping cart component that persists cart state, handles quantity updates, and integrates with the checkout process. Performance is important as we expect high traffic."
```

### Quality Control and Validation

#### When QA Engineer Gets Involved
The qa-engineer automatically coordinates on:
- New feature implementations
- Code changes affecting functionality
- Integration work between systems
- Performance-critical implementations
- Security-related changes

#### What to Expect from QA Review
- **Test Strategy**: Appropriate testing approach for your changes
- **Test Implementation**: Actual test code when needed
- **Quality Validation**: Verification that implementation meets requirements
- **Integration Testing**: Testing of interactions between components

#### Working with QA Feedback
- Review suggested tests and ask questions if unclear
- Provide additional context if QA identifies missing requirements
- Collaborate on edge cases and error scenarios
- Confirm acceptance criteria before implementation completion

### Agent Escalation and Senior Support

#### When Escalation Happens Automatically
The system escalates to senior agents when:
- A specialist agent fails to complete a task after 3 attempts
- The problem requires architecture-level decisions
- Multiple domains need coordination (e.g., AI + security + performance)
- Complex integration challenges arise
- System-wide impact needs consideration

#### Working with Senior Agents
- **Be patient**: Senior agents provide deeper analysis and take more time
- **Provide comprehensive context**: Senior agents need full system understanding
- **Ask strategic questions**: Focus on architecture, approach, and long-term implications
- **Leverage their expertise**: Ask about best practices and alternative approaches

#### Common Escalation Scenarios
- **sr-architect**: Complex system design, technology selection, performance architecture
- **sr-ai-researcher**: Advanced ML/AI problems, research methodology, model architecture
- **sr-quant-analyst**: Complex financial modeling, risk analysis, regulatory compliance
- **agent-architect**: Agent system issues, coordination problems, meta-system questions

### Best Practices for Agent Interaction

#### Communication Guidelines

**Be Specific and Contextual:**
- Include relevant file paths and current code
- Explain your project setup and technology stack
- Describe what you've already tried
- Specify your success criteria

**Ask for What You Need:**
- Request implementation if you want code written
- Ask for analysis if you need understanding
- Request testing if you need validation
- Ask for documentation if you need explanations

**Provide Feedback:**
- Let agents know if their output meets your needs
- Ask for adjustments if something isn't quite right
- Request clarification on anything unclear
- Confirm when work is complete and satisfactory

#### Optimization Tips

**For Better Performance:**
- Use Tier 1 agents for simple operations
- Provide clear, complete context upfront to avoid back-and-forth
- Let the system auto-select agents when possible
- Use specific agent requests only when you need particular expertise

**For Better Quality:**
- Allow qa-engineer coordination for development tasks
- Don't skip the testing phase for important functionality
- Ask for technical-writer documentation on user-facing features
- Request code review when implementing complex logic

**For Cost Efficiency:**
- Start with specialist (Tier 2) agents for most development work
- Only escalate to senior (Tier 3) agents when truly needed
- Use efficient (Tier 1) agents for routine operations
- Batch related requests to minimize context switching

### Managing Complex Projects

#### Project Coordinator Integration
For complex projects, the project-coordinator can help with:
- **Multi-agent workflows**: Coordinating multiple development streams
- **Timeline management**: Planning and tracking complex deliverables
- **Resource coordination**: Managing agent allocation across project phases
- **Stakeholder communication**: Status reporting and milestone tracking
- **Risk management**: Identifying and mitigating project risks

#### When to Request Project Coordination
- Projects involving multiple domains (frontend + backend + database + devops)
- Projects with complex dependencies and timing requirements
- Projects requiring coordination with external stakeholders
- Projects with significant risk or complexity
- Projects needing systematic planning and tracking

### Troubleshooting Common Issues

#### Agent Selection Problems
**Issue**: Wrong agent selected for your task
**Solution**: Explicitly request the correct agent: "Have the database-engineer help with this schema design"

**Issue**: No agent seems to understand your request
**Solution**: Provide more specific context about your technology stack and goals

#### Quality Issues
**Issue**: Output doesn't meet your quality expectations
**Solution**: Provide more specific quality criteria and ask for revision

**Issue**: Tests aren't comprehensive enough
**Solution**: Work with qa-engineer to define more comprehensive test scenarios

#### Coordination Problems
**Issue**: Agents seem to be working at cross-purposes
**Solution**: Request project-coordinator involvement for complex workflows

**Issue**: Handoffs between agents are losing context
**Solution**: Provide comprehensive context at the beginning and confirm handoff details

#### Performance Issues
**Issue**: Agents are taking too long to respond
**Solution**: Check if you're using appropriate tier agents for your task complexity

**Issue**: Getting charged more than expected
**Solution**: Use Tier 1 agents for simple tasks and provide complete context to avoid multiple iterations

### Advanced Usage Patterns

#### Custom Workflows
You can design custom workflows by:
- Requesting specific agent sequences
- Defining handoff points and quality gates
- Specifying coordination requirements
- Setting up validation checkpoints

#### Integration with Development Tools
The agent system integrates with:
- Git workflows and branch management
- IDE and development environment
- Testing frameworks and CI/CD pipelines
- Documentation systems
- Project management tools

#### Learning and Adaptation
The system learns from:
- Your feedback and preferences
- Successful workflow patterns
- Common error patterns and resolutions
- Quality improvements over time
- Integration challenges and solutions

This user guide provides the foundation for effective interaction with the Claude agent ecosystem. As you become more familiar with the system, you'll develop preferences and patterns that work best for your specific projects and work style.