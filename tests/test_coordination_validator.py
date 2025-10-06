"""Tests for coordination schema validation."""

import pytest
from pathlib import Path
import tempfile
import yaml
from claude_config.validator import CoordinationValidator, ValidationResult, ConfigValidator


@pytest.fixture
def temp_data_dir():
    """Create a minimal test data directory with agent definitions."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create directory structure
        (temp_path / "personas").mkdir()

        # Create some test agents for reference validation
        agents = ["python-engineer", "qa-engineer", "technical-writer", "frontend-engineer"]
        for agent in agents:
            agent_data = {
                "name": agent,
                "display_name": agent.replace("-", " ").title(),
                "description": f"Test {agent}",
                "expertise": ["Testing"],
                "responsibilities": ["Test things"]
            }
            with open(temp_path / "personas" / f"{agent}.yaml", 'w') as f:
                yaml.dump(agent_data, f)

        yield temp_path


def test_coordination_validator_initialization(temp_data_dir):
    """Test CoordinationValidator initialization."""
    validator = CoordinationValidator(temp_data_dir)
    assert validator.data_dir == temp_data_dir
    assert validator._agent_names is None


def test_get_all_agent_names(temp_data_dir):
    """Test agent name loading."""
    validator = CoordinationValidator(temp_data_dir)
    agent_names = validator.get_all_agent_names()

    assert "python-engineer" in agent_names
    assert "qa-engineer" in agent_names
    assert "technical-writer" in agent_names
    assert "frontend-engineer" in agent_names
    assert len(agent_names) == 4


def test_validate_coordination_empty():
    """Test validating empty coordination section."""
    validator = CoordinationValidator(Path("/tmp"))
    result = validator.validate_coordination({})

    assert result.is_valid is True
    assert len(result.errors) == 0


def test_validate_coordination_invalid_type():
    """Test validating coordination with wrong type."""
    validator = CoordinationValidator(Path("/tmp"))
    result = validator.validate_coordination("invalid")

    assert result.is_valid is False
    assert "must be a dictionary" in result.errors[0]


def test_validate_triggers_inbound_valid(temp_data_dir):
    """Test validating valid inbound triggers."""
    validator = CoordinationValidator(temp_data_dir)
    coordination = {
        "triggers": {
            "inbound": [
                {"pattern": "*.py files", "confidence": "high"},
                {"pattern": "Python API", "confidence": "medium"}
            ]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True


def test_validate_triggers_inbound_missing_pattern():
    """Test inbound trigger missing pattern field."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "triggers": {
            "inbound": [
                {"confidence": "high"}
            ]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("missing required field 'pattern'" in e for e in result.errors)


def test_validate_triggers_inbound_invalid_confidence():
    """Test inbound trigger with invalid confidence level."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "triggers": {
            "inbound": [
                {"pattern": "*.py", "confidence": "invalid"}
            ]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("must be one of" in e for e in result.errors)


def test_validate_triggers_inbound_missing_confidence_warning():
    """Test inbound trigger missing confidence generates warning."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "triggers": {
            "inbound": [
                {"pattern": "*.py"}
            ]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True
    assert any("missing recommended field 'confidence'" in w for w in result.warnings)


