"""Tests for the AgentComposer class - core templating functionality only."""

import pytest
from pathlib import Path
import tempfile
import yaml
from claude_config.composer import AgentComposer, TraitConfig, AgentConfig


@pytest.fixture
def temp_data_dir():
    """Create a minimal test data directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create directory structure
        (temp_path / "personas").mkdir()
        (temp_path / "traits" / "safety").mkdir(parents=True)
        
        # Create test agent
        agent_data = {
            "name": "test-agent",
            "display_name": "Test Agent",
            "description": "A test agent",
            "expertise": ["Testing"],
            "responsibilities": ["Test things"],
            "traits": ["safety/test-trait"]
        }
        
        with open(temp_path / "personas" / "test-agent.yaml", 'w') as f:
            yaml.dump(agent_data, f)
        
        # Create test trait
        trait_data = {
            "name": "test_trait",
            "category": "safety",
            "description": "Test trait",
            "implementation": "Test implementation"
        }
        
        with open(temp_path / "traits" / "safety" / "test-trait.yaml", 'w') as f:
            yaml.dump(trait_data, f)
        
        yield temp_path


@pytest.fixture
def temp_template_dir():
    """Create a minimal template directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        template_content = """---
name: {{ agent.name }}
model: {{ agent.model }}
---

# {{ agent.display_name }}

{{ agent.description }}

{% for trait in traits %}
## {{ trait.name }}
{{ trait.implementation }}
{% endfor %}
"""
        
        with open(temp_path / "agent.md.j2", 'w') as f:
            f.write(template_content)
        
        yield temp_path


def test_composer_initialization():
    """Test AgentComposer basic initialization."""
    composer = AgentComposer()
    assert composer.data_dir == Path("data")
    assert composer.template_dir == Path("src/claude_config/templates")


def test_load_agent(temp_data_dir):
    """Test loading agent from YAML file."""
    composer = AgentComposer(data_dir=temp_data_dir)
    agent = composer.load_agent("test-agent")
    
    assert agent.name == "test-agent"
    assert agent.display_name == "Test Agent"
    assert "safety/test-trait" in agent.traits


def test_load_trait(temp_data_dir):
    """Test loading trait from YAML file."""
    composer = AgentComposer(data_dir=temp_data_dir)
    trait = composer.load_trait("safety/test-trait")
    
    assert trait.name == "test_trait"
    assert trait.category == "safety"


def test_compose_agent(temp_data_dir, temp_template_dir):
    """Test composing an agent with template."""
    composer = AgentComposer(
        data_dir=temp_data_dir,
        template_dir=temp_template_dir
    )
    
    agent_config = composer.load_agent("test-agent")
    result = composer.compose_agent(agent_config)
    
    assert "test-agent" in result
    assert "Test Agent" in result
    assert "test_trait" in result


def test_build_agent(temp_data_dir, temp_template_dir):
    """Test building complete agent file."""
    with tempfile.TemporaryDirectory() as output_dir:
        composer = AgentComposer(
            data_dir=temp_data_dir,
            template_dir=temp_template_dir,
            output_dir=Path(output_dir)
        )
        
        output_path = composer.build_agent("test-agent")
        
        assert output_path.exists()
        assert output_path.name == "test-agent.md"


def test_load_agent_not_found():
    """Test loading non-existent agent."""
    composer = AgentComposer()
    
    with pytest.raises(FileNotFoundError, match="Agent not found"):
        composer.load_agent("nonexistent")