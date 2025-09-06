"""Tests for the ConfigValidator class."""

import pytest
from pathlib import Path
import tempfile
import yaml
from claude_config.validator import ConfigValidator, ValidationResult


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create directory structure
        (temp_path / "personas").mkdir()
        (temp_path / "traits" / "safety").mkdir(parents=True)
        (temp_path / "content" / "personas").mkdir(parents=True)
        
        # Create valid persona
        valid_persona = {
            "name": "valid_persona",
            "display_name": "Valid Persona",
            "description": "A valid test persona",
            "expertise": ["Testing"],
            "responsibilities": ["Test things"],
            "content_sections": {
                "core": "personas/core.md"
            }
        }
        
        with open(temp_path / "personas" / "valid.yaml", 'w') as f:
            yaml.dump(valid_persona, f)
        
        # Create invalid persona (missing required fields)
        invalid_persona = {
            "name": "invalid_persona"
            # Missing required fields
        }
        
        with open(temp_path / "personas" / "invalid.yaml", 'w') as f:
            yaml.dump(invalid_persona, f)
        
        # Create valid trait
        valid_trait = {
            "name": "valid_trait",
            "category": "testing",
            "description": "A valid test trait",
            "implementation": "Do test things"
        }
        
        with open(temp_path / "traits" / "safety" / "valid.yaml", 'w') as f:
            yaml.dump(valid_trait, f)
        
        # Create invalid trait (missing required fields)
        invalid_trait = {
            "name": "invalid_trait"
            # Missing required fields
        }
        
        with open(temp_path / "traits" / "safety" / "invalid.yaml", 'w') as f:
            yaml.dump(invalid_trait, f)
        
        # Create valid composition
        valid_composition = {
            "name": "valid-composition",
            "persona": "valid",
            "traits": ["safety/valid"]
        }
        
        with open(temp_path / "personas" / "valid-composition.yaml", 'w') as f:
            yaml.dump(valid_composition, f)
        
        # Create invalid composition (references missing persona)
        invalid_composition = {
            "name": "invalid-composition",
            "persona": "missing-persona",
            "traits": ["safety/valid"]
        }
        
        with open(temp_path / "personas" / "invalid-composition.yaml", 'w') as f:
            yaml.dump(invalid_composition, f)
        
        # Create content file
        with open(temp_path / "content" / "personas" / "core.md", 'w') as f:
            f.write("# Core content")
        
        yield temp_path


def test_validation_result():
    """Test ValidationResult model."""
    result = ValidationResult(is_valid=True)
    assert result.is_valid is True
    assert result.errors == []
    assert result.warnings == []
    
    result_with_errors = ValidationResult(
        is_valid=False,
        errors=["Error 1", "Error 2"],
        warnings=["Warning 1"]
    )
    assert result_with_errors.is_valid is False
    assert len(result_with_errors.errors) == 2
    assert len(result_with_errors.warnings) == 1


def test_validator_initialization():
    """Test ConfigValidator initialization."""
    validator = ConfigValidator()
    assert validator.data_dir == Path("data")
    
    custom_dir = Path("/custom/path")
    validator = ConfigValidator(custom_dir)
    assert validator.data_dir == custom_dir


def test_validate_yaml_file_valid(temp_data_dir):
    """Test validating a valid YAML file."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_yaml_file(temp_data_dir / "personas" / "valid.yaml")
    
    assert result.is_valid is True
    assert len(result.errors) == 0


def test_validate_yaml_file_missing(temp_data_dir):
    """Test validating a missing file."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_yaml_file(temp_data_dir / "missing.yaml")
    
    assert result.is_valid is False
    assert "does not exist" in result.errors[0]


def test_validate_yaml_file_invalid():
    """Test validating an invalid YAML file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create invalid YAML file
        invalid_yaml = temp_path / "invalid.yaml"
        with open(invalid_yaml, 'w') as f:
            f.write("invalid: yaml: content:\n  - missing quotes")
        
        validator = ConfigValidator(temp_path)
        result = validator.validate_yaml_file(invalid_yaml)
        
        assert result.is_valid is False
        assert "Invalid YAML" in result.errors[0]


def test_validate_persona_valid(temp_data_dir):
    """Test validating a valid persona."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_persona("valid")
    
    assert result.is_valid is True


def test_validate_persona_invalid(temp_data_dir):
    """Test validating an invalid persona."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_persona("invalid")
    
    assert result.is_valid is False
    assert any("Invalid persona structure" in error for error in result.errors)


def test_validate_persona_missing_content(temp_data_dir):
    """Test validating persona with missing content file."""
    # Create persona that references missing content
    persona_with_missing_content = {
        "name": "missing_content_persona",
        "display_name": "Missing Content",
        "description": "Persona with missing content",
        "expertise": ["Testing"],
        "responsibilities": ["Test things"],
        "content_sections": {
            "missing": "personas/missing.md"
        }
    }
    
    with open(temp_data_dir / "personas" / "missing-content.yaml", 'w') as f:
        yaml.dump(persona_with_missing_content, f)
    
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_persona("missing-content")
    
    assert result.is_valid is True  # Structure is valid
    assert any("Content file missing" in warning for warning in result.warnings)


def test_validate_trait_valid(temp_data_dir):
    """Test validating a valid trait."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_trait("safety/valid")
    
    assert result.is_valid is True


def test_validate_trait_invalid(temp_data_dir):
    """Test validating an invalid trait."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_trait("safety/invalid")
    
    assert result.is_valid is False
    assert any("Invalid trait structure" in error for error in result.errors)


def test_validate_composition_valid(temp_data_dir):
    """Test validating a valid composition."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_composition("valid-composition")
    
    assert result.is_valid is True


def test_validate_composition_invalid_persona_reference(temp_data_dir):
    """Test validating composition with invalid persona reference."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_composition("invalid-composition")
    
    assert result.is_valid is False
    assert any("Referenced persona not found" in error for error in result.errors)


def test_validate_content_files(temp_data_dir):
    """Test validating content files."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_content_files()
    
    assert result.is_valid is True


def test_validate_content_files_no_content_dir():
    """Test validating content files when content directory doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        validator = ConfigValidator(temp_path)
        result = validator.validate_content_files()
        
        assert result.is_valid is True
        assert any("Content directory does not exist" in warning for warning in result.warnings)


def test_find_circular_dependencies(temp_data_dir):
    """Test circular dependency detection."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.find_circular_dependencies()
    
    # Currently a stub implementation
    assert result.is_valid is True