"""Tests for the ConfigValidator class - basic validation and MCP validation."""

import pytest
from pathlib import Path
import tempfile
import yaml
from claude_config.validator import ConfigValidator, ValidationResult
from claude_config.mcp_processor import MCPValidationResult


@pytest.fixture
def temp_data_dir():
    """Create a minimal test data directory with valid and invalid configs."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create directory structure
        (temp_path / "personas").mkdir()
        (temp_path / "traits" / "safety").mkdir(parents=True)
        (temp_path / "mcp_servers").mkdir()
        
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

        # Valid MCP server
        valid_mcp_server = {
            "name": "test-server",
            "display_name": "Test MCP Server",
            "description": "A valid test MCP server",
            "category": "development",
            "server": {
                "command": "npx",
                "args": ["-y", "@test/server"],
                "timeout": 30
            },
            "environment": {
                "variables": {
                    "TEST_SERVER_API_KEY": {
                        "source": "env",
                        "variable": "TEST_SERVER_API_KEY",
                        "required": True,
                        "description": "API key for test server"
                    }
                },
                "secrets": ["TEST_SERVER_API_KEY"],
                "validation": {
                    "required": ["TEST_SERVER_API_KEY"],
                    "optional": []
                }
            },
            "metadata": {
                "version": "1.0.0",
                "author": "test-author",
                "tags": ["test", "development"],
                "documentation_url": "https://example.com/docs",
                "repository_url": "https://github.com/test/server"
            },
            "security": {
                "trust_level": "trusted",
                "permissions": ["network.example.com"],
                "data_access": ["api-data"],
                "network_access": True
            },
            "development": {
                "status": "stable",
                "last_tested": "2024-01-15",
                "known_issues": [],
                "dependencies": ["node.js", "npm"]
            }
        }

        with open(temp_path / "mcp_servers" / "test-server.yaml", 'w') as f:
            yaml.dump(valid_mcp_server, f)

        # Invalid MCP server (missing required fields)
        invalid_mcp_server = {
            "name": "invalid-server",
            "display_name": "Invalid Server"
            # Missing description, category, server config, etc.
        }

        with open(temp_path / "mcp_servers" / "invalid-server.yaml", 'w') as f:
            yaml.dump(invalid_mcp_server, f)

        # MCP server with validation warnings
        warning_mcp_server = {
            "name": "warning-server",
            "display_name": "Warning Server",
            "description": "Server that should trigger warnings",
            "category": "development",
            "server": {
                "command": "npm",  # Missing -y flag
                "args": ["run", "start"],
                "timeout": 30
            },
            "environment": {
                "variables": {
                    "api_key": {  # Lowercase var name (should warn)
                        "source": "env",
                        "variable": "api_key",
                        "required": True
                    }
                },
                "secrets": [],
                "validation": {
                    "required": ["api_key"],
                    "optional": []
                }
            },
            "metadata": {
                "version": "1.0.0"
                # Missing author and docs for stable server
            },
            "security": {
                "trust_level": "trusted",
                "permissions": [],  # Empty permissions with network access
                "data_access": [],
                "network_access": True
            },
            "development": {
                "status": "stable",  # Should have docs/author
                "dependencies": []
            }
        }

        with open(temp_path / "mcp_servers" / "warning-server.yaml", 'w') as f:
            yaml.dump(warning_mcp_server, f)

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

    # This will return False due to invalid-agent.yaml and invalid MCP server
    result = validator.validate_all()
    assert result is False


# MCP Validation Tests

def test_validation_result_from_mcp_result():
    """Test converting MCPValidationResult to ValidationResult."""
    mcp_result = MCPValidationResult(
        is_valid=True,
        errors=[],
        warnings=["Test warning"],
        server_name="test-server"
    )

    result = ValidationResult.from_mcp_result(mcp_result)
    assert result.is_valid is True
    assert result.errors == []
    assert result.warnings == ["Test warning"]


def test_validate_mcp_server_valid(temp_data_dir):
    """Test validating a valid MCP server."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_mcp_server("test-server")

    assert result.is_valid is True
    assert len(result.errors) == 0


