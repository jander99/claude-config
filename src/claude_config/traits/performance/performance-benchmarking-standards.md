---
name: "Performance Benchmarking Standards"
description: "Comprehensive performance testing and monitoring standards"
category: "performance"
coverage: "Load testing, performance metrics, SLA/SLO definitions, monitoring practices"
version: "1.0"
---

## Performance Testing Standards

### Load Testing Frameworks
- **JMeter**: Enterprise-grade performance testing with GUI and CLI modes
- **K6**: Modern load testing with JavaScript scripting and cloud integration
- **Artillery**: High-performance load testing with real-time metrics
- **Locust**: Python-based distributed load testing with web UI
- **Apache Bench (ab)**: Quick HTTP server benchmarking for basic tests

### Performance Metrics Collection
```yaml
response_time_metrics:
  - "P50 (median): Target < 200ms for web applications"
  - "P95: Target < 500ms for 95% of requests"
  - "P99: Target < 1000ms for 99% of requests"
  - "P99.9: Target < 2000ms for critical path optimization"

throughput_metrics:
  - "Requests per second (RPS) sustained load capacity"
  - "Concurrent user capacity with acceptable response times"
  - "Transaction throughput for business-critical operations"
  - "Data throughput for file transfers and streaming"

resource_utilization:
  - "CPU utilization target: < 80% under normal load"
  - "Memory utilization target: < 85% with GC overhead"
  - "Disk I/O target: < 80% sustained throughput"
  - "Network utilization target: < 70% bandwidth capacity"
```

### SLA/SLO Definitions
```yaml
availability_targets:
  tier_1_critical: "99.99% uptime (4.3 minutes downtime/month)"
  tier_2_important: "99.9% uptime (43 minutes downtime/month)"
  tier_3_standard: "99.5% uptime (3.6 hours downtime/month)"

performance_targets:
  api_endpoints: "P95 < 300ms, P99 < 800ms"
  database_queries: "P95 < 100ms, P99 < 500ms"
  file_uploads: "P95 < 2s for 10MB files"
  search_operations: "P95 < 150ms for typical queries"
```

## Monitoring and Observability

### Application Performance Monitoring (APM)
- **New Relic**: Full-stack observability with AI-driven insights
- **DataDog**: Infrastructure and application monitoring with alerting
- **AppDynamics**: Business transaction monitoring and root cause analysis
- **Dynatrace**: AI-powered performance monitoring and automatic discovery

### Infrastructure Monitoring Stack
```yaml
metrics_collection:
  - "Prometheus: Time-series metrics collection and storage"
  - "Grafana: Visualization dashboards and alerting"
  - "InfluxDB: High-performance time-series database"
  - "CloudWatch/Azure Monitor: Cloud-native monitoring services"

logging_aggregation:
  - "ELK Stack: Elasticsearch, Logstash, Kibana for log analysis"
  - "Fluentd: Data collection and processing for unified logging"
  - "Splunk: Enterprise log management and analysis"
  - "Loki: Prometheus-inspired log aggregation system"

distributed_tracing:
  - "Jaeger: Distributed tracing for microservices"
  - "Zipkin: Distributed tracing system for latency analysis"
  - "OpenTelemetry: Vendor-neutral observability framework"
  - "AWS X-Ray: Distributed application tracing service"
```

### Performance Testing Scenarios
```yaml
load_testing_types:
  smoke_testing: "Minimal load to verify basic functionality"
  load_testing: "Expected production load for sustained periods"
  stress_testing: "Beyond normal capacity to find breaking points"
  spike_testing: "Sudden load increases to test auto-scaling"
  volume_testing: "Large amounts of data processing capabilities"
  endurance_testing: "Sustained load over extended periods"
```

## Performance Optimization Strategies

### Database Performance
- **Query Optimization**: Index analysis, query plan review, parameter optimization
- **Connection Pooling**: Optimal pool sizing, connection lifecycle management
- **Caching Strategies**: Redis/Memcached implementation, cache invalidation
- **Read Replicas**: Load distribution, eventual consistency handling

### Application Performance
- **Code Profiling**: Memory usage analysis, CPU hotspot identification
- **Caching Layers**: Application-level caching, CDN optimization
- **Async Processing**: Queue-based processing, background job optimization
- **Resource Management**: Memory leak prevention, garbage collection tuning

### Infrastructure Performance
- **Auto-scaling**: Predictive scaling, threshold optimization
- **Load Balancing**: Algorithm selection, health check configuration
- **CDN Configuration**: Cache policies, geographic distribution
- **Network Optimization**: Compression, keep-alive connections

## Performance Benchmarking Checklist
- [ ] Load testing scenarios documented and automated
- [ ] Performance baselines established for all critical paths
- [ ] SLA/SLO targets defined with business stakeholder agreement
- [ ] Monitoring dashboards configured with actionable alerts
- [ ] Performance regression testing integrated into CI/CD
- [ ] Capacity planning models validated with actual load testing
- [ ] Performance optimization recommendations prioritized by impact
- [ ] Regular performance reviews scheduled with stakeholders