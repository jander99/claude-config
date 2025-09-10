"""Tests for the ConfigValidator class - basic validation only."""

import pytest
from pathlib import Path
import tempfile
import yaml
from claude_config.validator import ConfigValidator, ValidationResult


@pytest.fixture
def temp_data_dir():
    """Create a minimal test data directory with valid and invalid configs."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create directory structure
        (temp_path / "personas").mkdir()
        (temp_path / "traits" / "safety").mkdir(parents=True)
        
        # Valid agent
        valid_agent = {
            "name": "valid-agent",
            "display_name": "Valid Agent",
            "description": "A valid test agent",
            "expertise": ["Testing"],
            "responsibilities": ["Test things"],
            "traits": ["safety/valid-trait"]
        }
        
        with open(temp_path / "personas" / "valid-agent.yaml", 'w') as f:
            yaml.dump(valid_agent, f)
        
        # Invalid agent (missing required fields)
        invalid_agent = {
            "name": "invalid-agent"
            # Missing description, display_name
        }
        
        with open(temp_path / "personas" / "invalid-agent.yaml", 'w') as f:
            yaml.dump(invalid_agent, f)
        
        # Valid trait
        valid_trait = {
            "name": "valid_trait",
            "category": "safety",
            "description": "A valid trait",
            "implementation": "Test implementation"
        }
        
        with open(temp_path / "traits" / "safety" / "valid-trait.yaml", 'w') as f:
            yaml.dump(valid_trait, f)
        
        yield temp_path


def test_validation_result():
    """Test ValidationResult basic functionality."""
    result = ValidationResult(is_valid=True)
    assert result.is_valid is True
    assert result.errors == []
    
    result_with_errors = ValidationResult(
        is_valid=False,
        errors=["Error 1"]
    )
    assert result_with_errors.is_valid is False
    assert len(result_with_errors.errors) == 1


def test_validator_initialization():
    """Test ConfigValidator initialization."""
    validator = ConfigValidator()
    assert validator.data_dir == Path("data")


def test_validate_yaml_file_valid(temp_data_dir):
    """Test validating a valid YAML file."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_yaml_file(temp_data_dir / "personas" / "valid-agent.yaml")
    
    assert result.is_valid is True
    assert len(result.errors) == 0


def test_validate_yaml_file_missing(temp_data_dir):
    """Test validating a missing file."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_yaml_file(temp_data_dir / "missing.yaml")
    
    assert result.is_valid is False
    assert "not found" in result.errors[0] or "does not exist" in result.errors[0]


def test_validate_agent_valid(temp_data_dir):
    """Test validating a valid agent."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_agent("valid-agent")
    
    assert result.is_valid is True


def test_validate_agent_invalid(temp_data_dir):
    """Test validating an invalid agent."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_agent("invalid-agent")
    
    assert result.is_valid is False
    assert any("Invalid agent structure" in error for error in result.errors)


def test_validate_agent_not_found(temp_data_dir):
    """Test validating non-existent agent."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_agent("nonexistent")
    
    assert result.is_valid is False
    assert "not found" in result.errors[0] or "does not exist" in result.errors[0]


def test_validate_trait_valid(temp_data_dir):
    """Test validating a valid trait."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_trait("safety/valid-trait")
    
    assert result.is_valid is True


def test_validate_all_basic(temp_data_dir):
    """Test basic complete validation."""
    validator = ConfigValidator(temp_data_dir)
    
    # This will return False due to invalid-agent.yaml
    result = validator.validate_all()
    assert result is False