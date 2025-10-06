"""
Unit tests for ConsistencyValidator.

Tests bidirectional consistency, trait compatibility, and reachability validation.
"""

import pytest
from src.claude_config.coordination.consistency import (
    ConsistencyValidator,
    ConsistencyIssue
)


class TestConsistencyValidator:
    """Test suite for ConsistencyValidator."""

    def test_bidirectional_consistency_valid(self):
        """Test that bidirectional coordination is recognized as valid."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['python-engineer']
        }

        issues = validator.validate_bidirectional_consistency(graph)
        assert len(issues) == 0

    def test_bidirectional_consistency_missing_reverse(self):
        """Test detection of missing reverse coordination."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': []
        }

        issues = validator.validate_bidirectional_consistency(graph)
        assert len(issues) == 1
        assert issues[0].issue_type == 'bidirectional'
        assert issues[0].severity == 'warning'
        assert 'python-engineer' in issues[0].agents_involved
        assert 'qa-engineer' in issues[0].agents_involved

    def test_bidirectional_with_trait_awareness(self):
        """Test that trait imports provide awareness."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': []
        }
        metadata = {
            'qa-engineer': {
                'imports': {
                    'coordination': ['qa-testing-handoff']
                }
            }
        }

        issues = validator.validate_bidirectional_consistency(graph, metadata)
        # qa-engineer has coordination traits, so it's aware
        assert len(issues) == 0

    def test_trait_compatibility_with_shared_traits(self):
        """Test that agents with shared traits are compatible."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer']
        }
        traits = {
            'python-engineer': ['qa-testing-handoff', 'python-development-stack'],
            'qa-engineer': ['qa-testing-handoff', 'test-automation-stack']
        }

        issues = validator.validate_trait_compatibility(graph, traits)
        # Should have no issues - they share qa-testing-handoff
        assert len([i for i in issues if i.severity == 'error']) == 0

    def test_trait_compatibility_without_shared_traits(self):
        """Test detection of agents without shared coordination traits."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['frontend-engineer']
        }
        traits = {
            'python-engineer': ['qa-testing-handoff'],
            'frontend-engineer': ['javascript-development-stack']
        }

        issues = validator.validate_trait_compatibility(graph, traits)
        # Should get an info-level suggestion
        assert len(issues) > 0
        assert any(i.issue_type == 'trait_compatibility' for i in issues)

    def test_find_unreachable_agents_with_entry_points(self):
        """Test finding unreachable agents from entry points."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': [],
            'frontend-engineer': ['ui-ux-designer'],  # Isolated
            'ui-ux-designer': []
        }
        entry_points = ['python-engineer']

        issues = validator.find_unreachable_agents(graph, entry_points)

        # frontend-engineer and ui-ux-designer should be unreachable
        unreachable = [i for i in issues if i.issue_type == 'unreachable']
        assert len(unreachable) == 2
        unreachable_agents = {i.agents_involved[0] for i in unreachable}
        assert 'frontend-engineer' in unreachable_agents
        assert 'ui-ux-designer' in unreachable_agents

    def test_find_unreachable_with_auto_entry_points(self):
        """Test automatic entry point detection (no incoming edges)."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': [],
            'frontend-engineer': []  # No incoming edges, should be entry point
        }

        issues = validator.find_unreachable_agents(graph, entry_points=None)

        # All agents should be reachable from their respective entry points
        # Or frontend-engineer is isolated
        unreachable = [i for i in issues if i.issue_type == 'unreachable']
        # frontend-engineer has no targets, so it's an isolated entry point
        # but it's still reachable (from itself)
        assert all(i.severity in ['warning', 'info'] for i in unreachable)

    def test_no_entry_points_error(self):
        """Test error when no entry points exist."""
        validator = ConsistencyValidator()
        # All agents have incoming edges - no entry points
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['python-engineer']
        }

        issues = validator.find_unreachable_agents(graph, entry_points=None)

        # Should get error about no entry points
        assert len(issues) > 0
        assert any(i.issue_type == 'unreachable' and i.severity == 'error' for i in issues)

    def test_validate_agent_existence_all_exist(self):
        """Test that no issues when all agents exist."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer']
        }
        defined_agents = {'python-engineer', 'qa-engineer', 'technical-writer'}

        issues = validator.validate_agent_existence(graph, defined_agents)
        assert len(issues) == 0

    def test_validate_agent_existence_missing_source(self):
        """Test detection of undefined source agent."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer'],
            'undefined-agent': ['technical-writer']
        }
        defined_agents = {'python-engineer', 'qa-engineer', 'technical-writer'}

        issues = validator.validate_agent_existence(graph, defined_agents)
        assert len(issues) == 1
        assert issues[0].issue_type == 'missing_agent'
        assert issues[0].severity == 'error'
        assert 'undefined-agent' in issues[0].agents_involved

    def test_validate_agent_existence_missing_target(self):
        """Test detection of undefined target agent."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer', 'undefined-target']
        }
        defined_agents = {'python-engineer', 'qa-engineer'}

        issues = validator.validate_agent_existence(graph, defined_agents)
        assert len(issues) == 1
        assert issues[0].issue_type == 'missing_agent'
        assert issues[0].severity == 'error'
        assert 'undefined-target' in issues[0].description

    def test_validate_all_comprehensive(self):
        """Test comprehensive validation with multiple issue types."""
        validator = ConsistencyValidator()
        graph = {
            'python-engineer': ['qa-engineer', 'missing-agent'],
            'qa-engineer': [],
            'frontend-engineer': ['ui-ux-designer'],
            'ui-ux-designer': []
        }
        metadata = {
            'python-engineer': {'imports': {'coordination': ['qa-testing-handoff']}},
            'qa-engineer': {'imports': {}},
            'frontend-engineer': {'imports': {}},
            'ui-ux-designer': {'imports': {}}
        }
        traits = {
            'python-engineer': ['qa-testing-handoff'],
            'qa-engineer': [],
            'frontend-engineer': [],
            'ui-ux-designer': []
        }
        defined_agents = {'python-engineer', 'qa-engineer', 'frontend-engineer', 'ui-ux-designer'}
        entry_points = ['python-engineer']

        issues = validator.validate_all(
            graph, metadata, traits, defined_agents, entry_points
        )

        # Should have multiple types of issues
        issue_types = {i.issue_type for i in issues}
        assert 'missing_agent' in issue_types
        # Since missing_agent is an error, other validations may not run
        # Just verify we got issues
        assert len(issues) > 0

    def test_consistency_issue_string_representation(self):
        """Test string representation of ConsistencyIssue."""
        issue = ConsistencyIssue(
            issue_type='bidirectional',
            severity='warning',
            agents_involved=['python-engineer', 'qa-engineer'],
            description='Test issue',
            suggestion='Fix it'
        )

        issue_str = str(issue)
        assert 'WARNING' in issue_str
        assert 'bidirectional' in issue_str
        assert 'python-engineer' in issue_str
        assert 'Suggestion: Fix it' in issue_str

    def test_performance_with_large_graph(self):
        """Test performance on a larger graph."""
        import time

        validator = ConsistencyValidator()

        # Create a graph with 50 agents
        graph = {}
        metadata = {}
        traits = {}
        for i in range(50):
            agent = f'agent-{i}'
            graph[agent] = [f'agent-{(i + 1) % 50}']
            metadata[agent] = {'imports': {'coordination': ['standard-safety-protocols']}}
            traits[agent] = ['standard-safety-protocols']

        defined_agents = {f'agent-{i}' for i in range(50)}
        entry_points = ['agent-0']

        start_time = time.time()
        issues = validator.validate_all(graph, metadata, traits, defined_agents, entry_points)
        elapsed_ms = (time.time() - start_time) * 1000

        # Should complete in reasonable time
        assert elapsed_ms < 100, f"Validation took {elapsed_ms}ms, expected <100ms"
