"""
Intelligent Knowledge Caching Framework

Multi-layer caching system with dynamic TTL calculation, intelligent prefetching,
and content quality-based cache management for external knowledge sources.
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, asdict
import pickle
import redis
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class CacheMetrics:
    """Cache performance metrics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_requests: int = 0
    average_response_time_ms: float = 0.0
    cache_size_mb: float = 0.0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.hits / self.total_requests) * 100


@dataclass
class CacheEntry:
    """Individual cache entry with metadata"""
    content: Any
    created_at: datetime
    last_accessed: datetime
    access_count: int
    ttl_seconds: int
    authority_score: float
    source: str
    size_bytes: int

    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return datetime.now() > (self.created_at + timedelta(seconds=self.ttl_seconds))

    def is_stale(self, staleness_threshold: float = 0.8) -> bool:
        """Check if cache entry is approaching expiration"""
        age = (datetime.now() - self.created_at).total_seconds()
        return age > (self.ttl_seconds * staleness_threshold)


class IntelligentKnowledgeCache:
    """
    Multi-layer intelligent caching system optimized for external knowledge sources
    with dynamic TTL, content quality-based eviction, and predictive prefetching.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.metrics = CacheMetrics()

        # Initialize cache layers
        self._setup_cache_layers()

        # Cache statistics and intelligence
        self.access_patterns = defaultdict(list)
        self.content_popularity = defaultdict(int)

        # Start background tasks
        asyncio.create_task(self._cache_maintenance_loop())

    def _default_config(self) -> Dict:
        """Default caching configuration"""
        return {
            'l1_memory': {
                'max_size_mb': 256,
                'max_entries': 1000,
                'default_ttl': 1800  # 30 minutes
            },
            'l2_redis': {
                'host': 'localhost',
                'port': 6379,
                'db': 2,
                'max_connections': 10,
                'default_ttl': 7200  # 2 hours
            },
            'l3_persistent': {
                'enabled': True,
                'file_path': '/tmp/claude_config_knowledge_cache.db',
                'default_ttl': 86400  # 24 hours
            },
            'intelligence': {
                'dynamic_ttl': True,
                'predictive_prefetch': True,
                'quality_based_eviction': True,
                'staleness_threshold': 0.8
            }
        }

    def _setup_cache_layers(self):
        """Initialize multi-layer cache infrastructure"""
        # L1: In-memory cache for hot data
        self.l1_cache = {}
        self.l1_metadata = {}

        # L2: Redis cache for warm data
        try:
            self.redis_client = redis.asyncio.Redis(
                host=self.config['l2_redis']['host'],
                port=self.config['l2_redis']['port'],
                db=self.config['l2_redis']['db'],
                decode_responses=False  # Handle binary data
            )
            self.redis_available = True
            logger.info("Redis cache layer initialized")
        except Exception as e:
            logger.warning(f"Redis unavailable, using memory-only cache: {e}")
            self.redis_available = False

        # L3: Persistent cache for cold data
        self.persistent_cache = {}
        if self.config['l3_persistent']['enabled']:
            try:
                self._load_persistent_cache()
                logger.info("Persistent cache layer initialized")
            except Exception as e:
                logger.warning(f"Persistent cache initialization failed: {e}")

    async def get(self, key: str) -> Optional[Any]:
        """
        Intelligent cache lookup across all layers with automatic promotion
        """
        start_time = datetime.now()
        self.metrics.total_requests += 1

        # Normalize cache key
        cache_key = self._normalize_key(key)

        # L1 Memory cache check (fastest)
        if cache_key in self.l1_cache:
            entry = self.l1_metadata[cache_key]
            if not entry.is_expired():
                self._update_access_stats(entry, cache_key)
                self.metrics.hits += 1
                self._record_access_pattern(cache_key, 'l1_hit')
                return self.l1_cache[cache_key]
            else:
                # Remove expired entry
                del self.l1_cache[cache_key]
                del self.l1_metadata[cache_key]

        # L2 Redis cache check (medium speed)
        if self.redis_available:
            try:
                redis_data = await self.redis_client.get(f"knowledge:{cache_key}")
                if redis_data:
                    entry_data = pickle.loads(redis_data)
                    entry = CacheEntry(**entry_data['metadata'])

                    if not entry.is_expired():
                        content = entry_data['content']

                        # Promote to L1 if frequently accessed
                        if entry.access_count > 5:
                            await self._promote_to_l1(cache_key, content, entry)

                        self._update_access_stats(entry, cache_key)
                        self.metrics.hits += 1
                        self._record_access_pattern(cache_key, 'l2_hit')
                        return content
                    else:
                        # Remove expired entry
                        await self.redis_client.delete(f"knowledge:{cache_key}")
            except Exception as e:
                logger.warning(f"Redis cache error: {e}")

        # L3 Persistent cache check (slowest)
        if cache_key in self.persistent_cache:
            entry = self.persistent_cache[cache_key]
            if not entry.is_expired():
                content = entry.content

                # Promote to higher cache layers based on access patterns
                if entry.access_count > 2:
                    await self._promote_cache_entry(cache_key, content, entry)

                self._update_access_stats(entry, cache_key)
                self.metrics.hits += 1
                self._record_access_pattern(cache_key, 'l3_hit')
                return content
            else:
                # Remove expired entry
                del self.persistent_cache[cache_key]

        # Cache miss
        self.metrics.misses += 1
        self._record_access_pattern(cache_key, 'miss')

        # Update average response time
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        self._update_response_time(response_time)

        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None,
                 authority_score: float = 8.0, source: str = "unknown") -> bool:
        """
        Intelligent cache storage with dynamic layer selection and TTL optimization
        """
        cache_key = self._normalize_key(key)

        # Calculate dynamic TTL if not provided
        if ttl is None:
            ttl = self._calculate_dynamic_ttl(authority_score, source, cache_key)

        # Create cache entry with metadata
        entry = CacheEntry(
            content=value,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            access_count=1,
            ttl_seconds=ttl,
            authority_score=authority_score,
            source=source,
            size_bytes=self._calculate_size(value)
        )

        # Determine optimal cache layer
        cache_layer = self._select_cache_layer(entry, cache_key)

        # Store in selected layer(s)
        success = await self._store_in_layer(cache_key, value, entry, cache_layer)

        if success:
            self.content_popularity[cache_key] += 1
            self._record_access_pattern(cache_key, f'store_{cache_layer}')

        return success

    async def get_fallback_content(self, content_type: str, framework: Optional[str] = None) -> Optional[str]:
        """
        Get fallback content when primary sources are unavailable
        """
        fallback_patterns = [
            f"fallback:{content_type}:{framework}",
            f"fallback:{content_type}:*",
            f"fallback:*:{framework}",
            "fallback:generic"
        ]

        for pattern in fallback_patterns:
            content = await self.get(pattern)
            if content:
                logger.info(f"Using fallback content: {pattern}")
                return content

        return None

    def _calculate_dynamic_ttl(self, authority_score: float, source: str, cache_key: str) -> int:
        """
        Calculate dynamic TTL based on content characteristics and access patterns
        """
        if not self.config['intelligence']['dynamic_ttl']:
            return self.config['l1_memory']['default_ttl']

        # Base TTL from configuration
        base_ttl = self.config['l1_memory']['default_ttl']

        # Authority score multiplier (higher authority = longer cache)
        authority_multiplier = 1.0 + (authority_score - 5.0) / 10.0  # Scale 0.5-1.5

        # Source type multiplier
        source_multipliers = {
            'Context7': 1.2,      # Library docs change infrequently
            'DeepWiki': 1.0,      # Repository docs moderate change
            'GitHub': 0.8,        # Repository content changes frequently
            'SecurityStandards': 2.0,  # Security standards change slowly
            'BestPractices': 1.5   # Best practices are relatively stable
        }

        source_multiplier = 1.0
        for src_type, multiplier in source_multipliers.items():
            if src_type in source:
                source_multiplier = multiplier
                break

        # Access pattern multiplier (popular content cached longer)
        popularity = self.content_popularity.get(cache_key, 0)
        popularity_multiplier = 1.0 + min(popularity / 10.0, 0.5)

        # Calculate final TTL
        dynamic_ttl = int(base_ttl * authority_multiplier * source_multiplier * popularity_multiplier)

        # Bounds checking
        min_ttl = 300   # 5 minutes
        max_ttl = 86400  # 24 hours

        return max(min_ttl, min(dynamic_ttl, max_ttl))

    def _select_cache_layer(self, entry: CacheEntry, cache_key: str) -> str:
        """
        Select optimal cache layer based on content characteristics and access patterns
        """
        # High authority + frequent access = L1 (memory)
        if (entry.authority_score > 8.5 and
            self.content_popularity.get(cache_key, 0) > 5):
            return 'l1'

        # Medium authority + moderate access = L2 (Redis)
        if (entry.authority_score > 7.0 and
            self.content_popularity.get(cache_key, 0) > 2 and
            self.redis_available):
            return 'l2'

        # Everything else = L3 (Persistent)
        return 'l3'

    async def _store_in_layer(self, cache_key: str, content: Any,
                            entry: CacheEntry, layer: str) -> bool:
        """
        Store content in specified cache layer with appropriate eviction
        """
        try:
            if layer == 'l1':
                # Check memory limits and evict if necessary
                await self._ensure_l1_capacity()
                self.l1_cache[cache_key] = content
                self.l1_metadata[cache_key] = entry
                return True

            elif layer == 'l2' and self.redis_available:
                # Store in Redis with serialization
                entry_data = {
                    'content': content,
                    'metadata': asdict(entry)
                }
                serialized = pickle.dumps(entry_data)
                await self.redis_client.setex(
                    f"knowledge:{cache_key}",
                    entry.ttl_seconds,
                    serialized
                )
                return True

            elif layer == 'l3':
                # Store in persistent cache
                self.persistent_cache[cache_key] = entry
                # Periodic persistence is handled by maintenance loop
                return True

        except Exception as e:
            logger.error(f"Failed to store in {layer} cache: {e}")
            return False

        return False

    async def _ensure_l1_capacity(self):
        """
        Ensure L1 cache doesn't exceed memory limits through intelligent eviction
        """
        max_entries = self.config['l1_memory']['max_entries']

        if len(self.l1_cache) >= max_entries:
            # Evict based on quality and access patterns
            entries_to_evict = self._select_eviction_candidates()

            for key in entries_to_evict:
                if key in self.l1_cache:
                    # Demote to L2 if high value
                    entry = self.l1_metadata[key]
                    if entry.authority_score > 8.0 and self.redis_available:
                        await self._demote_to_l2(key, self.l1_cache[key], entry)

                    del self.l1_cache[key]
                    del self.l1_metadata[key]
                    self.metrics.evictions += 1

    def _select_eviction_candidates(self) -> List[str]:
        """
        Select cache entries for eviction based on intelligent scoring
        """
        if not self.l1_metadata:
            return []

        # Score entries for eviction (lower score = more likely to evict)
        scored_entries = []
        for key, entry in self.l1_metadata.items():
            score = self._calculate_eviction_score(entry, key)
            scored_entries.append((key, score))

        # Sort by score and return bottom 10% for eviction
        scored_entries.sort(key=lambda x: x[1])
        eviction_count = max(1, len(scored_entries) // 10)

        return [key for key, _ in scored_entries[:eviction_count]]

    def _calculate_eviction_score(self, entry: CacheEntry, cache_key: str) -> float:
        """
        Calculate eviction score for cache entry (lower = more likely to evict)
        """
        now = datetime.now()

        # Recency score (more recent = higher score)
        age_hours = (now - entry.last_accessed).total_seconds() / 3600
        recency_score = max(0, 10 - age_hours)  # 0-10 range

        # Frequency score (more accessed = higher score)
        frequency_score = min(entry.access_count, 10)  # Cap at 10

        # Authority score (higher authority = higher score)
        authority_score = entry.authority_score

        # Size penalty (larger = lower score)
        size_penalty = min(entry.size_bytes / (1024 * 1024), 5)  # MB to penalty

        # Combined score
        total_score = (recency_score * 0.3 +
                      frequency_score * 0.3 +
                      authority_score * 0.3 -
                      size_penalty * 0.1)

        return max(0, total_score)

    async def _promote_to_l1(self, cache_key: str, content: Any, entry: CacheEntry):
        """
        Promote frequently accessed content to L1 cache
        """
        await self._ensure_l1_capacity()
        self.l1_cache[cache_key] = content
        self.l1_metadata[cache_key] = entry
        logger.debug(f"Promoted {cache_key} to L1 cache")

    async def _demote_to_l2(self, cache_key: str, content: Any, entry: CacheEntry):
        """
        Demote content from L1 to L2 cache
        """
        if self.redis_available:
            await self._store_in_layer(cache_key, content, entry, 'l2')
            logger.debug(f"Demoted {cache_key} to L2 cache")

    async def _promote_cache_entry(self, cache_key: str, content: Any, entry: CacheEntry):
        """
        Promote cache entry to higher layer based on access patterns
        """
        if entry.access_count > 5:
            await self._promote_to_l1(cache_key, content, entry)
        elif entry.access_count > 2 and self.redis_available:
            await self._store_in_layer(cache_key, content, entry, 'l2')

    def _update_access_stats(self, entry: CacheEntry, cache_key: str):
        """Update access statistics for cache entry"""
        entry.last_accessed = datetime.now()
        entry.access_count += 1
        self.content_popularity[cache_key] += 1

    def _record_access_pattern(self, cache_key: str, access_type: str):
        """Record access patterns for intelligent prefetching"""
        if self.config['intelligence']['predictive_prefetch']:
            self.access_patterns[cache_key].append({
                'timestamp': datetime.now(),
                'type': access_type
            })

            # Limit access pattern history
            if len(self.access_patterns[cache_key]) > 100:
                self.access_patterns[cache_key] = self.access_patterns[cache_key][-50:]

    def _update_response_time(self, response_time_ms: float):
        """Update average response time metrics"""
        if self.metrics.total_requests == 1:
            self.metrics.average_response_time_ms = response_time_ms
        else:
            # Exponential moving average
            alpha = 0.1
            self.metrics.average_response_time_ms = (
                alpha * response_time_ms +
                (1 - alpha) * self.metrics.average_response_time_ms
            )

    def _normalize_key(self, key: str) -> str:
        """Normalize cache key for consistency"""
        # Create hash for very long keys
        if len(key) > 200:
            return hashlib.sha256(key.encode()).hexdigest()

        # Normalize case and special characters
        return key.lower().replace(' ', '_').replace(':', '_')

    def _calculate_size(self, value: Any) -> int:
        """Calculate approximate size of cached value in bytes"""
        try:
            if isinstance(value, str):
                return len(value.encode('utf-8'))
            else:
                return len(pickle.dumps(value))
        except Exception:
            return 1024  # Default estimate

    def _load_persistent_cache(self):
        """Load persistent cache from file"""
        try:
            cache_file = self.config['l3_persistent']['file_path']
            with open(cache_file, 'rb') as f:
                self.persistent_cache = pickle.load(f)
            logger.info(f"Loaded {len(self.persistent_cache)} entries from persistent cache")
        except FileNotFoundError:
            logger.info("No persistent cache file found, starting fresh")
        except Exception as e:
            logger.error(f"Failed to load persistent cache: {e}")

    async def _save_persistent_cache(self):
        """Save persistent cache to file"""
        try:
            cache_file = self.config['l3_persistent']['file_path']
            with open(cache_file, 'wb') as f:
                pickle.dump(self.persistent_cache, f)
            logger.debug(f"Saved {len(self.persistent_cache)} entries to persistent cache")
        except Exception as e:
            logger.error(f"Failed to save persistent cache: {e}")

    async def _cache_maintenance_loop(self):
        """
        Background maintenance tasks for cache optimization
        """
        while True:
            try:
                # Cleanup expired entries
                await self._cleanup_expired_entries()

                # Save persistent cache
                if self.config['l3_persistent']['enabled']:
                    await self._save_persistent_cache()

                # Predictive prefetching
                if self.config['intelligence']['predictive_prefetch']:
                    await self._predictive_prefetch()

                # Update cache metrics
                await self._update_cache_metrics()

                # Sleep for 5 minutes before next maintenance cycle
                await asyncio.sleep(300)

            except Exception as e:
                logger.error(f"Cache maintenance error: {e}")
                await asyncio.sleep(60)  # Retry after 1 minute on error

    async def _cleanup_expired_entries(self):
        """Remove expired entries from all cache layers"""
        # Clean L1 cache
        expired_l1 = [k for k, entry in self.l1_metadata.items() if entry.is_expired()]
        for key in expired_l1:
            del self.l1_cache[key]
            del self.l1_metadata[key]

        # Clean L3 persistent cache
        expired_l3 = [k for k, entry in self.persistent_cache.items() if entry.is_expired()]
        for key in expired_l3:
            del self.persistent_cache[key]

        if expired_l1 or expired_l3:
            logger.debug(f"Cleaned up {len(expired_l1)} L1 and {len(expired_l3)} L3 expired entries")

    async def _predictive_prefetch(self):
        """
        Predictive prefetching based on access patterns
        """
        # Analyze access patterns and predict next requests
        # This is a simplified implementation - could be enhanced with ML

        frequently_accessed = [
            key for key, count in self.content_popularity.items()
            if count > 10
        ]

        # Ensure frequently accessed content is in higher cache layers
        for key in frequently_accessed[:10]:  # Top 10
            if key not in self.l1_cache and key in self.persistent_cache:
                entry = self.persistent_cache[key]
                if not entry.is_expired():
                    await self._promote_to_l1(key, entry.content, entry)

    async def _update_cache_metrics(self):
        """Update cache size and performance metrics"""
        # Calculate L1 cache size
        l1_size = sum(
            self.l1_metadata[key].size_bytes
            for key in self.l1_cache
        ) / (1024 * 1024)  # Convert to MB

        self.metrics.cache_size_mb = l1_size

    async def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive cache performance metrics"""
        return {
            'performance': asdict(self.metrics),
            'cache_layers': {
                'l1_entries': len(self.l1_cache),
                'l2_available': self.redis_available,
                'l3_entries': len(self.persistent_cache)
            },
            'popular_content': dict(
                sorted(self.content_popularity.items(),
                       key=lambda x: x[1], reverse=True)[:10]
            ),
            'system_health': {
                'hit_rate_target': 85.0,
                'current_hit_rate': self.metrics.hit_rate,
                'response_time_target_ms': 100.0,
                'current_response_time_ms': self.metrics.average_response_time_ms
            }
        }

    async def clear_cache(self, pattern: Optional[str] = None):
        """Clear cache entries matching pattern or all if no pattern"""
        if pattern:
            # Clear matching entries
            keys_to_remove = [k for k in self.l1_cache.keys() if pattern in k]
            for key in keys_to_remove:
                if key in self.l1_cache:
                    del self.l1_cache[key]
                if key in self.l1_metadata:
                    del self.l1_metadata[key]
                if key in self.persistent_cache:
                    del self.persistent_cache[key]

            if self.redis_available:
                # Clear Redis entries matching pattern
                keys = await self.redis_client.keys(f"knowledge:*{pattern}*")
                if keys:
                    await self.redis_client.delete(*keys)

            logger.info(f"Cleared {len(keys_to_remove)} cache entries matching '{pattern}'")
        else:
            # Clear all caches
            self.l1_cache.clear()
            self.l1_metadata.clear()
            self.persistent_cache.clear()

            if self.redis_available:
                await self.redis_client.flushdb()

            # Reset metrics
            self.metrics = CacheMetrics()
            self.content_popularity.clear()
            self.access_patterns.clear()

            logger.info("Cleared all cache layers")