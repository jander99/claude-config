"""Tests for CLI interface - essential commands only."""

import pytest
import tempfile
import yaml
from pathlib import Path
from click.testing import CliRunner

from claude_config.cli import cli


@pytest.fixture
def sample_project():
    """Create a minimal sample project."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create directory structure
        (temp_path / "data" / "personas").mkdir(parents=True)
        (temp_path / "data" / "traits" / "safety").mkdir(parents=True)
        (temp_path / "src" / "claude_config" / "templates").mkdir(parents=True)
        
        # Create sample agent
        agent_data = {
            "name": "sample-agent",
            "display_name": "Sample Agent",
            "description": "A sample agent for CLI testing",
            "expertise": ["Testing"],
            "responsibilities": ["Test CLI commands"],
            "traits": ["safety/test-trait"]
        }
        
        with open(temp_path / "data" / "personas" / "sample-agent.yaml", 'w') as f:
            yaml.dump(agent_data, f)
        
        # Create sample trait
        trait_data = {
            "name": "test_trait",
            "category": "safety",
            "description": "Test trait for CLI",
            "implementation": "CLI testing trait"
        }
        
        with open(temp_path / "data" / "traits" / "safety" / "test-trait.yaml", 'w') as f:
            yaml.dump(trait_data, f)
        
        # Create simple template
        template_content = """---
name: {{ agent.name }}
---

# {{ agent.display_name }}

{{ agent.description }}
"""
        
        with open(temp_path / "src" / "claude_config" / "templates" / "agent.md.j2", 'w') as f:
            f.write(template_content)
        
        yield temp_path


def test_cli_build_command(sample_project):
    """Test the build command."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Copy sample project to isolated filesystem
        import shutil
        shutil.copytree(sample_project, "test_project")
        
        # Run build command from project directory
        import os
        original_dir = os.getcwd()
        os.chdir("test_project")
        try:
            result = runner.invoke(cli, ["build"])
        finally:
            os.chdir(original_dir)
        
        # Should succeed (exit code 0)
        assert result.exit_code == 0
        assert "Building agents" in result.output or "built" in result.output.lower()


def test_cli_validate_command(sample_project):
    """Test the validate command."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        import shutil
        shutil.copytree(sample_project, "test_project")
        
        import os
        original_dir = os.getcwd()
        os.chdir("test_project")
        try:
            result = runner.invoke(cli, ["validate"])
        finally:
            os.chdir(original_dir)
        
        # Should succeed for valid configuration
        assert result.exit_code == 0
        assert "valid" in result.output.lower() or "passed" in result.output.lower()


def test_cli_help_command():
    """Test the help command."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["--help"])
    
    assert result.exit_code == 0
    assert "build" in result.output
    assert "validate" in result.output


def test_cli_invalid_command():
    """Test invalid command handling."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["invalid-command"])
    
    assert result.exit_code != 0