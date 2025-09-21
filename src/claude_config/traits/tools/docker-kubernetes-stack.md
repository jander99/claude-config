# Docker Kubernetes Stack Trait

## Description
Comprehensive containerization and orchestration toolchain including Docker, Kubernetes, Helm, and related DevOps tools. This trait standardizes container and orchestration workflows across infrastructure agents.

## Content

### Container & Orchestration Tools

**Container Tools:**
- Docker ^24.0.0 - Container runtime with multi-stage builds and optimization
- Docker Compose ^2.23.0 - Multi-container application orchestration for development
- Buildah ^1.32.0 - Alternative container builder with enhanced security features
- Podman ^4.7.0 - Daemonless container engine with Docker compatibility

**Kubernetes Tools:**
- kubectl ^1.28.0 - Kubernetes command-line interface for cluster management
- Helm ^3.13.0 - Package manager for Kubernetes with templating and versioning
- Kustomize ^5.1.0 - Kubernetes native configuration management
- Skaffold ^2.8.0 - CI/CD workflow tool for Kubernetes development

**Infrastructure as Code:**
- Terraform ^1.6.0 - Infrastructure provisioning with provider ecosystem
- Pulumi ^3.90.0 - Modern infrastructure as code with programming language support
- Ansible ^8.5.0 - Configuration management and application deployment
- CloudFormation - AWS native infrastructure as code

**Monitoring & Observability:**
- Prometheus ^2.47.0 - Metrics collection and alerting for cloud-native environments
- Grafana ^10.2.0 - Visualization and dashboards for monitoring data
- Jaeger ^1.50.0 - Distributed tracing for microservices
- FluentD ^1.16.0 - Unified logging layer for containerized environments

### Docker Configuration Patterns

**Multi-stage Dockerfile:**
```dockerfile
# Multi-stage build for Python application
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim as runtime

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
WORKDIR /app
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Docker Compose Configuration:**
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Kubernetes Configuration Patterns

**Deployment Manifest:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: myapp:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**Service and Ingress:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  selector:
    app: web-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: web-app-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app-service
            port:
              number: 80
```

### Helm Chart Structure

**Chart.yaml:**
```yaml
apiVersion: v2
name: web-app
description: A Helm chart for web application
type: application
version: 0.1.0
appVersion: "1.0.0"
dependencies:
  - name: postgresql
    version: 12.1.2
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

**Values.yaml:**
```yaml
replicaCount: 3

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: ""

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: web-app-tls
      hosts:
        - myapp.example.com

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

postgresql:
  enabled: true
  auth:
    postgresPassword: secretpassword
    database: myapp
```

### Development Workflow

**Docker Development:**
```bash
# Build image
docker build -t myapp:latest .

# Run container locally
docker run -p 8000:8000 myapp:latest

# Run with compose
docker-compose up -d

# View logs
docker-compose logs -f app
```

**Kubernetes Development:**
```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app=web-app

# Port forward for local testing
kubectl port-forward svc/web-app-service 8000:80

# View logs
kubectl logs -l app=web-app -f
```

**Helm Workflow:**
```bash
# Install chart
helm install web-app ./helm-chart

# Upgrade deployment
helm upgrade web-app ./helm-chart

# Check status
helm status web-app

# Rollback if needed
helm rollback web-app 1
```

### Security Best Practices

**Container Security:**
- Use minimal base images (Alpine, distroless)
- Run containers as non-root users
- Implement proper health checks
- Scan images for vulnerabilities
- Use multi-stage builds to reduce attack surface

**Kubernetes Security:**
- Implement RBAC policies
- Use network policies for traffic control
- Configure security contexts
- Implement pod security standards
- Use secrets for sensitive data

## Usage Notes

- **Which agents should use this trait**: devops-engineer, platform-engineer, any agent working with containerization and orchestration
- **Customization guidance**: Cloud-specific configurations can be added (e.g., EKS-specific settings for AWS deployments)
- **Compatibility requirements**: Docker 20+ and Kubernetes 1.25+ with proper RBAC permissions

## Implementation Priority
**MEDIUM** - This trait affects 3-4 infrastructure-focused agents and provides comprehensive containerization standardization