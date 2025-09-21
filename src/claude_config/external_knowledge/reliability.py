"""
Knowledge Source Reliability Framework

Comprehensive monitoring, health checking, and fallback management for external
knowledge sources with 99.9% availability targets and intelligent degradation.
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import statistics

logger = logging.getLogger(__name__)


class SourceStatus(Enum):
    """Health status of knowledge sources"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    MAINTENANCE = "maintenance"
    UNKNOWN = "unknown"


class FailureType(Enum):
    """Types of failures that can occur"""
    TIMEOUT = "timeout"
    CONNECTION_ERROR = "connection_error"
    AUTHENTICATION_ERROR = "authentication_error"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    INVALID_RESPONSE = "invalid_response"
    SERVICE_UNAVAILABLE = "service_unavailable"
    QUOTA_EXCEEDED = "quota_exceeded"


@dataclass
class HealthMetric:
    """Individual health metric measurement"""
    timestamp: datetime
    response_time_ms: float
    success: bool
    error_type: Optional[FailureType] = None
    error_message: Optional[str] = None
    endpoint: Optional[str] = None


@dataclass
class SourceHealth:
    """Comprehensive health status for a knowledge source"""
    source_name: str
    status: SourceStatus
    last_check: datetime
    response_time_p95: float  # 95th percentile response time
    availability_24h: float   # 24-hour availability percentage
    error_rate_1h: float     # 1-hour error rate
    consecutive_failures: int
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    health_score: float = 100.0  # 0-100 health score
    metrics_history: List[HealthMetric] = field(default_factory=list)


@dataclass
class FallbackStrategy:
    """Fallback strategy configuration"""
    primary_sources: List[str]
    fallback_sources: List[str]
    cache_fallback: bool = True
    static_fallback: Optional[str] = None
    max_fallback_age_hours: int = 24
    priority_order: List[str] = field(default_factory=list)


