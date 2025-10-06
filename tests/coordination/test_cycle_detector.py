"""
Unit tests for CircularDependencyDetector.

Tests Tarjan's algorithm implementation for detecting cycles
in agent coordination graphs.
"""

import pytest
from src.claude_config.coordination.cycle_detector import (
    CircularDependencyDetector,
    CoordinationCycle
)


class TestCircularDependencyDetector:
    """Test suite for CircularDependencyDetector."""

    def test_no_cycles_in_linear_chain(self):
        """Test that no cycles are detected in a linear dependency chain."""
        detector = CircularDependencyDetector()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': ['git-helper'],
            'git-helper': []
        }

        cycles = detector.detect_cycles(graph)
        assert len(cycles) == 0

    def test_no_cycles_in_empty_graph(self):
        """Test empty graph has no cycles."""
        detector = CircularDependencyDetector()
        graph = {}

        cycles = detector.detect_cycles(graph)
        assert len(cycles) == 0

    def test_detect_simple_cycle(self):
        """Test detection of a simple 2-agent cycle."""
        detector = CircularDependencyDetector()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['python-engineer']
        }

        cycles = detector.detect_cycles(graph)
        assert len(cycles) == 1
        assert cycles[0].cycle_type == 'direct'
        assert set(cycles[0].agents) == {'python-engineer', 'qa-engineer'}

    def test_detect_three_agent_cycle(self):
        """Test detection of a 3-agent cycle."""
        detector = CircularDependencyDetector()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': ['python-engineer']
        }

        cycles = detector.detect_cycles(graph)
        assert len(cycles) == 1
        assert cycles[0].cycle_type == 'transitive'
        assert set(cycles[0].agents) == {'python-engineer', 'qa-engineer', 'technical-writer'}

    def test_detect_self_loop(self):
        """Test detection of agent coordinating with itself."""
        detector = CircularDependencyDetector()
        graph = {
            'python-engineer': ['python-engineer'],
            'qa-engineer': []
        }

        cycles = detector.detect_cycles(graph)
        assert len(cycles) == 1
        assert cycles[0].cycle_type == 'self'
        assert cycles[0].agents == ['python-engineer']

    def test_detect_multiple_cycles(self):
        """Test detection of multiple independent cycles."""
        detector = CircularDependencyDetector()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['python-engineer'],
            'frontend-engineer': ['ui-ux-designer'],
            'ui-ux-designer': ['frontend-engineer'],
            'devops-engineer': []
        }

        cycles = detector.detect_cycles(graph)
        assert len(cycles) == 2

        # Verify both cycles are detected
        cycle_agents = [set(cycle.agents) for cycle in cycles]
        assert {'python-engineer', 'qa-engineer'} in cycle_agents
        assert {'frontend-engineer', 'ui-ux-designer'} in cycle_agents

    def test_complex_graph_with_cycle(self):
        """Test cycle detection in a complex graph with multiple paths."""
        detector = CircularDependencyDetector()
        graph = {
            'python-engineer': ['qa-engineer', 'database-engineer'],
            'qa-engineer': ['technical-writer'],
            'database-engineer': ['python-engineer'],  # Creates cycle
            'technical-writer': ['git-helper'],
            'git-helper': []
        }

        cycles = detector.detect_cycles(graph)
        assert len(cycles) == 1
        assert set(cycles[0].agents) == {'python-engineer', 'database-engineer'}

    def test_has_cycles_method(self):
        """Test the has_cycles convenience method."""
        detector = CircularDependencyDetector()

        # Graph without cycles
        no_cycle_graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': []
        }
        assert not detector.has_cycles(no_cycle_graph)

        # Graph with cycle
        cycle_graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['python-engineer']
        }
        assert detector.has_cycles(cycle_graph)

    def test_get_cycle_paths(self):
        """Test extraction of actual paths through a cycle."""
        detector = CircularDependencyDetector()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': ['python-engineer']
        }

        cycles = detector.detect_cycles(graph)
        assert len(cycles) == 1

        paths = detector.get_cycle_paths(cycles[0], graph)
        assert len(paths) > 0
        # Verify path forms a cycle
        for path in paths:
            assert path[0] == path[-1]

    def test_coordination_cycle_string_representation(self):
        """Test string representation of CoordinationCycle."""
        cycle = CoordinationCycle(
            agents=['python-engineer', 'qa-engineer'],
            cycle_type='direct'
        )

        cycle_str = str(cycle)
        assert 'python-engineer' in cycle_str
        assert 'qa-engineer' in cycle_str
        assert 'Direct cycle' in cycle_str

    def test_coordination_cycle_hashable(self):
        """Test that CoordinationCycle is hashable for set operations."""
        cycle1 = CoordinationCycle(
            agents=['python-engineer', 'qa-engineer'],
            cycle_type='direct'
        )
        cycle2 = CoordinationCycle(
            agents=['qa-engineer', 'python-engineer'],
            cycle_type='direct'
        )

        # Both cycles should hash to same value (same agents)
        cycle_set = {cycle1, cycle2}
        assert len(cycle_set) == 1

    def test_large_graph_performance(self):
        """Test performance on a larger graph (should be <100ms)."""
        import time

        detector = CircularDependencyDetector()

        # Create a graph with 50 agents
        graph = {}
        for i in range(50):
            agent = f'agent-{i}'
            # Connect to next 3 agents (circular)
            targets = [f'agent-{(i + j) % 50}' for j in range(1, 4)]
            graph[agent] = targets

        start_time = time.time()
        cycles = detector.detect_cycles(graph)
        elapsed_ms = (time.time() - start_time) * 1000

        # Should detect cycles (graph is highly connected)
        assert len(cycles) > 0

        # Should complete in reasonable time
        assert elapsed_ms < 100, f"Detection took {elapsed_ms}ms, expected <100ms"
