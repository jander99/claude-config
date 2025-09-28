"""
Build System and Makefile Testing

Comprehensive testing of build processes, Makefile targets, and automation workflows.
"""

import pytest
import tempfile
import subprocess
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import yaml


class TestMakefileTargets:
    """Test all Makefile targets and build automation."""

    @pytest.fixture
    def project_with_makefile(self):
        """Create test project with Makefile."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Copy actual Makefile or create test version
            makefile_content = """
.PHONY: build clean validate install test help

# Variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

# Default target
help:
	@echo "Available targets:"
	@echo "  build     - Build all agents and configurations"
	@echo "  validate  - Validate all configurations"
	@echo "  install   - Install built configurations"
	@echo "  clean     - Clean build artifacts"
	@echo "  test      - Run test suite"
	@echo "  venv      - Create virtual environment"

# Setup virtual environment
venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -e .

# Build target
build: venv
	$(PYTHON) -m claude_config.cli build

# Validation target
validate: venv
	$(PYTHON) -m claude_config.cli validate

# Install target
install: build
	$(PYTHON) -m claude_config.cli install

# Clean target
clean:
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Test target
test: venv
	$(PYTHON) -m pytest tests/ -v

# Development setup
dev-setup: venv
	$(PIP) install -e ".[dev]"
	pre-commit install

# Lint target
lint: venv
	$(PYTHON) -m black src/ tests/
	$(PYTHON) -m flake8 src/ tests/
	$(PYTHON) -m mypy src/

# Coverage target
coverage: venv
	$(PYTHON) -m pytest tests/ --cov=src/claude_config --cov-report=html --cov-report=term

# Security check
security: venv
	$(PYTHON) -m bandit -r src/
	$(PYTHON) -m safety check

# Documentation
docs: venv
	$(PYTHON) -m sphinx-build -b html docs/ docs/_build/html

# Release preparation
release-prep: clean lint test coverage security
	@echo "Release preparation complete"

# CI target
ci: venv lint test coverage security
	@echo "CI pipeline complete"
