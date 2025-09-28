# Comprehensive Testing Suite for Claude Config

This directory contains a comprehensive testing suite for the Claude Config MCP system, ensuring production readiness through extensive validation, security testing, and performance benchmarking.

## Test Architecture

### Test Categories

#### 1. **Unit Tests** (`test_*.py`)
- Individual module testing with focused scope
- Mock external dependencies for isolation
- Fast execution for continuous feedback
- High coverage of core functionality

#### 2. **Integration Tests** (`test_mcp_integration.py`)
- End-to-end pipeline testing (YAML → Processing → JSON)
- Real environment variable resolution
- Multi-component interaction validation
- Performance profiling under realistic loads

#### 3. **Security Tests** (`test_security_validation.py`)
- Environment injection security validation
- Command execution safety verification
- File access permission enforcement
- Secret masking and leak prevention
- Attack vector testing and prevention

#### 4. **CLI Tests** (`test_cli_enhanced.py`)
- Comprehensive command testing with error scenarios
- User interface validation and error handling
- Build process integration and validation
- Configuration override and environment testing

#### 5. **Build System Tests** (`test_build_system.py`)
- Makefile target validation and dependency testing
- Build artifact integrity verification
- Continuous integration scenario testing
- Incremental build and performance optimization

#### 6. **Performance Tests** (`test_performance.py`)
- Large configuration handling and scalability
- Memory usage profiling and leak detection
- Concurrent processing and thread safety
- Resource consumption benchmarking

#### 7. **Error Scenario Tests** (`test_error_scenarios.py`)
- Comprehensive error handling validation
- Edge case and boundary condition testing
- Malicious input handling and security
- System resilience under adverse conditions

### Test Infrastructure

#### Mock Framework (`tests/mcp/mock_infrastructure.py`)
- **MockMCPServer**: Simulates real MCP server behavior
- **MockEnvironmentResolver**: Safe environment variable testing
- **MockMCPServerManager**: Orchestrates multiple mock servers
- **MockMCPTestContext**: Complete testing environment setup

#### Fixtures and Utilities
- **Comprehensive test datasets**: Large-scale configuration generation
- **Performance profiling**: Memory and CPU usage monitoring
- **Security testing helpers**: Attack simulation and validation
- **Error injection**: Controlled failure scenario testing

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_mcp_integration.py -v
pytest tests/test_security_validation.py -v
pytest tests/test_performance.py -v

# Run with coverage reporting
pytest tests/ --cov=src/claude_config --cov-report=html --cov-report=term
```

### Test Markers

```bash
# Quick smoke tests for CI/CD
pytest tests/ -m smoke

# Comprehensive validation suite
pytest tests/ -m comprehensive

# Integration tests only
pytest tests/ -m integration

# Skip slow tests
pytest tests/ -m "not slow"

# Security-focused tests
pytest tests/ -m security
```

### Performance Testing

```bash
# Performance benchmarks
pytest tests/test_performance.py -v --durations=10

# Memory profiling
pytest tests/test_performance.py::TestMemoryUsage -v

# Scalability limits
pytest tests/test_performance.py::TestScalabilityLimits -v
```

### Security Testing

```bash
# Security validation suite
pytest tests/test_security_validation.py -v

# Environment injection security
pytest tests/test_security_validation.py::TestEnvironmentInjectionSecurity -v

# Attack scenario testing
pytest tests/test_error_scenarios.py::TestMaliciousInputHandling -v
```

## Test Configuration

### pytest.ini Configuration

The test suite uses advanced pytest configuration with:

- **Coverage Requirements**: 80% minimum coverage threshold
- **Parallel Execution**: Optimized for multi-core systems
- **Timeout Management**: Prevents hanging tests
- **Detailed Reporting**: Comprehensive test result analysis
- **Marker System**: Categorized test execution

### Environment Setup

#### Required Environment Variables
```bash
# For MCP testing
export CLI_TEST_TOKEN="test_token_value"
export TEST_API_TOKEN="api_test_value"

# For security testing
export SECURITY_TEST_MODE="enabled"

# For performance testing
export PERFORMANCE_BENCHMARK_MODE="enabled"
```

#### Optional Configuration
```bash
# Verbose test output
export PYTEST_VERBOSE="1"

# Skip slow tests by default
export PYTEST_SKIP_SLOW="1"

