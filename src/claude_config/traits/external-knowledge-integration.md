# External Knowledge Integration Trait

**Type**: Enhancement
**Version**: 1.0
**Dependencies**: MCP servers (Context7, DeepWiki, GitHub)
**Purpose**: Real-time access to external documentation, best practices, and compliance standards

## Integration Capabilities

### Real-Time Documentation Access

**Context7 Integration:**
- Framework documentation with 99% coverage of popular libraries
- Real-time API reference with code examples and trust scoring
- Version-specific guidance with migration paths and best practices
- Intelligent caching with 2-second response time targets

**DeepWiki Integration:**
- Repository-specific documentation and implementation patterns
- Cross-project best practices and architectural insights
- Community-driven knowledge with quality filtering
- Automated content indexing and relevance scoring

**GitHub MCP Integration:**
- Release notes and changelog analysis for framework updates
- Issue tracking and known problem identification
- Community contribution patterns and project health metrics
- Security advisory monitoring and vulnerability tracking

### Industry Best Practices Database

**Content Sources:**
- Google Engineering Practices (Code review, documentation, testing)
- Microsoft Azure Architecture Patterns (Cloud-native, microservices)
- AWS Well-Architected Framework (Scalability, security, cost optimization)
- Martin Fowler Architecture Patterns (Enterprise patterns, refactoring)
- Clean Architecture Principles (SOLID, design patterns)
- The Twelve-Factor App (Cloud-native application methodology)

**Automated Curation:**
```python
# Quality scoring algorithm
def calculate_content_quality(content, source_authority):
    base_score = source_authority  # 7.5-10.0 range

    # Code example bonus
    code_blocks = len(re.findall(r'```[\s\S]*?```', content))
    code_bonus = min(code_blocks * 0.5, 2.0)

    # Structure bonus
    headers = len(re.findall(r'^#{1,6}\s+', content, re.MULTILINE))
    structure_bonus = min(headers * 0.2, 1.0)

    # Authority indicators
    authority_patterns = ['rfc', 'iso', 'nist', 'owasp']
    authority_bonus = sum(0.5 for pattern in authority_patterns if pattern in content.lower())

    return min(10.0, base_score + code_bonus + structure_bonus + authority_bonus)
```

### Security and Compliance Standards

**Supported Frameworks:**
- **OWASP Top 10 2021**: Web application security risks with implementation guidance
- **OWASP API Security Top 10**: API-specific security controls and validation
- **NIST Cybersecurity Framework**: Comprehensive cybersecurity risk management
- **ISO 27001:2022**: Information security management system controls
- **SOC 2 Type II**: Trust services criteria for security and availability
- **GDPR Compliance**: Data protection and privacy requirements

**Compliance Assessment:**
```python
async def assess_framework_compliance(framework, technology_stack):
    applicable_controls = get_applicable_controls(framework, technology_stack)

    assessment_result = {
        'framework': framework,
        'overall_score': 0.0,
        'control_results': {},
        'recommendations': []
    }

    for control in applicable_controls:
        control_score = evaluate_control_implementation(control, technology_stack)
        assessment_result['control_results'][control.id] = control_score

        if control_score['status'] != 'compliant':
            assessment_result['recommendations'].extend(control_score['recommendations'])

    return assessment_result
```

## Agent Integration Patterns

### Framework-Specific Enhancement

**Python/Django Agents:**
```yaml
external_knowledge:
  framework_docs:
    - source: "Context7:/websites/django"
      trust_threshold: 8.0
      cache_ttl: 7200
    - source: "DeepWiki:django/django"
      focus: "security,performance,best_practices"

  security_standards:
    - framework: "OWASP_TOP_10"
      applicable_controls: ["A01_2021", "A02_2021", "A03_2021"]
    - framework: "GDPR"
      focus: "data_protection,privacy_by_design"

  best_practices:
    - domain: "web_security"
      sources: ["OWASP", "Django Security Guide"]
    - domain: "performance"
      sources: ["Django Performance", "Database Optimization"]
```

**React/Frontend Agents:**
```yaml
external_knowledge:
  framework_docs:
    - source: "Context7:/facebook/react"
      version_specific: true
      focus: "hooks,performance,testing"
    - source: "Context7:/vercel/next.js"
      integration_patterns: true

  security_standards:
    - framework: "OWASP_TOP_10"
      applicable_controls: ["A01_2021", "A05_2021", "A06_2021"]
      frontend_specific: true

  performance_guides:
    - source: "Web Vitals"
    - source: "React Performance"
    - source: "Bundle Optimization"
```

