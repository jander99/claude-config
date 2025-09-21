"""
External Knowledge Integration Framework

This module provides comprehensive external knowledge integration capabilities
for the claude-config agent ecosystem, including real-time documentation access,
industry best practices, and compliance standards integration.

Key Components:
- MCP server integration (Context7, DeepWiki, GitHub)
- Intelligent caching and reliability framework
- Security and compliance standards integration
- Knowledge source quality assurance and validation
"""

from .mcp_integration import MCPKnowledgeProvider
from .caching import IntelligentKnowledgeCache
from .curation import KnowledgeCurationEngine
from .reliability import KnowledgeSourceReliability
from .security_compliance import SecurityComplianceProvider

__all__ = [
    'MCPKnowledgeProvider',
    'IntelligentKnowledgeCache',
    'KnowledgeCurationEngine',
    'KnowledgeSourceReliability',
    'SecurityComplianceProvider'
]

__version__ = '1.0.0'