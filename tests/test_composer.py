"""Tests for the AgentComposer class."""

import pytest
from pathlib import Path
import tempfile
import yaml
from claude_config.composer import AgentComposer, PersonaConfig, TraitConfig, AgentComposition


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create directory structure
        (temp_path / "personas").mkdir()
        (temp_path / "traits" / "safety").mkdir(parents=True)
        (temp_path / "content" / "personas" / "test").mkdir(parents=True)
        
        # Create test persona
        persona_data = {
            "name": "test_developer",
            "display_name": "Test Developer",
            "model": "sonnet",
            "description": "A test developer for unit testing",
            "expertise": ["Testing", "Quality Assurance"],
            "responsibilities": ["Write tests", "Ensure quality"],
            "proactive_triggers": {
                "file_patterns": ["*.test.py", "test_*.py"],
                "project_indicators": ["pytest", "unittest"]
            },
            "content_sections": {
                "core": "personas/test/core.md"
            }
        }
        
        with open(temp_path / "personas" / "test-developer.yaml", 'w') as f:
            yaml.dump(persona_data, f)
        
        # Create test trait
        trait_data = {
            "name": "branch_safety",
            "category": "safety",
            "version": "1.0.0",
            "description": "Branch safety checks",
            "implementation": "Always check git branch before work",
            "coordination_patterns": [
                {
                    "name": "safety_check",
                    "trigger": "before development",
                    "action": "verify branch status",
                    "context_required": ["git_status"]
                }
            ]
        }
        
        with open(temp_path / "traits" / "safety" / "branch-check.yaml", 'w') as f:
            yaml.dump(trait_data, f)
        
        # Create test composition
        composition_data = {
            "name": "test-engineer",
            "model": "sonnet",
            "persona": "test-developer",
            "traits": ["safety/branch-check"],
            "custom_instructions": "Focus on comprehensive testing"
        }
        
        with open(temp_path / "personas" / "test-engineer.yaml", 'w') as f:
            yaml.dump(composition_data, f)
        
        # Create test content
        content = "# Core Responsibilities\n\nThis is test content for the core section."
        with open(temp_path / "content" / "personas" / "test" / "core.md", 'w') as f:
            f.write(content)
        
        yield temp_path


@pytest.fixture
def temp_template_dir():
    """Create a temporary template directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a simple test template
        template_content = """---
name: {{ composition.name }}
description: {{ persona.display_name }}
model: {{ composition.model }}
---

# {{ persona.display_name }}

{{ persona.description }}

{% for trait in traits %}
## {{ trait.name }}
{{ trait.implementation }}
{% endfor %}
"""
        
        with open(temp_path / "agent.md.j2", 'w') as f:
            f.write(template_content)
        
        yield temp_path


def test_persona_config_validation():
    """Test PersonaConfig validation."""
    valid_data = {
        "name": "test",
        "display_name": "Test",
        "description": "A test persona",
        "expertise": ["Testing"],
        "responsibilities": ["Test things"]
    }
    
    persona = PersonaConfig(**valid_data)
    assert persona.name == "test"
    assert persona.model == "sonnet"  # default value


def test_trait_config_validation():
    """Test TraitConfig validation."""
    valid_data = {
        "name": "test_trait",
        "category": "testing",
        "description": "A test trait",
        "implementation": "Do test things"
    }
    
    trait = TraitConfig(**valid_data)
    assert trait.name == "test_trait"
    assert trait.version == "1.0.0"  # default value


def test_agent_composition_validation():
    """Test AgentComposition validation."""
    valid_data = {
        "name": "test-agent",
        "persona": "test-persona",
        "traits": ["trait1", "trait2"]
    }
    
    composition = AgentComposition(**valid_data)
    assert composition.name == "test-agent"
    assert composition.model == "sonnet"  # default value


def test_composer_initialization():
    """Test AgentComposer initialization."""
    composer = AgentComposer()
    assert composer.data_dir == Path("data")
    assert composer.template_dir == Path("src/claude_config/templates")
    assert composer.output_dir == Path("dist")


def test_load_persona(temp_data_dir):
    """Test loading persona from YAML file."""
    composer = AgentComposer(data_dir=temp_data_dir)
    persona = composer.load_persona("test-developer")
    
    assert persona.name == "test_developer"
    assert persona.display_name == "Test Developer"
    assert "Testing" in persona.expertise


def test_load_trait(temp_data_dir):
    """Test loading trait from YAML file."""
    composer = AgentComposer(data_dir=temp_data_dir)
    trait = composer.load_trait("safety/branch-check")
    
    assert trait.name == "branch_safety"
    assert trait.category == "safety"
    assert "Always check git branch" in trait.implementation


def test_load_content(temp_data_dir):
    """Test loading content from markdown file."""
    composer = AgentComposer(data_dir=temp_data_dir)
    content = composer.load_content("personas/test/core.md")
    
    assert "Core Responsibilities" in content


def test_load_missing_content(temp_data_dir):
    """Test loading missing content file."""
    composer = AgentComposer(data_dir=temp_data_dir)
    content = composer.load_content("missing/file.md")
    
    assert "Content not found" in content


def test_compose_agent(temp_data_dir, temp_template_dir):
    """Test composing an agent from components."""
    with tempfile.TemporaryDirectory() as output_dir:
        composer = AgentComposer(
            data_dir=temp_data_dir,
            template_dir=temp_template_dir,
            output_dir=Path(output_dir)
        )
        
        composition_data = {
            "name": "test-agent",
            "model": "sonnet",
            "persona": "test-developer",
            "traits": ["safety/branch-check"],
            "custom_instructions": "Test instructions"
        }
        
        composition = AgentComposition(**composition_data)
        result = composer.compose_agent(composition)
        
        assert "test-agent" in result
        assert "Test Developer" in result
        assert "branch_safety" in result


def test_build_agent(temp_data_dir, temp_template_dir):
    """Test building a complete agent file."""
    with tempfile.TemporaryDirectory() as output_dir:
        composer = AgentComposer(
            data_dir=temp_data_dir,
            template_dir=temp_template_dir,
            output_dir=Path(output_dir)
        )
        
        output_path = composer.build_agent("test-engineer")
        
        assert output_path.exists()
        assert output_path.name == "test-engineer.md"
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        assert "test-engineer" in content
        assert "Test Developer" in content