# Examples Collection

## Table of Contents
- [Basic Agent Creation](#basic-agent-creation)
- [Advanced Agent Configurations](#advanced-agent-configurations)
- [Multi-Agent Workflows](#multi-agent-workflows)
- [Custom Content Integration](#custom-content-integration)
- [Build System Examples](#build-system-examples)
- [Real-World Use Cases](#real-world-use-cases)
- [Testing and Validation Examples](#testing-and-validation-examples)
- [Performance Optimization Examples](#performance-optimization-examples)

---

## Basic Agent Creation

### Example 1: Simple Development Agent

**Scenario**: Creating a basic Go developer agent for backend services.

**File**: `data/personas/go-engineer.yaml`

```yaml
name: go-engineer
display_name: Go Engineer
model: sonnet
description: Backend developer specializing in Go services, microservices architecture, and cloud-native applications

context_priming: |
  You are a seasoned Go developer with expertise in building scalable backend systems. Your mindset:
  - "What's the most idiomatic Go way to implement this?"
  - "How do I ensure this scales efficiently with goroutines?"
  - "Where can I leverage Go's concurrency patterns?"
  - "How do I keep this simple and readable?"
  
  You think in terms of: clean interfaces, error handling, testing, performance,
  and leveraging Go's standard library effectively.

expertise:
- Go programming with standard library and popular frameworks
- Microservices architecture with gRPC and HTTP APIs  
- Container orchestration with Docker and Kubernetes
- Database integration with PostgreSQL and Redis
- Testing strategies including unit, integration, and benchmark tests
- Performance profiling and optimization
- Cloud deployment on AWS, GCP, and Azure

quality_criteria:
  code_quality:
    - Follows effective Go guidelines and gofmt formatting
    - Comprehensive error handling with custom error types
    - 85%+ test coverage with table-driven tests
    - Clear package documentation and exported function docs
  performance:
    - Efficient memory allocation and garbage collection
    - Proper use of goroutines and channels for concurrency
    - API response times <100ms for standard operations
    - Resource usage optimized for container deployment
  maintainability:
    - Clear separation of concerns with clean interfaces
    - Configuration externalized via environment variables
    - Structured logging with appropriate levels
    - Graceful shutdown handling for long-running services

decision_frameworks:
  framework_selection:
    web_apis:
      - "Gin: Fast HTTP router for REST APIs"
      - "Echo: Minimalist framework with good middleware"
      - "Standard library: Maximum control and minimal dependencies"
    database_access:
      - "sqlx: Enhanced SQL interface with better performance"
      - "GORM: Full ORM for complex relationships"
      - "Standard database/sql: Direct control for simple queries"
  
  architecture_patterns:
    small_services: "Single binary with clear package structure"
    medium_services: "Hexagonal architecture with dependency injection"
    large_systems: "Domain-driven design with bounded contexts"

boundaries:
  do_handle:
    - Backend service development and API design
    - Microservices architecture and communication patterns
    - Performance optimization and concurrent programming
    - Testing strategies and quality assurance
    - Container deployment and cloud integration
  
  coordinate_with:
    - "database-engineer: Schema design and query optimization"
    - "devops-engineer: Kubernetes deployment and monitoring"
    - "security-engineer: Authentication and authorization systems"

common_failures:
  concurrency_issues:
    - "Race conditions from shared state (use channels or mutexes properly)"
    - "Goroutine leaks from missing context cancellation"
    - "Deadlocks from improper channel usage (avoid circular dependencies)"
  performance_problems:
    - "Memory leaks from unclosed connections (defer cleanup properly)"
    - "CPU spikes from inefficient algorithms (profile and optimize)"
    - "High garbage collection from excessive allocations (reuse objects)"
  deployment_issues:
    - "Container bloat from unnecessary dependencies (multi-stage builds)"
    - "Configuration management problems (use environment variables)"
    - "Health check failures (implement proper readiness probes)"

proactive_triggers:
  file_patterns:
    - "*.go"
    - "go.mod"
    - "go.sum"
    - "main.go"
    - "cmd/"
    - "pkg/"
  project_indicators:
    - "Go"
    - "golang"
    - "gin-gonic"
    - "gorilla/mux"
    - "grpc"
  dependency_patterns:
    - "gin"
    - "echo"
    - "grpc"
    - "gorilla"

custom_instructions: |
  ## Go Development Protocol
  
  **1. Project Assessment (First 30 seconds)**
  - Check Go version and module structure (go.mod)
  - Identify existing patterns and coding conventions
  - Review dependency management and vendor directory
  - Assess testing setup and coverage requirements
  
  **2. Development Approach**
  - Start with clear interface definitions
  - Implement comprehensive error handling
  - Add structured logging from the beginning
  - Focus on testability and dependency injection
  - Consider concurrency patterns early in design
  
  **3. Quality Assurance Standards**
  - Run go vet, gofmt, and golint before committing
  - Write table-driven tests for all public functions
  - Include benchmark tests for performance-critical code
  - Implement integration tests for external dependencies
  - Profile memory and CPU usage for optimization opportunities
```

**Build Command**:
```bash
claude-config build --agent go-engineer
```

**Expected Output**: Complete agent with Go-specific guidance, quality standards, and coordination patterns.

---

### Example 2: Research-Focused Agent

**Scenario**: Creating a specialized research agent for academic literature analysis.

**File**: `data/personas/academic-researcher.yaml`

```yaml
name: academic-researcher
display_name: Academic Researcher
model: sonnet
description: Research specialist focused on academic literature analysis, methodology design, and evidence synthesis across multiple domains

context_priming: |
  You are a seasoned academic researcher with experience across multiple disciplines. Your mindset:
  - "What does the current literature say about this topic?"
  - "How do I design a methodology that produces reliable results?"
  - "What are the potential biases and limitations in this approach?"
  - "How do I synthesize findings across different studies?"
  
  You think in terms of: research rigor, methodological soundness, evidence quality,
  statistical significance, and reproducible research practices.

expertise:
- Academic literature search and systematic review methodology
- Research design including experimental, observational, and mixed methods
- Statistical analysis and interpretation of research findings
- Citation management and academic writing standards
- Peer review process and publication strategies
- Research ethics and institutional review board procedures
- Cross-disciplinary research synthesis and meta-analysis

quality_criteria:
  methodological_rigor:
    - Systematic literature search with documented strategy
    - Appropriate research design for the research question
    - Statistical analysis with effect sizes and confidence intervals
    - Proper control for confounding variables and bias
  evidence_quality:
    - Primary sources prioritized over secondary sources
    - Peer-reviewed publications from reputable journals
    - Recent findings balanced with foundational studies
    - Critical appraisal of study limitations and methodology
  reporting_standards:
    - Following discipline-specific reporting guidelines (CONSORT, PRISMA)
    - Complete methodology section with reproducible procedures
    - Transparent discussion of limitations and future directions
    - Proper citation format and reference management

decision_frameworks:
  research_design:
    exploratory_questions:
      - "Qualitative methods: In-depth understanding of phenomena"
      - "Mixed methods: Comprehensive view combining qual/quant"
    hypothesis_testing:
      - "Experimental design: Causal relationships with control"
      - "Observational studies: Associations in natural settings"
  
  literature_search:
    comprehensive_review: "Multiple databases with systematic protocol"
    focused_review: "Targeted search with specific inclusion criteria"
    rapid_review: "Time-limited search for emerging topics"

boundaries:
  do_handle:
    - Literature search and systematic review methodology
    - Research design and statistical analysis planning
    - Academic writing and publication strategy
    - Evidence synthesis and meta-analysis
    - Research ethics and methodology guidance
  
  coordinate_with:
    - "data-engineer: Research data management and analysis pipelines"
    - "ai-engineer: Machine learning applications in research"
    - "technical-writer: Research dissemination and public engagement"

common_failures:
  methodological_issues:
    - "Publication bias from excluding negative results (search grey literature)"
    - "Selection bias from narrow inclusion criteria (broaden search terms)"
    - "Measurement bias from inconsistent outcome definitions (standardize metrics)"
  analysis_problems:
    - "Multiple comparisons without correction (adjust p-values appropriately)"
    - "Confounding variables not accounted for (use stratification or matching)"
    - "Sample size insufficient for reliable conclusions (conduct power analysis)"
  reporting_deficiencies:
    - "Incomplete methodology preventing replication (follow reporting guidelines)"
    - "Cherry-picking results that support hypothesis (report all findings)"
    - "Overgeneralization beyond study population (acknowledge limitations)"

proactive_triggers:
  file_patterns:
    - "*.bib"
    - "*.ris"
    - "literature_review.md"
    - "methodology.md"
    - "references/"
  project_indicators:
    - "research"
    - "literature review" 
    - "systematic review"
    - "meta-analysis"
    - "academic"

content_sections:
  search_methodology: personas/academic-researcher/search-methodology.md
  analysis_frameworks: personas/academic-researcher/analysis-frameworks.md
  writing_guidelines: personas/academic-researcher/writing-guidelines.md
```

---

## Advanced Agent Configurations

### Example 3: Multi-Modal AI Agent with Complex Coordination

**Scenario**: Creating an AI agent that handles computer vision, NLP, and multimodal AI systems with sophisticated coordination patterns.

**File**: `data/personas/multimodal-ai-engineer.yaml`

```yaml
name: multimodal-ai-engineer
display_name: Multimodal AI Engineer
model: opus
description: Advanced AI specialist focusing on multimodal systems combining computer vision, NLP, and cross-modal learning for complex AI applications

context_priming: |
  You are a cutting-edge AI researcher and engineer specializing in multimodal AI systems. Your mindset:
  - "How do I effectively fuse information from multiple modalities?"
  - "What are the architectural patterns for cross-modal learning?"
  - "How do I handle modal alignment and synchronization?"
  - "What evaluation metrics capture multimodal performance effectively?"
  
  You think in terms of: modal fusion strategies, cross-attention mechanisms,
  representation learning, evaluation protocols, and scalable architectures.

expertise:
- Computer vision with transformers, CNNs, and attention mechanisms
- Natural language processing with large language models and embeddings
- Multimodal architectures including CLIP, ALIGN, and custom fusion approaches
- Cross-modal retrieval and generation systems
- Video understanding and temporal modeling
- Audio processing and speech-text alignment
- Self-supervised learning and contrastive learning methods
- Distributed training and model optimization for large-scale systems

quality_criteria:
  model_performance:
    - Multimodal benchmarks achieving SOTA or competitive results
    - Ablation studies demonstrating individual component contributions
    - Cross-modal retrieval metrics (R@1, R@5, R@10) above baseline
    - Generation quality measured with both automatic and human evaluation
  architectural_design:
    - Modular architecture supporting different modal combinations
    - Efficient attention mechanisms with linear or sub-quadratic complexity
    - Gradient flow analysis ensuring proper cross-modal learning
    - Memory-efficient implementation for large-scale deployment
  experimental_rigor:
    - Multiple random seeds and statistical significance testing
    - Comprehensive comparison with relevant baselines
    - Dataset diversity and out-of-distribution generalization
    - Computational efficiency analysis and optimization

decision_frameworks:
  fusion_strategies:
    early_fusion:
      - "Concatenate features before processing (simple but limited)"
      - "Joint embedding learning (requires aligned training data)"
    late_fusion:
      - "Independent processing then combine predictions (flexible)"
      - "Ensemble methods with learned combination weights"
    attention_fusion:
      - "Cross-attention between modalities (captures fine-grained interactions)"
      - "Self-attention over concatenated features (end-to-end learning)"
  
  architecture_selection:
    small_scale: "Pretrained backbones with simple fusion layers"
    medium_scale: "Custom architectures with cross-modal attention"
    large_scale: "Transformer-based with distributed training"

boundaries:
  do_handle:
    - Multimodal architecture design and implementation
    - Cross-modal learning and alignment strategies
    - Advanced training techniques for large-scale models
    - Evaluation frameworks for multimodal systems
    - Research integration and SOTA method implementation
  
  coordinate_with:
    - "ai-researcher: Literature review and methodology design"
    - "data-engineer: Multimodal dataset preparation and pipeline optimization"
    - "performance-engineer: Large-scale training optimization and deployment"
    - "python-engineer: Production serving infrastructure for multimodal models"

common_failures:
  training_instability:
    - "Modal collapse where one modality dominates (balance loss terms carefully)"
    - "Gradient explosion in cross-attention layers (use gradient clipping)"
    - "Memory overflow with large batch sizes (gradient accumulation strategies)"
  performance_issues:
    - "Poor cross-modal alignment (improve contrastive learning objectives)"
    - "Overfitting to training modal combinations (data augmentation strategies)"
    - "Inference latency from complex attention (knowledge distillation optimization)"
  evaluation_problems:
    - "Inconsistent evaluation protocols (standardize benchmark procedures)"
    - "Metric gaming without real improvement (use diverse evaluation suites)"
    - "Dataset leakage between modalities (careful train/test splitting)"

proactive_triggers:
  file_patterns:
    - "*multimodal*"
    - "*vision_language*"
    - "*clip*"
    - "*cross_modal*"
    - "models/fusion/"
    - "datasets/multimodal/"
  project_indicators:
    - "multimodal"
    - "vision-language"
    - "CLIP"
    - "cross-modal"
    - "video understanding"
    - "audio-visual"
  dependency_patterns:
    - "transformers"
    - "timm"
    - "opencv"
    - "librosa"
    - "clip-by-openai"

coordination_overrides:
  research_methodology: "Advanced experimentation with statistical rigor and ablation studies"
  performance_optimization: "Large-scale distributed training with modal-specific optimizations"  
  evaluation_strategy: "Comprehensive multimodal benchmarking across multiple datasets"
  deployment_approach: "Scalable serving with modal caching and efficient attention"

custom_instructions: |
  ## Multimodal AI Development Protocol
  
  **1. Architecture Planning (First Hour)**
  - Define modal inputs and expected output format
  - Select fusion strategy based on data alignment and task requirements
  - Plan evaluation protocol with appropriate benchmarks
  - Design modular components for different modal combinations
  
  **2. Implementation Strategy**
  - Start with proven backbone architectures for each modality
  - Implement cross-modal alignment mechanisms carefully
  - Add comprehensive logging for modal contribution analysis
  - Build evaluation framework before training complex models
  
  **3. Advanced Quality Standards**
  - Implement gradient analysis tools for cross-modal learning
  - Create ablation study framework for architectural choices
  - Add modal contribution visualization and interpretation tools
  - Profile memory and computational requirements for deployment planning
```

---

## Multi-Agent Workflows

### Example 4: Full-Stack Development Workflow

**Scenario**: Coordinated development of a modern web application with React frontend, Python backend, and PostgreSQL database.

**Agent Coordination Flow**:

```yaml
# Project Detection: package.json + requirements.txt + database migrations
# Triggers: frontend-engineer, python-engineer, database-engineer

workflow_example:
  project_structure: |
    my-app/
    ├── frontend/
    │   ├── package.json        # Triggers frontend-engineer
    │   ├── src/components/
    │   └── public/
    ├── backend/
    │   ├── requirements.txt    # Triggers python-engineer  
    │   ├── app/
    │   └── tests/
    ├── database/
    │   ├── migrations/         # Triggers database-engineer
    │   └── schema.sql
    └── docker-compose.yml      # Triggers devops-engineer

  coordination_sequence:
    1_database_setup:
      agent: database-engineer
      tasks:
        - Design normalized schema with proper indexing
        - Create migration scripts with rollback procedures
        - Set up connection pooling and performance monitoring
      output: Database schema and migration files
      
    2_backend_development:
      agent: python-engineer
      dependencies: [database_setup]
      tasks:
        - Implement FastAPI with async database connections
        - Create comprehensive API endpoints with validation
        - Add authentication and authorization middleware
        - Implement error handling and logging
      coordination:
        - database-engineer: "Optimize queries and add proper indexing"
        - security-engineer: "Review authentication implementation"
      output: REST API with documentation
      
    3_frontend_development:
      agent: frontend-engineer
      dependencies: [backend_development]
      tasks:
        - Build React components with TypeScript
        - Implement state management with Redux Toolkit
        - Add responsive UI with Material-UI or Tailwind
        - Integrate API calls with error handling
      coordination:
        - python-engineer: "Ensure API contract compatibility"
        - ui-ux-designer: "Review component design and accessibility"
      output: React application with API integration
      
    4_infrastructure_setup:
      agent: devops-engineer
      dependencies: [backend_development, frontend_development]
      tasks:
        - Create Docker containers for all services
        - Set up Kubernetes deployment manifests
        - Configure CI/CD pipeline with testing stages
        - Implement monitoring and logging infrastructure
      coordination:
        - security-engineer: "Review container security and secrets management"
      output: Deployment infrastructure and CI/CD pipeline
      
    5_quality_assurance:
      agent: qa-engineer
      dependencies: [infrastructure_setup]
      tasks:
        - Create end-to-end test suite with Playwright
        - Implement API testing with automated validation
        - Set up performance testing and load testing
        - Add security testing and vulnerability scanning
      output: Comprehensive test suite and quality reports
      
    6_documentation:
      agent: technical-writer
      dependencies: [quality_assurance]
      tasks:
        - Generate API documentation from OpenAPI specs
        - Create user guides and developer documentation
        - Write deployment and maintenance guides
        - Document testing and troubleshooting procedures
      output: Complete project documentation
```

**CLI Commands for Workflow**:

```bash
# Initialize project with multi-agent coordination
claude-config init-project --type fullstack --agents frontend-engineer,python-engineer,database-engineer

# Build coordinated workflow
make build-workflow

# Deploy with coordinated testing
make deploy-with-testing
```

---

### Example 5: AI Research and Development Pipeline

**Scenario**: End-to-end ML research project from literature review to production deployment.

**Workflow Configuration**:

```yaml
ai_research_pipeline:
  project_context: |
    Research Goal: Develop novel transformer architecture for multimodal sentiment analysis
    Timeline: 3 months research + 2 months productionization
    Team: Research + Engineering collaboration
    
  agent_coordination:
    phase_1_research:
      primary: ai-researcher
      support: [academic-researcher]
      duration: "4 weeks"
      deliverables:
        - Comprehensive literature review
        - Research methodology design
        - Baseline implementation strategy
        - Evaluation framework specification
      
    phase_2_experimentation:
      primary: multimodal-ai-engineer
      support: [ai-researcher, data-engineer]
      duration: "6 weeks"  
      deliverables:
        - Novel architecture implementation
        - Comprehensive experiments and ablation studies
        - Performance benchmarking against baselines
        - Research paper draft
      coordination_points:
        - ai-researcher: "Methodology validation and experimental design"
        - data-engineer: "Optimized data pipeline for large-scale experiments"
      
    phase_3_optimization:
      primary: performance-engineer
      support: [multimodal-ai-engineer, python-engineer]
      duration: "3 weeks"
      deliverables:
        - Model optimization for production constraints
        - Inference speed and memory optimization
        - Deployment architecture design
        - Performance benchmarking
      
    phase_4_productionization:
      primary: python-engineer
      support: [devops-engineer, qa-engineer]
      duration: "4 weeks"
      deliverables:
        - Production API with model serving
        - Monitoring and logging infrastructure
        - Comprehensive testing suite
        - Deployment automation
      
    phase_5_deployment:
      primary: devops-engineer
      support: [security-engineer, performance-engineer]
      duration: "2 weeks"
      deliverables:
        - Cloud deployment with auto-scaling
        - Security hardening and compliance
        - Monitoring and alerting setup
        - Documentation and runbooks

  cross_cutting_coordination:
    quality_assurance:
      agent: qa-engineer
      involvement: "Continuous throughout all phases"
      responsibilities:
        - Research methodology validation
        - Code quality and testing standards
        - Performance regression testing
        - Production readiness assessment
    
    documentation:
      agent: technical-writer  
      involvement: "Documentation sprints at phase boundaries"
      responsibilities:
        - Research documentation and paper writing support
        - API documentation and user guides
        - Deployment and operational documentation
        - Knowledge transfer materials

  success_metrics:
    research_quality:
      - Novel contribution validated by peer review
      - Reproducible experiments with open-source code
      - Performance improvements over established baselines
    
    production_quality:
      - 99.9% uptime with <100ms latency
      - Comprehensive monitoring and alerting
      - Automated testing with >90% coverage
      - Security compliance and vulnerability management
```

---

## Custom Content Integration

### Example 6: Agent with Rich Content Sections

**Scenario**: Creating a security engineer agent with extensive external content for different security domains.

**File Structure**:
```
data/
├── personas/
│   └── security-engineer.yaml
└── content/
    └── personas/
        └── security-engineer/
            ├── threat-modeling.md
            ├── secure-coding.md
            ├── penetration-testing.md
            ├── compliance-frameworks.md
            └── incident-response.md
```

**Main Agent Configuration**:

**File**: `data/personas/security-engineer.yaml`

```yaml
name: security-engineer
display_name: Security Engineer
model: sonnet
description: Cybersecurity specialist focusing on application security, threat modeling, and security architecture

# ... standard fields ...

content_sections:
  threat_modeling: personas/security-engineer/threat-modeling.md
  secure_coding: personas/security-engineer/secure-coding.md
  penetration_testing: personas/security-engineer/penetration-testing.md
  compliance_frameworks: personas/security-engineer/compliance-frameworks.md
  incident_response: personas/security-engineer/incident-response.md
```

**Content Files**:

**File**: `data/content/personas/security-engineer/threat-modeling.md`

```markdown
## Threat Modeling Methodology

### STRIDE Framework Application

**Spoofing Identity**
- Authentication bypass vulnerabilities
- Session hijacking and token theft
- Identity verification weaknesses

**Tampering with Data**
- Input validation failures
- Data integrity violations
- Man-in-the-middle attacks

**Repudiation**
- Insufficient logging and monitoring
- Non-repudiation mechanism failures
- Audit trail tampering

**Information Disclosure**
- Data exposure vulnerabilities
- Information leakage through error messages
- Unauthorized access to sensitive data

**Denial of Service**
- Resource exhaustion attacks
- Application layer DoS vulnerabilities
- Infrastructure-level availability threats

**Elevation of Privilege**
- Authorization bypass vulnerabilities
- Privilege escalation paths
- Access control mechanism failures

### Threat Modeling Process

1. **Define Security Objectives**
   - Identify assets and their value
   - Determine security requirements
   - Establish threat tolerance levels

2. **Create Architecture Overview**
   - Data flow diagrams
   - Trust boundaries identification
   - Entry and exit points mapping

3. **Identify Threats**
   - Apply STRIDE to each component
   - Consider attack vectors and threat actors
   - Prioritize threats by risk level

4. **Mitigate Identified Threats**
   - Design security controls
   - Implement defense-in-depth strategies
   - Validate mitigation effectiveness
```

**File**: `data/content/personas/security-engineer/secure-coding.md`

```markdown
## Secure Coding Standards

### Input Validation and Sanitization

**Validation Principles**
- Whitelist validation over blacklist filtering
- Server-side validation for all inputs
- Length, type, and format validation
- Encoding validation for different contexts

**Implementation Examples**

```python
# Python secure input validation
import re
from html import escape

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email) or len(email) > 254:
        raise ValueError("Invalid email format")
    return email.lower()

def sanitize_html_input(user_input):
    # Remove potentially dangerous HTML
    clean_input = escape(user_input)
    return clean_input[:1000]  # Limit length
```

### SQL Injection Prevention

**Parameterized Queries**
```python
# Safe database query
cursor.execute(
    "SELECT * FROM users WHERE email = %s AND status = %s",
    (email, 'active')
)

# NEVER do this - vulnerable to injection
query = f"SELECT * FROM users WHERE email = '{email}'"
```

**ORM Best Practices**
```python
# Django ORM - safe by default
User.objects.filter(email=email, status='active')

# Raw queries with parameters
User.objects.raw(
    "SELECT * FROM auth_user WHERE email = %s", 
    [email]
)
```

### Authentication and Session Management

**Secure Password Handling**
```python
import bcrypt
import secrets

def hash_password(password):
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def generate_secure_token():
    return secrets.token_urlsafe(32)
```

**Session Security**
- Use secure, httpOnly cookies
- Implement proper session timeout
- Regenerate session IDs after login
- Use CSRF tokens for state-changing operations
```

---

## Build System Examples

### Example 7: Custom Build Configuration

**Scenario**: Configuring the build system for a team with specific requirements and multiple environments.

**File**: `data/config.yaml`

```yaml
# Team configuration for claude-config build system
name: "enterprise-ai-team"
version: "2.0.0"
description: "Enterprise AI development team configuration"

# Global settings
settings:
  model_preferences:
    default: sonnet
    research_tasks: opus
    simple_operations: haiku
    cost_optimization: true
  
  output_configuration:
    base_directory: "dist/"
    agent_directory: "agents/"
    backup_existing: true
    generate_index: true
  
  validation:
    strict_mode: true
    check_boundaries: true
    validate_content_links: true
    require_proactive_triggers: true

# Agent selection for this team
agents:
  # Core development agents
  core_development:
    - python-engineer
    - frontend-engineer
    - database-engineer
    - devops-engineer
    
  # AI/ML specialists
  ai_specialists:
    - ai-engineer
    - multimodal-ai-engineer
    - ai-researcher
    - data-engineer
    
  # Quality and support
  quality_assurance:
    - qa-engineer
    - security-engineer
    - performance-engineer
    
  # Research and strategy
  research_strategy:
    - sr-ai-researcher
    - academic-researcher
    - product-manager
    
  # Utility agents
  utilities:
    - git-helper
    - technical-writer
    - project-coordinator

# Custom build profiles
build_profiles:
  development:
    agents: 
      - python-engineer
      - frontend-engineer
      - git-helper
    validation_level: "standard"
    include_debug_info: true
    
  production:
    agents: "all"
    validation_level: "strict"
    include_debug_info: false
    optimize_output: true
    
  research:
    agents:
      - ai-researcher
      - sr-ai-researcher
      - multimodal-ai-engineer
      - academic-researcher
    model_override: "opus"
    validation_level: "research"

# Team-specific customizations
customizations:
  quality_standards:
    code_coverage_threshold: 90
    documentation_required: true
    security_review_required: true
    performance_benchmarks: true
    
  coordination_patterns:
    escalation_chain:
      - level_1: "peer_agents"
      - level_2: "senior_agents" 
      - level_3: "team_lead"
    
    review_requirements:
      code_changes: ["qa-engineer", "security-engineer"]
      architecture_decisions: ["sr-architect"]
      research_methodology: ["sr-ai-researcher"]
  
  deployment_preferences:
    target_directory: "/home/team/.claude/"
    backup_previous: true
    validate_before_install: true
    generate_team_index: true

# Environment-specific overrides
environments:
  staging:
    model_preferences:
      default: haiku  # Cost optimization for staging
    validation:
      strict_mode: false
      
  production:
    model_preferences:
      default: sonnet
    validation:
      strict_mode: true
      require_security_review: true
    
    monitoring:
      performance_tracking: true
      error_reporting: true
      usage_analytics: true
```

**Build Commands with Profiles**:

```bash
# Build with development profile
claude-config build --profile development

# Build for production with strict validation
claude-config build --profile production --validate

# Research-focused build with Opus model
claude-config build --profile research

# Custom build with specific agents
claude-config build --agents ai-engineer,python-engineer,qa-engineer --environment staging
```

**Custom Makefile Integration**:

```makefile
# Enhanced Makefile with profile support

# Development workflow
dev-build:
	claude-config build --profile development --validate
	claude-config install --target ./.claude-dev

# Production deployment  
prod-build:
	claude-config build --profile production --strict
	claude-config validate --comprehensive
	claude-config install --backup

# Research environment
research-build:
	claude-config build --profile research --model opus
	claude-config install --target ./research/.claude

# Team deployment with validation
team-deploy:
	@echo "Deploying team configuration..."
	claude-config build --profile production
	claude-config validate --team-standards
	claude-config install --team-directory /shared/claude-config
	@echo "Team deployment complete"

# Continuous integration
ci-validate:
	claude-config validate --strict --check-all
	claude-config build --profile production --dry-run
	claude-config test-agents --comprehensive

.PHONY: dev-build prod-build research-build team-deploy ci-validate
```

---

## Real-World Use Cases

### Example 8: Startup Technology Stack

**Scenario**: Early-stage startup needs comprehensive development support for rapid prototyping and scaling.

**Project Structure**:
```
startup-app/
├── mobile/              # React Native app
├── web/                 # Next.js frontend
├── api/                 # Python FastAPI backend  
├── ml/                  # ML models and training
├── infrastructure/      # Terraform + K8s
└── docs/               # Documentation
```

**Agent Activation Sequence**:

```yaml
startup_workflow:
  context: "Early stage startup building AI-powered mobile and web applications"
  team_size: "5 developers"
  timeline: "MVP in 3 months, scaling in 6 months"
  
  phase_1_mvp:
    duration: "6 weeks"
    focus: "Core functionality and user validation"
    
    week_1_foundation:
      agents: [python-engineer, frontend-engineer, database-engineer]
      tasks:
        - Set up FastAPI with PostgreSQL
        - Create Next.js app with authentication
        - Design database schema for core entities
      coordination: "Daily standups between agents"
      
    week_2_3_core_features:
      agents: [ai-engineer, python-engineer, frontend-engineer]
      tasks:
        - Implement ML model for core AI features
        - Build REST API with ML integration
        - Create responsive web interface
      coordination: "AI-engineer → python-engineer → frontend-engineer"
      
    week_4_5_mobile:
      agents: [mobile-engineer, python-engineer]  
      tasks:
        - Develop React Native app
        - Optimize API for mobile consumption
        - Implement offline capabilities
      coordination: "Mobile-specific API requirements feedback"
      
    week_6_deployment:
      agents: [devops-engineer, security-engineer, qa-engineer]
      tasks:
        - Set up AWS infrastructure with Terraform
        - Implement CI/CD pipeline
        - Security audit and testing
      coordination: "Parallel deployment and security validation"

  phase_2_scaling:
    duration: "6 weeks"
    focus: "Performance optimization and advanced features"
    
    optimization_sprint:
      agents: [performance-engineer, ai-engineer, database-engineer]
      tasks:
        - Database query optimization
        - ML model optimization for production
        - API performance tuning
      success_metrics:
        - API response time <200ms
        - Database query time <50ms
        - ML inference time <100ms
        
    advanced_features:
      agents: [ai-engineer, multimodal-ai-engineer, python-engineer]
      tasks:
        - Advanced AI features with multimodal inputs
        - Real-time processing capabilities
        - Advanced analytics and insights
      coordination: "Research-to-production pipeline"

  ongoing_operations:
    agents: [qa-engineer, security-engineer, technical-writer, git-helper]
    responsibilities:
      - Continuous testing and quality assurance
      - Security monitoring and updates
      - Documentation maintenance
      - Version control and release management
```

**Cost Optimization Strategy**:

```yaml
cost_optimization:
  model_selection:
    rapid_prototyping: 
      agents: ["python-engineer", "frontend-engineer", "mobile-engineer"]
      model: "sonnet"  # Balance of speed and quality
      
    ai_development:
      agents: ["ai-engineer", "multimodal-ai-engineer"] 
      model: "opus"  # Best quality for complex AI tasks
      
    utility_tasks:
      agents: ["git-helper", "technical-writer", "qa-engineer"]
      model: "haiku"  # Fast and cost-effective
      
  escalation_strategy:
    - Try Sonnet agents for 3 attempts
    - Escalate to Opus senior agents if unresolved
    - Document learnings to reduce future escalations
    
  monitoring:
    - Track model usage and costs weekly
    - Optimize agent selection based on task complexity
    - Regular review of escalation patterns
```

---

### Example 9: Enterprise Integration Project

**Scenario**: Large enterprise modernizing legacy systems with microservices architecture and AI integration.

**Project Scope**:
```yaml
enterprise_modernization:
  context: "Fortune 500 company modernizing 20-year-old monolithic system"
  team_size: "50+ developers across multiple teams"
  timeline: "18-month transformation"
  constraints:
    - Legacy system must remain operational
    - Compliance with SOX, PCI DSS, HIPAA
    - Zero downtime requirements
    - Integration with 15+ external systems

  architecture_strategy:
    current_state: "Monolithic .NET application with SQL Server"
    target_state: "Cloud-native microservices with AI capabilities"
    migration_approach: "Strangler Fig pattern with parallel services"

  agent_coordination_model:
    architecture_team:
      lead: sr-architect
      agents: [integration-architect, security-engineer, database-engineer]
      responsibilities:
        - Overall system architecture design
        - Technology selection and standards
        - Integration patterns and API design
        - Security architecture and compliance
        
    development_teams:
      team_alpha:
        focus: "User management and authentication services"
        agents: [java-engineer, security-engineer, database-engineer]
        tech_stack: "Spring Boot, PostgreSQL, OAuth2/OIDC"
        
      team_beta:  
        focus: "Core business logic microservices"
        agents: [python-engineer, java-engineer, database-engineer]
        tech_stack: "FastAPI, Spring Boot, Event Sourcing"
        
      team_gamma:
        focus: "AI-powered analytics and insights"
        agents: [ai-engineer, data-engineer, python-engineer]
        tech_stack: "MLflow, Apache Kafka, TensorFlow Serving"
        
      team_delta:
        focus: "Frontend modernization"
        agents: [frontend-engineer, ui-ux-designer]
        tech_stack: "React, TypeScript, Micro-frontends"
        
    platform_team:
      agents: [devops-engineer, security-engineer, performance-engineer]
      responsibilities:
        - Kubernetes platform management
        - CI/CD pipeline architecture
        - Monitoring and observability
        - Security scanning and compliance
        
    quality_assurance:
      agents: [qa-engineer, performance-engineer, security-engineer]
      responsibilities:
        - Cross-service integration testing
        - Performance and load testing
        - Security testing and vulnerability management
        - Compliance validation and reporting

  migration_phases:
    phase_1_foundation:
      duration: "3 months"
      agents: [sr-architect, devops-engineer, security-engineer]
      deliverables:
        - Cloud infrastructure setup (AWS/Azure)
        - CI/CD pipeline implementation
        - Security framework and compliance baseline
        - Monitoring and logging infrastructure
        
    phase_2_core_services:
      duration: "6 months" 
      agents: [java-engineer, python-engineer, database-engineer]
      deliverables:
        - Authentication and authorization service
        - Core business entity services
        - Data migration and synchronization tools
        - API gateway and service mesh setup
        
    phase_3_ai_integration:
      duration: "4 months"
      agents: [ai-engineer, data-engineer, multimodal-ai-engineer]
      deliverables:
        - ML pipeline for predictive analytics
        - Real-time recommendation engine
        - Document processing with NLP
        - Business intelligence dashboard
        
    phase_4_frontend_modernization:
      duration: "3 months"
      agents: [frontend-engineer, ui-ux-designer, mobile-engineer]
      deliverables:
        - Modern web application with React
        - Mobile application for key workflows
        - Progressive web app capabilities
        - Accessibility compliance (WCAG 2.1)
        
    phase_5_legacy_retirement:
      duration: "2 months"
      agents: [sr-architect, database-engineer, qa-engineer]
      deliverables:
        - Legacy system decommissioning
        - Data archival and compliance
        - Performance validation
        - Go-live support and monitoring

  governance_framework:
    architecture_review_board:
      frequency: "Bi-weekly"
      participants: [sr-architect, integration-architect, team-leads]
      decisions: "Technology standards, integration patterns, security policies"
      
    quality_gates:
      code_quality: "90% test coverage, security scan pass"
      performance: "99.9% uptime, <200ms response times"
      security: "OWASP compliance, penetration test pass"
      documentation: "API docs, runbooks, disaster recovery plans"
      
    success_metrics:
      business:
        - 50% reduction in processing time
        - 30% improvement in user satisfaction
        - 25% reduction in operational costs
      technical:
        - 99.99% system availability
        - <100ms API response times
        - Zero security incidents
        - 90% automated test coverage
```

This enterprise example demonstrates how claude-config scales to support large, complex projects with multiple teams, sophisticated coordination requirements, and enterprise-grade quality standards.

---

## Testing and Validation Examples

### Example 10: Comprehensive Agent Testing Strategy

**Scenario**: Setting up automated testing for agent configurations to ensure quality and consistency.

**Test Configuration Structure**:
```
tests/
├── fixtures/
│   ├── personas/
│   │   ├── valid-agent.yaml
│   │   ├── invalid-agent.yaml  
│   │   └── boundary-conflict-agent.yaml
│   └── content/
│       └── test-content.md
├── unit/
│   ├── test_composer.py
│   ├── test_validator.py
│   └── test_cli.py
├── integration/
│   ├── test_build_process.py
│   ├── test_agent_coordination.py
│   └── test_deployment.py
└── performance/
    ├── test_build_performance.py
    └── test_validation_speed.py
```

**Unit Test Examples**:

**File**: `tests/unit/test_composer.py`

```python
import pytest
import yaml
from pathlib import Path
from claude_config.composer import AgentComposer
from claude_config.exceptions import AgentNotFoundError, ValidationError

class TestAgentComposer:
    """Test suite for AgentComposer class."""
    
    @pytest.fixture
    def composer(self):
        """Create composer instance with test fixtures."""
        return AgentComposer(
            config_path="tests/fixtures/personas",
            template_path="src/claude_config/templates"
        )
    
    @pytest.fixture
    def valid_agent_config(self):
        """Load valid agent configuration for testing."""
        with open("tests/fixtures/personas/valid-agent.yaml") as f:
            return yaml.safe_load(f)
    
    def test_compose_valid_agent(self, composer):
        """Test composing a valid agent configuration."""
        result = composer.compose_agent("valid-agent")
        
        # Check that result contains expected sections
        assert "# Valid Agent" in result
        assert "## Context Priming" in result
        assert "## Expertise" in result
        assert "## Quality Criteria" in result
        assert "## Decision Frameworks" in result
        assert "## Boundaries" in result
        
        # Check YAML frontmatter
        lines = result.split('\n')
        assert lines[0] == "---"
        assert "name: valid-agent" in result
        assert "model: sonnet" in result
    
    def test_compose_nonexistent_agent(self, composer):
        """Test error handling for nonexistent agent."""
        with pytest.raises(AgentNotFoundError) as exc_info:
            composer.compose_agent("nonexistent-agent")
        
        assert "nonexistent-agent" in str(exc_info.value)
    
    def test_list_available_agents(self, composer):
        """Test listing available agents."""
        agents = composer.list_available_agents()
        
        assert isinstance(agents, list)
        assert "valid-agent" in agents
        assert len(agents) > 0
    
    def test_validate_agent_config_valid(self, composer):
        """Test validation of valid configuration."""
        result = composer.validate_agent_config("valid-agent")
        assert result is True
    
    def test_validate_agent_config_invalid(self, composer):
        """Test validation of invalid configuration."""
        with pytest.raises(ValidationError):
            composer.validate_agent_config("invalid-agent")
    
    @pytest.mark.parametrize("field_name,field_value", [
        ("name", "test-agent"),
        ("model", "sonnet"),
        ("description", "Test agent description"),
    ])
    def test_required_fields_present(self, composer, valid_agent_config, field_name, field_value):
        """Test that all required fields are present in composed output."""
        result = composer.compose_agent("valid-agent")
        assert field_value in result
```

**Integration Test Examples**:

**File**: `tests/integration/test_build_process.py`

```python
import pytest
import tempfile
import shutil
from pathlib import Path
from claude_config.cli import build_command
from claude_config.composer import AgentComposer

class TestBuildProcess:
    """Integration tests for the complete build process."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_complete_build_process(self, temp_output_dir):
        """Test complete build process from YAML to output files."""
        # Run build command
        result = build_command(
            agent_name=None,  # Build all agents
            output_dir=str(temp_output_dir),
            validate=True,
            verbose=True
        )
        
        # Check that build succeeded
        assert result.success is True
        assert result.errors == []
        
        # Check output files exist
        agents_dir = temp_output_dir / "agents"
        assert agents_dir.exists()
        
        agent_files = list(agents_dir.glob("*.md"))
        assert len(agent_files) > 0
        
        # Check specific agent file
        python_agent = agents_dir / "python-engineer.md"
        if python_agent.exists():
            content = python_agent.read_text()
            assert "# Python Engineer" in content
            assert "---" in content  # YAML frontmatter
    
    def test_build_with_validation_errors(self, temp_output_dir):
        """Test build process with validation errors."""
        # This would use fixtures with intentionally invalid configs
        result = build_command(
            agent_name="invalid-agent",
            output_dir=str(temp_output_dir),
            validate=True
        )
        
        assert result.success is False
        assert len(result.errors) > 0
        assert "validation" in result.errors[0].lower()
    
    def test_incremental_build(self, temp_output_dir):
        """Test incremental build only rebuilding changed agents."""
        # Initial build
        result1 = build_command(
            agent_name=None,
            output_dir=str(temp_output_dir),
            validate=True
        )
        
        initial_files = list((temp_output_dir / "agents").glob("*.md"))
        initial_mtimes = {f.name: f.stat().st_mtime for f in initial_files}
        
        # Second build without changes
        result2 = build_command(
            agent_name=None,
            output_dir=str(temp_output_dir),
            validate=True,
            incremental=True
        )
        
        # Check that unchanged files weren't rebuilt
        current_files = list((temp_output_dir / "agents").glob("*.md"))
        current_mtimes = {f.name: f.stat().st_mtime for f in current_files}
        
        # Most files should have same modification time
        unchanged_count = sum(
            1 for name in initial_mtimes 
            if name in current_mtimes and initial_mtimes[name] == current_mtimes[name]
        )
        
        # Allow for some variation but most should be unchanged
        assert unchanged_count >= len(initial_files) * 0.8
```

**Performance Test Examples**:

**File**: `tests/performance/test_build_performance.py`

```python
import pytest
import time
import psutil
import os
from pathlib import Path
from claude_config.cli import build_command

class TestBuildPerformance:
    """Performance tests for build process."""
    
    def test_build_speed_benchmark(self, tmp_path):
        """Test that build completes within acceptable time limits."""
        start_time = time.time()
        
        result = build_command(
            agent_name=None,  # Build all agents
            output_dir=str(tmp_path),
            validate=True
        )
        
        elapsed_time = time.time() - start_time
        
        # Build should complete within 30 seconds for full build
        assert elapsed_time < 30, f"Build took {elapsed_time:.2f}s, expected <30s"
        assert result.success is True
    
    def test_memory_usage(self, tmp_path):
        """Test that build process doesn't consume excessive memory."""
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        result = build_command(
            agent_name=None,
            output_dir=str(tmp_path), 
            validate=True
        )
        
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = memory_after - memory_before
        
        # Memory increase should be reasonable (less than 500MB)
        assert memory_increase < 500, f"Memory increased by {memory_increase:.1f}MB"
        assert result.success is True
    
    @pytest.mark.parametrize("agent_count", [1, 5, 10, 20])
    def test_scalability(self, tmp_path, agent_count):
        """Test build performance scales reasonably with agent count."""
        # This would create test agents dynamically
        agent_names = [f"test-agent-{i}" for i in range(agent_count)]
        
        start_time = time.time()
        
        for agent_name in agent_names:
            result = build_command(
                agent_name=agent_name,
                output_dir=str(tmp_path),
                validate=False  # Skip validation for performance test
            )
        
        elapsed_time = time.time() - start_time
        time_per_agent = elapsed_time / agent_count
        
        # Should be roughly linear scaling, allow some overhead
        expected_max_time_per_agent = 2.0  # seconds
        assert time_per_agent < expected_max_time_per_agent, \
            f"Time per agent: {time_per_agent:.2f}s, expected <{expected_max_time_per_agent}s"
```

**Continuous Integration Configuration**:

**File**: `.github/workflows/test.yml`

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11"]
        
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Run linting
      run: |
        black --check src/ tests/
        isort --check-only src/ tests/
        mypy src/
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=claude_config --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v
    
    - name: Run performance tests
      run: |
        pytest tests/performance/ -v --timeout=60
    
    - name: Validate all agent configurations
      run: |
        claude-config validate --strict
    
    - name: Test build process
      run: |
        claude-config build --validate --output-dir ./test-build
        
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## Performance Optimization Examples

### Example 11: Large-Scale Agent Management

**Scenario**: Optimizing claude-config for organizations with 100+ custom agents and frequent builds.

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Analyze current documentation structure and files", "status": "completed", "activeForm": "Analyzing current documentation structure and files"}, {"content": "Create comprehensive documentation plan based on existing structure", "status": "completed", "activeForm": "Creating comprehensive documentation plan based on existing structure"}, {"content": "Create API reference documentation for Python package", "status": "completed", "activeForm": "Creating API reference documentation for Python package"}, {"content": "Build troubleshooting and FAQ documentation", "status": "completed", "activeForm": "Building troubleshooting and FAQ documentation"}, {"content": "Create examples collection with practical use cases", "status": "completed", "activeForm": "Creating examples collection with practical use cases"}, {"content": "Generate performance and optimization guide", "status": "in_progress", "activeForm": "Generating performance and optimization guide"}]