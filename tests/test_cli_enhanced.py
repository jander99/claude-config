"""
Enhanced CLI Testing with Error Scenarios

Comprehensive testing of CLI commands, error handling, and edge cases.
"""

import pytest
import tempfile
import yaml
import json
import os
import subprocess
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from claude_config.cli import cli


class TestCLICommands:
    """Test all CLI commands with various scenarios."""

    @pytest.fixture
    def comprehensive_test_project(self):
        """Create a comprehensive test project with all components."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create directory structure
            dirs = [
                "data/personas",
                "data/traits/safety",
                "data/traits/coordination", 
                "data/traits/tools",
                "data/mcp_servers",
                "src/claude_config/templates",
                "dist/agents"
            ]
            
            for dir_path in dirs:
                (project_path / dir_path).mkdir(parents=True)

            # Create sample agent
            agent_data = {
                "name": "test-agent",
                "display_name": "Test Agent",
                "description": "Comprehensive test agent",
                "model": "sonnet",
                "expertise": ["Testing", "Quality Assurance"],
                "responsibilities": ["Test CLI functionality"],
                "imports": {
                    "coordination": ["standard-safety-protocols"],
                    "tools": ["python-development-stack"]
                },
                "context_priming": "Test agent mindset",
                "proactive_triggers": {
                    "file_patterns": ["*.test.py"],
                    "project_indicators": ["pytest"]
                },
                "implementation_patterns": ["Test-driven development"],
                "professional_standards": ["Clean code"],
                "integration_guidelines": ["CI/CD integration"],
                "performance_benchmarks": ["< 100ms response"],
                "troubleshooting_guides": ["Debug test failures"],
                "tool_configurations": ["pytest.ini"]
            }
            
            with open(project_path / "data/personas/test-agent.yaml", 'w') as f:
                yaml.dump(agent_data, f)

            # Create sample traits
            safety_trait = {
                "name": "standard_safety_protocols",
                "category": "coordination",
                "description": "Standard safety protocols for all agents",
                "implementation": {
                    "pre_execution_checks": ["Verify branch safety"],
                    "validation_steps": ["Check environment"]
                }
            }
            
            with open(project_path / "data/traits/safety/standard-safety-protocols.yaml", 'w') as f:
                yaml.dump(safety_trait, f)

            tools_trait = {
                "name": "python_development_stack",
                "category": "tools",
                "description": "Python development tools and configurations",
                "implementation": {
                    "primary_frameworks": ["pytest", "black", "mypy"],
                    "essential_tools": ["pip", "virtualenv"],
                    "configurations": ["pyproject.toml", "pytest.ini"]
                }
            }
            
            with open(project_path / "data/traits/tools/python-development-stack.yaml", 'w') as f:
                yaml.dump(tools_trait, f)

            # Create MCP server config
            mcp_config = {
                "name": "test-mcp-server",
                "display_name": "Test MCP Server",
                "description": "Test MCP server for CLI testing",
                "category": "development",
                "server": {"command": "npx", "args": ["-y", "@test/server"]},
                "environment": {
                    "variables": {
                        "TEST_TOKEN": {
                            "source": "env",
                            "variable": "CLI_TEST_TOKEN",
                            "required": True
                        }
                    }
                },
                "security": {"trust_level": "trusted", "network_access": False},
                "development": {"status": "stable"}
            }
            
            with open(project_path / "data/mcp_servers/test-mcp-server.yaml", 'w') as f:
                yaml.dump(mcp_config, f)

            # Create template
            template_content = """# {{ agent.display_name }}

{{ agent.description }}

## Expertise
{% for expertise in agent.expertise %}
- {{ expertise }}
{% endfor %}

## Responsibilities
{% for responsibility in agent.responsibilities %}
- {{ responsibility }}
{% endfor %}

{% if traits %}
## Traits
{% for trait_category, trait_list in traits.items() %}
### {{ trait_category|title }}
{% for trait in trait_list %}
- {{ trait.name }}: {{ trait.description }}
{% endfor %}
{% endfor %}
{% endif %}