### Real-Time Knowledge Injection

**Template Integration:**
```jinja2
{% if external_knowledge.enabled %}
## Real-Time Documentation Access

{{ agent_type|get_framework_documentation(focus_area="security") }}

### Current Best Practices

{{ agent_type|get_best_practices(domain="performance", limit=5) }}

### Security Compliance

{{ technology_stack|get_security_requirements(frameworks=["OWASP_TOP_10", "NIST_CSF"]) }}

### Implementation Examples

{{ framework|get_implementation_examples(pattern="authentication", trust_threshold=8.0) }}
{% endif %}
```

### Intelligent Caching Strategy

**Multi-Layer Caching:**
```python
class ExternalKnowledgeCache:
    def __init__(self):
        self.l1_memory = {}     # Hot data: 30min TTL
        self.l2_redis = {}      # Warm data: 2hour TTL
        self.l3_persistent = {} # Cold data: 24hour TTL

    async def get_knowledge(self, key, authority_threshold=7.5):
        # L1 check: Memory cache for frequent lookups
        if cached := self.l1_memory.get(key):
            if not self.is_expired(cached) and cached.authority >= authority_threshold:
                return cached

        # L2 check: Redis cache for recent lookups
        if cached := await self.l2_redis.get(key):
            if not self.is_expired(cached) and cached.authority >= authority_threshold:
                self.promote_to_l1(key, cached)
                return cached

        # L3 check: Persistent cache for older content
        if cached := self.l3_persistent.get(key):
            if not self.is_expired(cached) and cached.authority >= authority_threshold:
                return cached

        # Fetch from external source
        return await self.fetch_external(key)
```

## Performance Optimization

### Response Time Targets

| Source Type | Target Response Time | Cache Strategy | Fallback Method |
|-------------|---------------------|----------------|-----------------|
| Framework Docs | <2 seconds | L1 Memory (30min) | Static fallback |
| Best Practices | <3 seconds | L2 Redis (2hour) | Cached content |
| Security Standards | <1 second | L3 Persistent (24hour) | Local standards |
| Code Examples | <2 seconds | L1 Memory (1hour) | Template examples |

### Reliability Framework

**Circuit Breaker Pattern:**
```python
class KnowledgeSourceCircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = 'closed'  # closed, open, half-open

    async def call_with_protection(self, source_func, *args, **kwargs):
        if self.state == 'open':
            if self.should_attempt_reset():
                self.state = 'half-open'
            else:
                raise CircuitBreakerOpenError()

        try:
            result = await source_func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
```

**Fallback Chain:**
```python
async def get_knowledge_with_fallback(request):
    fallback_chain = [
        ('primary_source', primary_knowledge_source),
        ('backup_source', backup_knowledge_source),
        ('cache_fallback', cached_knowledge_source),
        ('static_fallback', static_knowledge_base)
    ]

    for source_name, source_func in fallback_chain:
        try:
            result = await source_func(request)
            if result and result.quality_score >= request.min_quality:
                return result
        except Exception as e:
            logger.warning(f"Fallback {source_name} failed: {e}")
            continue

    raise AllFallbacksExhaustedError()
```

## Quality Assurance

### Content Validation

**Authority Scoring:**
- Official documentation: 10.0 (NIST, ISO, W3C standards)
- Major tech companies: 9.0-9.5 (Google, Microsoft, AWS practices)
- Recognized experts: 8.5-9.0 (Martin Fowler, Uncle Bob principles)
- Community projects: 7.5-8.5 (Popular open source frameworks)
- Experimental content: 6.0-7.5 (New technologies, beta features)

**Quality Metrics:**
```python
def validate_content_quality(content, source):
    quality_score = 5.0  # Base score

    # Length appropriateness
    if 500 <= len(content) <= 5000:
        quality_score += 1.0

    # Code example presence
    code_examples = len(re.findall(r'```[\s\S]*?```', content))
    quality_score += min(code_examples * 0.5, 2.0)

    # Structured format
    if re.search(r'^#{1,6}\s+', content, re.MULTILINE):
        quality_score += 1.0

    # Reference links
    reference_links = len(re.findall(r'\[.*?\]\(https?://.*?\)', content))
    quality_score += min(reference_links * 0.2, 1.0)

    # Authority indicators
    authority_patterns = ['rfc \d+', 'iso \d+', 'nist sp', 'doi:']
    authority_matches = sum(1 for pattern in authority_patterns
                          if re.search(pattern, content, re.IGNORECASE))
    quality_score += authority_matches * 0.5

    return min(10.0, quality_score)
```

