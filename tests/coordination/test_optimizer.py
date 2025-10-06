"""
Unit tests for GraphOptimizer.

Tests graph optimization including transitive closure, path caching,
and performance optimization.
"""

import pytest
from src.claude_config.coordination.optimizer import (
    GraphOptimizer,
    OptimizationResult
)


class TestGraphOptimizer:
    """Test suite for GraphOptimizer."""

    def test_compute_transitive_closure_simple(self):
        """Test transitive closure on a simple chain."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': []
        }

        closure = optimizer.compute_transitive_closure(graph)

        # python-engineer can reach qa-engineer and technical-writer
        assert 'qa-engineer' in closure['python-engineer']
        assert 'technical-writer' in closure['python-engineer']

        # qa-engineer can reach technical-writer
        assert 'technical-writer' in closure['qa-engineer']

        # technical-writer reaches no one
        assert len(closure['technical-writer']) == 0

    def test_compute_transitive_closure_with_cycle(self):
        """Test transitive closure with circular dependencies."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': ['python-engineer']
        }

        closure = optimizer.compute_transitive_closure(graph)

        # All agents should reach all other agents (due to cycle)
        for agent in graph.keys():
            other_agents = set(graph.keys()) - {agent}
            assert closure[agent] == other_agents

    def test_compute_transitive_closure_disconnected_graph(self):
        """Test transitive closure with disconnected components."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': [],
            'frontend-engineer': ['ui-ux-designer'],
            'ui-ux-designer': []
        }

        closure = optimizer.compute_transitive_closure(graph)

        # python-engineer reaches qa-engineer but not frontend components
        assert 'qa-engineer' in closure['python-engineer']
        assert 'frontend-engineer' not in closure['python-engineer']
        assert 'ui-ux-designer' not in closure['python-engineer']

    def test_build_agent_index(self):
        """Test building agent index with metadata."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer', 'technical-writer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': []
        }
        metadata = {
            'python-engineer': {
                'model': 'sonnet',
                'imports': {'coordination': ['qa-testing-handoff']},
                'proactive_activation': {'file_patterns': ['*.py']}
            },
            'qa-engineer': {
                'model': 'sonnet',
                'imports': {'coordination': []},
                'proactive_activation': {}
            },
            'technical-writer': {
                'model': 'haiku',
                'imports': {'coordination': []},
                'proactive_activation': {}
            }
        }

        index = optimizer.build_agent_index(graph, metadata)

        # Check python-engineer entry
        assert index['python-engineer']['out_degree'] == 2
        assert index['python-engineer']['in_degree'] == 0
        assert index['python-engineer']['is_entry_point'] is True
        assert index['python-engineer']['model'] == 'sonnet'
        assert '*.py' in index['python-engineer']['file_patterns']

        # Check technical-writer entry
        assert index['technical-writer']['out_degree'] == 0
        assert index['technical-writer']['in_degree'] == 2
        assert index['technical-writer']['is_terminal'] is True
        assert index['technical-writer']['model'] == 'haiku'

    def test_cache_common_paths(self):
        """Test caching of common paths."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': ['git-helper'],
            'git-helper': []
        }

        paths = optimizer.cache_common_paths(graph)

        # Should have paths from python-engineer to all downstream agents
        assert ('python-engineer', 'qa-engineer') in paths
        assert ('python-engineer', 'technical-writer') in paths
        assert ('python-engineer', 'git-helper') in paths

        # Verify path correctness
        assert paths[('python-engineer', 'git-helper')] == [
            'python-engineer', 'qa-engineer', 'technical-writer', 'git-helper'
        ]

    def test_cache_common_paths_respects_max_length(self):
        """Test that path caching respects max_path_length."""
        optimizer = GraphOptimizer()

        # Create a long chain
        graph = {}
        for i in range(10):
            graph[f'agent-{i}'] = [f'agent-{i+1}'] if i < 9 else []

        paths = optimizer.cache_common_paths(graph, max_path_length=3)

        # Should not cache paths longer than 3
        assert ('agent-0', 'agent-5') not in paths
        # But should cache shorter paths
        assert ('agent-0', 'agent-2') in paths

    def test_generate_entry_point_paths(self):
        """Test generation of paths from entry points."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer', 'technical-writer'],
            'qa-engineer': ['git-helper'],
            'technical-writer': ['git-helper'],
            'git-helper': []
        }
        entry_points = ['python-engineer']

        entry_paths = optimizer.generate_entry_point_paths(graph, entry_points)

        assert 'python-engineer' in entry_paths
        paths = entry_paths['python-engineer']

        # Should have multiple paths from python-engineer
        assert len(paths) > 0

        # Verify some expected paths exist
        path_sets = [set(path) for path in paths]
        assert any('qa-engineer' in p for p in path_sets)
        assert any('technical-writer' in p for p in path_sets)

    def test_optimize_comprehensive(self):
        """Test full optimization flow."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': [],
            'frontend-engineer': ['ui-ux-designer'],
            'ui-ux-designer': []
        }
        metadata = {
            'python-engineer': {
                'model': 'sonnet',
                'imports': {'coordination': []},
                'proactive_activation': {'file_patterns': ['*.py']}
            },
            'qa-engineer': {
                'model': 'sonnet',
                'imports': {'coordination': []},
                'proactive_activation': {}
            },
            'technical-writer': {
                'model': 'haiku',
                'imports': {'coordination': []},
                'proactive_activation': {}
            },
            'frontend-engineer': {
                'model': 'sonnet',
                'imports': {'coordination': []},
                'proactive_activation': {'file_patterns': ['*.tsx']}
            },
            'ui-ux-designer': {
                'model': 'sonnet',
                'imports': {'coordination': []},
                'proactive_activation': {}
            }
        }

        result = optimizer.optimize(graph, metadata)

        # Verify optimization result structure
        assert result.transitive_closure is not None
        assert result.agent_index is not None
        assert result.common_paths is not None
        assert result.entry_point_paths is not None
        assert result.optimization_stats is not None

        # Verify statistics
        stats = result.optimization_stats
        assert stats['total_agents'] == 5
        assert stats['entry_points'] == 2
        assert 'optimization_time_ms' in stats
        assert stats['optimization_time_ms'] < 100  # Should be fast

    def test_optimization_result_get_all_descendants(self):
        """Test OptimizationResult.get_all_descendants method."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': []
        }
        metadata = {agent: {'model': 'sonnet', 'imports': {}, 'proactive_activation': {}}
                   for agent in graph.keys()}

        result = optimizer.optimize(graph, metadata)

        descendants = result.get_all_descendants('python-engineer')
        assert 'qa-engineer' in descendants
        assert 'technical-writer' in descendants

    def test_optimization_result_get_path(self):
        """Test OptimizationResult.get_path method."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': ['technical-writer'],
            'technical-writer': []
        }
        metadata = {agent: {'model': 'sonnet', 'imports': {}, 'proactive_activation': {}}
                   for agent in graph.keys()}

        result = optimizer.optimize(graph, metadata)

        path = result.get_path('python-engineer', 'technical-writer')
        assert path is not None
        assert path == ['python-engineer', 'qa-engineer', 'technical-writer']

    def test_optimization_result_get_agent_info(self):
        """Test OptimizationResult.get_agent_info method."""
        optimizer = GraphOptimizer()
        graph = {
            'python-engineer': ['qa-engineer'],
            'qa-engineer': []
        }
        metadata = {
            'python-engineer': {
                'model': 'sonnet',
                'imports': {'coordination': ['qa-testing-handoff']},
                'proactive_activation': {'file_patterns': ['*.py']}
            },
            'qa-engineer': {
                'model': 'sonnet',
                'imports': {},
                'proactive_activation': {}
            }
        }

        result = optimizer.optimize(graph, metadata)

        info = result.get_agent_info('python-engineer')
        assert info is not None
        assert info['model'] == 'sonnet'
        assert info['is_entry_point'] is True
        assert '*.py' in info['file_patterns']

    def test_suggest_optimizations_high_in_degree(self):
        """Test optimization suggestions for high in-degree agents."""
        optimizer = GraphOptimizer()
        graph = {
            f'agent-{i}': ['central-hub'] for i in range(10)
        }
        graph['central-hub'] = []

        metadata = {agent: {'model': 'sonnet', 'imports': {}, 'proactive_activation': {}}
                   for agent in graph.keys()}

        result = optimizer.optimize(graph, metadata)
        suggestions = optimizer.suggest_optimizations(graph, result)

        # Should suggest splitting for high in-degree agent
        assert len(suggestions) > 0
        assert any('high in-degree' in s.lower() for s in suggestions)

    def test_suggest_optimizations_long_chains(self):
        """Test optimization suggestions for long coordination chains."""
        optimizer = GraphOptimizer()

        # Create a long chain
        graph = {}
        for i in range(6):
            graph[f'agent-{i}'] = [f'agent-{i+1}'] if i < 5 else []

        metadata = {agent: {'model': 'sonnet', 'imports': {}, 'proactive_activation': {}}
                   for agent in graph.keys()}

        result = optimizer.optimize(graph, metadata)
        suggestions = optimizer.suggest_optimizations(graph, result)

        # Should suggest addressing long chains
        assert any('long coordination chain' in s.lower() for s in suggestions)

    def test_suggest_optimizations_high_opus_usage(self):
        """Test optimization suggestions for high opus usage."""
        optimizer = GraphOptimizer()
        graph = {
            f'agent-{i}': [] for i in range(10)
        }
        metadata = {
            agent: {'model': 'opus', 'imports': {}, 'proactive_activation': {}}
            for agent in graph.keys()
        }

        result = optimizer.optimize(graph, metadata)
        suggestions = optimizer.suggest_optimizations(graph, result)

        # Should suggest reducing opus usage
        assert any('opus usage' in s.lower() for s in suggestions)

    def test_performance_large_graph(self):
        """Test optimization performance on a large graph."""
        import time

        optimizer = GraphOptimizer()

        # Create a graph with 100 agents
        graph = {}
        metadata = {}
        for i in range(100):
            agent = f'agent-{i}'
            # Connect to next 3 agents
            graph[agent] = [f'agent-{(i + j) % 100}' for j in range(1, 4)]
            metadata[agent] = {
                'model': 'sonnet',
                'imports': {},
                'proactive_activation': {'file_patterns': [f'*.{i}']} if i < 10 else {}
            }

        start_time = time.time()
        result = optimizer.optimize(graph, metadata)
        elapsed_ms = (time.time() - start_time) * 1000

        # Verify optimization completed
        assert result is not None
        assert len(result.agent_index) == 100

        # Should complete in reasonable time (<100ms as per requirement)
        assert elapsed_ms < 100, f"Optimization took {elapsed_ms}ms, expected <100ms"
