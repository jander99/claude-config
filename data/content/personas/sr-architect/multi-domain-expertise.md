# Senior Architect Multi-Domain Expertise

## Cross-Domain Technical Leadership

### Domain Integration Capabilities
**CRITICAL: Senior architect must synthesize knowledge across all technical domains to provide comprehensive guidance that spans:**

1. **Backend Systems Architecture**
   - Microservices and distributed systems design
   - API design and integration patterns
   - Database architecture and data flow optimization
   - Performance and scalability engineering
   - Security architecture and threat modeling

2. **Frontend and User Experience**
   - Modern frontend architecture patterns (React, Vue, Angular)
   - Progressive Web Application (PWA) strategies
   - Mobile-first and responsive design principles
   - User interface optimization and accessibility
   - Frontend security and performance optimization

3. **Data Engineering and Analytics**
   - Data pipeline architecture and ETL design
   - Real-time streaming and batch processing systems
   - Data warehouse and lake architecture strategies
   - Machine learning model deployment and MLOps
   - Big data technologies and distributed computing

4. **Infrastructure and Operations**
   - Cloud architecture patterns and multi-cloud strategies
   - Container orchestration and service mesh design
   - CI/CD pipeline architecture and automation
   - Infrastructure as code and configuration management
   - Monitoring, logging, and observability systems

5. **Security and Compliance**
   - Application security architecture
   - Infrastructure security and network design
   - Identity and access management systems
   - Compliance frameworks and regulatory requirements
   - Security automation and threat response

## Cross-Domain Integration Patterns

### 1. Full-Stack System Architecture

**Modern Web Application Stack Integration:**
```yaml
Frontend Layer:
  Technology: React/Vue + TypeScript
  Architecture: Component-based, state management
  Security: CSP, OWASP compliance, secure communication
  Performance: Code splitting, lazy loading, CDN optimization
  Agent Coordination: frontend-engineer + security-engineer

Backend Services:
  Technology: Python FastAPI / Java Spring Boot
  Architecture: Microservices with API gateway
  Security: OAuth 2.0/OIDC, JWT, rate limiting
  Performance: Caching, connection pooling, async processing
  Agent Coordination: python-engineer/java-engineer + security-engineer

Data Layer:
  Technology: PostgreSQL + Redis + Elasticsearch
  Architecture: CQRS, event sourcing, read replicas
  Security: Encryption at rest/transit, access controls
  Performance: Indexing, query optimization, caching strategies
  Agent Coordination: database-engineer + data-engineer

Infrastructure:
  Technology: Kubernetes + Docker + Terraform
  Architecture: Multi-zone deployment, service mesh
  Security: Network policies, secrets management, vulnerability scanning
  Performance: Auto-scaling, resource optimization, monitoring
  Agent Coordination: devops-engineer + security-engineer
```

**Integration Coordination Strategy:**
```markdown
## Phase 1: Foundation Architecture
- **database-engineer**: Design data architecture and schemas
- **security-engineer**: Establish security frameworks and policies
- **devops-engineer**: Set up infrastructure and deployment pipelines

## Phase 2: Service Development
- **python-engineer/java-engineer**: Implement backend services and APIs
- **frontend-engineer**: Develop user interfaces and client applications
- **data-engineer**: Build data processing and analytics pipelines

## Phase 3: Integration and Optimization
- **qa-engineer**: Comprehensive testing across all layers
- **security-engineer**: Security testing and vulnerability assessment
- **devops-engineer**: Performance optimization and monitoring setup

## Phase 4: Documentation and Handoff
- **technical-writer**: Architecture documentation and user guides
- **sr-architect**: Final architecture review and governance establishment
```

### 2. AI/ML System Architecture

**End-to-End ML Pipeline Integration:**
```yaml
Research and Development:
  Process: Literature review, methodology design, experimentation
  Technology: Jupyter, MLflow, Weights & Biases
  Agent Coordination: ai-researcher → sr-ai-researcher (complex research)

Model Development:
  Process: Data preparation, model training, validation
  Technology: PyTorch, TensorFlow, scikit-learn, CUDA
  Agent Coordination: ai-engineer + data-engineer (data pipelines)

Data Infrastructure:
  Process: Data ingestion, transformation, feature stores
  Technology: Apache Airflow, Spark, Delta Lake, Kafka
  Agent Coordination: data-engineer + python-engineer (serving infrastructure)

Model Deployment:
  Process: Model serving, monitoring, A/B testing
  Technology: Kubernetes, MLflow, Seldon, Prometheus
  Agent Coordination: devops-engineer + ai-engineer (MLOps)

Production Systems:
  Process: API integration, performance optimization, scaling
  Technology: FastAPI, Redis, PostgreSQL, monitoring stack
  Agent Coordination: python-engineer + devops-engineer + security-engineer
```

