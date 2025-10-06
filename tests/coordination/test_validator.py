"""
Unit tests for CoordinationValidator.

Tests the main orchestrator that coordinates cycle detection,
consistency checking, and trait validation.
"""

import pytest
from pathlib import Path
from src.claude_config.coordination.validator import (
    CoordinationValidator,
    ValidationReport
)


class TestCoordinationValidator:
    """Test suite for CoordinationValidator."""

    def test_build_coordination_graph_from_configs(self):
        """Test building coordination graph from agent configurations."""
        validator = CoordinationValidator()

        configs = {
            'python-engineer': {
                'imports': {
                    'coordination': ['qa-testing-handoff', 'documentation-handoff']
                },
                'custom_coordination': {}
            },
            'qa-engineer': {
                'imports': {'coordination': []},
                'custom_coordination': {}
            },
            'technical-writer': {
                'imports': {'coordination': []},
                'custom_coordination': {}
            }
        }

        graph = validator.build_coordination_graph(configs)

        # python-engineer should coordinate with qa-engineer and technical-writer
        assert 'qa-engineer' in graph['python-engineer']
        assert 'technical-writer' in graph['python-engineer']

    def test_build_coordination_graph_with_custom_patterns(self):
        """Test extracting coordination from custom_coordination field."""
        validator = CoordinationValidator()

        configs = {
            'python-engineer': {
                'imports': {'coordination': []},
                'custom_coordination': {
                    'ml_handoff': 'For ML tasks, coordinates with ai-engineer for implementation'
                }
            },
            'ai-engineer': {
                'imports': {'coordination': []},
                'custom_coordination': {}
            }
        }

        graph = validator.build_coordination_graph(configs)

        # Should extract ai-engineer from custom coordination
        assert 'ai-engineer' in graph['python-engineer']

    def test_extract_agent_metadata(self):
        """Test extraction of agent metadata."""
        validator = CoordinationValidator()

        configs = {
            'python-engineer': {
                'imports': {'coordination': ['qa-testing-handoff']},
                'custom_coordination': {'ml': 'test'},
                'proactive_activation': {'file_patterns': ['*.py']},
                'model': 'sonnet'
            }
        }

        metadata = validator.extract_agent_metadata(configs)

        assert 'python-engineer' in metadata
        assert metadata['python-engineer']['model'] == 'sonnet'
        assert 'qa-testing-handoff' in metadata['python-engineer']['imports']['coordination']

    def test_extract_agent_traits(self):
        """Test extraction of trait imports."""
        validator = CoordinationValidator()

        configs = {
            'python-engineer': {
                'imports': {
                    'coordination': ['qa-testing-handoff', 'documentation-handoff'],
                    'tools': ['python-development-stack']
                }
            }
        }

        traits = validator.extract_agent_traits(configs)

        assert 'python-engineer' in traits
        assert 'qa-testing-handoff' in traits['python-engineer']
        assert 'documentation-handoff' in traits['python-engineer']
        assert 'python-development-stack' in traits['python-engineer']

    def test_find_entry_points(self):
        """Test finding entry point agents."""
        validator = CoordinationValidator()

        configs = {
            'python-engineer': {
                'proactive_activation': {
                    'file_patterns': ['*.py']
                },
                'imports': {'coordination': ['qa-testing-handoff']},
                'custom_coordination': {}
            },
            'qa-engineer': {
                'proactive_activation': {},
                'imports': {'coordination': []},
                'custom_coordination': {}
            },
            'frontend-engineer': {
                'proactive_activation': {
                    'file_patterns': ['*.tsx', '*.jsx']
                },
                'imports': {'coordination': []},
                'custom_coordination': {}
            }
        }

        # Build coordination graph to identify incoming edges
        coordination_graph = validator.build_coordination_graph(configs)

        entry_points = validator.find_entry_points(configs, coordination_graph)

        # python-engineer and frontend-engineer have file patterns
        assert 'python-engineer' in entry_points
        assert 'frontend-engineer' in entry_points

        # qa-engineer has incoming edge from python-engineer (via qa-testing-handoff)
        # so it should NOT be an entry point
        assert 'qa-engineer' not in entry_points

    def test_validate_coordination_valid_graph(self):
        """Test validation of a valid coordination graph."""
        validator = CoordinationValidator()

        configs = {
            'python-engineer': {
                'imports': {'coordination': ['qa-testing-handoff']},
                'custom_coordination': {},
                'proactive_activation': {'file_patterns': ['*.py']}
            },
            'qa-engineer': {
                'imports': {'coordination': ['standard-safety-protocols']},
                'custom_coordination': {},
                'proactive_activation': {}
            }
        }

        report = validator.validate_coordination(configs)

        assert report.is_valid
        assert len(report.cycles) == 0
        # May have some info/warning issues but no errors
        assert not report.has_errors()

    def test_validate_coordination_with_cycle(self):
        """Test validation detects circular dependencies."""
        validator = CoordinationValidator()

        configs = {
            'python-engineer': {
                'imports': {'coordination': []},
                'custom_coordination': {
                    'cycle': 'coordinates with qa-engineer'
                },
                'proactive_activation': {}
            },
            'qa-engineer': {
                'imports': {'coordination': []},
                'custom_coordination': {
                    'reverse': 'coordinates with python-engineer'
                },
                'proactive_activation': {}
            }
        }

        report = validator.validate_coordination(configs)

        assert not report.is_valid
        assert len(report.cycles) > 0
        assert report.has_errors()

    def test_validate_coordination_missing_agent(self):
        """Test validation detects missing agent references in graph."""
        validator = CoordinationValidator()

        configs = {
            'python-engineer': {
                'imports': {'coordination': []},
                'custom_coordination': {},
                'proactive_activation': {}
            }
        }

        # Manually build a graph with a missing agent to test the validator
        # This simulates what would happen if an agent reference was somehow created
        # In real usage, the build_coordination_graph won't create references to non-existent agents
        # But we test the consistency validator's ability to detect them
        graph = {
            'python-engineer': ['nonexistent-agent']
        }
        metadata = {
            'python-engineer': {'imports': {}, 'custom_coordination': {}}
        }
        defined_agents = {'python-engineer'}

        issues = validator.consistency_validator.validate_agent_existence(graph, defined_agents)

        # Should detect missing agent
        assert len(issues) > 0
        assert any(i.issue_type == 'missing_agent' for i in issues)

    def test_validation_report_summary(self):
        """Test ValidationReport summary generation."""
        from src.claude_config.coordination.consistency import ConsistencyIssue
        from src.claude_config.coordination.cycle_detector import CoordinationCycle

        report = ValidationReport(
            is_valid=False,
            cycles=[
                CoordinationCycle(
                    agents=['python-engineer', 'qa-engineer'],
                    cycle_type='direct'
                )
            ],
            consistency_issues=[
                ConsistencyIssue(
                    issue_type='bidirectional',
                    severity='warning',
                    agents_involved=['python-engineer', 'technical-writer'],
                    description='Missing reverse coordination'
                )
            ]
        )

        summary = report.summary()

        assert 'FAILED' in summary
        assert 'Circular Dependencies' in summary
        assert 'Warnings' in summary

    def test_validation_report_has_errors(self):
        """Test ValidationReport error detection."""
        from src.claude_config.coordination.consistency import ConsistencyIssue

        report = ValidationReport(is_valid=False)
        assert not report.has_errors()

        report.errors = ['Test error']
        assert report.has_errors()

        report.errors = []
        report.consistency_issues = [
            ConsistencyIssue(
                issue_type='test',
                severity='error',
                agents_involved=[],
                description='Error'
            )
        ]
        assert report.has_errors()

    def test_validation_report_has_warnings(self):
        """Test ValidationReport warning detection."""
        from src.claude_config.coordination.consistency import ConsistencyIssue

        report = ValidationReport(is_valid=True)
        assert not report.has_warnings()

        report.warnings = ['Test warning']
        assert report.has_warnings()

        report.warnings = []
        report.consistency_issues = [
            ConsistencyIssue(
                issue_type='test',
                severity='warning',
                agents_involved=[],
                description='Warning'
            )
        ]
        assert report.has_warnings()

    def test_load_and_validate_missing_directory(self):
        """Test handling of missing personas directory."""
        validator = CoordinationValidator(data_dir=Path('/nonexistent'))

        report = validator.load_and_validate()

        assert not report.is_valid
        assert len(report.errors) > 0
        assert 'not found' in report.errors[0].lower()

    def test_comprehensive_validation_flow(self):
        """Test complete validation flow with multiple agents."""
        validator = CoordinationValidator()

        configs = {
            'python-engineer': {
                'imports': {'coordination': ['qa-testing-handoff', 'documentation-handoff']},
                'custom_coordination': {},
                'proactive_activation': {'file_patterns': ['*.py']}
            },
            'qa-engineer': {
                'imports': {'coordination': ['standard-safety-protocols']},
                'custom_coordination': {},
                'proactive_activation': {}
            },
            'technical-writer': {
                'imports': {'coordination': ['version-control-coordination']},
                'custom_coordination': {},
                'proactive_activation': {}
            },
            'git-helper': {
                'imports': {'coordination': []},
                'custom_coordination': {},
                'proactive_activation': {'file_patterns': ['.git/**']}
            }
        }

        report = validator.validate_coordination(configs)

        # Should validate successfully
        assert report.is_valid or not report.has_errors()

        # Verify all agents are in the graph
        graph = validator.build_coordination_graph(configs)
        assert len(graph) == 4
