# CI/CD Pipeline Architecture

## Overview

CI/CD pipeline architecture provides automated build, test, and deployment processes that ensure code quality, security, and reliable software delivery through comprehensive testing, security scanning, and progressive deployment strategies across multiple environments.

## Pipeline Design Patterns

### Multi-Stage Pipeline Architecture

**Comprehensive CI/CD Flow:**
```yaml
# GitHub Actions - Comprehensive CI/CD Pipeline
name: Production CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  release:
    types: [published]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.11'

jobs:
  # Phase 1: Code Quality and Security
  code-quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Full history for SonarCloud

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Lint code
      run: npm run lint

    - name: Type check
      run: npm run type-check

    - name: Security audit
      run: npm audit --audit-level=high

    - name: SonarCloud Scan
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  # Phase 2: Comprehensive Testing
  test:
    runs-on: ubuntu-latest
    needs: code-quality
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Unit tests
      run: npm run test:unit
      env:
        CI: true

    - name: Integration tests
      run: npm run test:integration
      env:
        DATABASE_URL: postgresql://test:test@localhost:5432/testdb
        REDIS_URL: redis://localhost:6379

    - name: E2E tests
      run: npm run test:e2e
      env:
        DATABASE_URL: postgresql://test:test@localhost:5432/testdb

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage/lcov.info
        flags: unittests
        name: codecov-umbrella

  # Phase 3: Security Scanning
  security:
    runs-on: ubuntu-latest
    needs: code-quality
    steps:
    - uses: actions/checkout@v4

    - name: Run Snyk to check for vulnerabilities
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        args: --severity-threshold=high

    - name: OWASP ZAP Baseline Scan
      uses: zaproxy/action-baseline@v0.10.0
      with:
        target: 'http://testserver:3000'
        rules_file_name: '.zap/rules.tsv'

  # Phase 4: Build and Push Container
  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.event_name != 'pull_request'
    outputs:
      image-digest: ${{ steps.build.outputs.digest }}
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
    - uses: actions/checkout@v4

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
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}

    - name: Build and push Docker image
      id: build
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
        build-args: |
          VERSION=${{ github.sha }}
          BUILD_DATE=${{ github.event.head_commit.timestamp }}

  # Phase 5: Container Security Scanning
  container-security:
    runs-on: ubuntu-latest
    needs: build
    steps:
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ needs.build.outputs.image-tag }}
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy scan results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  # Phase 6: Deploy to Staging
  deploy-staging:
    runs-on: ubuntu-latest
    needs: [build, container-security]
    if: github.ref == 'refs/heads/develop'
    environment: 
      name: staging
      url: https://staging.myapp.com
    steps:
    - uses: actions/checkout@v4

    - name: Setup kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.28.0'

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1

    - name: Update kubeconfig
      run: aws eks update-kubeconfig --name staging-cluster

    - name: Deploy to staging
      run: |
        envsubst < k8s/staging/deployment.yaml | kubectl apply -f -
        kubectl rollout status deployment/myapp-staging -n staging
      env:
        IMAGE_TAG: ${{ needs.build.outputs.image-digest }}
        ENVIRONMENT: staging

    - name: Run smoke tests
      run: npm run test:smoke
      env:
        TARGET_URL: https://staging.myapp.com

  # Phase 7: Deploy to Production
  deploy-production:
    runs-on: ubuntu-latest
    needs: [build, container-security]
    if: github.ref == 'refs/heads/main'
    environment: 
      name: production
      url: https://myapp.com
    steps:
    - uses: actions/checkout@v4

    - name: Setup kubectl
      uses: azure/setup-kubectl@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1

    - name: Update kubeconfig
      run: aws eks update-kubeconfig --name production-cluster

    - name: Blue-Green deployment
      run: |
        # Deploy to green environment
        envsubst < k8s/production/deployment-green.yaml | kubectl apply -f -
        kubectl rollout status deployment/myapp-green -n production
        
        # Run production validation tests
        npm run test:production-validation
        
        # Switch traffic to green
        kubectl patch service myapp-service -n production -p '{"spec":{"selector":{"version":"green"}}}'
        
        # Wait and validate
        sleep 60
        npm run test:production-health
        
        # Scale down blue deployment
        kubectl scale deployment myapp-blue --replicas=0 -n production
      env:
        IMAGE_TAG: ${{ needs.build.outputs.image-digest }}
        ENVIRONMENT: production

    - name: Notify deployment success
      uses: 8398a7/action-slack@v3
      with:
        status: success
        text: "Production deployment successful! :rocket:"
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### GitLab CI/CD Advanced Pipeline

**Enterprise GitLab Pipeline:**
```yaml
# .gitlab-ci.yml - Enterprise pipeline with comprehensive stages
stages:
  - validate
  - test
  - security
  - build
  - deploy-staging
  - performance-test
  - deploy-production
  - post-deploy

