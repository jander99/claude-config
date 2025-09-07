# Kubernetes Orchestration

## Overview

Kubernetes orchestration provides automated deployment, scaling, and management of containerized applications through declarative configuration, service discovery, load balancing, and self-healing capabilities that ensure reliable and scalable application operations.

## Cluster Architecture and Setup

### Production Cluster Configuration

**High-Availability Cluster Setup:**
```yaml
# Cluster configuration with kubeadm
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: v1.28.2
clusterName: production-cluster
controlPlaneEndpoint: "k8s-api.company.com:6443"

# High availability configuration
etcd:
  external:
    endpoints:
    - https://etcd1.company.com:2379
    - https://etcd2.company.com:2379
    - https://etcd3.company.com:2379
    caFile: /etc/ssl/etcd/ca.crt
    certFile: /etc/ssl/etcd/etcd.crt
    keyFile: /etc/ssl/etcd/etcd.key

networking:
  serviceSubnet: "10.96.0.0/16"
  podSubnet: "10.244.0.0/16"

apiServer:
  advertiseAddress: "10.0.1.10"
  bindPort: 6443
  certSANs:
  - "k8s-api.company.com"
  - "10.0.1.10"
  - "10.0.1.11"
  - "10.0.1.12"
  extraArgs:
    audit-log-maxage: "30"
    audit-log-maxbackup: "10"
    audit-log-maxsize: "100"
    audit-log-path: "/var/log/audit.log"
    enable-admission-plugins: "NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook"

controllerManager:
  extraArgs:
    bind-address: "0.0.0.0"
    
scheduler:
  extraArgs:
    bind-address: "0.0.0.0"

---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
ipvs:
  strictARP: true
```

**Node Configuration and Taints:**
```yaml
# Node labeling and taints for workload separation
apiVersion: v1
kind: Node
metadata:
  name: worker-node-1
  labels:
    node-role.kubernetes.io/worker: ""
    node.kubernetes.io/instance-type: "m5.2xlarge"
    topology.kubernetes.io/zone: "us-east-1a"
    workload-type: "compute-optimized"
spec:
  taints:
  - key: "workload-type"
    value: "compute-optimized"
    effect: "NoSchedule"

---
# Dedicated node pool for database workloads
apiVersion: v1
kind: Node
metadata:
  name: database-node-1
  labels:
    node-role.kubernetes.io/database: ""
    node.kubernetes.io/instance-type: "r5.xlarge"
    workload-type: "memory-optimized"
spec:
  taints:
  - key: "workload-type"
    value: "memory-optimized" 
    effect: "NoSchedule"
```

### Network Policies and Security

**Network Segmentation:**
```yaml
# Default deny-all network policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# Allow frontend to backend communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend-api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    - namespaceSelector:
        matchLabels:
          name: frontend
    ports:
    - protocol: TCP
      port: 8080

---
# Allow backend to database communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-to-database
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: postgresql
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend-api
    ports:
    - protocol: TCP
      port: 5432

---
# Egress policy for external API calls
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-egress-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend-api
  policyTypes:
  - Egress
  egress:
  # Allow DNS resolution
  - ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
  # Allow HTTPS to external APIs
  - ports:
    - protocol: TCP
      port: 443
    to:
    - namespaceSelector: {}
  # Allow database connection
  - ports:
    - protocol: TCP
      port: 5432
    to:
    - podSelector:
        matchLabels:
          app: postgresql
```

## Application Deployment

### Deployment Strategies

**Blue-Green Deployment:**
```yaml
# Blue deployment (current production)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  namespace: production
  labels:
    app: myapp
    version: blue
    deployment-strategy: blue-green
spec:
  replicas: 5
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myregistry.com/myapp:v1.2.3
        ports:
        - containerPort: 8080
        env:
        - name: ENV
          value: "production"
        - name: VERSION
          value: "blue"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
  namespace: production
  labels:
    app: myapp
    version: green
    deployment-strategy: blue-green
spec:
  replicas: 5
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: myapp
        image: myregistry.com/myapp:v1.3.0
        ports:
        - containerPort: 8080
        env:
        - name: ENV
          value: "production"
        - name: VERSION
          value: "green"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

---
# Service that can switch between blue and green
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: production
spec:
  selector:
    app: myapp
    version: blue  # Switch to 'green' during deployment
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
```