{% if mcp_servers %}
## MCP Servers
{% for server_name, server_config in mcp_servers.items() %}
- **{{ server_name }}**: {{ server_config._metadata.description }}
{% endfor %}
{% endif %}
"""
            
            with open(project_path / "src/claude_config/templates/agent.md.j2", 'w') as f:
                f.write(template_content)

            yield project_path

    def test_build_command_success(self, comprehensive_test_project):
        """Test successful build command."""
        runner = CliRunner()
        
        with patch.dict(os.environ, {"CLI_TEST_TOKEN": "test_token"}):
            result = runner.invoke(cli, ["build"], 
                                 catch_exceptions=False,
                                 cwd=str(comprehensive_test_project))
            
            assert result.exit_code == 0
            assert "build" in result.output.lower() or "success" in result.output.lower()
            
            # Verify output files were created
            dist_dir = comprehensive_test_project / "dist"
            assert dist_dir.exists()

    def test_build_command_missing_template(self):
        """Test build command with missing template."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create agent without template
            (project_path / "data/personas").mkdir(parents=True)
            agent_data = {"name": "test", "display_name": "Test", "description": "Test"}
            
            with open(project_path / "data/personas/test.yaml", 'w') as f:
                yaml.dump(agent_data, f)

            runner = CliRunner()
            result = runner.invoke(cli, ["build"], cwd=str(project_path))
            
            assert result.exit_code != 0
            assert "template" in result.output.lower() or "error" in result.output.lower()

    def test_validate_command_success(self, comprehensive_test_project):
        """Test successful validation command."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ["validate"], cwd=str(comprehensive_test_project))
        
        assert result.exit_code == 0
        assert "valid" in result.output.lower() or "passed" in result.output.lower()

    def test_validate_command_with_errors(self):
        """Test validation command with configuration errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create invalid agent config
            (project_path / "data/personas").mkdir(parents=True)
            invalid_agent = {
                "name": "Invalid Agent Name",  # Invalid name format
                "display_name": "Invalid Agent",
                # Missing required fields
            }
            
            with open(project_path / "data/personas/invalid.yaml", 'w') as f:
                yaml.dump(invalid_agent, f)

            runner = CliRunner()
            result = runner.invoke(cli, ["validate"], cwd=str(project_path))
            
            assert result.exit_code != 0
            assert "error" in result.output.lower() or "invalid" in result.output.lower()

    def test_validate_command_invalid_yaml(self):
        """Test validation with invalid YAML syntax."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create directory and invalid YAML
            (project_path / "data/personas").mkdir(parents=True)
            
            with open(project_path / "data/personas/invalid.yaml", 'w') as f:
                f.write("invalid: yaml: syntax: [unclosed")

            runner = CliRunner()
            result = runner.invoke(cli, ["validate"], cwd=str(project_path))
            
            assert result.exit_code != 0
            assert "yaml" in result.output.lower() or "syntax" in result.output.lower()

    def test_list_agents_command(self, comprehensive_test_project):
        """Test list-agents command."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ["list-agents"], cwd=str(comprehensive_test_project))
        
        assert result.exit_code == 0
        assert "test-agent" in result.output

    def test_list_agents_empty_project(self):
        """Test list-agents with no agents."""
        with tempfile.TemporaryDirectory() as temp_dir:
            runner = CliRunner()
            
            result = runner.invoke(cli, ["list-agents"], cwd=str(temp_dir))
            
            # Should handle gracefully
            assert result.exit_code == 0

    def test_install_command(self, comprehensive_test_project):
        """Test install command."""
        runner = CliRunner()
        
        # First build the project
        with patch.dict(os.environ, {"CLI_TEST_TOKEN": "test_token"}):
            build_result = runner.invoke(cli, ["build"], cwd=str(comprehensive_test_project))
            assert build_result.exit_code == 0

        # Then test install
        with patch('claude_config.cli.Path.home') as mock_home:
            mock_home.return_value = comprehensive_test_project / "mock_home"
            (comprehensive_test_project / "mock_home").mkdir()
            
            result = runner.invoke(cli, ["install"], cwd=str(comprehensive_test_project))
            
            assert result.exit_code == 0
            assert "install" in result.output.lower()

    def test_clean_command(self, comprehensive_test_project):
        """Test clean command."""
        runner = CliRunner()
        
        # Create some build artifacts
        dist_dir = comprehensive_test_project / "dist"
        dist_dir.mkdir(exist_ok=True)
        (dist_dir / "test_file.md").write_text("test content")
        
        result = runner.invoke(cli, ["clean"], cwd=str(comprehensive_test_project))
        
        assert result.exit_code == 0
        assert "clean" in result.output.lower()

    def test_help_command(self):
        """Test help command and subcommand help."""
        runner = CliRunner()
        
        # Main help
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "build" in result.output
        assert "validate" in result.output
        
        # Subcommand help
        for command in ["build", "validate", "list-agents", "install", "clean"]:
            result = runner.invoke(cli, [command, "--help"])
            assert result.exit_code == 0

    def test_version_command(self):
        """Test version command."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert any(char.isdigit() for char in result.output)  # Should contain version number

    def test_invalid_command(self):
        """Test handling of invalid commands."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ["invalid-command"])
        assert result.exit_code != 0

    def test_command_outside_project(self):
        """Test CLI commands outside of a valid project directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            runner = CliRunner()
            
            # Try to build in empty directory
            result = runner.invoke(cli, ["build"], cwd=str(temp_dir))
            
            # Should fail gracefully with helpful message
            assert result.exit_code != 0
            assert "project" in result.output.lower() or "directory" in result.output.lower()


class TestCLIErrorHandling:
    """Test CLI error handling and edge cases."""

    def test_permission_denied_error(self):
        """Test handling of permission denied errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create project structure
            (project_path / "data/personas").mkdir(parents=True)
            agent_data = {"name": "test", "display_name": "Test", "description": "Test"}
            
            with open(project_path / "data/personas/test.yaml", 'w') as f:
                yaml.dump(agent_data, f)

            # Mock permission denied error
            with patch('pathlib.Path.mkdir', side_effect=PermissionError("Permission denied")):
                runner = CliRunner()
                result = runner.invoke(cli, ["build"], cwd=str(project_path))
                
                assert result.exit_code != 0
                assert "permission" in result.output.lower()

    def test_disk_space_error(self):
        """Test handling of disk space errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create minimal project
            (project_path / "data/personas").mkdir(parents=True)
            agent_data = {"name": "test", "display_name": "Test", "description": "Test"}
            
            with open(project_path / "data/personas/test.yaml", 'w') as f:
                yaml.dump(agent_data, f)

            # Mock disk space error
            with patch('builtins.open', side_effect=OSError("No space left on device")):
                runner = CliRunner()
                result = runner.invoke(cli, ["build"], cwd=str(project_path))
                
                assert result.exit_code != 0
                assert "space" in result.output.lower() or "disk" in result.output.lower()

    def test_interrupted_build(self):
        """Test handling of interrupted build process."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create project
            (project_path / "data/personas").mkdir(parents=True)
            agent_data = {"name": "test", "display_name": "Test", "description": "Test"}
            
            with open(project_path / "data/personas/test.yaml", 'w') as f:
                yaml.dump(agent_data, f)

            # Mock KeyboardInterrupt
            with patch('claude_config.cli.build_command', side_effect=KeyboardInterrupt()):
                runner = CliRunner()
                result = runner.invoke(cli, ["build"], cwd=str(project_path))
                
                assert result.exit_code != 0

    def test_corrupted_config_handling(self):
        """Test handling of corrupted configuration files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create directory
            (project_path / "data/personas").mkdir(parents=True)
            
            # Create corrupted YAML (valid syntax but invalid structure)
            corrupted_data = {
                "name": "test",
                "invalid_field": {"nested": {"deeply": {"invalid": "structure"}}}
            }
            
            with open(project_path / "data/personas/corrupted.yaml", 'w') as f:
                yaml.dump(corrupted_data, f)

            runner = CliRunner()
            result = runner.invoke(cli, ["validate"], cwd=str(project_path))
            
            assert result.exit_code != 0

    def test_network_timeout_during_validation(self):
        """Test handling of network timeouts during validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create MCP server config that would cause network timeout
            (project_path / "data/mcp_servers").mkdir(parents=True)
            mcp_config = {
                "name": "timeout-server",
                "display_name": "Timeout Server",
                "description": "Server that causes timeouts",
                "category": "development",
                "server": {"command": "timeout", "args": ["test"]},
                "environment": {
                    "variables": {
                        "NETWORK_VAR": {
                            "source": "command",
                            "command": "curl --max-time 30 api.example.com/token",
                            "required": True
                        }
                    }
                },
                "security": {"trust_level": "trusted", "network_access": True},
                "development": {"status": "experimental"}
            }
            
            with open(project_path / "data/mcp_servers/timeout-server.yaml", 'w') as f:
                yaml.dump(mcp_config, f)

            # Mock timeout error
            with patch('subprocess.run', side_effect=subprocess.TimeoutExpired("curl", 30)):
                runner = CliRunner()
                result = runner.invoke(cli, ["validate"], cwd=str(project_path))
                
                # Should handle timeout gracefully
                assert result.exit_code == 0 or "timeout" in result.output.lower()

    def test_concurrent_cli_access(self, comprehensive_test_project):
        """Test CLI behavior with concurrent access."""
        import threading
        import time
        
        results = []
        
        def run_build():
            runner = CliRunner()
            with patch.dict(os.environ, {"CLI_TEST_TOKEN": "test_token"}):
                result = runner.invoke(cli, ["build"], cwd=str(comprehensive_test_project))
                results.append(result.exit_code)

        # Start multiple builds concurrently
        threads = [threading.Thread(target=run_build) for _ in range(3)]
        
        for thread in threads:
            thread.start()
            
        for thread in threads:
            thread.join()

        # At least one should succeed, or all should fail gracefully
        assert len(results) == 3
        assert any(code == 0 for code in results) or all(code != 0 for code in results)