def test_validate_mcp_server_invalid(temp_data_dir):
    """Test validating an invalid MCP server."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_mcp_server("invalid-server")

    assert result.is_valid is False
    assert len(result.errors) > 0


def test_validate_mcp_server_not_found(temp_data_dir):
    """Test validating non-existent MCP server."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_mcp_server("nonexistent")

    assert result.is_valid is False
    assert any("not found" in error for error in result.errors)


def test_validate_mcp_server_with_warnings(temp_data_dir):
    """Test validating MCP server that should generate warnings."""
    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_mcp_server("warning-server")

    # The server should be valid but have warnings
    assert result.is_valid is True
    assert len(result.warnings) > 0

    # Check for specific warnings we expect
    warning_text = " ".join(result.warnings)
    assert "npm/npx commands should include -y" in warning_text
    assert "should be uppercase" in warning_text
    assert "should provide documentation URL" in warning_text
    assert "should specify author information" in warning_text


def test_validate_all_mcp_servers(temp_data_dir):
    """Test validating all MCP servers."""
    validator = ConfigValidator(temp_data_dir)

    # Should return False due to invalid-server.yaml
    result = validator.validate_all_mcp_servers()
    assert result is False


def test_validate_all_mcp_servers_no_directory(temp_data_dir):
    """Test validating MCP servers when directory doesn't exist."""
    # Remove MCP servers directory
    import shutil
    shutil.rmtree(temp_data_dir / "mcp_servers")

    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_all_mcp_servers()

    # Should return True when no MCP directory exists
    assert result is True


def test_mcp_specific_validation_rules(temp_data_dir):
    """Test MCP-specific validation rules."""
    validator = ConfigValidator(temp_data_dir)

    # Test our custom validation rules
    warnings = validator._validate_mcp_specific_rules("warning-server")

    assert len(warnings) > 0
    warning_text = " ".join(warnings)

    # Check for specific rule validations
    assert "npm/npx commands should include -y" in warning_text
    assert "should be uppercase" in warning_text
    assert "should be prefixed with server name" in warning_text
    assert "should provide documentation URL" in warning_text


def test_validate_all_includes_mcp(temp_data_dir):
    """Test that validate_all includes MCP validation."""
    validator = ConfigValidator(temp_data_dir)

    # Should return False due to both invalid agent and invalid MCP server
    result = validator.validate_all()
    assert result is False


def test_mcp_server_environment_variable_naming(temp_data_dir):
    """Test environment variable naming convention validation."""
    validator = ConfigValidator(temp_data_dir)
    warnings = validator._validate_mcp_specific_rules("warning-server")

    # Should warn about lowercase variable name and missing prefix
    lowercase_warning = any("should be uppercase" in w for w in warnings)
    prefix_warning = any("should be prefixed with server name" in w for w in warnings)

    assert lowercase_warning
    assert prefix_warning


def test_mcp_server_npm_command_validation(temp_data_dir):
    """Test npm/npx command validation."""
    validator = ConfigValidator(temp_data_dir)
    warnings = validator._validate_mcp_specific_rules("warning-server")

    # Should warn about missing -y flag
    npm_warning = any("npm/npx commands should include -y" in w for w in warnings)
    assert npm_warning


def test_mcp_server_metadata_validation(temp_data_dir):
    """Test metadata completeness validation for stable servers."""
    validator = ConfigValidator(temp_data_dir)
    warnings = validator._validate_mcp_specific_rules("warning-server")

    # Should warn about missing documentation and author for stable server
    doc_warning = any("should provide documentation URL" in w for w in warnings)
    author_warning = any("should specify author information" in w for w in warnings)

    assert doc_warning
    assert author_warning