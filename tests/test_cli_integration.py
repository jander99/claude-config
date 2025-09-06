"""
Integration tests for the CLI interface.

Tests the complete workflow from command line invocation to file generation.
"""

import pytest
import tempfile
import yaml
from pathlib import Path
from click.testing import CliRunner

from claude_config.cli import cli


@pytest.fixture
def sample_project():
    """Create a complete sample project for integration testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create directory structure
        (temp_path / "data" / "personas").mkdir(parents=True)
        (temp_path / "data" / "traits" / "safety").mkdir(parents=True)
        (temp_path / "data" / "content" / "personas").mkdir(parents=True)
        (temp_path / "src" / "claude_config" / "templates").mkdir(parents=True)
        
        # Create sample persona
        persona_data = {
            "name": "sample_developer",
            "display_name": "Sample Developer",
            "model": "sonnet",
            "description": "A sample developer for integration testing",
            "expertise": ["Python", "Testing"],
            "responsibilities": ["Write code", "Ensure quality"],
            "proactive_triggers": {
                "file_patterns": ["*.py"],
                "project_indicators": ["pytest.ini"]
            },
            "content_sections": {
                "approach": "personas/approach.md"
            }
        }
        
        with open(temp_path / "data" / "personas" / "sample-developer.yaml", 'w') as f:
            yaml.dump(persona_data, f)
        
        # Create sample trait
        trait_data = {
            "name": "branch_safety",
            "category": "safety",
            "version": "1.0.0",
            "description": "Ensures safe branching practices",
            "implementation": "Always verify git branch status before making changes",
            "coordination_patterns": [
                {
                    "name": "pre_development_check",
                    "trigger": "before_development_work",
                    "action": "verify_branch_status",
                    "context_required": ["git_status", "branch_name"]
                }
            ]
        }
        
        with open(temp_path / "data" / "traits" / "safety" / "branch-check.yaml", 'w') as f:
            yaml.dump(trait_data, f)
        
        # Create sample composition
        composition_data = {
            "name": "test-developer",
            "model": "sonnet",
            "persona": "sample-developer",
            "traits": ["safety/branch-check"],
            "custom_instructions": "Focus on test-driven development and code quality"
        }
        
        with open(temp_path / "data" / "personas" / "test-developer.yaml", 'w') as f:
            yaml.dump(composition_data, f)
        
        # Create content file
        content = """# Technical Approach

This agent follows a systematic approach to software development:

1. **Analysis Phase**: Understanding requirements and constraints
2. **Design Phase**: Planning architecture and implementation
3. **Implementation Phase**: Writing clean, maintainable code
4. **Testing Phase**: Comprehensive testing and validation
5. **Documentation Phase**: Clear documentation and examples
"""
        
        with open(temp_path / "data" / "content" / "personas" / "approach.md", 'w') as f:
            f.write(content)
        
        # Create template
        template_content = """---
name: {{ composition.name }}
description: {{ persona.display_name }}{% if traits %} with specialized traits{% endif %}
model: {{ composition.model }}
---

# {{ persona.display_name }}

{{ persona.description }}

## Core Responsibilities
{% for responsibility in persona.responsibilities %}
- {{ responsibility }}
{% endfor %}

## Expertise Areas
{% for area in persona.expertise %}
- {{ area }}
{% endfor %}

{% if persona.proactive_triggers %}
## Proactive Activation
{% if persona.proactive_triggers.file_patterns %}
File patterns: {{ persona.proactive_triggers.file_patterns | join(', ') }}
{% endif %}
{% endif %}

{% for section_name, content in content_sections.items() %}
## {{ section_name|title }}

{{ content }}
{% endfor %}

{% for trait in traits %}
---
## {{ trait.name|title }} ({{ trait.category }})

{{ trait.description }}

### Implementation
{{ trait.implementation }}
{% endfor %}

{% if composition.custom_instructions %}
---
## Custom Instructions

{{ composition.custom_instructions }}
{% endif %}
"""
        
        with open(temp_path / "src" / "claude_config" / "templates" / "agent.md.j2", 'w') as f:
            f.write(template_content)
        
        yield temp_path


def test_cli_build_command(sample_project):
    """Test the build command end-to-end."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Change to sample project directory
        import os
        os.chdir(sample_project)
        
        # Run build command
        result = runner.invoke(cli, ['build', '--data-dir', 'data', '--output-dir', 'test-output'])
        
        # Check command succeeded
        assert result.exit_code == 0
        
        # Check output files were created
        output_dir = sample_project / "test-output" / "agents"
        assert output_dir.exists()
        
        agent_file = output_dir / "test-developer.md"
        assert agent_file.exists()
        
        # Check content
        with open(agent_file, 'r') as f:
            content = f.read()
        
        assert "test-developer" in content
        assert "Sample Developer" in content
        assert "branch_safety" in content
        assert "Technical Approach" in content


def test_cli_validate_command(sample_project):
    """Test the validate command."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        import os
        os.chdir(sample_project)
        
        result = runner.invoke(cli, ['validate', '--data-dir', 'data'])
        
        assert result.exit_code == 0
        assert "✅" in result.output or "valid" in result.output.lower()


def test_cli_list_agents_command(sample_project):
    """Test the list-agents command."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        import os
        os.chdir(sample_project)
        
        result = runner.invoke(cli, ['list-agents', '--data-dir', 'data'])
        
        assert result.exit_code == 0
        assert "sample-developer" in result.output or "test-developer" in result.output


def test_cli_list_traits_command(sample_project):
    """Test the list-traits command."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        import os
        os.chdir(sample_project)
        
        result = runner.invoke(cli, ['list-traits', '--data-dir', 'data'])
        
        assert result.exit_code == 0
        assert "branch-check" in result.output or "safety" in result.output


def test_cli_build_with_validation(sample_project):
    """Test build with validation enabled."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        import os
        os.chdir(sample_project)
        
        result = runner.invoke(cli, ['build', '--validate', '--data-dir', 'data'])
        
        assert result.exit_code == 0
        assert "Validation passed" in result.output or "✅" in result.output


def test_cli_build_specific_agent(sample_project):
    """Test building a specific agent."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        import os
        os.chdir(sample_project)
        
        result = runner.invoke(cli, ['build', '--agent', 'test-developer', '--data-dir', 'data'])
        
        assert result.exit_code == 0
        
        # Check only the specified agent was built
        output_dir = sample_project / "dist" / "agents"
        agent_files = list(output_dir.glob("*.md"))
        assert len(agent_files) == 1
        assert agent_files[0].name == "test-developer.md"


def test_cli_install_dry_run(sample_project):
    """Test the install command with dry run."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        import os
        os.chdir(sample_project)
        
        # First build
        runner.invoke(cli, ['build', '--data-dir', 'data'])
        
        # Then test install dry run
        result = runner.invoke(cli, ['install', '--dry-run'])
        
        assert result.exit_code == 0
        assert "dry run" in result.output.lower() or "would install" in result.output.lower()


def test_cli_error_handling_missing_data(sample_project):
    """Test CLI error handling with missing data directory."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ['build', '--data-dir', 'nonexistent'])
    
    # Should fail gracefully
    assert result.exit_code != 0


def test_cli_error_handling_invalid_persona(sample_project):
    """Test CLI error handling with invalid persona reference."""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        import os
        os.chdir(sample_project)
        
        result = runner.invoke(cli, ['build', '--agent', 'nonexistent-agent', '--data-dir', 'data'])
        
        # Should handle error gracefully
        assert result.exit_code != 0
        assert "not found" in result.output or "error" in result.output.lower()