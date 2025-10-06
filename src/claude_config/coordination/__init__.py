"""
Coordination validation and optimization framework for Claude Config Generator.

This package provides comprehensive validation for agent coordination patterns,
including circular dependency detection, consistency checking, and graph optimization.
"""

from .cycle_detector import CircularDependencyDetector, CoordinationCycle
from .consistency import ConsistencyValidator, ConsistencyIssue
from .validator import CoordinationValidator, ValidationReport
from .optimizer import GraphOptimizer, OptimizationResult

__all__ = [
    "CircularDependencyDetector",
    "CoordinationCycle",
    "ConsistencyValidator",
    "ConsistencyIssue",
    "CoordinationValidator",
    "ValidationReport",
    "GraphOptimizer",
    "OptimizationResult",
]