variables:
  DOCKER_REGISTRY: $CI_REGISTRY
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE
  KUBERNETES_NAMESPACE: $CI_PROJECT_NAME
  SONAR_PROJECT_KEY: $CI_PROJECT_NAME

# Global before_script
before_script:
  - echo "CI/CD Pipeline started at $(date)"
  - echo "Commit SHA: $CI_COMMIT_SHA"
  - echo "Branch: $CI_COMMIT_REF_NAME"

# Template jobs for reusability
.base-job: &base-job
  image: node:18-alpine
  before_script:
    - npm ci --cache .npm --prefer-offline

.kubectl-job: &kubectl-job
  image: bitnami/kubectl:latest
  before_script:
    - kubectl version --client

# Validation stage
code-quality:
  <<: *base-job
  stage: validate
  script:
    - npm run lint
    - npm run prettier:check
    - npm run type-check
  artifacts:
    reports:
      codequality: gl-codequality.json
  rules:
    - if: $CI_MERGE_REQUEST_ID

dependency-check:
  <<: *base-job
  stage: validate
  script:
    - npm audit --audit-level=moderate
    - npm run license-check
  allow_failure: true

# Testing stage
unit-tests:
  <<: *base-job
  stage: test
  services:
    - name: postgres:15-alpine
      alias: postgres
    - name: redis:7-alpine
      alias: redis
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: "postgresql://test:test@postgres:5432/testdb"
    REDIS_URL: "redis://redis:6379"
  script:
    - npm run test:unit
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/

integration-tests:
  <<: *base-job
  stage: test
  services:
    - name: postgres:15-alpine
      alias: postgres
    - name: redis:7-alpine
      alias: redis
  variables:
    DATABASE_URL: "postgresql://test:test@postgres:5432/testdb"
    REDIS_URL: "redis://redis:6379"
  script:
    - npm run test:integration
  artifacts:
    reports:
      junit: integration-junit.xml

e2e-tests:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0-focal
  services:
    - name: postgres:15-alpine
      alias: postgres
    - name: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      alias: app
  variables:
    DATABASE_URL: "postgresql://test:test@postgres:5432/testdb"
    APP_URL: "http://app:3000"
  script:
    - npm ci
    - npx playwright test
  artifacts:
    reports:
      junit: e2e-results.xml
    paths:
      - playwright-report/
    when: always
    expire_in: 1 week

# Security stage
sast-sonarqube:
  stage: security
  image: sonarsource/sonar-scanner-cli:latest
  script:
    - sonar-scanner
      -Dsonar.projectKey=$SONAR_PROJECT_KEY
      -Dsonar.sources=.
      -Dsonar.host.url=$SONAR_HOST_URL
      -Dsonar.login=$SONAR_TOKEN
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_MERGE_REQUEST_ID

container-scanning:
  stage: security
  image: docker:24
  services:
    - docker:24-dind
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker pull $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - |
      docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        -v $PWD:/tmp/.cache/ \
        aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL \
        --format template --template "@contrib/sarif.tpl" \
        -o /tmp/.cache/trivy-report.sarif \
        $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    reports:
      sast: trivy-report.sarif
  needs: ["build-image"]

# Build stage
build-image:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - |
      docker build \
        --build-arg VERSION=$CI_COMMIT_SHA \
        --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
        --cache-from $CI_REGISTRY_IMAGE:latest \
        -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA \
        -t $CI_REGISTRY_IMAGE:latest \
        .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_BRANCH == "develop"

# Staging deployment
deploy-staging:
  <<: *kubectl-job
  stage: deploy-staging
  environment:
    name: staging
    url: https://staging.$CI_PROJECT_NAME.company.com
  script:
    - envsubst < k8s/staging/deployment.yaml | kubectl apply -f -
    - kubectl rollout status deployment/$CI_PROJECT_NAME-staging -n staging
    - kubectl get services -n staging
  variables:
    IMAGE_TAG: $CI_COMMIT_SHA
    ENVIRONMENT: staging
    KUBECONFIG: /tmp/kubeconfig
  before_script:
    - echo $KUBE_CONFIG_STAGING | base64 -d > $KUBECONFIG
    - kubectl version --client
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"
  needs: ["build-image", "container-scanning"]

# Performance testing
performance-test:
  stage: performance-test
  image: grafana/k6:latest
  script:
    - k6 run --out json=results.json performance-tests/load-test.js
  artifacts:
    reports:
      performance: results.json
  environment:
    name: staging
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"
  needs: ["deploy-staging"]