# Enable security audit logging
export SECURITY_AUDIT_LOG="enabled"
```

## Test Results and Coverage

### Coverage Targets

| Component | Target Coverage | Critical Functions |
|-----------|-----------------|-------------------|
| MCP Processor | 95% | Configuration loading, validation, processing |
| Environment Injector | 100% | Security validation, variable resolution |
| Agent Composer | 90% | Template processing, trait merging |
| CLI Interface | 85% | Command handling, error scenarios |
| Build System | 80% | Makefile targets, automation workflows |

### Performance Benchmarks

| Operation | Target Performance | Memory Limit |
|-----------|-------------------|--------------|
| Load 100 MCP configs | < 10 seconds | < 100MB |
| Validate 100 configs | < 30 seconds | < 200MB |
| Process all configs | < 60 seconds | < 300MB |
| Agent composition | < 20 seconds | < 300MB |
| Concurrent processing | < 45 seconds | < 500MB |

### Security Gates

| Security Check | Requirement | Implementation |
|----------------|-------------|----------------|
| Command injection prevention | 100% | Whitelist validation, pattern blocking |
| Path traversal protection | 100% | Path normalization, dangerous path blocking |
| Environment variable validation | 100% | Name format enforcement, source validation |
| Secret masking | 100% | Automatic detection and replacement |
| Network access control | 100% | Trust level enforcement |

## Continuous Integration

### GitHub Actions Integration

```yaml
# .github/workflows/test.yml
name: Comprehensive Testing

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Run smoke tests
      run: pytest tests/ -m smoke --cov=src/claude_config
    
    - name: Run security tests
      run: pytest tests/test_security_validation.py -v
    
    - name: Run integration tests
      run: pytest tests/test_mcp_integration.py -v
    
    - name: Generate coverage report
      run: pytest tests/ --cov=src/claude_config --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
- repo: local
  hooks:
  - id: pytest-smoke
    name: Run smoke tests
    entry: pytest tests/ -m smoke --tb=short
    language: system
    pass_filenames: false
    
  - id: security-tests
    name: Run security tests
    entry: pytest tests/test_security_validation.py --tb=short
    language: system
    pass_filenames: false
```

## Debugging and Troubleshooting

### Common Test Failures

#### 1. **Permission Errors**
```bash
# Fix file permissions
chmod 644 tests/fixtures/mcp_servers/*.yaml

# Run with proper user permissions
sudo -u testuser pytest tests/
```

#### 2. **Environment Variable Issues**
```bash
# Set required test variables
export $(cat .env.test | xargs)

# Verify environment setup
pytest tests/test_env_injector.py::test_environment_setup -v
```

#### 3. **Resource Exhaustion**
```bash
# Increase resource limits
ulimit -n 4096  # File descriptors
ulimit -v 2048000  # Virtual memory (KB)

# Run resource-intensive tests separately
pytest tests/test_performance.py::TestScalabilityLimits -v --maxfail=1
```

#### 4. **Network-dependent Test Failures**
```bash
# Skip network tests in offline environments
pytest tests/ -m "not network" -v

# Use mock networking
pytest tests/ --use-mocks -v
```

### Test Data Generation

#### Large Dataset Generation
```python
# Generate test datasets
python tests/generate_test_data.py --mcp-servers 100 --agents 50

# Create performance test scenarios
python tests/generate_performance_scenarios.py --scale large
```

#### Security Test Vectors
```python
# Generate security test cases
python tests/generate_security_tests.py --attack-vectors all

# Create malicious input datasets
python tests/generate_malicious_inputs.py --comprehensive
```

## Contributing to Tests

### Adding New Tests

1. **Follow naming conventions**: `test_*.py` for test files
2. **Use appropriate markers**: `@pytest.mark.integration`, `@pytest.mark.slow`
3. **Include docstrings**: Describe test purpose and expected behavior
4. **Mock external dependencies**: Ensure test isolation
5. **Add performance assertions**: Verify scalability requirements

### Test Quality Guidelines

1. **Test Independence**: Each test should run independently
2. **Clear Assertions**: Use descriptive assertion messages
3. **Error Scenarios**: Test both success and failure paths
4. **Resource Cleanup**: Properly clean up temporary resources
5. **Documentation**: Document complex test scenarios

### Security Test Requirements

1. **No Real Secrets**: Never use real credentials in tests
2. **Safe Commands**: Only use safe command substitutions
3. **Isolated Environment**: Use temporary directories and mock networks
4. **Attack Simulation**: Test realistic attack scenarios safely
5. **Vulnerability Disclosure**: Follow responsible disclosure for findings

## Maintenance and Updates

### Regular Maintenance Tasks

1. **Update test data**: Refresh fixtures and test configurations
2. **Performance baseline**: Update performance benchmarks
3. **Security vectors**: Add new attack patterns and prevention tests
4. **Dependency updates**: Keep test dependencies current
5. **Coverage analysis**: Identify and test uncovered code paths

### Monitoring and Alerting

1. **Coverage regression**: Alert on coverage drops
2. **Performance degradation**: Monitor test execution time
3. **Flaky test detection**: Identify and fix unreliable tests
4. **Security test failures**: Immediate alerts for security violations
5. **Resource usage tracking**: Monitor test infrastructure health

This comprehensive testing suite ensures the Claude Config MCP system meets production quality standards with robust security, performance, and reliability validation.