**Canary Deployment with Argo Rollouts:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp-canary
  namespace: production
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 60s}
      - setWeight: 20
      - pause: {duration: 60s}
      - setWeight: 50
      - pause: {duration: 300s}
      - setWeight: 80
      - pause: {duration: 300s}
      canaryService: myapp-canary
      stableService: myapp-stable
      trafficRouting:
        nginx:
          stableIngress: myapp-ingress
          additionalIngressAnnotations:
            canary-by-header: "X-Canary"
      analysis:
        templates:
        - templateName: success-rate
        args:
        - name: service-name
          value: myapp-canary
        - name: prometheus-url
          value: http://prometheus.monitoring:9090
        startingStep: 2
        interval: 60s
        count: 5
        successCondition: result[0] >= 0.95
        failureCondition: result[0] < 0.90
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myregistry.com/myapp:v1.3.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi" 
            cpu: "500m"

---
# Analysis template for canary validation
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
  namespace: production
spec:
  args:
  - name: service-name
  - name: prometheus-url
  metrics:
  - name: success-rate
    interval: 60s
    count: 5
    successCondition: result[0] >= 0.95
    failureCondition: result[0] < 0.90
    provider:
      prometheus:
        address: "{{args.prometheus-url}}"
        query: |
          rate(
            http_requests_total{
              job="{{args.service-name}}",
              status!~"5.."
            }[2m]
          ) /
          rate(
            http_requests_total{
              job="{{args.service-name}}"
            }[2m]
          )
```

### ConfigMaps and Secrets Management

**Comprehensive Configuration Management:**
```yaml
# Application configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: production
data:
  app.yaml: |
    server:
      port: 8080
      timeout: 30s
    database:
      host: postgresql-service
      port: 5432
      name: myapp_db
      ssl_mode: require
    cache:
      host: redis-service
      port: 6379
      ttl: 3600
    logging:
      level: info
      format: json
    features:
      new_ui: true
      advanced_metrics: true

---
# Database credentials (sealed secret)
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  encryptedData:
    username: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEQAx...
    password: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEQAx...
    connection_string: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEQAx...
  template:
    metadata:
      name: database-credentials
      namespace: production
    type: Opaque

---
# TLS certificates
apiVersion: v1
kind: Secret
metadata:
  name: tls-certificate
  namespace: production
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t...
  tls.key: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0t...

---
# External secrets operator configuration
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.company.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp-role"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-secret
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: database/production
      property: username
  - secretKey: password
    remoteRef:
      key: database/production
      property: password
```

## Service Mesh and Load Balancing

### Istio Service Mesh Configuration

**Service Mesh Architecture:**
```yaml
# Istio Gateway for external traffic
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: myapp-gateway
  namespace: production
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: myapp-tls-secret
    hosts:
    - "api.mycompany.com"
    - "app.mycompany.com"
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "api.mycompany.com"
    - "app.mycompany.com"
    tls:
      httpsRedirect: true

---
# Virtual Service for traffic routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp-routes
  namespace: production
spec:
  hosts:
  - "api.mycompany.com"
  - "app.mycompany.com"
  gateways:
  - myapp-gateway
  http:
  - match:
    - uri:
        prefix: "/api/v1"
    route:
    - destination:
        host: backend-service
        port:
          number: 8080
      weight: 90
    - destination:
        host: backend-service-canary
        port:
          number: 8080
      weight: 10
    fault:
      delay:
        percentage:
          value: 0.1
        fixedDelay: 5s
    retries:
      attempts: 3
      perTryTimeout: 2s
  - match:
    - uri:
        prefix: "/"
    route:
    - destination:
        host: frontend-service
        port:
          number: 80

