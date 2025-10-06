#!/usr/bin/env python3
"""
Example script demonstrating the coordination validation framework.

This example shows how to use the validation framework to check
agent coordination patterns for cycles, consistency, and optimization opportunities.
"""

from pathlib import Path
from src.claude_config.coordination import (
    CircularDependencyDetector,
    ConsistencyValidator,
    CoordinationValidator,
    GraphOptimizer
)


def example_1_cycle_detection():
    """Example 1: Detect circular dependencies in a simple graph."""
    print("=" * 70)
    print("EXAMPLE 1: Circular Dependency Detection")
    print("=" * 70)

    detector = CircularDependencyDetector()

    # Example with a cycle
    graph_with_cycle = {
        'python-engineer': ['qa-engineer'],
        'qa-engineer': ['technical-writer'],
        'technical-writer': ['python-engineer']  # Creates cycle
    }

    cycles = detector.detect_cycles(graph_with_cycle)
    print(f"\n✓ Detected {len(cycles)} cycle(s):")
    for cycle in cycles:
        print(f"  - {cycle}")
        paths = detector.get_cycle_paths(cycle, graph_with_cycle)
        print(f"    Path: {' -> '.join(paths[0])}")

    # Example without cycles
    graph_no_cycle = {
        'python-engineer': ['qa-engineer'],
        'qa-engineer': ['technical-writer'],
        'technical-writer': ['git-helper'],
        'git-helper': []
    }

    cycles = detector.detect_cycles(graph_no_cycle)
    print(f"\n✓ Linear graph has {len(cycles)} cycle(s)")
    print()


def example_2_consistency_validation():
    """Example 2: Validate coordination consistency."""
    print("=" * 70)
    print("EXAMPLE 2: Consistency Validation")
    print("=" * 70)

    validator = ConsistencyValidator()

    graph = {
        'python-engineer': ['qa-engineer', 'technical-writer'],
        'qa-engineer': [],
        'technical-writer': []
    }

    metadata = {
        'python-engineer': {
            'imports': {'coordination': ['qa-testing-handoff', 'documentation-handoff']}
        },
        'qa-engineer': {
            'imports': {'coordination': ['qa-testing-handoff']}
        },
        'technical-writer': {
            'imports': {'coordination': []}
        }
    }

    # Bidirectional consistency check
    issues = validator.validate_bidirectional_consistency(graph, metadata)
    print(f"\n✓ Bidirectional consistency issues: {len(issues)}")
    for issue in issues:
        print(f"  [{issue.severity.upper()}] {issue.description}")

    # Unreachable agents check
    entry_points = ['python-engineer']
    unreachable = validator.find_unreachable_agents(graph, entry_points)
    print(f"\n✓ Unreachable agents: {len(unreachable)}")
    for issue in unreachable:
        print(f"  - {issue.agents_involved[0]}")
    print()


def example_3_full_validation():
    """Example 3: Complete validation flow."""
    print("=" * 70)
    print("EXAMPLE 3: Full Validation Flow")
    print("=" * 70)

    validator = CoordinationValidator()

    # Example agent configurations
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

    # Run validation
    report = validator.validate_coordination(configs)

    print(f"\n{report.summary()}")
    print()


def example_4_graph_optimization():
    """Example 4: Graph optimization and analysis."""
    print("=" * 70)
    print("EXAMPLE 4: Graph Optimization")
    print("=" * 70)

    optimizer = GraphOptimizer()

    graph = {
        'python-engineer': ['qa-engineer', 'database-engineer'],
        'qa-engineer': ['technical-writer'],
        'database-engineer': ['qa-engineer'],
        'technical-writer': ['git-helper'],
        'git-helper': []
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
        },
        'database-engineer': {
            'model': 'sonnet',
            'imports': {},
            'proactive_activation': {}
        },
        'technical-writer': {
            'model': 'haiku',
            'imports': {},
            'proactive_activation': {}
        },
        'git-helper': {
            'model': 'haiku',
            'imports': {},
            'proactive_activation': {}
        }
    }

    # Optimize graph
    result = optimizer.optimize(graph, metadata)

    print("\n✓ Optimization Statistics:")
    for key, value in result.optimization_stats.items():
        print(f"  {key}: {value}")

    print("\n✓ Transitive Closure (Reachable Agents):")
    for agent, reachable in result.transitive_closure.items():
        if reachable:
            print(f"  {agent} → {', '.join(sorted(reachable))}")

    print("\n✓ Cached Paths:")
    for (source, target), path in list(result.common_paths.items())[:5]:
        print(f"  {source} → {target}: {' → '.join(path)}")

    # Get suggestions
    suggestions = optimizer.suggest_optimizations(graph, result)
    if suggestions:
        print("\n✓ Optimization Suggestions:")
        for suggestion in suggestions:
            print(f"  💡 {suggestion}")
    print()


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("COORDINATION VALIDATION FRAMEWORK EXAMPLES")
    print("=" * 70)
    print()

    example_1_cycle_detection()
    example_2_consistency_validation()
    example_3_full_validation()
    example_4_graph_optimization()

    print("=" * 70)
    print("EXAMPLES COMPLETE")
    print("=" * 70)
    print()