### Compliance Validation

**Implementation Verification:**
```python
async def verify_compliance_implementation(control, technology_stack):
    verification_result = {
        'control_id': control.id,
        'status': 'not_implemented',
        'evidence': [],
        'recommendations': []
    }

    # Check each verification criterion
    for criterion in control.verification_criteria:
        criterion_result = await check_criterion_implementation(
            criterion, technology_stack
        )

        if criterion_result.implemented:
            verification_result['evidence'].append(criterion_result.evidence)
        else:
            verification_result['recommendations'].append(
                f"Implement: {criterion}"
            )

    # Calculate compliance percentage
    implemented_count = len(verification_result['evidence'])
    total_criteria = len(control.verification_criteria)
    compliance_percentage = (implemented_count / total_criteria) * 100

    if compliance_percentage >= 90:
        verification_result['status'] = 'compliant'
    elif compliance_percentage >= 50:
        verification_result['status'] = 'partially_compliant'

    return verification_result
```

## Error Handling and Graceful Degradation

### Failure Modes

**Source Unavailability:**
- Automatic fallback to cached content
- Circuit breaker protection with exponential backoff
- Static knowledge base as last resort
- User notification of degraded service

**Content Quality Issues:**
- Real-time quality scoring validation
- Automatic content filtering below quality thresholds
- Multiple source validation for critical information
- User feedback integration for quality improvement

**Performance Degradation:**
- Intelligent cache warming for popular content
- Predictive prefetching based on usage patterns
- Response time monitoring with automatic optimization
- Load balancing across multiple knowledge sources

### Monitoring and Alerting

**Health Metrics:**
```python
class ExternalKnowledgeMetrics:
    def __init__(self):
        self.response_times = []
        self.success_rates = {}
        self.cache_hit_rates = {}
        self.quality_scores = []

    async def record_request(self, source, response_time, success, quality_score):
        self.response_times.append(response_time)

        if source not in self.success_rates:
            self.success_rates[source] = []
        self.success_rates[source].append(success)

        if quality_score:
            self.quality_scores.append(quality_score)

    def get_health_summary(self):
        return {
            'avg_response_time': statistics.mean(self.response_times[-100:]),
            'overall_success_rate': sum(all_successes) / len(all_successes),
            'avg_quality_score': statistics.mean(self.quality_scores[-100:]),
            'source_health': {
                source: sum(successes[-50:]) / len(successes[-50:])
                for source, successes in self.success_rates.items()
            }
        }
```

## Configuration and Customization

### Agent-Specific Configuration

```yaml
# Configuration in agent YAML files
external_knowledge:
  enabled: true

  sources:
    context7:
      enabled: true
      trust_threshold: 8.0
      max_tokens: 8000
      cache_ttl: 3600

    deepwiki:
      enabled: true
      max_depth: 1
      focus_areas: ["implementation", "best_practices"]

    github_mcp:
      enabled: true
      rate_limit: 100  # requests per hour

  compliance:
    frameworks: ["OWASP_TOP_10", "NIST_CSF"]
    assessment_frequency: "quarterly"
    min_compliance_score: 85.0

  performance:
    response_time_target: 2000  # milliseconds
    cache_strategy: "intelligent"
    fallback_enabled: true
```

### Template Customization

```jinja2
{# Custom knowledge injection based on agent type #}
{% set knowledge_config = external_knowledge.get_config(agent_type) %}

{% if knowledge_config.framework_docs %}
## {{ framework|title }} Documentation Integration

{{ get_framework_documentation(
    framework=framework,
    version=knowledge_config.version,
    focus=knowledge_config.focus_areas,
    trust_threshold=knowledge_config.trust_threshold
) }}
{% endif %}

{% if knowledge_config.security_standards %}
## Security and Compliance Requirements

{% for framework in knowledge_config.compliance.frameworks %}
{{ get_compliance_requirements(
    framework=framework,
    technology_stack=technology_stack,
    implementation_guide=true
) }}
{% endfor %}
{% endif %}
```

This trait provides comprehensive external knowledge integration capabilities, ensuring agents have access to up-to-date documentation, industry best practices, and compliance standards while maintaining high performance and reliability standards.