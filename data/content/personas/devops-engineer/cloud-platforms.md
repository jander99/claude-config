# Containerization and Docker

## Overview

Containerization provides lightweight, portable, and scalable deployment solutions through Docker containers and orchestration platforms. This encompasses container design, multi-stage builds, security best practices, and integration with CI/CD pipelines for consistent application deployment across environments.

## Docker Container Design

### Optimal Dockerfile Strategies

**Multi-Stage Build Patterns:**
```dockerfile
# Multi-stage build for Node.js application
# Stage 1: Build environment
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies (including dev dependencies)
RUN yarn install --frozen-lockfile

# Copy source code
COPY . .

# Build application
RUN yarn build

# Run tests
RUN yarn test:ci

# Stage 2: Production environment
FROM node:18-alpine AS production

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install only production dependencies
RUN yarn install --production --frozen-lockfile && \
    yarn cache clean

# Copy built application from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Set security-focused environment
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Start application
CMD ["node", "dist/server.js"]
```

**Language-Specific Optimizations:**

```dockerfile
# Python application with security best practices
FROM python:3.11-alpine AS base

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

# Create non-root user
RUN adduser -D -s /bin/sh appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base AS development
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
USER appuser
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

# Production stage
FROM base AS production

# Copy application code
COPY --chown=appuser:appuser . .

# Remove development files
RUN rm -rf tests/ requirements-dev.txt .pytest_cache/ && \
    find . -name "*.pyc" -delete && \
    find . -name "__pycache__" -delete

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Container Security Best Practices

**Security-Hardened Container Configuration:**
```dockerfile
# Java Spring Boot application with comprehensive security
FROM eclipse-temurin:17-jre-alpine AS production