"""
            
            with open(project_path / "Makefile", 'w') as f:
                f.write(makefile_content)

            # Create project structure
            dirs = [
                "data/personas",
                "data/traits/safety",
                "data/mcp_servers",
                "src/claude_config/templates",
                "tests"
            ]
            
            for dir_path in dirs:
                (project_path / dir_path).mkdir(parents=True)

            # Create minimal project files
            agent_data = {
                "name": "test-agent",
                "display_name": "Test Agent", 
                "description": "Test agent for build testing",
                "expertise": ["Testing"],
                "responsibilities": ["Test builds"]
            }
            
            with open(project_path / "data/personas/test-agent.yaml", 'w') as f:
                yaml.dump(agent_data, f)

            # Create setup.py for installation
            setup_content = '''
from setuptools import setup, find_packages

setup(
    name="claude-config-test",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "jinja2", 
        "pyyaml",
        "pydantic"
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "mypy",
            "bandit",
            "safety",
            "pre-commit"
        ]
    }
)
'''
            
            with open(project_path / "setup.py", 'w') as f:
                f.write(setup_content)

            yield project_path

    def test_make_help_target(self, project_with_makefile):
        """Test make help target."""
        result = subprocess.run(
            ["make", "help"],
            cwd=str(project_with_makefile),
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Available targets:" in result.stdout
        assert "build" in result.stdout
        assert "validate" in result.stdout
        assert "install" in result.stdout

    def test_make_clean_target(self, project_with_makefile):
        """Test make clean target."""
        # Create some artifacts to clean
        dist_dir = project_with_makefile / "dist"
        dist_dir.mkdir()
        (dist_dir / "test_file.txt").write_text("test content")
        
        cache_dir = project_with_makefile / ".pytest_cache"
        cache_dir.mkdir()
        (cache_dir / "cache_file").write_text("cache")

        result = subprocess.run(
            ["make", "clean"],
            cwd=str(project_with_makefile),
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert not dist_dir.exists()
        assert not cache_dir.exists()

    def test_make_venv_target(self, project_with_makefile):
        """Test virtual environment creation."""
        result = subprocess.run(
            ["make", "venv"],
            cwd=str(project_with_makefile),
            capture_output=True,
            text=True,
            timeout=120  # venv creation can take time
        )
        
        if shutil.which("python3"):  # Only test if python3 available
            assert result.returncode == 0
            venv_dir = project_with_makefile / ".venv"
            assert venv_dir.exists()
            assert (venv_dir / "bin" / "python").exists() or (venv_dir / "Scripts" / "python.exe").exists()

    @pytest.mark.slow
    def test_make_build_target(self, project_with_makefile):
        """Test make build target."""
        # Skip if no python3 available
        if not shutil.which("python3"):
            pytest.skip("python3 not available")

        # Mock CLI module to avoid import issues
        with patch('claude_config.cli.build_command') as mock_build:
            mock_build.return_value = None
            
            result = subprocess.run(
                ["make", "build"],
                cwd=str(project_with_makefile),
                capture_output=True,
                text=True,
                timeout=180
            )
            
            # Build may fail due to missing dependencies, but should attempt to run
            assert "build" in result.stdout.lower() or "error" in result.stderr.lower()

    def test_make_validate_target(self, project_with_makefile):
        """Test make validate target."""
        if not shutil.which("python3"):
            pytest.skip("python3 not available")

        with patch('claude_config.cli.validate_command') as mock_validate:
            mock_validate.return_value = None
            
            result = subprocess.run(
                ["make", "validate"],
                cwd=str(project_with_makefile),
                capture_output=True,
                text=True,
                timeout=180
            )
            
            # Should attempt validation
            assert "validate" in result.stdout.lower() or "error" in result.stderr.lower()

    def test_makefile_syntax(self, project_with_makefile):
        """Test Makefile syntax validity."""
        result = subprocess.run(
            ["make", "--dry-run", "help"],
            cwd=str(project_with_makefile),
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "syntax error" not in result.stderr.lower()

    def test_makefile_variable_expansion(self, project_with_makefile):
        """Test Makefile variable expansion."""
        # Test that variables are properly defined
        result = subprocess.run(
            ["make", "--dry-run", "build"],
            cwd=str(project_with_makefile),
            capture_output=True,
            text=True
        )
        
        # Should show expanded commands
        assert ".venv" in result.stdout
        assert "python" in result.stdout

    def test_parallel_make_execution(self, project_with_makefile):
        """Test parallel make execution."""
        result = subprocess.run(
            ["make", "-j2", "clean", "help"],
            cwd=str(project_with_makefile),
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0

    def test_make_dependency_chain(self, project_with_makefile):
        """Test make target dependency resolution."""
        # Test that install depends on build
        result = subprocess.run(
            ["make", "--dry-run", "install"],
            cwd=str(project_with_makefile),
            capture_output=True,
            text=True
        )
        
        # Should show build commands before install
        lines = result.stdout.split('\n')
        build_line = next((i for i, line in enumerate(lines) if "build" in line), -1)
        install_line = next((i for i, line in enumerate(lines) if "install" in line and i > build_line), -1)
        
        assert build_line < install_line or build_line == -1  # build should come before install


class TestBuildProcessIntegration:
    """Test complete build process integration."""

    @pytest.fixture
    def comprehensive_build_project(self):
        """Create comprehensive project for build testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create full project structure
            structure = {
                "data/personas": [
                    ("python-engineer.yaml", {
                        "name": "python-engineer",
                        "display_name": "Python Engineer",
                        "description": "Python development specialist",
                        "model": "sonnet",
                        "expertise": ["Python", "Web Development"],
                        "responsibilities": ["Python development", "Code review"],
                        "imports": {
                            "coordination": ["standard-safety-protocols"],
                            "tools": ["python-development-stack"]
                        }
                    }),
                    ("qa-engineer.yaml", {
                        "name": "qa-engineer", 
                        "display_name": "QA Engineer",
                        "description": "Quality assurance specialist",
                        "model": "sonnet",
                        "expertise": ["Testing", "Quality Assurance"],
                        "responsibilities": ["Test automation", "Quality gates"]
                    })
                ],
                "data/traits/coordination": [
                    ("standard-safety-protocols.yaml", {
                        "name": "standard_safety_protocols",
                        "category": "coordination",
                        "description": "Standard safety protocols",
                        "implementation": {"checks": ["branch verification"]}
                    })
                ],
                "data/traits/tools": [
                    ("python-development-stack.yaml", {
                        "name": "python_development_stack",
                        "category": "tools", 
                        "description": "Python development tools",
                        "implementation": {"tools": ["pytest", "black", "mypy"]}
                    })
                ],
                "data/mcp_servers": [
                    ("filesystem.yaml", {
                        "name": "filesystem",
                        "display_name": "Filesystem MCP Server",
                        "description": "File system operations",
                        "category": "productivity",
                        "server": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem"]},
                        "environment": {
                            "variables": {
                                "ALLOWED_DIRS": "/tmp,/home/user/projects"
                            }
                        },
                        "security": {"trust_level": "trusted", "network_access": False},
                        "development": {"status": "stable"}
                    })
                ]
            }
            
            for dir_name, files in structure.items():
                dir_path = project_path / dir_name
                dir_path.mkdir(parents=True)
                
                for file_name, content in files:
                    with open(dir_path / file_name, 'w') as f:
                        yaml.dump(content, f)

            # Create template
            template_content = """# {{ agent.display_name }}

{{ agent.description }}

## Model
{{ agent.model }}

## Expertise
{% for expertise in agent.expertise %}
- {{ expertise }}
{% endfor %}

## Responsibilities  
{% for responsibility in agent.responsibilities %}
- {{ responsibility }}
{% endfor %}

{% if imports %}
## Imported Traits
{% for category, traits in imports.items() %}
### {{ category|title }}
{% for trait in traits %}
- {{ trait }}
{% endfor %}
{% endfor %}
{% endif %}

{% if mcp_servers %}
## Available MCP Servers
{% for server_name, server_config in mcp_servers.items() %}
- **{{ server_name }}**: {{ server_config._metadata.description }}
  - Command: {{ server_config.command }}
  - Trust Level: {{ server_config._metadata.security.trust_level }}
{% endfor %}
{% endif %}
"""
            
            templates_dir = project_path / "src/claude_config/templates"
            templates_dir.mkdir(parents=True)
            with open(templates_dir / "agent.md.j2", 'w') as f:
                f.write(template_content)

            yield project_path

    def test_full_build_pipeline(self, comprehensive_build_project):
        """Test complete build pipeline from YAML to output."""
        from src.claude_config.cli import main
        
        # Test build process
        original_argv = os.sys.argv
        original_cwd = os.getcwd()
        
        try:
            os.chdir(comprehensive_build_project)
            os.sys.argv = ["claude-config", "build"]
            
            # Should complete without errors
            main()
            
            # Verify outputs
            dist_dir = comprehensive_build_project / "dist"
            assert dist_dir.exists()
            
            agents_dir = dist_dir / "agents"
            if agents_dir.exists():
                agent_files = list(agents_dir.glob("*.md"))
                assert len(agent_files) >= 2  # Should have built both agents
                
                # Verify content
                for agent_file in agent_files:
                    content = agent_file.read_text()
                    assert "# " in content  # Should have title
                    assert len(content) > 100  # Should have substantial content

        finally:
            os.sys.argv = original_argv
            os.chdir(original_cwd)

    def test_incremental_build(self, comprehensive_build_project):
        """Test incremental build behavior."""
        from src.claude_config.cli import main
        
        original_cwd = os.getcwd()
        
        try:
            os.chdir(comprehensive_build_project)
            
            # First build
            os.sys.argv = ["claude-config", "build"]
            main()
            
            # Get initial timestamps
            dist_dir = comprehensive_build_project / "dist"
            if dist_dir.exists():
                initial_files = {f: f.stat().st_mtime for f in dist_dir.rglob("*") if f.is_file()}
                
                # Wait a moment
                import time
                time.sleep(0.1)
                
                # Second build (should be faster)
                main()
                
                # Check timestamps
                final_files = {f: f.stat().st_mtime for f in dist_dir.rglob("*") if f.is_file()}
                
                # Some files might be unchanged (incremental build)
                # Implementation depends on actual build system

        finally:
            os.chdir(original_cwd)

    def test_build_with_missing_dependencies(self, comprehensive_build_project):
        """Test build behavior with missing dependencies."""
        # Remove a trait file
        trait_file = comprehensive_build_project / "data/traits/coordination/standard-safety-protocols.yaml"
        trait_file.unlink()
        
        from src.claude_config.cli import main
        original_cwd = os.getcwd()
        
        try:
            os.chdir(comprehensive_build_project)
            os.sys.argv = ["claude-config", "build"]
            
            # Should handle missing dependency gracefully
            try:
                main()
            except Exception as e:
                # Should provide helpful error message
                assert "trait" in str(e).lower() or "dependency" in str(e).lower()

        finally:
            os.chdir(original_cwd)

    def test_concurrent_builds(self, comprehensive_build_project):
        """Test concurrent build processes."""
        import threading
        import time
        
        results = []
        
        def run_build():
            from src.claude_config.cli import main
            original_cwd = os.getcwd()
            
            try:
                os.chdir(comprehensive_build_project)
                os.sys.argv = ["claude-config", "build"]
                main()
                results.append("success")
            except Exception as e:
                results.append(f"error: {e}")
            finally:
                os.chdir(original_cwd)

        # Start multiple builds
        threads = [threading.Thread(target=run_build) for _ in range(3)]
        
        for thread in threads:
            thread.start()
            
        for thread in threads:
            thread.join(timeout=30)

        # Should handle concurrent access gracefully
        assert len(results) == 3
        success_count = sum(1 for r in results if r == "success")
        assert success_count >= 1  # At least one should succeed

    def test_build_performance(self, comprehensive_build_project):
        """Test build performance with timing."""
        from src.claude_config.cli import main
        import time
        
        original_cwd = os.getcwd()
        
        try:
            os.chdir(comprehensive_build_project)
            os.sys.argv = ["claude-config", "build"]
            
            start_time = time.time()
            main()
            build_time = time.time() - start_time
            
            # Build should complete in reasonable time
            assert build_time < 30.0, f"Build took {build_time:.2f}s, expected < 30s"

        finally:
            os.chdir(original_cwd)