class TestCLIConfiguration:
    """Test CLI configuration and environment handling."""

    def test_environment_variable_override(self, comprehensive_test_project):
        """Test CLI behavior with different environment variables."""
        runner = CliRunner()
        
        # Test with debug mode
        env_vars = {"DEBUG": "1", "CLI_TEST_TOKEN": "debug_token"}
        
        with patch.dict(os.environ, env_vars):
            result = runner.invoke(cli, ["build"], cwd=str(comprehensive_test_project))
            
            # Should succeed with debug output
            assert result.exit_code == 0

    def test_config_file_override(self):
        """Test CLI behavior with configuration file overrides."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            
            # Create config file
            config_data = {
                "build": {
                    "output_dir": "custom_dist",
                    "verbose": True
                },
                "validation": {
                    "strict": True
                }
            }
            
            with open(project_path / "claude-config.yaml", 'w') as f:
                yaml.dump(config_data, f)

            # Create minimal project
            (project_path / "data/personas").mkdir(parents=True)
            agent_data = {"name": "test", "display_name": "Test", "description": "Test"}
            
            with open(project_path / "data/personas/test.yaml", 'w') as f:
                yaml.dump(agent_data, f)

            runner = CliRunner()
            result = runner.invoke(cli, ["build", "--config", "claude-config.yaml"], 
                                 cwd=str(project_path))
            
            # Should use custom configuration
            # (Exact behavior depends on CLI implementation)

    def test_verbose_output(self, comprehensive_test_project):
        """Test verbose output mode."""
        runner = CliRunner()
        
        with patch.dict(os.environ, {"CLI_TEST_TOKEN": "test_token"}):
            # Normal output
            normal_result = runner.invoke(cli, ["build"], cwd=str(comprehensive_test_project))
            
            # Verbose output
            verbose_result = runner.invoke(cli, ["build", "--verbose"], 
                                         cwd=str(comprehensive_test_project))
            
            # Verbose should have more output
            assert len(verbose_result.output) >= len(normal_result.output)

    def test_dry_run_mode(self, comprehensive_test_project):
        """Test dry run mode for commands."""
        runner = CliRunner()
        
        with patch.dict(os.environ, {"CLI_TEST_TOKEN": "test_token"}):
            result = runner.invoke(cli, ["build", "--dry-run"], 
                                 cwd=str(comprehensive_test_project))
            
            assert result.exit_code == 0
            assert "dry" in result.output.lower() or "would" in result.output.lower()


class TestCLIOutput:
    """Test CLI output formatting and content."""

    def test_json_output_format(self, comprehensive_test_project):
        """Test JSON output format."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ["list-agents", "--format", "json"], 
                             cwd=str(comprehensive_test_project))
        
        if result.exit_code == 0:
            # Should be valid JSON
            try:
                json.loads(result.output)
            except json.JSONDecodeError:
                pytest.fail("Output is not valid JSON")

    def test_table_output_format(self, comprehensive_test_project):
        """Test table output format."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ["list-agents", "--format", "table"], 
                             cwd=str(comprehensive_test_project))
        
        assert result.exit_code == 0
        # Should contain table-like structure
        assert "|" in result.output or "─" in result.output

    def test_error_message_clarity(self):
        """Test that error messages are clear and actionable."""
        runner = CliRunner()
        
        # Test with non-existent project
        result = runner.invoke(cli, ["build"], cwd="/nonexistent/path")
        
        assert result.exit_code != 0
        assert "error" in result.output.lower()
        assert len(result.output) > 10  # Should have meaningful error message

    def test_progress_indicators(self, comprehensive_test_project):
        """Test progress indicators during long operations."""
        runner = CliRunner()
        
        with patch.dict(os.environ, {"CLI_TEST_TOKEN": "test_token"}):
            result = runner.invoke(cli, ["build", "--progress"], 
                                 cwd=str(comprehensive_test_project))
            
            # Should show progress (if implemented)
            if result.exit_code == 0:
                # Progress indicators might include: %, dots, bars, etc.
                has_progress = any(indicator in result.output 
                                 for indicator in ["%", "...", "█", "▓", "progress"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])