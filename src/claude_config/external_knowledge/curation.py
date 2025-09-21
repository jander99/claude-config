"""
Knowledge Curation Engine

Automated content curation system for industry best practices, security standards,
and authoritative technical guidance with quality scoring and relevance ranking.
"""

import asyncio
import re
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import logging
from urllib.parse import urlparse
import json

logger = logging.getLogger(__name__)


class ContentType(Enum):
    """Types of content for curation"""
    FRAMEWORK_DOCS = "framework_docs"
    BEST_PRACTICES = "best_practices"
    SECURITY_STANDARDS = "security_standards"
    COMPLIANCE_FRAMEWORKS = "compliance_frameworks"
    DESIGN_PATTERNS = "design_patterns"
    PERFORMANCE_GUIDES = "performance_guides"
    ARCHITECTURE_PATTERNS = "architecture_patterns"


class AuthorityLevel(Enum):
    """Authority levels for content sources"""
    OFFICIAL = 10.0      # Official documentation, standards bodies
    AUTHORITATIVE = 9.0  # Major tech companies, recognized experts
    TRUSTED = 8.0        # Well-known organizations, popular frameworks
    COMMUNITY = 7.0      # Community-driven, open source projects
    EXPERIMENTAL = 6.0   # New frameworks, experimental approaches
    UNKNOWN = 5.0        # Unknown or unverified sources