class CircuitBreaker:
    """Circuit breaker pattern implementation for external sources"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # 'closed', 'open', 'half-open'

    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == 'open':
            if self._should_attempt_reset():
                self.state = 'half-open'
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) >= self.recovery_timeout

    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.state = 'closed'

    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = 'open'
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")


class KnowledgeSourceReliability:
    """
    Comprehensive reliability management for external knowledge sources
    with health monitoring, circuit breakers, and intelligent fallback strategies.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.source_health: Dict[str, SourceHealth] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.fallback_strategies: Dict[str, FallbackStrategy] = {}

        # Monitoring and alerting
        self.alert_handlers: List[Callable] = []
        self.health_history: Dict[str, List[HealthMetric]] = {}

        # Start background monitoring
        asyncio.create_task(self._health_monitoring_loop())
        asyncio.create_task(self._health_analysis_loop())

    def _default_config(self) -> Dict:
        """Default configuration for reliability framework"""
        return {
            'monitoring': {
                'check_interval_seconds': 60,
                'health_check_timeout_ms': 5000,
                'metrics_retention_hours': 168,  # 7 days
                'availability_target': 99.9,
                'response_time_target_ms': 2000
            },
            'circuit_breaker': {
                'failure_threshold': 5,
                'recovery_timeout_seconds': 60,
                'half_open_max_calls': 3
            },
            'fallback': {
                'max_fallback_chain_length': 3,
                'cache_fallback_enabled': True,
                'static_fallback_enabled': True,
                'fallback_timeout_ms': 1000
            },
            'alerting': {
                'availability_threshold': 95.0,
                'response_time_threshold_ms': 5000,
                'error_rate_threshold': 10.0,
                'consecutive_failure_threshold': 3
            }
        }

    def register_source(self, source_name: str, health_check_func: Callable,
                       fallback_strategy: Optional[FallbackStrategy] = None):
        """Register a knowledge source for reliability monitoring"""

        # Initialize health tracking
        self.source_health[source_name] = SourceHealth(
            source_name=source_name,
            status=SourceStatus.UNKNOWN,
            last_check=datetime.now(),
            response_time_p95=0.0,
            availability_24h=100.0,
            error_rate_1h=0.0,
            consecutive_failures=0
        )

        # Initialize circuit breaker
        self.circuit_breakers[source_name] = CircuitBreaker(
            failure_threshold=self.config['circuit_breaker']['failure_threshold'],
            recovery_timeout=self.config['circuit_breaker']['recovery_timeout_seconds']
        )

        # Set up fallback strategy
        if fallback_strategy:
            self.fallback_strategies[source_name] = fallback_strategy

        # Initialize metrics history
        self.health_history[source_name] = []

        logger.info(f"Registered knowledge source for monitoring: {source_name}")

    async def execute_with_reliability(self, source_name: str, operation: Callable,
                                     *args, **kwargs) -> Any:
        """
        Execute operation with full reliability framework protection
        """
        start_time = time.time()

        try:
            # Check circuit breaker
            if source_name in self.circuit_breakers:
                circuit_breaker = self.circuit_breakers[source_name]
                if circuit_breaker.state == 'open':
                    logger.warning(f"Circuit breaker open for {source_name}, using fallback")
                    return await self._execute_fallback(source_name, operation, *args, **kwargs)

            # Execute with timeout
            timeout = self.config['monitoring']['health_check_timeout_ms'] / 1000
            result = await asyncio.wait_for(operation(*args, **kwargs), timeout=timeout)

            # Record successful execution
            response_time = (time.time() - start_time) * 1000
            await self._record_health_metric(source_name, response_time, True)

            return result

        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            await self._record_health_metric(
                source_name, response_time, False, FailureType.TIMEOUT
            )
            return await self._execute_fallback(source_name, operation, *args, **kwargs)

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            failure_type = self._classify_failure(e)
            await self._record_health_metric(
                source_name, response_time, False, failure_type, str(e)
            )

            # Try fallback
            return await self._execute_fallback(source_name, operation, *args, **kwargs)

    async def _execute_fallback(self, source_name: str, operation: Callable,
                              *args, **kwargs) -> Any:
        """Execute fallback strategy for failed source"""

        if source_name not in self.fallback_strategies:
            logger.error(f"No fallback strategy configured for {source_name}")
            raise Exception(f"Source {source_name} unavailable and no fallback configured")

        strategy = self.fallback_strategies[source_name]

        # Try fallback sources in priority order
        for fallback_source in strategy.fallback_sources:
            if fallback_source in self.source_health:
                health = self.source_health[fallback_source]

                # Skip unhealthy fallback sources
                if health.status == SourceStatus.UNHEALTHY:
                    continue

                try:
                    logger.info(f"Using fallback source {fallback_source} for {source_name}")

                    # Execute with shorter timeout for fallback
                    timeout = self.config['fallback']['fallback_timeout_ms'] / 1000
                    result = await asyncio.wait_for(operation(*args, **kwargs), timeout=timeout)

                    return result

                except Exception as e:
                    logger.warning(f"Fallback source {fallback_source} also failed: {e}")
                    continue

        # Try cache fallback if enabled
        if strategy.cache_fallback:
            cache_result = await self._try_cache_fallback(source_name, *args, **kwargs)
            if cache_result is not None:
                logger.info(f"Using cached fallback for {source_name}")
                return cache_result

        # Try static fallback if configured
        if strategy.static_fallback:
            logger.info(f"Using static fallback for {source_name}")
            return strategy.static_fallback

        # All fallbacks exhausted
        raise Exception(f"All fallback strategies exhausted for {source_name}")

    async def _try_cache_fallback(self, source_name: str, *args, **kwargs) -> Optional[Any]:
        """Try to get cached result as fallback"""
        # This would integrate with the caching system
        # For now, return None to indicate no cached result
        return None

    def _classify_failure(self, error: Exception) -> FailureType:
        """Classify failure type based on exception"""
        error_str = str(error).lower()

        if 'timeout' in error_str or 'timed out' in error_str:
            return FailureType.TIMEOUT
        elif 'connection' in error_str or 'network' in error_str:
            return FailureType.CONNECTION_ERROR
        elif 'auth' in error_str or 'unauthorized' in error_str:
            return FailureType.AUTHENTICATION_ERROR
        elif 'rate limit' in error_str or 'too many requests' in error_str:
            return FailureType.RATE_LIMIT_EXCEEDED
        elif 'quota' in error_str or 'exceeded' in error_str:
            return FailureType.QUOTA_EXCEEDED
        elif 'service unavailable' in error_str or '503' in error_str:
            return FailureType.SERVICE_UNAVAILABLE
        else:
            return FailureType.INVALID_RESPONSE

    async def _record_health_metric(self, source_name: str, response_time_ms: float,
                                  success: bool, error_type: Optional[FailureType] = None,
                                  error_message: Optional[str] = None):
        """Record health metric for a source"""

        metric = HealthMetric(
            timestamp=datetime.now(),
            response_time_ms=response_time_ms,
            success=success,
            error_type=error_type,
            error_message=error_message
        )

        # Add to history
        if source_name not in self.health_history:
            self.health_history[source_name] = []

        self.health_history[source_name].append(metric)

        # Maintain history size
        max_metrics = self.config['monitoring']['metrics_retention_hours'] * 60  # Assume 1 check per minute
        if len(self.health_history[source_name]) > max_metrics:
            self.health_history[source_name] = self.health_history[source_name][-max_metrics:]

        # Update source health
        await self._update_source_health(source_name)

    async def _update_source_health(self, source_name: str):
        """Update overall health status for a source"""

        if source_name not in self.source_health or source_name not in self.health_history:
            return

        health = self.source_health[source_name]
        metrics = self.health_history[source_name]

        if not metrics:
            return

        # Calculate metrics for different time windows
        now = datetime.now()

        # Last 24 hours
        metrics_24h = [m for m in metrics if (now - m.timestamp).total_seconds() <= 86400]

        # Last 1 hour
        metrics_1h = [m for m in metrics if (now - m.timestamp).total_seconds() <= 3600]

        # Calculate availability (24h)
        if metrics_24h:
            successful_24h = sum(1 for m in metrics_24h if m.success)
            health.availability_24h = (successful_24h / len(metrics_24h)) * 100
        else:
            health.availability_24h = 100.0

        # Calculate error rate (1h)
        if metrics_1h:
            failed_1h = sum(1 for m in metrics_1h if not m.success)
            health.error_rate_1h = (failed_1h / len(metrics_1h)) * 100
        else:
            health.error_rate_1h = 0.0

        # Calculate response time percentiles
        successful_metrics = [m for m in metrics if m.success]
        if successful_metrics:
            response_times = [m.response_time_ms for m in successful_metrics]
            health.response_time_p95 = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        else:
            health.response_time_p95 = float('inf')

        # Update consecutive failures
        latest_metrics = sorted(metrics, key=lambda x: x.timestamp, reverse=True)[:10]
        consecutive_failures = 0
        for metric in latest_metrics:
            if not metric.success:
                consecutive_failures += 1
            else:
                break
        health.consecutive_failures = consecutive_failures

        # Update last success/failure times
        latest_success = next((m for m in reversed(metrics) if m.success), None)
        latest_failure = next((m for m in reversed(metrics) if not m.success), None)

        if latest_success:
            health.last_success = latest_success.timestamp
        if latest_failure:
            health.last_failure = latest_failure.timestamp

        # Calculate overall health score
        health.health_score = self._calculate_health_score(health)

        # Update status based on health metrics
        health.status = self._determine_health_status(health)
        health.last_check = now

        # Trigger alerts if necessary
        await self._check_alert_conditions(source_name, health)

    def _calculate_health_score(self, health: SourceHealth) -> float:
        """Calculate overall health score (0-100)"""

        # Base score from availability
        availability_score = health.availability_24h

        # Penalty for high error rates
        error_penalty = min(health.error_rate_1h * 2, 50)  # Max 50 point penalty

        # Penalty for slow response times
        target_response_time = self.config['monitoring']['response_time_target_ms']
        if health.response_time_p95 > target_response_time:
            response_penalty = min((health.response_time_p95 / target_response_time - 1) * 20, 30)
        else:
            response_penalty = 0

        # Penalty for consecutive failures
        failure_penalty = min(health.consecutive_failures * 5, 25)

        # Calculate final score
        final_score = availability_score - error_penalty - response_penalty - failure_penalty
        return max(0, min(100, final_score))

    def _determine_health_status(self, health: SourceHealth) -> SourceStatus:
        """Determine health status based on metrics"""

        if health.health_score >= 95:
            return SourceStatus.HEALTHY
        elif health.health_score >= 80:
            return SourceStatus.DEGRADED
        else:
            return SourceStatus.UNHEALTHY

    async def _check_alert_conditions(self, source_name: str, health: SourceHealth):
        """Check if alert conditions are met and trigger alerts"""

        alerts = []

        # Availability alert
        if health.availability_24h < self.config['alerting']['availability_threshold']:
            alerts.append({
                'type': 'availability',
                'severity': 'high',
                'message': f"{source_name} availability ({health.availability_24h:.1f}%) below threshold",
                'metric': health.availability_24h
            })

        # Response time alert
        if health.response_time_p95 > self.config['alerting']['response_time_threshold_ms']:
            alerts.append({
                'type': 'response_time',
                'severity': 'medium',
                'message': f"{source_name} response time ({health.response_time_p95:.0f}ms) above threshold",
                'metric': health.response_time_p95
            })

        # Error rate alert
        if health.error_rate_1h > self.config['alerting']['error_rate_threshold']:
            alerts.append({
                'type': 'error_rate',
                'severity': 'high',
                'message': f"{source_name} error rate ({health.error_rate_1h:.1f}%) above threshold",
                'metric': health.error_rate_1h
            })

        # Consecutive failures alert
        if health.consecutive_failures >= self.config['alerting']['consecutive_failure_threshold']:
            alerts.append({
                'type': 'consecutive_failures',
                'severity': 'critical',
                'message': f"{source_name} has {health.consecutive_failures} consecutive failures",
                'metric': health.consecutive_failures
            })

        # Send alerts
        for alert in alerts:
            await self._send_alert(source_name, alert)

    async def _send_alert(self, source_name: str, alert: Dict[str, Any]):
        """Send alert to registered handlers"""

        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'source': source_name,
            **alert
        }

        for handler in self.alert_handlers:
            try:
                await handler(alert_data)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")

        logger.warning(f"ALERT: {alert['message']}")

    def add_alert_handler(self, handler: Callable):
        """Add alert handler function"""
        self.alert_handlers.append(handler)

    async def _health_monitoring_loop(self):
        """Background loop for continuous health monitoring"""

        while True:
            try:
                # Perform health checks for all registered sources
                for source_name in self.source_health.keys():
                    await self._perform_health_check(source_name)

                # Sleep until next check
                await asyncio.sleep(self.config['monitoring']['check_interval_seconds'])

            except Exception as e:
                logger.error(f"Health monitoring loop error: {e}")
                await asyncio.sleep(60)  # Retry after 1 minute

    async def _perform_health_check(self, source_name: str):
        """Perform health check for a specific source"""

        try:
            # Simple connectivity test (this would be customized per source)
            start_time = time.time()

            # Simulate health check (in real implementation, this would test actual connectivity)
            await asyncio.sleep(0.1)  # Simulate network call

            response_time = (time.time() - start_time) * 1000

            # Record successful health check
            await self._record_health_metric(source_name, response_time, True)

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            failure_type = self._classify_failure(e)
            await self._record_health_metric(source_name, response_time, False, failure_type, str(e))

    async def _health_analysis_loop(self):
        """Background loop for health analysis and optimization"""

        while True:
            try:
                # Analyze health trends
                await self._analyze_health_trends()

                # Optimize fallback strategies
                await self._optimize_fallback_strategies()

                # Clean up old metrics
                await self._cleanup_old_metrics()

                # Sleep for 5 minutes
                await asyncio.sleep(300)

            except Exception as e:
                logger.error(f"Health analysis loop error: {e}")
                await asyncio.sleep(300)

    async def _analyze_health_trends(self):
        """Analyze health trends and patterns"""

        for source_name, health in self.source_health.items():
            if source_name not in self.health_history:
                continue

            metrics = self.health_history[source_name]
            if len(metrics) < 10:  # Need sufficient data
                continue

            # Analyze response time trends
            recent_metrics = metrics[-60:]  # Last hour
            if recent_metrics:
                response_times = [m.response_time_ms for m in recent_metrics if m.success]
                if len(response_times) > 5:
                    avg_response_time = statistics.mean(response_times)

                    # Check for degrading performance
                    if avg_response_time > health.response_time_p95 * 1.5:
                        logger.warning(f"Degrading performance detected for {source_name}")

    async def _optimize_fallback_strategies(self):
        """Optimize fallback strategies based on performance data"""

        for source_name, strategy in self.fallback_strategies.items():
            # Analyze fallback source performance
            fallback_performance = {}

            for fallback_source in strategy.fallback_sources:
                if fallback_source in self.source_health:
                    health = self.source_health[fallback_source]
                    fallback_performance[fallback_source] = health.health_score

            # Reorder fallback sources by performance
            if fallback_performance:
                sorted_fallbacks = sorted(
                    fallback_performance.items(),
                    key=lambda x: x[1],
                    reverse=True
                )

                new_order = [source for source, _ in sorted_fallbacks]
                if new_order != strategy.fallback_sources:
                    strategy.fallback_sources = new_order
                    logger.info(f"Optimized fallback order for {source_name}: {new_order}")

    async def _cleanup_old_metrics(self):
        """Clean up old health metrics to prevent memory growth"""

        cutoff_time = datetime.now() - timedelta(
            hours=self.config['monitoring']['metrics_retention_hours']
        )

        for source_name in self.health_history:
            old_count = len(self.health_history[source_name])
            self.health_history[source_name] = [
                m for m in self.health_history[source_name]
                if m.timestamp > cutoff_time
            ]
            new_count = len(self.health_history[source_name])

            if old_count != new_count:
                logger.debug(f"Cleaned up {old_count - new_count} old metrics for {source_name}")

    async def get_reliability_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive reliability dashboard data"""

        dashboard = {
            'overall_health': self._calculate_overall_health(),
            'sources': {},
            'alerts': {
                'active_alerts': await self._get_active_alerts(),
                'alert_history_24h': await self._get_alert_history(24)
            },
            'performance_summary': await self._get_performance_summary(),
            'availability_sla': self._calculate_sla_compliance(),
            'last_updated': datetime.now().isoformat()
        }

        # Add individual source data
        for source_name, health in self.source_health.items():
            circuit_breaker = self.circuit_breakers.get(source_name)

            dashboard['sources'][source_name] = {
                'status': health.status.value,
                'health_score': health.health_score,
                'availability_24h': health.availability_24h,
                'response_time_p95': health.response_time_p95,
                'error_rate_1h': health.error_rate_1h,
                'consecutive_failures': health.consecutive_failures,
                'last_success': health.last_success.isoformat() if health.last_success else None,
                'last_failure': health.last_failure.isoformat() if health.last_failure else None,
                'circuit_breaker_state': circuit_breaker.state if circuit_breaker else 'disabled'
            }

        return dashboard

    def _calculate_overall_health(self) -> float:
        """Calculate overall system health score"""
        if not self.source_health:
            return 100.0

        health_scores = [health.health_score for health in self.source_health.values()]
        return statistics.mean(health_scores)

    async def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get currently active alerts"""
        # This would maintain a list of active alerts
        # For now, return empty list
        return []

    async def _get_alert_history(self, hours: int) -> List[Dict[str, Any]]:
        """Get alert history for specified time period"""
        # This would maintain alert history
        # For now, return empty list
        return []

    async def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary across all sources"""
        if not self.source_health:
            return {}

        return {
            'avg_availability': statistics.mean([h.availability_24h for h in self.source_health.values()]),
            'avg_response_time': statistics.mean([h.response_time_p95 for h in self.source_health.values()]),
            'avg_error_rate': statistics.mean([h.error_rate_1h for h in self.source_health.values()]),
            'total_sources': len(self.source_health),
            'healthy_sources': len([h for h in self.source_health.values() if h.status == SourceStatus.HEALTHY]),
            'degraded_sources': len([h for h in self.source_health.values() if h.status == SourceStatus.DEGRADED]),
            'unhealthy_sources': len([h for h in self.source_health.values() if h.status == SourceStatus.UNHEALTHY])
        }

    def _calculate_sla_compliance(self) -> Dict[str, float]:
        """Calculate SLA compliance metrics"""
        target_availability = self.config['monitoring']['availability_target']

        compliance = {}
        for source_name, health in self.source_health.items():
            compliance[source_name] = min(100.0, (health.availability_24h / target_availability) * 100)

        return compliance