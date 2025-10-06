"""
Generator package for creating orchestration files.

This package contains the ClaudeMdGenerator class for generating
the master CLAUDE.md file from agent YAML definitions.
"""

from .claude_md_generator import ClaudeMdGenerator

__all__ = ['ClaudeMdGenerator']
