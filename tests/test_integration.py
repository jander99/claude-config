"""Integration tests for end-to-end workflow."""

import pytest
import tempfile
import yaml
from pathlib import Path
from claude_config.composer import AgentComposer
from claude_config.validator import ConfigValidator


@pytest.fixture
def complete_project():
    """Create a complete minimal project for integration testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create directory structure
        (temp_path / "data" / "personas").mkdir(parents=True)
        (temp_path / "data" / "traits" / "safety").mkdir(parents=True)
        (temp_path / "templates").mkdir()
        
        # Create agent
        agent_data = {
            "name": "integration-agent",
            "display_name": "Integration Agent",
            "description": "Agent for integration testing",
            "expertise": ["Integration", "Testing"],
            "responsibilities": ["End-to-end testing"],
            "traits": ["safety/integration-trait"]
        }
        
        with open(temp_path / "data" / "personas" / "integration-agent.yaml", 'w') as f:
            yaml.dump(agent_data, f)
        
        # Create trait
        trait_data = {
            "name": "integration_trait",
            "category": "safety",
            "description": "Integration testing trait",
            "implementation": "Perform integration tests"
        }
        
        with open(temp_path / "data" / "traits" / "safety" / "integration-trait.yaml", 'w') as f:
            yaml.dump(trait_data, f)
        
        # Create template
        template_content = """---
name: {{ agent.name }}
model: {{ agent.model }}
---

# {{ agent.display_name }}

{{ agent.description }}

## Expertise
{% for area in agent.expertise %}
- {{ area }}
{% endfor %}

{% for trait in traits %}
## {{ trait.name }}
{{ trait.implementation }}
{% endfor %}
"""
        
        with open(temp_path / "templates" / "agent.md.j2", 'w') as f:
            f.write(template_content)
        
        yield temp_path


def test_end_to_end_workflow(complete_project):
    """Test complete workflow: validate -> build -> verify output."""
    data_dir = complete_project / "data"
    template_dir = complete_project / "templates"
    
    with tempfile.TemporaryDirectory() as output_dir:
        # Step 1: Validate configuration
        validator = ConfigValidator(data_dir)
        validation_result = validator.validate_all()
        assert validation_result is True
        
        # Step 2: Build agent
        composer = AgentComposer(
            data_dir=data_dir,
            template_dir=template_dir,
            output_dir=Path(output_dir)
        )
        
        output_path = composer.build_agent("integration-agent")
        
        # Step 3: Verify output
        assert output_path.exists()
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        assert "integration-agent" in content
        assert "Integration Agent" in content
        assert "integration_trait" in content
        assert "Integration" in content  # from expertise
        assert "Perform integration tests" in content  # from trait


def test_build_all_agents_workflow(complete_project):
    """Test building all agents in a project."""
    data_dir = complete_project / "data"
    template_dir = complete_project / "templates"
    
    with tempfile.TemporaryDirectory() as output_dir:
        composer = AgentComposer(
            data_dir=data_dir,
            template_dir=template_dir,
            output_dir=Path(output_dir)
        )
        
        built_agents = composer.build_all_agents()
        
        assert len(built_agents) == 1
        assert built_agents[0].name == "integration-agent.md"
        assert built_agents[0].exists()


def test_validation_prevents_invalid_build():
    """Test that validation catches issues before building."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create invalid configuration
        (temp_path / "personas").mkdir()
        
        invalid_agent = {
            "name": "invalid-agent"
            # Missing required fields
        }
        
        with open(temp_path / "personas" / "invalid-agent.yaml", 'w') as f:
            yaml.dump(invalid_agent, f)
        
        # Validation should fail
        validator = ConfigValidator(temp_path)
        result = validator.validate_all()
        assert result is False