# Production deployment
deploy-production:
  <<: *kubectl-job
  stage: deploy-production
  environment:
    name: production
    url: https://$CI_PROJECT_NAME.company.com
  when: manual
  script:
    # Blue-Green deployment strategy
    - |
      # Deploy green version
      envsubst < k8s/production/deployment-green.yaml | kubectl apply -f -
      kubectl rollout status deployment/$CI_PROJECT_NAME-green -n production
      
      # Run production smoke tests
      k6 run --quiet smoke-tests/production-health.js
      
      # Switch traffic to green
      kubectl patch service $CI_PROJECT_NAME-service -n production \
        -p '{"spec":{"selector":{"version":"green"}}}'
      
      # Wait for traffic switch
      sleep 30
      
      # Final health check
      k6 run --quiet smoke-tests/production-health.js
      
      # Scale down blue deployment
      kubectl scale deployment $CI_PROJECT_NAME-blue --replicas=0 -n production
  variables:
    IMAGE_TAG: $CI_COMMIT_SHA
    ENVIRONMENT: production
    KUBECONFIG: /tmp/kubeconfig
  before_script:
    - echo $KUBE_CONFIG_PRODUCTION | base64 -d > $KUBECONFIG
    - kubectl version --client
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  needs: ["build-image", "container-scanning"]

# Post-deployment monitoring
post-deploy-monitoring:
  stage: post-deploy
  image: alpine/curl:latest
  script:
    - |
      # Send deployment notification to Slack
      curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"🚀 Production deployment completed successfully!\nCommit: $CI_COMMIT_SHA\nBranch: $CI_COMMIT_REF_NAME\"}" \
        $SLACK_WEBHOOK_URL
      
      # Trigger monitoring alerts setup
      curl -X POST "$MONITORING_API_URL/deployments" \
        -H "Authorization: Bearer $MONITORING_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"version\":\"$CI_COMMIT_SHA\",\"environment\":\"production\"}"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  needs: ["deploy-production"]
```

## Testing Integration

### Comprehensive Testing Strategy

**Multi-Layer Testing Framework:**
```python
# pytest configuration and testing utilities
# conftest.py - Shared test configuration
import pytest
import asyncio
import docker
import psycopg2
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db, Base
from app.config import get_settings

class TestEnvironment:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.postgres_container = None
        self.redis_container = None
        self.test_db_url = None
        
    def setup_test_infrastructure(self):
        """Set up test infrastructure with Docker containers"""
        # Start PostgreSQL container
        self.postgres_container = self.docker_client.containers.run(
            "postgres:15-alpine",
            environment={
                "POSTGRES_DB": "testdb",
                "POSTGRES_USER": "test",
                "POSTGRES_PASSWORD": "test"
            },
            ports={"5432/tcp": ("127.0.0.1", 0)},  # Random available port
            detach=True,
            remove=True
        )
        
        # Wait for PostgreSQL to be ready
        self._wait_for_postgres()
        
        # Start Redis container
        self.redis_container = self.docker_client.containers.run(
            "redis:7-alpine",
            ports={"6379/tcp": ("127.0.0.1", 0)},
            detach=True,
            remove=True
        )
        
        # Wait for Redis to be ready
        self._wait_for_redis()
        
    def _wait_for_postgres(self):
        """Wait for PostgreSQL to be ready"""
        import time
        postgres_port = self.postgres_container.ports["5432/tcp"][0]["HostPort"]
        self.test_db_url = f"postgresql://test:test@localhost:{postgres_port}/testdb"
        
        max_retries = 30
        for _ in range(max_retries):
            try:
                conn = psycopg2.connect(self.test_db_url)
                conn.close()
                break
            except psycopg2.OperationalError:
                time.sleep(1)
        else:
            raise RuntimeError("PostgreSQL container failed to start")
    
    def _wait_for_redis(self):
        """Wait for Redis to be ready"""
        import time
        redis_port = self.redis_container.ports["6379/tcp"][0]["HostPort"]
        
        max_retries = 30
        for _ in range(max_retries):
            try:
                r = redis.Redis(host='localhost', port=redis_port)
                r.ping()
                break
            except redis.ConnectionError:
                time.sleep(1)
        else:
            raise RuntimeError("Redis container failed to start")
    
    def cleanup(self):
        """Clean up test infrastructure"""
        if self.postgres_container:
            self.postgres_container.stop()
        if self.redis_container:
            self.redis_container.stop()