# Security: Install security updates and minimal tools
RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        dumb-init \
        curl \
    && rm -rf /var/cache/apk/*

# Security: Create non-root user with specific UID/GID
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

# Security: Set secure working directory
WORKDIR /app

# Security: Copy JAR with proper ownership
COPY --chown=appuser:appgroup target/application.jar app.jar

# Security: Remove unnecessary packages
RUN apk del --purge \
    && rm -rf /tmp/* /var/tmp/* \
    && rm -rf /root/.cache

# Security: Set file permissions
RUN chmod 500 app.jar && \
    chmod 700 /app

# Security: Switch to non-root user
USER appuser:appgroup

# Security: Expose minimal port
EXPOSE 8080

# Security: Set resource limits via environment
ENV JAVA_OPTS="-Xmx512m -Xms256m -XX:+UseG1GC"

# Health check with timeout
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Security: Use dumb-init as PID 1
ENTRYPOINT ["dumb-init", "--"]
CMD ["java", "$JAVA_OPTS", "-jar", "app.jar"]

# Security: Add labels for image metadata
LABEL maintainer="devops-team@company.com" \
      version="1.0.0" \
      description="Secure Spring Boot application" \
      org.opencontainers.image.source="https://github.com/company/app"
```

**Container Scanning and Vulnerability Management:**
```yaml
# Docker Compose with security scanning
version: '3.8'

services:
  app:
    build: 
      context: .
      dockerfile: Dockerfile
      target: production
    image: myapp:${VERSION:-latest}
    container_name: myapp
    
    # Security: Resource limits
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    
    # Security: Read-only root filesystem
    read_only: true
    
    # Security: Temporary filesystem for writable areas
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
      - /var/tmp:noexec,nosuid,size=50m
    
    # Security: Drop all capabilities and add only needed ones
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    
    # Security: Set user namespace
    user: "10001:10001"
    
    # Security: Prevent privilege escalation
    security_opt:
      - no-new-privileges:true
    
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## Container Orchestration

### Docker Compose for Development

**Comprehensive Development Environment:**
```yaml
# docker-compose.yml for full-stack development
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:15-alpine
    container_name: dev-postgres
    environment:
      POSTGRES_DB: ${DB_NAME:-myapp}
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-devpassword}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d:ro
    ports:
      - "${DB_PORT:-5432}:5432"
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres} -d ${DB_NAME:-myapp}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis for caching and sessions
  redis:
    image: redis:7-alpine
    container_name: dev-redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-devredis}
    volumes:
      - redis_data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
    ports:
      - "${REDIS_PORT:-6379}:6379"
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Backend API
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: development
    container_name: dev-api
    volumes:
      - ./backend:/app:cached
      - /app/node_modules
      - ./logs:/app/logs
    environment:
      NODE_ENV: development
      DATABASE_URL: postgresql://${DB_USER:-postgres}:${DB_PASSWORD:-devpassword}@postgres:5432/${DB_NAME:-myapp}
      REDIS_URL: redis://:${REDIS_PASSWORD:-devredis}@redis:6379
      JWT_SECRET: ${JWT_SECRET:-dev-jwt-secret}
      LOG_LEVEL: debug
    ports:
      - "${API_PORT:-3001}:3001"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend
      - frontend
    command: npm run dev

  # Frontend Application
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: development
    container_name: dev-frontend
    volumes:
      - ./frontend:/app:cached
      - /app/node_modules
      - /app/.next
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:${API_PORT:-3001}
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET:-dev-nextauth-secret}
      NEXTAUTH_URL: http://localhost:${FRONTEND_PORT:-3000}
    ports:
      - "${FRONTEND_PORT:-3000}:3000"
    depends_on:
      - api
    networks:
      - frontend
    command: npm run dev

  # Message Queue
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: dev-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER:-admin}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD:-devrabbit}
      RABBITMQ_DEFAULT_VHOST: ${RABBITMQ_VHOST:-/}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
      - ./rabbitmq/rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf:ro
    ports:
      - "${RABBITMQ_PORT:-5672}:5672"
      - "${RABBITMQ_MANAGEMENT_PORT:-15672}:15672"
    networks:
      - backend
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 30s
      timeout: 30s
      retries: 3

  # Background Worker
  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: development
    container_name: dev-worker
    volumes:
      - ./backend:/app:cached
      - /app/node_modules
      - ./logs:/app/logs
    environment:
      NODE_ENV: development
      DATABASE_URL: postgresql://${DB_USER:-postgres}:${DB_PASSWORD:-devpassword}@postgres:5432/${DB_NAME:-myapp}
      REDIS_URL: redis://:${REDIS_PASSWORD:-devredis}@redis:6379
      RABBITMQ_URL: amqp://${RABBITMQ_USER:-admin}:${RABBITMQ_PASSWORD:-devrabbit}@rabbitmq:5672
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    networks:
      - backend
    command: npm run worker

  # Monitoring and Observability
  prometheus:
    image: prom/prometheus:latest
    container_name: dev-prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    ports:
      - "${PROMETHEUS_PORT:-9090}:9090"
    networks:
      - monitoring
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    container_name: dev-grafana
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD:-devgrafana}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning:ro
    ports:
      - "${GRAFANA_PORT:-3001}:3000"
    depends_on:
      - prometheus
    networks:
      - monitoring

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
  prometheus_data:
  grafana_data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
  monitoring:
    driver: bridge
```

### Production Container Strategies

**Container Optimization for Production:**
```python
class ProductionContainerManager:
    def __init__(self):
        self.registry_url = os.getenv('CONTAINER_REGISTRY_URL')
        self.image_scanning_enabled = True
        self.security_policies = SecurityPolicyManager()
    
    def build_production_image(self, app_config):
        """
        Build optimized production container images
        """
        build_args = {
            'BUILD_ENV': 'production',
            'NODE_ENV': 'production',
            'PYTHON_ENV': 'production'
        }
        
        # Multi-arch build for ARM and AMD64
        build_platforms = ['linux/amd64', 'linux/arm64']
        
        # Build with security scanning
        build_config = {
            'dockerfile': 'Dockerfile',
            'context': app_config['build_context'],
            'target': 'production',
            'build_args': build_args,
            'platforms': build_platforms,
            'cache_from': [f"{self.registry_url}/{app_config['name']}:cache"],
            'cache_to': f"{self.registry_url}/{app_config['name']}:cache",
            'labels': {
                'version': app_config['version'],
                'git.commit': app_config['git_commit'],
                'build.date': datetime.utcnow().isoformat(),
                'maintainer': 'devops@company.com'
            }
        }
        
        # Execute build
        image = self.docker_client.images.build(**build_config)
        
        # Security scan before push
        if self.image_scanning_enabled:
            scan_results = self.scan_image_vulnerabilities(image.id)
            if scan_results['critical_vulns'] > 0:
                raise SecurityVulnerabilityError(
                    f"Critical vulnerabilities found: {scan_results['critical_vulns']}"
                )
        
        return image
    
    def scan_image_vulnerabilities(self, image_id):
        """
        Scan container image for security vulnerabilities
        """
        # Use Trivy for vulnerability scanning
        scan_command = [
            'trivy', 'image',
            '--format', 'json',
            '--severity', 'HIGH,CRITICAL',
            '--ignore-unfixed',
            image_id
        ]
        
        result = subprocess.run(scan_command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise ImageScanError(f"Image scan failed: {result.stderr}")
        
        scan_data = json.loads(result.stdout)
        
        # Analyze results
        vulnerability_summary = {
            'critical_vulns': 0,
            'high_vulns': 0,
            'medium_vulns': 0,
            'low_vulns': 0,
            'total_vulns': 0
        }
        
        for target in scan_data.get('Results', []):
            for vuln in target.get('Vulnerabilities', []):
                severity = vuln.get('Severity', '').lower()
                vulnerability_summary[f'{severity}_vulns'] += 1
                vulnerability_summary['total_vulns'] += 1
        
        return vulnerability_summary
    
    def deploy_with_rolling_update(self, service_config):
        """
        Deploy container with zero-downtime rolling update
        """
        deployment_config = {
            'image': f"{self.registry_url}/{service_config['name']}:{service_config['version']}",
            'replicas': service_config.get('replicas', 3),
            'update_config': {
                'parallelism': 1,
                'delay': '10s',
                'failure_action': 'rollback',
                'monitor': '60s',
                'max_failure_ratio': 0.1
            },
            'restart_policy': {
                'condition': 'on-failure',
                'delay': '5s',
                'max_attempts': 3,
                'window': '120s'
            },
            'resources': {
                'limits': {
                    'memory': service_config.get('memory_limit', '512M'),
                    'cpus': service_config.get('cpu_limit', '0.5')
                },
                'reservations': {
                    'memory': service_config.get('memory_reservation', '256M'),
                    'cpus': service_config.get('cpu_reservation', '0.25')
                }
            },
            'healthcheck': {
                'test': service_config.get('health_check_cmd', ['CMD', 'curl', '-f', 'http://localhost/health']),
                'interval': '30s',
                'timeout': '10s',
                'retries': 3,
                'start_period': '60s'
            }
        }
        
        # Execute deployment
        service = self.docker_client.services.create(**deployment_config)
        
        # Monitor deployment progress
        self.monitor_deployment_progress(service.id, service_config)
        
        return service
    
    def monitor_deployment_progress(self, service_id, service_config):
        """
        Monitor deployment progress and handle failures
        """
        timeout = service_config.get('deployment_timeout', 300)  # 5 minutes
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            service = self.docker_client.services.get(service_id)
            
            # Check service update status
            update_status = service.attrs.get('UpdateStatus', {})
            state = update_status.get('State', 'unknown')
            
            if state == 'completed':
                logger.info(f"Deployment completed successfully for service {service_id}")
                return True
            elif state == 'rollback_completed':
                logger.error(f"Deployment rolled back for service {service_id}")
                raise DeploymentError("Deployment failed and was rolled back")
            elif state in ['rollback_started', 'rollback_paused']:
                logger.warning(f"Deployment rollback in progress for service {service_id}")
            
            # Check task health
            tasks = service.tasks()
            healthy_tasks = sum(1 for task in tasks if task.get('Status', {}).get('State') == 'running')
            desired_replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas']
            
            logger.info(f"Service {service_id}: {healthy_tasks}/{desired_replicas} tasks healthy")
            
            time.sleep(10)
        
        raise DeploymentTimeoutError(f"Deployment timeout after {timeout} seconds")
```

## Registry Management

### Container Registry Operations

**Automated Registry Workflows:**
```yaml
# GitHub Actions workflow for container registry management
name: Container Build and Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix=sha-
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        target: production
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  security-scan:
    runs-on: ubuntu-latest
    needs: build
    steps:
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy scan results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  deploy-staging:
    runs-on: ubuntu-latest
    needs: [build, security-scan]
    if: github.ref == 'refs/heads/develop'
    environment: staging
    steps:
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment"
        # Add deployment logic here

  deploy-production:
    runs-on: ubuntu-latest
    needs: [build, security-scan]
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
    - name: Deploy to production
      run: |
        echo "Deploying to production environment"
        # Add deployment logic here
```

**Registry Cleanup and Management:**
```python
class ContainerRegistryManager:
    def __init__(self, registry_config):
        self.registry_url = registry_config['url']
        self.credentials = registry_config['credentials']
        self.cleanup_policies = registry_config.get('cleanup_policies', {})
    
    def cleanup_old_images(self):
        """
        Clean up old container images based on retention policies
        """
        repositories = self.list_repositories()
        
        for repo in repositories:
            images = self.list_repository_images(repo)
            images_to_delete = self.apply_retention_policies(repo, images)
            
            if images_to_delete:
                self.delete_images(repo, images_to_delete)
                logger.info(f"Cleaned up {len(images_to_delete)} images from {repo}")
    
    def apply_retention_policies(self, repository, images):
        """
        Apply retention policies to determine which images to delete
        """
        policy = self.cleanup_policies.get(repository, self.cleanup_policies.get('default', {}))
        
        # Sort images by creation date (newest first)
        images.sort(key=lambda x: x['created_at'], reverse=True)
        
        images_to_delete = []
        
        # Keep minimum number of images
        min_keep = policy.get('min_keep', 10)
        if len(images) <= min_keep:
            return images_to_delete
        
        # Apply age-based retention
        max_age_days = policy.get('max_age_days', 30)
        cutoff_date = datetime.utcnow() - timedelta(days=max_age_days)
        
        for image in images[min_keep:]:  # Skip the minimum keep count
            if image['created_at'] < cutoff_date:
                # Don't delete if image has specific tags to preserve
                protected_tags = policy.get('protected_tags', ['latest', 'stable'])
                if not any(tag in protected_tags for tag in image.get('tags', [])):
                    images_to_delete.append(image)
        
        return images_to_delete
    
    def scan_registry_security(self):
        """
        Scan all images in registry for security vulnerabilities
        """
        repositories = self.list_repositories()
        vulnerability_report = {}
        
        for repo in repositories:
            images = self.list_repository_images(repo)
            repo_vulnerabilities = {}
            
            for image in images:
                scan_results = self.scan_image_vulnerabilities(
                    f"{self.registry_url}/{repo}:{image['digest']}"
                )
                repo_vulnerabilities[image['digest']] = scan_results
            
            vulnerability_report[repo] = repo_vulnerabilities
        
        # Generate security report
        self.generate_security_report(vulnerability_report)
        
        return vulnerability_report
    
    def promote_image(self, source_tag, target_tag, environment):
        """
        Promote image from one environment to another
        """
        # Validate source image exists
        source_image = f"{self.registry_url}/{source_tag}"
        if not self.image_exists(source_image):
            raise ImageNotFoundError(f"Source image not found: {source_image}")
        
        # Security scan before promotion
        scan_results = self.scan_image_vulnerabilities(source_image)
        if scan_results['critical_vulns'] > 0:
            raise SecurityVulnerabilityError(
                f"Cannot promote image with critical vulnerabilities: {scan_results['critical_vulns']}"
            )
        
        # Tag image for target environment
        target_image = f"{self.registry_url}/{target_tag}"
        
        # Copy image to target tag
        self.copy_image(source_image, target_image)
        
        # Update deployment manifest
        self.update_deployment_manifest(target_tag, environment)
        
        logger.info(f"Successfully promoted {source_tag} to {target_tag} for {environment}")
        
        return {
            'source_tag': source_tag,
            'target_tag': target_tag,
            'environment': environment,
            'promotion_time': datetime.utcnow().isoformat()
        }
```

This comprehensive containerization framework provides production-ready container strategies, security best practices, and automated registry management for scalable application deployment across different environments.