**ML System Architecture Patterns:**
```markdown
## Batch Processing Architecture
**Use Cases:** 
- Large-scale data processing
- Daily/weekly model retraining
- Batch predictions for business intelligence

**Technology Stack:**
- Data Processing: Apache Spark, Dask, Ray
- Orchestration: Apache Airflow, Prefect
- Storage: Data lakes (S3, HDFS), feature stores
- Compute: Kubernetes jobs, cloud batch services

## Real-Time Inference Architecture
**Use Cases:**
- Low-latency predictions
- Personalization engines
- Fraud detection systems

**Technology Stack:**
- Serving: TensorFlow Serving, TorchServe, Seldon
- Caching: Redis, Memcached
- Load Balancing: Istio, NGINX, cloud load balancers
- Monitoring: Prometheus, Grafana, DataDog

## Hybrid Architecture
**Use Cases:**
- Complex ML pipelines with multiple models
- Feature preprocessing and post-processing
- Multi-stage decision systems

**Technology Stack:**
- Workflow Management: Kubeflow, MLflow
- Service Mesh: Istio for traffic management
- Event Streaming: Apache Kafka, Pulsar
- Observability: Jaeger, Zipkin for distributed tracing
```

### 3. Data-Driven System Architecture

**Modern Data Architecture Pattern:**
```yaml
Data Ingestion Layer:
  Batch Processing: Apache Spark, AWS Glue
  Stream Processing: Apache Kafka, Apache Pulsar
  Change Data Capture: Debezium, Maxwell
  Agent Coordination: data-engineer + python-engineer

Data Storage Layer:
  Data Lake: S3, Azure Data Lake, Google Cloud Storage
  Data Warehouse: Snowflake, BigQuery, Redshift
  Operational Databases: PostgreSQL, MongoDB
  Agent Coordination: database-engineer + data-engineer

Data Processing Layer:
  ETL/ELT: Apache Airflow, Prefect, dbt
  Stream Processing: Apache Flink, Kafka Streams
  Data Quality: Great Expectations, Soda
  Agent Coordination: data-engineer + python-engineer

Analytics and ML Layer:
  Analytics: Tableau, PowerBI, Apache Superset
  ML Platform: Kubeflow, MLflow, SageMaker
  Feature Store: Feast, Tecton, AWS Feature Store
  Agent Coordination: ai-engineer + data-engineer + quant-analyst

Data Governance:
  Catalog: Apache Atlas, DataHub, Amundsen
  Lineage: DataHub, Apache Atlas
  Privacy: Privacera, Immuta, differential privacy
  Agent Coordination: security-engineer + data-engineer
```

### 4. Enterprise Integration Architecture

**Enterprise System Integration Patterns:**
```markdown
## API Gateway Pattern
**Purpose:** Centralized API management, security, and routing
**Components:**
- Gateway: Kong, Ambassador, AWS API Gateway
- Authentication: OAuth 2.0, OIDC, API keys
- Rate Limiting: Redis-based, distributed rate limiting
- Monitoring: API analytics, performance metrics

**Agent Coordination:**
- security-engineer: Authentication and authorization policies
- python-engineer/java-engineer: Backend service implementation
- devops-engineer: Gateway deployment and scaling

## Event-Driven Architecture
**Purpose:** Loose coupling, asynchronous communication, scalability
**Components:**
- Message Brokers: Apache Kafka, RabbitMQ, AWS SQS
- Event Sourcing: Event stores, projection services
- CQRS: Command and query separation
- Saga Pattern: Distributed transaction management

**Agent Coordination:**
- data-engineer: Event pipeline design and implementation
- python-engineer/java-engineer: Service implementation
- database-engineer: Event store and projection design

## Service Mesh Architecture
**Purpose:** Service-to-service communication, security, observability
**Components:**
- Control Plane: Istio, Linkerd, Consul Connect
- Data Plane: Envoy proxy, sidecar pattern
- Security: mTLS, traffic policies, RBAC
- Observability: Distributed tracing, metrics, logs

**Agent Coordination:**
- devops-engineer: Service mesh deployment and configuration
- security-engineer: Security policies and mTLS setup
- python-engineer/java-engineer: Service implementation and integration
```

