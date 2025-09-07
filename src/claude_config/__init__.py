"""
Claude Config Generator.

This package provides a system for generating Claude agent configurations.
"""

from .composer import AgentComposer
from .validator import ConfigValidator

__version__ = "0.1.0"

__all__ = [
    'AgentComposer',
    'ConfigValidator'
]