---
# Destination Rule for load balancing and circuit breaking
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: backend-destination
  namespace: production
spec:
  host: backend-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 200
        maxRequestsPerConnection: 10
        maxRetries: 5
        consecutiveGatewayErrors: 5
        interval: 30s
        baseEjectionTime: 30s
    circuitBreaker:
      consecutiveGatewayErrors: 5
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  portLevelSettings:
  - port:
      number: 8080
    connectionPool:
      tcp:
        maxConnections: 50

---
# Service Entry for external dependencies
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: external-payment-api
  namespace: production
spec:
  hosts:
  - payment-api.external-company.com
  ports:
  - number: 443
    name: https
    protocol: HTTPS
  location: MESH_EXTERNAL
  resolution: DNS

---
# Istio Authorization Policy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: backend-access-control
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend-service
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend-service"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/v1/*"]
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/admin-service"]
    to:
    - operation:
        methods: ["GET", "POST", "PUT", "DELETE"]
        paths: ["/admin/*"]
```

### Horizontal Pod Autoscaling

**Advanced HPA Configuration:**
```yaml
# HPA with custom metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-deployment
  minReplicas: 3
  maxReplicas: 50
  metrics:
  # CPU utilization
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Memory utilization
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  # Custom metric: requests per second
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
  # External metric: queue length
  - type: External
    external:
      metric:
        name: queue_length
        selector:
          matchLabels:
            queue: myapp-queue
      target:
        type: AverageValue
        averageValue: "10"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 5
        periodSeconds: 60
      selectPolicy: Max

---
# Vertical Pod Autoscaler
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-deployment
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: myapp
      maxAllowed:
        cpu: "2"
        memory: "4Gi"
      minAllowed:
        cpu: "100m"
        memory: "128Mi"
      controlledResources: ["cpu", "memory"]
```

## Monitoring and Observability

### Prometheus and Grafana Setup

**Comprehensive Monitoring Stack:**
```yaml
# Prometheus configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
    - "/etc/prometheus/rules/*.yml"
    
    scrape_configs:
    - job_name: 'kubernetes-apiservers'
      kubernetes_sd_configs:
      - role: endpoints
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

    - job_name: 'kubernetes-nodes'
      kubernetes_sd_configs:
      - role: node
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)

    - job_name: 'istio-mesh'
      kubernetes_sd_configs:
      - role: endpoints
        namespaces:
          names:
          - istio-system
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: istio-telemetry;prometheus

---
# Alert rules
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-rules
  namespace: monitoring
data:
  app-rules.yml: |
    groups:
    - name: application.rules
      rules:
      - alert: HighErrorRate
        expr: |
          (
            rate(http_requests_total{status=~"5.."}[5m])
            /
            rate(http_requests_total[5m])
          ) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High error rate detected
          description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.job }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
          description: "95th percentile latency is {{ $value }}s for {{ $labels.job }}"

      - alert: PodCrashLooping
        expr: |
          rate(kube_pod_container_status_restarts_total[15m]) * 60 * 15 > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: Pod is crash looping
          description: "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is crash looping"

---
# Grafana dashboard for application metrics
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-app
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  app-dashboard.json: |
    {
      "dashboard": {
        "id": null,
        "title": "Application Metrics",
        "tags": ["kubernetes", "application"],
        "timezone": "browser",
        "panels": [
          {
            "id": 1,
            "title": "Request Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total[5m])",
                "legendFormat": "{{ job }} - {{ method }}"
              }
            ]
          },
          {
            "id": 2,
            "title": "Error Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
                "legendFormat": "{{ job }} - Errors"
              }
            ]
          },
          {
            "id": 3,
            "title": "Response Time",
            "type": "graph",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
                "legendFormat": "{{ job }} - 95th percentile"
              }
            ]
          }
        ],
        "time": {
          "from": "now-1h",
          "to": "now"
        },
        "refresh": "30s"
      }
    }
```

This comprehensive Kubernetes orchestration framework provides production-ready cluster management, advanced deployment strategies, service mesh integration, and comprehensive monitoring for scalable and reliable application operations.