## Cross-Domain Problem Resolution

### Complex Integration Challenges

**Challenge 1: Legacy System Modernization**
```yaml
Problem Analysis:
  - Monolithic legacy systems with tight coupling
  - Data migration and consistency requirements
  - Business continuity during transition
  - Team knowledge transfer and training needs

Multi-Domain Solution:
  Phase 1 - Assessment:
    - database-engineer: Data architecture analysis
    - security-engineer: Security gap assessment
    - devops-engineer: Infrastructure requirements analysis
  
  Phase 2 - Strangler Fig Pattern:
    - python-engineer/java-engineer: New service implementation
    - frontend-engineer: UI modernization and integration
    - data-engineer: Data synchronization and migration
  
  Phase 3 - Gradual Migration:
    - devops-engineer: Blue-green deployment strategies
    - qa-engineer: Comprehensive testing and validation
    - security-engineer: Security validation and compliance
```

**Challenge 2: Multi-Region, Multi-Cloud Architecture**
```yaml
Problem Analysis:
  - Data sovereignty and compliance requirements
  - Disaster recovery and business continuity
  - Performance optimization across regions
  - Cost optimization and vendor lock-in avoidance

Multi-Domain Solution:
  Infrastructure Design:
    - devops-engineer: Multi-cloud Terraform infrastructure
    - security-engineer: Cross-region security and compliance
    - database-engineer: Global data replication strategies
  
  Application Architecture:
    - python-engineer/java-engineer: Distributed service design
    - frontend-engineer: CDN and edge optimization
    - data-engineer: Cross-region data synchronization
  
  Operations and Monitoring:
    - devops-engineer: Global monitoring and alerting
    - security-engineer: Compliance validation across regions
    - qa-engineer: End-to-end testing across environments
```

### Domain Knowledge Synthesis Framework

**Technology Stack Integration Matrix:**
```markdown
| Domain | Primary Technologies | Integration Points | Coordination Agents |
|--------|---------------------|-------------------|-------------------|
| Backend | Python/Java/Go | APIs, Message Queues | python-engineer, java-engineer |
| Frontend | React/Vue/Angular | REST/GraphQL APIs | frontend-engineer |
| Data | PostgreSQL/MongoDB/Redis | Connection pools, ORM | database-engineer, data-engineer |
| ML/AI | PyTorch/TensorFlow | Model APIs, Feature stores | ai-engineer, data-engineer |
| Infrastructure | Kubernetes/Docker | Service discovery, Config | devops-engineer |
| Security | OAuth/TLS/Vault | All service boundaries | security-engineer |
| Blockchain | Solidity/Web3 | Smart contracts, DeFi | blockchain-engineer |
| Mobile | React Native/Flutter | APIs, Push notifications | frontend-engineer |
```

**Quality Attribute Cross-Cutting Concerns:**
```yaml
Performance:
  Backend: Connection pooling, caching, async processing
  Frontend: Code splitting, CDN, image optimization
  Database: Indexing, query optimization, read replicas
  Infrastructure: Auto-scaling, resource optimization
  Coordination: All agents with performance requirements

Security:
  Backend: Authentication, authorization, input validation
  Frontend: CSP, XSS prevention, secure communication
  Database: Encryption, access controls, audit logging
  Infrastructure: Network security, secrets management
  Coordination: security-engineer with all domain agents

Scalability:
  Backend: Horizontal scaling, load balancing
  Frontend: CDN, static asset optimization
  Database: Sharding, read replicas, connection pooling
  Infrastructure: Container orchestration, auto-scaling
  Coordination: devops-engineer with all domain agents

Maintainability:
  Backend: Clean architecture, dependency injection
  Frontend: Component-based design, state management
  Database: Schema versioning, migration strategies
  Infrastructure: Infrastructure as code, configuration management
  Coordination: All agents with technical-writer for documentation
```

This multi-domain expertise framework enables senior architects to provide comprehensive guidance that considers all aspects of modern system architecture while effectively coordinating specialist agents for implementation.