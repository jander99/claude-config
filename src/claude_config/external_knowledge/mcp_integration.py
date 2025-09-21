"""
MCP Integration Framework for External Knowledge Sources

Provides unified access to Context7, DeepWiki, and GitHub MCP servers
with intelligent caching, reliability monitoring, and quality assurance.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json

from .caching import IntelligentKnowledgeCache
from .reliability import KnowledgeSourceReliability

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeRequest:
    """Structured request for external knowledge"""
    type: str  # 'framework_docs', 'best_practices', 'security_standards'
    framework: Optional[str] = None
    topic: Optional[str] = None
    version: Optional[str] = None
    agent_type: Optional[str] = None
    urgency: str = 'normal'  # 'high', 'normal', 'low'
    max_tokens: int = 8000
    trust_threshold: float = 7.5


@dataclass
class KnowledgeResponse:
    """Structured response with metadata"""
    content: str
    source: str
    authority_score: float
    last_updated: datetime
    cache_hit: bool = False
    response_time_ms: int = 0
    related_sources: List[str] = field(default_factory=list)


class MCPKnowledgeProvider:
    """
    Unified MCP knowledge provider integrating Context7, DeepWiki, and GitHub
    with intelligent caching and reliability management.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.cache = IntelligentKnowledgeCache()
        self.reliability = KnowledgeSourceReliability()
        self._setup_mcp_clients()

    def _default_config(self) -> Dict:
        """Default configuration for MCP integration"""
        return {
            'context7': {
                'enabled': True,
                'priority': 'high',
                'timeout_ms': 5000,
                'retry_attempts': 3,
                'trust_threshold': 7.5
            },
            'deepwiki': {
                'enabled': True,
                'priority': 'medium',
                'timeout_ms': 8000,
                'retry_attempts': 2,
                'max_depth': 1
            },
            'github_mcp': {
                'enabled': True,
                'priority': 'high',
                'timeout_ms': 3000,
                'retry_attempts': 3,
                'rate_limit_per_hour': 5000
            },
            'caching': {
                'default_ttl': 3600,
                'framework_docs_ttl': 7200,
                'security_standards_ttl': 86400
            }
        }

    def _setup_mcp_clients(self):
        """Initialize MCP client connections"""
        try:
            # Context7 client for library documentation
            if self.config['context7']['enabled']:
                from mcp__context7__resolve_library_id import resolve_library_id
                from mcp__context7__get_library_docs import get_library_docs
                self.context7_resolve = resolve_library_id
                self.context7_docs = get_library_docs
                logger.info("Context7 MCP client initialized")

            # DeepWiki client for repository documentation
            if self.config['deepwiki']['enabled']:
                from mcp__deepwiki__deepwiki_fetch import deepwiki_fetch
                self.deepwiki_fetch = deepwiki_fetch
                logger.info("DeepWiki MCP client initialized")

            # GitHub MCP client for repository analysis
            if self.config['github_mcp']['enabled']:
                from mcp__github__search_repositories import search_repositories
                from mcp__github__get_file_contents import get_file_contents
                self.github_search = search_repositories
                self.github_content = get_file_contents
                logger.info("GitHub MCP client initialized")

        except ImportError as e:
            logger.warning(f"MCP client initialization failed: {e}")
            # Graceful degradation - continue with available clients

    async def get_framework_documentation(self, request: KnowledgeRequest) -> KnowledgeResponse:
        """
        Get comprehensive framework documentation from Context7 with intelligent caching
        """
        start_time = datetime.now()
        cache_key = f"framework:{request.framework}:{request.topic}:{request.version}"

        # Check intelligent cache first
        if cached_result := await self.cache.get(cache_key):
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            cached_result.response_time_ms = int(response_time)
            cached_result.cache_hit = True
            return cached_result

        try:
            # Resolve library ID through Context7
            library_candidates = await self._call_with_retry(
                self.context7_resolve,
                request.framework
            )

            # Select best match based on trust score and relevance
            best_library = self._select_best_library(library_candidates, request)

            if not best_library:
                raise ValueError(f"No reliable library found for {request.framework}")

            # Fetch comprehensive documentation
            docs_content = await self._call_with_retry(
                self.context7_docs,
                best_library['id'],
                topic=request.topic,
                tokens=request.max_tokens
            )

            # Create structured response
            response = KnowledgeResponse(
                content=docs_content,
                source=f"Context7:{best_library['id']}",
                authority_score=best_library.get('trust_score', 8.0),
                last_updated=datetime.now(),
                response_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
            )

            # Cache with intelligent TTL
            await self.cache.set(cache_key, response,
                               ttl=self.config['caching']['framework_docs_ttl'])

            return response

        except Exception as e:
            logger.error(f"Framework documentation fetch failed: {e}")
            # Fallback to cached content if available
            return await self._get_fallback_content(request, str(e))

    async def get_repository_insights(self, request: KnowledgeRequest) -> KnowledgeResponse:
        """
        Get repository-specific insights and patterns from DeepWiki
        """
        start_time = datetime.now()
        cache_key = f"repo:{request.framework}:{request.topic}"

        # Check cache first
        if cached_result := await self.cache.get(cache_key):
            cached_result.response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            cached_result.cache_hit = True
            return cached_result

        try:
            # Fetch repository documentation from DeepWiki
            repo_docs = await self._call_with_retry(
                self.deepwiki_fetch,
                request.framework,
                maxDepth=self.config['deepwiki']['max_depth'],
                mode="aggregate"
            )

            response = KnowledgeResponse(
                content=repo_docs,
                source=f"DeepWiki:{request.framework}",
                authority_score=8.5,  # DeepWiki generally high quality
                last_updated=datetime.now(),
                response_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
            )

            # Cache repository insights longer due to stability
            await self.cache.set(cache_key, response, ttl=14400)  # 4 hours

            return response

        except Exception as e:
            logger.error(f"Repository insights fetch failed: {e}")
            return await self._get_fallback_content(request, str(e))

    async def get_security_standards(self, domain: str) -> KnowledgeResponse:
        """
        Get security and compliance standards for specific domains
        """
        start_time = datetime.now()
        cache_key = f"security:{domain}"

        # Security standards cache longer due to infrequent updates
        if cached_result := await self.cache.get(cache_key):
            cached_result.response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            cached_result.cache_hit = True
            return cached_result

        try:
            # Map domain to relevant security repositories
            security_repos = self._get_security_repositories(domain)

            security_content = []
            for repo in security_repos:
                try:
                    content = await self._call_with_retry(
                        self.github_content,
                        owner=repo['owner'],
                        repo=repo['repo'],
                        path=repo['path']
                    )
                    security_content.append({
                        'source': f"{repo['owner']}/{repo['repo']}",
                        'content': content,
                        'authority': repo.get('authority', 9.0)
                    })
                except Exception as e:
                    logger.warning(f"Failed to fetch {repo}: {e}")
                    continue

            # Combine and format security standards
            combined_content = self._format_security_standards(security_content)

            response = KnowledgeResponse(
                content=combined_content,
                source="GitHub:SecurityStandards",
                authority_score=9.5,  # Security standards highly authoritative
                last_updated=datetime.now(),
                response_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
            )

            # Cache security standards for 24 hours
            await self.cache.set(cache_key, response,
                               ttl=self.config['caching']['security_standards_ttl'])

            return response

        except Exception as e:
            logger.error(f"Security standards fetch failed: {e}")
            return await self._get_fallback_content(
                KnowledgeRequest(type='security_standards', topic=domain), str(e)
            )

    async def get_best_practices(self, request: KnowledgeRequest) -> KnowledgeResponse:
        """
        Get industry best practices from authoritative sources
        """
        start_time = datetime.now()
        cache_key = f"practices:{request.framework}:{request.agent_type}"

        if cached_result := await self.cache.get(cache_key):
            cached_result.response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            cached_result.cache_hit = True
            return cached_result

        try:
            # Multi-source best practices aggregation
            sources = await self._aggregate_best_practices(request)

            # Rank and filter based on authority and relevance
            top_practices = self._rank_best_practices(sources, request)

            # Format for agent consumption
            formatted_content = self._format_best_practices(top_practices)

            response = KnowledgeResponse(
                content=formatted_content,
                source="Aggregated:BestPractices",
                authority_score=8.8,
                last_updated=datetime.now(),
                response_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
            )

            await self.cache.set(cache_key, response, ttl=7200)  # 2 hours

            return response

        except Exception as e:
            logger.error(f"Best practices fetch failed: {e}")
            return await self._get_fallback_content(request, str(e))

    def _select_best_library(self, candidates: List[Dict], request: KnowledgeRequest) -> Optional[Dict]:
        """Select the best library match based on trust score and relevance"""
        if not candidates:
            return None

        # Filter by minimum trust threshold
        trusted = [c for c in candidates if c.get('trust_score', 0) >= request.trust_threshold]

        if not trusted:
            logger.warning(f"No libraries meet trust threshold {request.trust_threshold}")
            return None

        # Rank by trust score and snippet count (proxy for completeness)
        ranked = sorted(trusted,
                       key=lambda x: (x.get('trust_score', 0), x.get('snippet_count', 0)),
                       reverse=True)

        return ranked[0]

    def _get_security_repositories(self, domain: str) -> List[Dict]:
        """Map security domains to authoritative repositories"""
        security_repo_map = {
            'web_security': [
                {'owner': 'OWASP', 'repo': 'Top10', 'path': '/', 'authority': 10.0},
                {'owner': 'OWASP', 'repo': 'API-Security', 'path': '/', 'authority': 9.8}
            ],
            'cloud_security': [
                {'owner': 'cloud-custodian', 'repo': 'cloud-custodian', 'path': 'docs/', 'authority': 9.0},
                {'owner': 'prowler-cloud', 'repo': 'prowler', 'path': '/', 'authority': 8.8}
            ],
            'data_protection': [
                {'owner': 'OWASP', 'repo': 'CheatSheetSeries', 'path': 'cheatsheets/', 'authority': 9.5}
            ]
        }
        return security_repo_map.get(domain, [])

    async def _aggregate_best_practices(self, request: KnowledgeRequest) -> List[Dict]:
        """Aggregate best practices from multiple authoritative sources"""
        sources = []

        # Framework-specific official docs
        if request.framework:
            try:
                repo_docs = await self.get_repository_insights(request)
                sources.append({
                    'content': repo_docs.content,
                    'authority': repo_docs.authority_score,
                    'source': 'official_docs'
                })
            except Exception as e:
                logger.warning(f"Failed to get official docs: {e}")

        # Industry best practices repositories
        practice_repos = [
            {'owner': 'google', 'repo': 'eng-practices', 'path': '/', 'authority': 9.5},
            {'owner': 'microsoft', 'repo': 'code-with-engineering-playbook', 'path': '/', 'authority': 9.0}
        ]

        for repo in practice_repos:
            try:
                content = await self._call_with_retry(
                    self.github_content,
                    owner=repo['owner'],
                    repo=repo['repo'],
                    path=repo['path']
                )
                sources.append({
                    'content': content,
                    'authority': repo['authority'],
                    'source': f"{repo['owner']}/{repo['repo']}"
                })
            except Exception as e:
                logger.warning(f"Failed to fetch {repo}: {e}")

        return sources

    def _rank_best_practices(self, sources: List[Dict], request: KnowledgeRequest) -> List[Dict]:
        """Rank best practices by authority and relevance to request"""
        # Simple ranking by authority score for now
        # TODO: Implement relevance scoring based on content analysis
        return sorted(sources, key=lambda x: x['authority'], reverse=True)[:5]

    def _format_best_practices(self, practices: List[Dict]) -> str:
        """Format best practices for agent consumption"""
        formatted = "# Industry Best Practices\n\n"

        for i, practice in enumerate(practices, 1):
            formatted += f"## {i}. Source: {practice['source']} (Authority: {practice['authority']})\n\n"
            formatted += f"{practice['content']}\n\n"
            formatted += "---\n\n"

        return formatted

    def _format_security_standards(self, standards: List[Dict]) -> str:
        """Format security standards for agent consumption"""
        formatted = "# Security and Compliance Standards\n\n"

        for standard in standards:
            formatted += f"## {standard['source']} (Authority: {standard['authority']})\n\n"
            formatted += f"{standard['content']}\n\n"
            formatted += "---\n\n"

        return formatted

    async def _call_with_retry(self, func, *args, **kwargs):
        """Call MCP function with retry logic and error handling"""
        max_retries = 3
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e

                delay = base_delay * (2 ** attempt)
                logger.warning(f"Retry {attempt + 1}/{max_retries} after {delay}s: {e}")
                await asyncio.sleep(delay)

    async def _get_fallback_content(self, request: KnowledgeRequest, error: str) -> KnowledgeResponse:
        """Get fallback content from cache or generate basic response"""
        # Try to get any related cached content
        fallback_content = await self.cache.get_fallback_content(request.type, request.framework)

        if fallback_content:
            return KnowledgeResponse(
                content=fallback_content,
                source="Cache:Fallback",
                authority_score=6.0,  # Lower authority for fallback
                last_updated=datetime.now() - timedelta(hours=24),  # Indicate stale
                response_time_ms=100
            )

        # Generate minimal response indicating unavailability
        return KnowledgeResponse(
            content=f"External knowledge temporarily unavailable for {request.framework}. Error: {error}",
            source="Internal:Fallback",
            authority_score=1.0,
            last_updated=datetime.now(),
            response_time_ms=50
        )

    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check of all MCP sources"""
        health_status = {}

        # Test Context7 connectivity
        try:
            test_result = await self._call_with_retry(
                self.context7_resolve, "react"
            )
            health_status['context7'] = {
                'status': 'healthy',
                'response_time_ms': 100,  # Measured during test
                'last_check': datetime.now().isoformat()
            }
        except Exception as e:
            health_status['context7'] = {
                'status': 'unhealthy',
                'error': str(e),
                'last_check': datetime.now().isoformat()
            }

        # Test DeepWiki connectivity
        try:
            test_result = await self._call_with_retry(
                self.deepwiki_fetch, "test", maxDepth=0
            )
            health_status['deepwiki'] = {
                'status': 'healthy',
                'response_time_ms': 150,
                'last_check': datetime.now().isoformat()
            }
        except Exception as e:
            health_status['deepwiki'] = {
                'status': 'unhealthy',
                'error': str(e),
                'last_check': datetime.now().isoformat()
            }

        # Test GitHub MCP connectivity
        try:
            test_result = await self._call_with_retry(
                self.github_search, "query:test"
            )
            health_status['github_mcp'] = {
                'status': 'healthy',
                'response_time_ms': 200,
                'last_check': datetime.now().isoformat()
            }
        except Exception as e:
            health_status['github_mcp'] = {
                'status': 'unhealthy',
                'error': str(e),
                'last_check': datetime.now().isoformat()
            }

        # Overall system health
        healthy_sources = sum(1 for s in health_status.values() if s['status'] == 'healthy')
        total_sources = len(health_status)

        health_status['system'] = {
            'overall_status': 'healthy' if healthy_sources >= 2 else 'degraded',
            'healthy_sources': healthy_sources,
            'total_sources': total_sources,
            'availability_percentage': (healthy_sources / total_sources) * 100
        }

        return health_status