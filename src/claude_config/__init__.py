"""
Claude Code Configuration Generator

A composable system for generating Claude Code agent configurations
through personas, traits, and content composition.
"""

__version__ = "0.1.0"
__author__ = "Claude Config Team"

from .composer import AgentComposer
from .validator import ConfigValidator

__all__ = ["AgentComposer", "ConfigValidator"]