# Global test environment
test_env = TestEnvironment()

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment for the entire test session"""
    test_env.setup_test_infrastructure()
    yield
    test_env.cleanup()

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test"""
    engine = create_engine(test_env.test_db_url)
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield SessionLocal()
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture
def client(test_db):
    """FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def authenticated_client(client, test_user):
    """Authenticated test client"""
    login_data = {"username": test_user.email, "password": "testpassword"}
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

# Unit test example
# test_user_service.py
import pytest
from unittest.mock import Mock, patch
from app.services.user_service import UserService
from app.models.user import User
from app.exceptions import UserNotFoundError

class TestUserService:
    @pytest.fixture
    def user_service(self, test_db):
        return UserService(test_db)
    
    @pytest.fixture
    def sample_user(self):
        return User(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            is_active=True
        )
    
    def test_create_user_success(self, user_service, test_db):
        """Test successful user creation"""
        user_data = {
            "email": "newuser@example.com",
            "password": "securepassword",
            "first_name": "New",
            "last_name": "User"
        }
        
        user = user_service.create_user(user_data)
        
        assert user.email == user_data["email"]
        assert user.first_name == user_data["first_name"]
        assert user.is_active is True
        assert user.id is not None
    
    def test_create_user_duplicate_email(self, user_service, sample_user, test_db):
        """Test user creation with duplicate email"""
        test_db.add(sample_user)
        test_db.commit()
        
        user_data = {
            "email": sample_user.email,
            "password": "password",
            "first_name": "Duplicate",
            "last_name": "User"
        }
        
        with pytest.raises(ValueError, match="Email already exists"):
            user_service.create_user(user_data)
    
    @patch('app.services.email_service.send_welcome_email')
    def test_create_user_sends_welcome_email(self, mock_send_email, user_service):
        """Test that welcome email is sent on user creation"""
        user_data = {
            "email": "newuser@example.com",
            "password": "securepassword",
            "first_name": "New",
            "last_name": "User"
        }
        
        user = user_service.create_user(user_data)
        
        mock_send_email.assert_called_once_with(user.email, user.first_name)

# Integration test example
# test_api_integration.py
import pytest
import asyncio
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
class TestUserAPIIntegration:
    async def test_user_registration_flow(self, client):
        """Test complete user registration and login flow"""
        # Register new user
        registration_data = {
            "email": "integration@example.com",
            "password": "securepassword123",
            "first_name": "Integration",
            "last_name": "Test"
        }
        
        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == 201
        
        user_data = response.json()
        assert user_data["email"] == registration_data["email"]
        assert "id" in user_data
        
        # Login with new user
        login_data = {
            "username": registration_data["email"],
            "password": registration_data["password"]
        }
        
        login_response = client.post("/auth/login", data=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        
        # Access protected endpoint
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        profile_response = client.get("/users/profile", headers=headers)
        
        assert profile_response.status_code == 200
        profile_data = profile_response.json()
        assert profile_data["email"] == registration_data["email"]

# Load testing with k6
load_test_script = """
// load-test.js - K6 load testing script
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

export let options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 200 }, // Ramp up to 200 users
    { duration: '5m', target: 200 }, // Stay at 200 users
    { duration: '2m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must be below 500ms
    http_req_failed: ['rate<0.1'],    // Error rate must be below 10%
    errors: ['rate<0.1'],             // Custom error rate must be below 10%
  },
};

const BASE_URL = __ENV.TARGET_URL || 'http://localhost:3000';

export function setup() {
  // Create test user for authenticated requests
  const registerResponse = http.post(`${BASE_URL}/auth/register`, {
    email: 'loadtest@example.com',
    password: 'testpassword123',
    first_name: 'Load',
    last_name: 'Test'
  });
  
  const loginResponse = http.post(`${BASE_URL}/auth/login`, {
    username: 'loadtest@example.com',
    password: 'testpassword123'
  });
  
  return { token: loginResponse.json('access_token') };
}

export default function(data) {
  const headers = {
    'Authorization': `Bearer ${data.token}`,
    'Content-Type': 'application/json'
  };
  
  // Test health endpoint
  let healthResponse = http.get(`${BASE_URL}/health`);
  check(healthResponse, {
    'health check status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);
  
  // Test authenticated API endpoint
  let apiResponse = http.get(`${BASE_URL}/api/v1/users/profile`, { headers });
  check(apiResponse, {
    'profile API status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  }) || errorRate.add(1);
  
  // Test product listing
  let productsResponse = http.get(`${BASE_URL}/api/v1/products`);
  check(productsResponse, {
    'products API status is 200': (r) => r.status === 200,
    'products response has data': (r) => r.json('data').length > 0,
  }) || errorRate.add(1);
  
  sleep(1);
}

export function teardown(data) {
  // Cleanup if needed
  console.log('Load test completed');
}
"""
```

This comprehensive CI/CD pipeline architecture provides automated quality assurance, security scanning, multi-environment deployment, and performance validation ensuring reliable and scalable software delivery across the development lifecycle.