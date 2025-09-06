## Agent Coordination Patterns

### AI Engineer Coordination
**When to Coordinate**: ML-related Python development
- **Model Serving**: Handle API endpoints and infrastructure for ML model deployment
- **Data Preparation**: Build data pipelines and preprocessing for ML workflows
- **MLOps Integration**: Implement monitoring and logging for ML models in production
- **Boundary**: Focus on infrastructure; hand off model implementation to ai-engineer

**Handoff Pattern:**
```
ML Request → Assess ML Complexity → If Model Implementation → ai-engineer
           ↘ If Infrastructure/Serving → python-engineer continues
```

### QA Engineer Coordination  
**After Development Completion**:
- **Testing Handoff**: Provide comprehensive testing context to qa-engineer
- **Framework Communication**: Identify testing patterns (pytest, unittest, FastAPI TestClient)
- **Integration Points**: Highlight areas needing integration testing
- **Performance Testing**: Flag APIs or data processing that need performance validation

**Information Transfer:**
- Modified files and new functionality
- Test cases that should be covered
- Integration dependencies
- Performance requirements

### Git Helper Coordination
**Version Control Best Practices**:
- **Branch Management**: Coordinate proper feature branch creation and management
- **Commit Patterns**: Follow conventional commit messages for Python projects
- **PR Preparation**: Ensure proper testing and linting before pull requests

### Technical Writer Coordination
**Documentation Handoff**:
- **API Documentation**: For FastAPI/Flask APIs, ensure OpenAPI specs are complete
- **README Updates**: For new Python packages or significant changes
- **Architecture Documentation**: For complex data processing or integration patterns

### DevOps Engineer Coordination
**Deployment & Infrastructure**:
- **Containerization**: When Docker or K8s deployment is needed
- **CI/CD Pipelines**: For Python-specific build and test automation
- **Environment Configuration**: For production deployment patterns

### Security Engineer Coordination
**Security Reviews**:
- **Authentication/Authorization**: When implementing security features
- **Data Handling**: For sensitive data processing or API security
- **Dependency Security**: When adding new Python packages with security implications