def test_validate_triggers_outbound_valid(temp_data_dir):
    """Test validating valid outbound triggers."""
    validator = CoordinationValidator(temp_data_dir)
    coordination = {
        "triggers": {
            "outbound": [
                {"trigger": "code_complete", "agents": ["qa-engineer"], "mode": "automatic"},
                {"trigger": "api_modified", "agents": ["technical-writer"], "mode": "suggest"}
            ]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True


def test_validate_triggers_outbound_missing_fields():
    """Test outbound trigger missing required fields."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "triggers": {
            "outbound": [
                {"mode": "automatic"}
            ]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("missing required field 'trigger'" in e for e in result.errors)
    assert any("missing required field 'agents'" in e for e in result.errors)


def test_validate_triggers_outbound_invalid_mode():
    """Test outbound trigger with invalid mode."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "triggers": {
            "outbound": [
                {"trigger": "test", "agents": ["qa-engineer"], "mode": "invalid"}
            ]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("must be one of" in e for e in result.errors)


def test_validate_triggers_outbound_unknown_agent(temp_data_dir):
    """Test outbound trigger referencing unknown agent generates warning."""
    validator = CoordinationValidator(temp_data_dir)
    coordination = {
        "triggers": {
            "outbound": [
                {"trigger": "test", "agents": ["unknown-agent"], "mode": "automatic"}
            ]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True
    assert any("unknown agent" in w for w in result.warnings)


def test_validate_relationships_valid(temp_data_dir):
    """Test validating valid relationships."""
    validator = CoordinationValidator(temp_data_dir)
    coordination = {
        "relationships": {
            "parallel": ["frontend-engineer", "qa-engineer"],
            "delegates_to": ["python-engineer"],
            "exclusive_from": ["technical-writer"]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True


def test_validate_relationships_invalid_type():
    """Test relationships with wrong type."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "relationships": "invalid"
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert "must be a dictionary" in result.errors[0]


def test_validate_relationships_invalid_list_type():
    """Test relationship list with wrong type."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "relationships": {
            "parallel": "not-a-list"
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("must be a list" in e for e in result.errors)


def test_validate_relationships_invalid_agent_type():
    """Test relationship with non-string agent name."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "relationships": {
            "parallel": [123, 456]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("must be a string" in e for e in result.errors)


def test_validate_relationships_unknown_agent(temp_data_dir):
    """Test relationship referencing unknown agent generates warning."""
    validator = CoordinationValidator(temp_data_dir)
    coordination = {
        "relationships": {
            "parallel": ["unknown-agent"]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True
    assert any("unknown agent" in w for w in result.warnings)


def test_validate_relationships_conflicting(temp_data_dir):
    """Test conflicting parallel and exclusive_from relationships."""
    validator = CoordinationValidator(temp_data_dir)
    coordination = {
        "relationships": {
            "parallel": ["qa-engineer"],
            "exclusive_from": ["qa-engineer"]
        }
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True
    assert any("both parallel and exclusive_from" in w for w in result.warnings)


def test_validate_task_patterns_valid(temp_data_dir):
    """Test validating valid task patterns."""
    validator = CoordinationValidator(temp_data_dir)
    coordination = {
        "task_patterns": [
            {
                "pattern": "authentication system",
                "decomposition": {
                    "python-engineer": "Implement endpoints",
                    "qa-engineer": "Security testing"
                }
            }
        ]
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True


def test_validate_task_patterns_invalid_type():
    """Test task patterns with wrong type."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "task_patterns": "invalid"
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert "must be a list" in result.errors[0]


def test_validate_task_patterns_missing_pattern():
    """Test task pattern missing pattern field."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "task_patterns": [
            {
                "decomposition": {"qa-engineer": "Test"}
            }
        ]
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("missing required field 'pattern'" in e for e in result.errors)


def test_validate_task_patterns_missing_decomposition():
    """Test task pattern missing decomposition field."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "task_patterns": [
            {
                "pattern": "test pattern"
            }
        ]
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("missing required field 'decomposition'" in e for e in result.errors)


def test_validate_task_patterns_invalid_decomposition_type():
    """Test task pattern with invalid decomposition type."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "task_patterns": [
            {
                "pattern": "test",
                "decomposition": "invalid"
            }
        ]
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("decomposition must be a dictionary" in e for e in result.errors)


def test_validate_task_patterns_unknown_agent(temp_data_dir):
    """Test task pattern with unknown agent generates warning."""
    validator = CoordinationValidator(temp_data_dir)
    coordination = {
        "task_patterns": [
            {
                "pattern": "test",
                "decomposition": {
                    "unknown-agent": "Do something"
                }
            }
        ]
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True
    assert any("unknown agent" in w for w in result.warnings)


def test_validate_task_patterns_invalid_subtask_type():
    """Test task pattern with non-string subtask."""
    validator = CoordinationValidator(Path("/tmp"))
    coordination = {
        "task_patterns": [
            {
                "pattern": "test",
                "decomposition": {
                    "qa-engineer": 123
                }
            }
        ]
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is False
    assert any("must be a string" in e for e in result.errors)


def test_config_validator_with_coordination(temp_data_dir):
    """Test ConfigValidator integrates coordination validation."""
    # Create agent with coordination
    agent_with_coordination = {
        "name": "test-agent",
        "display_name": "Test Agent",
        "description": "Test agent with coordination",
        "expertise": ["Testing"],
        "responsibilities": ["Test coordination"],
        "coordination": {
            "triggers": {
                "inbound": [
                    {"pattern": "test files", "confidence": "high"}
                ],
                "outbound": [
                    {"trigger": "test_complete", "agents": ["qa-engineer"], "mode": "automatic"}
                ]
            },
            "relationships": {
                "parallel": ["python-engineer"]
            }
        }
    }

    with open(temp_data_dir / "personas" / "test-agent.yaml", 'w') as f:
        yaml.dump(agent_with_coordination, f)

    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_agent("test-agent")

    assert result.is_valid is True


def test_config_validator_with_invalid_coordination(temp_data_dir):
    """Test ConfigValidator catches coordination errors."""
    agent_with_bad_coordination = {
        "name": "bad-agent",
        "display_name": "Bad Agent",
        "description": "Agent with invalid coordination",
        "expertise": ["Testing"],
        "responsibilities": ["Test coordination"],
        "coordination": {
            "triggers": {
                "inbound": [
                    {"confidence": "high"}  # Missing pattern
                ]
            }
        }
    }

    with open(temp_data_dir / "personas" / "bad-agent.yaml", 'w') as f:
        yaml.dump(agent_with_bad_coordination, f)

    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_agent("bad-agent")

    assert result.is_valid is False
    assert any("missing required field 'pattern'" in e for e in result.errors)


def test_config_validator_without_coordination(temp_data_dir):
    """Test ConfigValidator works with agents without coordination (backward compatible)."""
    agent_without_coordination = {
        "name": "simple-agent",
        "display_name": "Simple Agent",
        "description": "Agent without coordination",
        "expertise": ["Testing"],
        "responsibilities": ["Simple tasks"]
    }

    with open(temp_data_dir / "personas" / "simple-agent.yaml", 'w') as f:
        yaml.dump(agent_without_coordination, f)

    validator = ConfigValidator(temp_data_dir)
    result = validator.validate_agent("simple-agent")

    assert result.is_valid is True
    assert len(result.errors) == 0


def test_validate_all_shows_coordination_warnings(temp_data_dir, capsys):
    """Test that validate_all displays coordination warnings."""
    agent_with_warnings = {
        "name": "warning-agent",
        "display_name": "Warning Agent",
        "description": "Agent with coordination warnings",
        "expertise": ["Testing"],
        "responsibilities": ["Test warnings"],
        "coordination": {
            "triggers": {
                "inbound": [
                    {"pattern": "test"}  # Missing confidence
                ]
            }
        }
    }

    with open(temp_data_dir / "personas" / "warning-agent.yaml", 'w') as f:
        yaml.dump(agent_with_warnings, f)

    validator = ConfigValidator(temp_data_dir)
    validator.validate_all()

    captured = capsys.readouterr()
    assert "⚠️" in captured.out
    assert "missing recommended field 'confidence'" in captured.out


def test_comprehensive_coordination_validation(temp_data_dir):
    """Test comprehensive coordination schema with all sections."""
    validator = CoordinationValidator(temp_data_dir)
    coordination = {
        "triggers": {
            "inbound": [
                {"pattern": "*.py files", "confidence": "high"},
                {"pattern": "Python API", "confidence": "medium"}
            ],
            "outbound": [
                {"trigger": "code_complete", "agents": ["qa-engineer"], "mode": "automatic"},
                {"trigger": "api_modified", "agents": ["technical-writer"], "mode": "suggest"}
            ]
        },
        "relationships": {
            "parallel": ["frontend-engineer"],
            "delegates_to": ["python-engineer"],
            "exclusive_from": ["technical-writer"]
        },
        "task_patterns": [
            {
                "pattern": "authentication system",
                "decomposition": {
                    "python-engineer": "Implement endpoints",
                    "qa-engineer": "Security testing"
                }
            },
            {
                "pattern": "API documentation",
                "decomposition": {
                    "technical-writer": "Write docs",
                    "qa-engineer": "Validate examples"
                }
            }
        ]
    }

    result = validator.validate_coordination(coordination)
    assert result.is_valid is True
    assert len(result.errors) == 0