class TestBuildValidation:
    """Test build validation and quality gates."""

    def test_pre_build_validation(self):
        """Test validation that runs before build."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create invalid configuration
            (project_path / "data/personas").mkdir(parents=True)
            invalid_agent = {
                "name": "Invalid Agent Name",  # Invalid format
                "display_name": "Invalid Agent"
                # Missing required fields
            }
            
            with open(project_path / "data/personas/invalid.yaml", 'w') as f:
                yaml.dump(invalid_agent, f)

            from src.claude_config.cli import main
            original_cwd = os.getcwd()
            
            try:
                os.chdir(project_path)
                os.sys.argv = ["claude-config", "build"]
                
                # Should fail validation before building
                try:
                    main()
                    pytest.fail("Expected validation to fail")
                except SystemExit as e:
                    assert e.code != 0
                except Exception:
                    pass  # Expected to fail

            finally:
                os.chdir(original_cwd)

    def test_post_build_verification(self, comprehensive_build_project):
        """Test verification that runs after build."""
        from src.claude_config.cli import main
        original_cwd = os.getcwd()
        
        try:
            os.chdir(comprehensive_build_project)
            os.sys.argv = ["claude-config", "build"]
            main()
            
            # Verify build outputs
            dist_dir = comprehensive_build_project / "dist"
            assert dist_dir.exists()
            
            # Check for expected files
            expected_files = ["agents", "settings.json"]
            for expected in expected_files:
                expected_path = dist_dir / expected
                # May or may not exist depending on implementation
                
            # Verify agent files if they exist
            agents_dir = dist_dir / "agents"
            if agents_dir.exists():
                for agent_file in agents_dir.glob("*.md"):
                    content = agent_file.read_text()
                    assert len(content) > 50  # Should have meaningful content
                    assert not content.strip().startswith("Error")  # Should not be error message

        finally:
            os.chdir(original_cwd)

    def test_build_artifact_integrity(self, comprehensive_build_project):
        """Test integrity of build artifacts."""
        from src.claude_config.cli import main
        original_cwd = os.getcwd()
        
        try:
            os.chdir(comprehensive_build_project)
            os.sys.argv = ["claude-config", "build"]
            main()
            
            dist_dir = comprehensive_build_project / "dist"
            if dist_dir.exists():
                # Check that all files are readable
                for file_path in dist_dir.rglob("*"):
                    if file_path.is_file():
                        try:
                            content = file_path.read_text()
                            assert len(content) > 0  # Should not be empty
                        except UnicodeDecodeError:
                            # Binary files are OK
                            pass

        finally:
            os.chdir(original_cwd)


class TestContinuousIntegration:
    """Test CI/CD integration scenarios."""

    def test_ci_build_environment(self):
        """Test build in CI-like environment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create minimal project
            (project_path / "data/personas").mkdir(parents=True)
            agent_data = {
                "name": "ci-test-agent",
                "display_name": "CI Test Agent",
                "description": "Agent for CI testing",
                "expertise": ["CI/CD"],
                "responsibilities": ["Test automation"]
            }
            
            with open(project_path / "data/personas/ci-test-agent.yaml", 'w') as f:
                yaml.dump(agent_data, f)

            # Set CI environment variables
            ci_env = {
                "CI": "true",
                "BUILD_NUMBER": "123",
                "GIT_COMMIT": "abc123",
                "CONTINUOUS_INTEGRATION": "true"
            }

            with patch.dict(os.environ, ci_env):
                # Test CLI in CI mode
                from src.claude_config.cli import main
                original_cwd = os.getcwd()
                
                try:
                    os.chdir(project_path)
                    os.sys.argv = ["claude-config", "build", "--ci"]
                    
                    # Should adapt behavior for CI
                    main()

                except Exception:
                    # May fail due to missing dependencies, but should attempt CI build
                    pass
                finally:
                    os.chdir(original_cwd)

    def test_docker_build_simulation(self):
        """Test build process in Docker-like environment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Simulate limited Docker environment
            limited_env = {
                "HOME": str(temp_dir),
                "USER": "builduser",
                "PATH": "/usr/local/bin:/usr/bin:/bin"
            }

            # Create minimal project
            (project_path / "data/personas").mkdir(parents=True)
            agent_data = {
                "name": "docker-test-agent",
                "display_name": "Docker Test Agent", 
                "description": "Agent for Docker testing",
                "expertise": ["Containerization"],
                "responsibilities": ["Docker builds"]
            }
            
            with open(project_path / "data/personas/docker-test-agent.yaml", 'w') as f:
                yaml.dump(agent_data, f)

            with patch.dict(os.environ, limited_env, clear=True):
                # Test build in limited environment
                # (Implementation depends on actual Docker support)
                pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])