@dataclass
class ContentSource:
    """Definition of a content source for curation"""
    name: str
    base_url: str
    authority_level: AuthorityLevel
    content_types: List[ContentType]
    update_frequency: str  # 'daily', 'weekly', 'monthly', 'quarterly'
    extraction_patterns: Dict[str, str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_updated: Optional[datetime] = None
    active: bool = True


@dataclass
class CuratedContent:
    """Curated content with quality scoring and metadata"""
    id: str
    title: str
    content: str
    content_type: ContentType
    source: ContentSource
    authority_score: float
    relevance_score: float
    quality_score: float
    tags: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_validated: Optional[datetime] = None
    access_count: int = 0
    url: Optional[str] = None
    summary: Optional[str] = None


class KnowledgeCurationEngine:
    """
    Automated content curation engine for industry best practices and standards
    with intelligent quality scoring, relevance ranking, and content validation.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.content_sources = self._initialize_content_sources()
        self.curated_content: Dict[str, CuratedContent] = {}
        self.content_index = self._build_content_index()

        # Quality and relevance scoring models
        self.quality_patterns = self._initialize_quality_patterns()
        self.framework_keywords = self._initialize_framework_keywords()

        # Start background curation tasks
        asyncio.create_task(self._content_curation_loop())

    def _default_config(self) -> Dict:
        """Default configuration for content curation"""
        return {
            'curation': {
                'min_quality_score': 7.0,
                'min_authority_score': 7.5,
                'max_content_age_days': 365,
                'duplicate_threshold': 0.85,
                'batch_size': 50
            },
            'sources': {
                'update_interval_hours': 24,
                'max_concurrent_fetches': 5,
                'request_timeout_seconds': 30,
                'retry_attempts': 3
            },
            'quality': {
                'content_length_min': 500,
                'content_length_optimal': 2000,
                'code_example_bonus': 1.2,
                'reference_link_bonus': 1.1,
                'structured_format_bonus': 1.15
            }
        }

    def _initialize_content_sources(self) -> List[ContentSource]:
        """Initialize authoritative content sources for curation"""
        return [
            # Google Engineering Practices
            ContentSource(
                name="Google Engineering Practices",
                base_url="https://google.github.io/eng-practices/",
                authority_level=AuthorityLevel.AUTHORITATIVE,
                content_types=[ContentType.BEST_PRACTICES, ContentType.DESIGN_PATTERNS],
                update_frequency="weekly",
                extraction_patterns={
                    "review_guide": r"review/.*\.md$",
                    "style_guides": r"style/.*\.md$"
                },
                metadata={"focus": "code_review,engineering_process"}
            ),

            # Microsoft Architecture Patterns
            ContentSource(
                name="Microsoft Azure Architecture",
                base_url="https://docs.microsoft.com/en-us/azure/architecture/",
                authority_level=AuthorityLevel.AUTHORITATIVE,
                content_types=[ContentType.ARCHITECTURE_PATTERNS, ContentType.BEST_PRACTICES],
                update_frequency="bi-weekly",
                extraction_patterns={
                    "patterns": r"patterns/.*\.md$",
                    "best_practices": r"best-practices/.*\.md$"
                },
                metadata={"focus": "cloud_architecture,microservices,scalability"}
            ),

            # AWS Well-Architected Framework
            ContentSource(
                name="AWS Well-Architected",
                base_url="https://aws.amazon.com/architecture/well-architected/",
                authority_level=AuthorityLevel.AUTHORITATIVE,
                content_types=[ContentType.ARCHITECTURE_PATTERNS, ContentType.PERFORMANCE_GUIDES],
                update_frequency="monthly",
                extraction_patterns={
                    "pillars": r"pillars/.*\.html$",
                    "patterns": r"patterns/.*\.html$"
                },
                metadata={"focus": "cloud_architecture,security,cost_optimization"}
            ),

            # OWASP Security Standards
            ContentSource(
                name="OWASP Security Guidelines",
                base_url="https://owasp.org/",
                authority_level=AuthorityLevel.OFFICIAL,
                content_types=[ContentType.SECURITY_STANDARDS, ContentType.BEST_PRACTICES],
                update_frequency="quarterly",
                extraction_patterns={
                    "top_10": r"www-project-top-ten/.*\.md$",
                    "cheat_sheets": r"CheatSheetSeries/.*\.md$"
                },
                metadata={"focus": "web_security,api_security,application_security"}
            ),

            # NIST Cybersecurity Framework
            ContentSource(
                name="NIST Cybersecurity Framework",
                base_url="https://www.nist.gov/cyberframework/",
                authority_level=AuthorityLevel.OFFICIAL,
                content_types=[ContentType.SECURITY_STANDARDS, ContentType.COMPLIANCE_FRAMEWORKS],
                update_frequency="quarterly",
                extraction_patterns={
                    "framework": r"framework/.*\.pdf$",
                    "implementation": r"implementation-guide/.*\.pdf$"
                },
                metadata={"focus": "cybersecurity,risk_management,compliance"}
            ),

            # Clean Architecture (Uncle Bob)
            ContentSource(
                name="Clean Architecture Principles",
                base_url="https://blog.cleancoder.com/",
                authority_level=AuthorityLevel.AUTHORITATIVE,
                content_types=[ContentType.DESIGN_PATTERNS, ContentType.ARCHITECTURE_PATTERNS],
                update_frequency="monthly",
                extraction_patterns={
                    "articles": r"uncle-bob/.*\.html$"
                },
                metadata={"focus": "clean_architecture,solid_principles,design_patterns"}
            ),

            # Martin Fowler's Architecture Patterns
            ContentSource(
                name="Martin Fowler Architecture",
                base_url="https://martinfowler.com/",
                authority_level=AuthorityLevel.AUTHORITATIVE,
                content_types=[ContentType.ARCHITECTURE_PATTERNS, ContentType.DESIGN_PATTERNS],
                update_frequency="monthly",
                extraction_patterns={
                    "articles": r"articles/.*\.html$",
                    "patterns": r"eaaCatalog/.*\.html$"
                },
                metadata={"focus": "enterprise_architecture,design_patterns,refactoring"}
            ),

            # GitHub Engineering Blog
            ContentSource(
                name="GitHub Engineering",
                base_url="https://github.blog/category/engineering/",
                authority_level=AuthorityLevel.AUTHORITATIVE,
                content_types=[ContentType.BEST_PRACTICES, ContentType.PERFORMANCE_GUIDES],
                update_frequency="weekly",
                extraction_patterns={
                    "engineering": r"engineering/.*\.html$"
                },
                metadata={"focus": "scalability,performance,git_workflows"}
            ),

            # The Twelve-Factor App
            ContentSource(
                name="The Twelve-Factor App",
                base_url="https://12factor.net/",
                authority_level=AuthorityLevel.AUTHORITATIVE,
                content_types=[ContentType.BEST_PRACTICES, ContentType.ARCHITECTURE_PATTERNS],
                update_frequency="yearly",
                extraction_patterns={
                    "factors": r"/.*$"
                },
                metadata={"focus": "cloud_native,microservices,deployment"}
            ),

            # High Scalability
            ContentSource(
                name="High Scalability",
                base_url="http://highscalability.com/",
                authority_level=AuthorityLevel.TRUSTED,
                content_types=[ContentType.ARCHITECTURE_PATTERNS, ContentType.PERFORMANCE_GUIDES],
                update_frequency="weekly",
                extraction_patterns={
                    "articles": r"blog/.*\.html$"
                },
                metadata={"focus": "scalability,performance,system_design"}
            )
        ]

    def _initialize_quality_patterns(self) -> Dict[str, Dict[str, float]]:
        """Initialize patterns for content quality scoring"""
        return {
            'code_examples': {
                r'```[\s\S]*?```': 2.0,          # Code blocks
                r'`[^`]+`': 0.5,                 # Inline code
                r'example[s]?:': 1.0,            # Example sections
                r'implementation': 1.5,           # Implementation details
            },
            'structure_indicators': {
                r'^#{1,6}\s+': 1.0,              # Headers
                r'^\*\s+|\d+\.\s+': 0.5,        # Lists
                r'\[.*?\]\(.*?\)': 0.3,         # Links
                r'^\|.*?\|': 0.8,               # Tables
            },
            'authority_indicators': {
                r'rfc\s+\d+': 2.0,              # RFC references
                r'iso\s+\d+': 2.0,              # ISO standards
                r'nist\s+sp': 2.0,              # NIST publications
                r'doi:\s*10\.': 1.5,            # DOI references
            },
            'quality_detractors': {
                r'todo:?': -1.0,                # TODO items
                r'fixme:?': -1.0,               # FIXME items
                r'hack:?': -0.5,                # Hack indicators
                r'temporary': -0.5,             # Temporary solutions
            }
        }

    def _initialize_framework_keywords(self) -> Dict[str, List[str]]:
        """Initialize framework-specific keywords for relevance scoring"""
        return {
            'react': [
                'jsx', 'hooks', 'component', 'props', 'state', 'virtual dom',
                'react router', 'redux', 'context api', 'useEffect', 'useState'
            ],
            'angular': [
                'typescript', 'component', 'service', 'directive', 'module',
                'dependency injection', 'rxjs', 'observables', 'angular cli'
            ],
            'vue': [
                'template', 'component', 'directive', 'vuex', 'vue router',
                'composition api', 'options api', 'single file component'
            ],
            'django': [
                'orm', 'models', 'views', 'templates', 'url patterns',
                'middleware', 'forms', 'admin', 'rest framework'
            ],
            'fastapi': [
                'pydantic', 'async', 'dependency injection', 'swagger',
                'openapi', 'middleware', 'request', 'response'
            ],
            'spring': [
                'bean', 'annotation', 'dependency injection', 'aop',
                'mvc', 'boot', 'data', 'security', 'actuator'
            ],
            'kubernetes': [
                'pod', 'service', 'deployment', 'ingress', 'configmap',
                'secret', 'namespace', 'helm', 'kubectl'
            ],
            'docker': [
                'container', 'image', 'dockerfile', 'compose', 'volume',
                'network', 'registry', 'orchestration'
            ]
        }

    async def curate_framework_content(self, framework: str,
                                     content_types: Optional[List[ContentType]] = None) -> List[CuratedContent]:
        """
        Curate content specific to a framework with quality and relevance scoring
        """
        if content_types is None:
            content_types = [ContentType.BEST_PRACTICES, ContentType.FRAMEWORK_DOCS]

        curated_items = []

        # Search existing curated content
        for content in self.curated_content.values():
            if (framework.lower() in [f.lower() for f in content.frameworks] and
                content.content_type in content_types and
                content.quality_score >= self.config['curation']['min_quality_score']):
                curated_items.append(content)

        # Sort by combined quality and relevance score
        curated_items.sort(
            key=lambda x: (x.quality_score + x.relevance_score) / 2,
            reverse=True
        )

        return curated_items[:20]  # Return top 20 items

    async def curate_security_standards(self, domain: str) -> List[CuratedContent]:
        """
        Curate security and compliance standards for specific domains
        """
        domain_mappings = {
            'web_security': ['owasp', 'xss', 'csrf', 'injection', 'authentication'],
            'api_security': ['owasp api', 'oauth', 'jwt', 'rate limiting', 'authorization'],
            'cloud_security': ['aws security', 'azure security', 'gcp security', 'iam'],
            'data_protection': ['gdpr', 'encryption', 'pii', 'data classification'],
            'compliance': ['sox', 'hipaa', 'pci dss', 'iso 27001', 'nist']
        }

        keywords = domain_mappings.get(domain.lower(), [domain])

        security_content = []
        for content in self.curated_content.values():
            if (content.content_type in [ContentType.SECURITY_STANDARDS, ContentType.COMPLIANCE_FRAMEWORKS] and
                self._content_matches_keywords(content, keywords) and
                content.authority_score >= self.config['curation']['min_authority_score']):
                security_content.append(content)

        # Sort by authority score and recency
        security_content.sort(
            key=lambda x: (x.authority_score, x.created_at.timestamp()),
            reverse=True
        )

        return security_content[:15]  # Return top 15 items

    async def curate_best_practices(self, domain: str, framework: Optional[str] = None) -> List[CuratedContent]:
        """
        Curate industry best practices for specific domains and frameworks
        """
        domain_keywords = {
            'testing': ['unit test', 'integration test', 'tdd', 'bdd', 'coverage'],
            'architecture': ['design pattern', 'clean architecture', 'solid', 'microservices'],
            'performance': ['optimization', 'caching', 'profiling', 'benchmark'],
            'security': ['secure coding', 'authentication', 'authorization', 'encryption'],
            'deployment': ['ci/cd', 'docker', 'kubernetes', 'automation', 'pipeline'],
            'code_quality': ['code review', 'linting', 'formatting', 'refactoring']
        }

        keywords = domain_keywords.get(domain.lower(), [domain])

        # Add framework-specific keywords if provided
        if framework:
            framework_keywords = self.framework_keywords.get(framework.lower(), [])
            keywords.extend(framework_keywords)

        best_practices = []
        for content in self.curated_content.values():
            if (content.content_type == ContentType.BEST_PRACTICES and
                self._content_matches_keywords(content, keywords) and
                content.quality_score >= self.config['curation']['min_quality_score']):

                # Boost score if framework matches
                relevance_boost = 1.0
                if framework and framework.lower() in [f.lower() for f in content.frameworks]:
                    relevance_boost = 1.5

                content.relevance_score *= relevance_boost
                best_practices.append(content)

        # Sort by combined quality, relevance, and authority
        best_practices.sort(
            key=lambda x: (x.quality_score * 0.4 + x.relevance_score * 0.4 + x.authority_score * 0.2),
            reverse=True
        )

        return best_practices[:25]  # Return top 25 items

    def _content_matches_keywords(self, content: CuratedContent, keywords: List[str]) -> bool:
        """Check if content matches any of the provided keywords"""
        text = f"{content.title} {content.content} {' '.join(content.tags)}".lower()

        return any(keyword.lower() in text for keyword in keywords)

    async def add_content_source(self, source: ContentSource) -> bool:
        """
        Add a new content source for curation
        """
        try:
            # Validate source configuration
            if not source.base_url or not source.name:
                raise ValueError("Source must have name and base_url")

            # Test accessibility
            is_accessible = await self._test_source_accessibility(source)
            if not is_accessible:
                logger.warning(f"Source {source.name} is not accessible")
                return False

            self.content_sources.append(source)
            logger.info(f"Added content source: {source.name}")

            # Trigger immediate curation for new source
            asyncio.create_task(self._curate_from_source(source))

            return True

        except Exception as e:
            logger.error(f"Failed to add content source {source.name}: {e}")
            return False

    async def update_content_quality_scores(self) -> int:
        """
        Recalculate quality scores for all curated content
        """
        updated_count = 0

        for content in self.curated_content.values():
            old_score = content.quality_score

            # Recalculate quality score
            content.quality_score = self._calculate_quality_score(content.content, content.content_type)

            # Recalculate relevance score
            content.relevance_score = self._calculate_relevance_score(content)

            if abs(content.quality_score - old_score) > 0.5:
                updated_count += 1
                logger.debug(f"Updated quality score for {content.id}: {old_score:.2f} -> {content.quality_score:.2f}")

        logger.info(f"Updated quality scores for {updated_count} content items")
        return updated_count

    def _calculate_quality_score(self, content: str, content_type: ContentType) -> float:
        """
        Calculate quality score based on content characteristics
        """
        base_score = 5.0  # Starting score
        score_adjustments = 0.0

        # Length score (optimal length gets bonus)
        content_length = len(content)
        if content_length < self.config['quality']['content_length_min']:
            score_adjustments -= 1.0  # Too short
        elif content_length > self.config['quality']['content_length_optimal']:
            score_adjustments += 0.5  # Good length
        else:
            # Scale between min and optimal
            length_ratio = content_length / self.config['quality']['content_length_optimal']
            score_adjustments += length_ratio * 0.5

        # Pattern-based scoring
        for category, patterns in self.quality_patterns.items():
            for pattern, weight in patterns.items():
                matches = len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))
                if matches > 0:
                    # Diminishing returns for multiple matches
                    adjustment = weight * min(matches, 5) * 0.2
                    score_adjustments += adjustment

        # Content type specific adjustments
        if content_type == ContentType.SECURITY_STANDARDS:
            # Security content should be more authoritative
            if any(term in content.lower() for term in ['rfc', 'iso', 'nist', 'owasp']):
                score_adjustments += 1.0

        elif content_type == ContentType.BEST_PRACTICES:
            # Best practices should have examples
            if '```' in content or 'example' in content.lower():
                score_adjustments += self.config['quality']['code_example_bonus']

        # Final score calculation with bounds
        final_score = base_score + score_adjustments
        return max(1.0, min(10.0, final_score))

    def _calculate_relevance_score(self, content: CuratedContent) -> float:
        """
        Calculate relevance score based on framework matching and content freshness
        """
        base_score = 5.0

        # Framework relevance
        framework_boost = 0.0
        for framework in content.frameworks:
            if framework.lower() in self.framework_keywords:
                keywords = self.framework_keywords[framework.lower()]
                matches = sum(1 for keyword in keywords
                            if keyword.lower() in content.content.lower())
                framework_boost += min(matches * 0.3, 2.0)  # Cap at 2.0

        # Recency boost (newer content gets slight boost)
        days_old = (datetime.now() - content.created_at).days
        recency_boost = max(0, 1.0 - (days_old / 365))  # Linear decay over 1 year

        # Access count boost (popular content)
        popularity_boost = min(content.access_count * 0.1, 1.0)  # Cap at 1.0

        final_score = base_score + framework_boost + recency_boost + popularity_boost
        return max(1.0, min(10.0, final_score))

    async def _content_curation_loop(self):
        """
        Background loop for continuous content curation
        """
        while True:
            try:
                # Curate from all active sources
                for source in self.content_sources:
                    if source.active:
                        try:
                            await self._curate_from_source(source)
                        except Exception as e:
                            logger.error(f"Curation failed for {source.name}: {e}")

                # Update quality scores
                await self.update_content_quality_scores()

                # Clean up old or low-quality content
                await self._cleanup_old_content()

                # Rebuild content index
                self.content_index = self._build_content_index()

                # Sleep until next curation cycle
                sleep_hours = self.config['sources']['update_interval_hours']
                await asyncio.sleep(sleep_hours * 3600)

            except Exception as e:
                logger.error(f"Content curation loop error: {e}")
                await asyncio.sleep(3600)  # Retry after 1 hour

    async def _curate_from_source(self, source: ContentSource):
        """
        Curate content from a specific source
        """
        logger.info(f"Curating content from {source.name}")

        try:
            # Fetch content from source (this would be implemented with actual web scraping)
            # For now, simulate content extraction
            raw_content_items = await self._extract_content_from_source(source)

            for raw_item in raw_content_items:
                # Check for duplicates
                content_hash = self._calculate_content_hash(raw_item['content'])
                if content_hash in self.curated_content:
                    continue

                # Create curated content item
                curated_item = CuratedContent(
                    id=content_hash,
                    title=raw_item['title'],
                    content=raw_item['content'],
                    content_type=raw_item['content_type'],
                    source=source,
                    authority_score=source.authority_level.value,
                    relevance_score=self._calculate_relevance_score_from_raw(raw_item),
                    quality_score=self._calculate_quality_score(raw_item['content'], raw_item['content_type']),
                    tags=raw_item.get('tags', []),
                    frameworks=raw_item.get('frameworks', []),
                    url=raw_item.get('url'),
                    summary=raw_item.get('summary')
                )

                # Only add high-quality content
                if (curated_item.quality_score >= self.config['curation']['min_quality_score'] and
                    curated_item.authority_score >= self.config['curation']['min_authority_score']):

                    self.curated_content[content_hash] = curated_item
                    logger.debug(f"Added curated content: {curated_item.title}")

            source.last_updated = datetime.now()
            logger.info(f"Completed curation from {source.name}: {len(raw_content_items)} items processed")

        except Exception as e:
            logger.error(f"Failed to curate from {source.name}: {e}")

    async def _extract_content_from_source(self, source: ContentSource) -> List[Dict]:
        """
        Extract content from source (placeholder for actual implementation)
        """
        # This would implement actual web scraping/API calls
        # For demonstration, return mock data

        mock_content = [
            {
                'title': f"Best Practices from {source.name}",
                'content': f"Comprehensive guide to {source.metadata.get('focus', 'development')} best practices...",
                'content_type': ContentType.BEST_PRACTICES,
                'tags': ['best-practices', 'guidelines'],
                'frameworks': ['react', 'vue'] if 'frontend' in source.metadata.get('focus', '') else [],
                'url': f"{source.base_url}/guide",
                'summary': f"Essential guidelines from {source.name}"
            }
        ]

        return mock_content

    async def _test_source_accessibility(self, source: ContentSource) -> bool:
        """
        Test if a content source is accessible
        """
        try:
            # This would implement actual connectivity testing
            # For now, assume all sources are accessible
            return True
        except Exception:
            return False

    def _calculate_content_hash(self, content: str) -> str:
        """Calculate unique hash for content deduplication"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _calculate_relevance_score_from_raw(self, raw_item: Dict) -> float:
        """Calculate initial relevance score from raw content"""
        # Simple implementation - could be enhanced with ML
        base_score = 5.0

        # Framework matching
        frameworks = raw_item.get('frameworks', [])
        if frameworks:
            base_score += len(frameworks) * 0.5

        # Tag relevance
        tags = raw_item.get('tags', [])
        if tags:
            base_score += len(tags) * 0.2

        return min(10.0, base_score)

    async def _cleanup_old_content(self):
        """Remove old or low-quality content"""
        cutoff_date = datetime.now() - timedelta(days=self.config['curation']['max_content_age_days'])
        min_quality = self.config['curation']['min_quality_score']

        items_to_remove = []
        for content_id, content in self.curated_content.items():
            if (content.created_at < cutoff_date or
                content.quality_score < min_quality):
                items_to_remove.append(content_id)

        for content_id in items_to_remove:
            del self.curated_content[content_id]

        if items_to_remove:
            logger.info(f"Removed {len(items_to_remove)} outdated content items")

    def _build_content_index(self) -> Dict[str, List[str]]:
        """Build searchable index of curated content"""
        index = {}

        for content_id, content in self.curated_content.items():
            # Index by content type
            content_type_key = content.content_type.value
            if content_type_key not in index:
                index[content_type_key] = []
            index[content_type_key].append(content_id)

            # Index by frameworks
            for framework in content.frameworks:
                framework_key = f"framework:{framework.lower()}"
                if framework_key not in index:
                    index[framework_key] = []
                index[framework_key].append(content_id)

            # Index by tags
            for tag in content.tags:
                tag_key = f"tag:{tag.lower()}"
                if tag_key not in index:
                    index[tag_key] = []
                index[tag_key].append(content_id)

        return index

    async def search_content(self, query: str, content_type: Optional[ContentType] = None,
                           framework: Optional[str] = None, limit: int = 20) -> List[CuratedContent]:
        """
        Search curated content with ranking
        """
        results = []

        # Build search keys
        search_keys = []
        if content_type:
            search_keys.append(content_type.value)
        if framework:
            search_keys.append(f"framework:{framework.lower()}")

        # Get candidate content IDs
        candidate_ids = set()
        if search_keys:
            for key in search_keys:
                if key in self.content_index:
                    candidate_ids.update(self.content_index[key])
        else:
            candidate_ids = set(self.curated_content.keys())

        # Score and filter candidates
        scored_results = []
        query_terms = query.lower().split()

        for content_id in candidate_ids:
            content = self.curated_content[content_id]

            # Calculate search relevance
            search_score = self._calculate_search_score(content, query_terms)

            if search_score > 0:
                total_score = (
                    search_score * 0.4 +
                    content.quality_score * 0.3 +
                    content.relevance_score * 0.2 +
                    content.authority_score * 0.1
                )
                scored_results.append((content, total_score))

        # Sort by score and return top results
        scored_results.sort(key=lambda x: x[1], reverse=True)
        return [content for content, _ in scored_results[:limit]]

    def _calculate_search_score(self, content: CuratedContent, query_terms: List[str]) -> float:
        """Calculate search relevance score"""
        searchable_text = f"{content.title} {content.content} {' '.join(content.tags)}".lower()

        score = 0.0
        for term in query_terms:
            # Title matches get higher score
            if term in content.title.lower():
                score += 3.0

            # Content matches
            content_matches = searchable_text.count(term)
            score += min(content_matches * 0.5, 5.0)  # Cap at 5.0

            # Tag matches
            if term in [tag.lower() for tag in content.tags]:
                score += 2.0

        return score

    async def get_curation_metrics(self) -> Dict[str, Any]:
        """Get comprehensive curation metrics"""
        total_content = len(self.curated_content)

        # Content by type
        content_by_type = {}
        for content in self.curated_content.values():
            content_type = content.content_type.value
            content_by_type[content_type] = content_by_type.get(content_type, 0) + 1

        # Content by source
        content_by_source = {}
        for content in self.curated_content.values():
            source_name = content.source.name
            content_by_source[source_name] = content_by_source.get(source_name, 0) + 1

        # Quality distribution
        quality_scores = [c.quality_score for c in self.curated_content.values()]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

        # Top frameworks
        framework_counts = {}
        for content in self.curated_content.values():
            for framework in content.frameworks:
                framework_counts[framework] = framework_counts.get(framework, 0) + 1

        top_frameworks = sorted(framework_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            'total_content_items': total_content,
            'content_by_type': content_by_type,
            'content_by_source': content_by_source,
            'average_quality_score': avg_quality,
            'top_frameworks': dict(top_frameworks),
            'active_sources': len([s for s in self.content_sources if s.active]),
            'total_sources': len(self.content_sources),
            'last_curation_run': max(
                [s.last_updated for s in self.content_sources if s.last_updated],
                default=None
            )
        }