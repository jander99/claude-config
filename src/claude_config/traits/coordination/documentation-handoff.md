# Documentation Handoff Trait

## Description
Standardized coordination pattern for handoff to technical-writer for documentation generation, API docs, and user guides. This trait ensures consistent documentation practices across all development agents.

## Content

### Technical Writer Coordination

**When to coordinate:**
- When APIs are created or modified
- For user-facing features requiring documentation
- After significant architectural changes
- When configuration or setup procedures change

**Handoff Criteria:**
- API documentation with OpenAPI/Swagger specs
- README updates for new Python packages or significant changes
- Architecture documentation for complex data processing or integration patterns
- User guides for new features or configuration changes
- Technical documentation for deployment procedures

**Documentation Scope:**
- API endpoint documentation with examples
- Configuration file documentation
- Architecture diagrams and system design
- Troubleshooting guides and FAQ sections
- Installation and setup instructions

### Coordination Pattern

```yaml
technical_writer_handoff:
  trigger_conditions:
    - api_endpoints_created_modified
    - user_facing_features_implemented
    - configuration_changes_made
    - architectural_updates_completed

  documentation_types:
    api_documentation:
      - endpoint_specifications
      - request_response_examples
      - authentication_requirements
      - error_handling_documentation

    user_documentation:
      - feature_usage_guides
      - configuration_instructions
      - troubleshooting_procedures
      - best_practices_documentation

    technical_documentation:
      - architecture_diagrams
      - system_integration_guides
      - deployment_procedures
      - performance_tuning_guides

  context_provided:
    - technical_specifications
    - code_examples_and_snippets
    - configuration_templates
    - use_case_scenarios
    - target_audience_definition
```

### Handoff Protocol

**Documentation Request Types:**

**API Documentation:**
- For FastAPI/Flask APIs, ensure OpenAPI specs are complete
- Include authentication and authorization examples
- Provide request/response examples for all endpoints
- Document error codes and handling procedures

**README Updates:**
- For new Python packages or significant changes
- Include installation and setup instructions
- Add usage examples and configuration guidance
- Update dependency requirements and compatibility notes

**Architecture Documentation:**
- For complex data processing or integration patterns
- Include system diagrams and data flow illustrations
- Document design decisions and trade-offs
- Explain scalability and performance considerations

### Handoff Message Template

```
**Documentation Handoff Request**

**Documentation Type:** [API/README/Architecture/User Guide]

**Technical Context:**
- Framework: [FastAPI/Django/Flask/React/etc.]
- Audience: [Developers/End Users/System Administrators]
- Complexity: [Basic/Intermediate/Advanced]

**Content Requirements:**
- [Specific documentation needs]
- [Code examples or API endpoints to document]
- [Configuration or setup procedures]

**Resources Provided:**
- [Links to code files or specifications]
- [Existing documentation to update]
- [Reference materials or standards to follow]
```

## Usage Notes

- **Which agents should use this trait**: ALL development agents (python-engineer, frontend-engineer, devops-engineer, ai-engineer, mobile-engineer, java-engineer, etc.)
- **Customization guidance**: Each agent can specify domain-specific documentation requirements (e.g., API docs for backend agents, component docs for frontend agents)
- **Compatibility requirements**: Clear technical context and examples must be provided for effective documentation

## Implementation Priority
**HIGH** - This trait affects 15+ development agents and ensures consistent documentation quality