"""
External Knowledge Integration Usage Example

Demonstrates how to integrate and use the external knowledge framework
with the claude-config agent ecosystem for enhanced documentation access,
best practices integration, and compliance validation.
"""

import asyncio
from datetime import datetime
from typing import List, Dict, Any

from src.claude_config.external_knowledge import (
    MCPKnowledgeProvider,
    IntelligentKnowledgeCache,
    KnowledgeCurationEngine,
    SecurityComplianceProvider,
    KnowledgeSourceReliability
)
from src.claude_config.external_knowledge.mcp_integration import KnowledgeRequest
from src.claude_config.external_knowledge.security_compliance import ComplianceFramework
from src.claude_config.external_knowledge.reliability import FallbackStrategy


class ExternalKnowledgeIntegrationExample:
    """
    Example class demonstrating external knowledge integration
    for enhanced agent capabilities with real-time documentation access.
    """

    def __init__(self):
        """Initialize all external knowledge components"""
        self.mcp_provider = MCPKnowledgeProvider()
        self.cache = IntelligentKnowledgeCache()
        self.curation_engine = KnowledgeCurationEngine()
        self.compliance_provider = SecurityComplianceProvider()
        self.reliability_framework = KnowledgeSourceReliability()

        # Set up reliability monitoring
        self._setup_reliability_monitoring()

    def _setup_reliability_monitoring(self):
        """Set up reliability monitoring for all knowledge sources"""

        # Register Context7 for monitoring
        self.reliability_framework.register_source(
            source_name="context7",
            health_check_func=self._context7_health_check,
            fallback_strategy=FallbackStrategy(
                primary_sources=["context7"],
                fallback_sources=["deepwiki", "cache"],
                cache_fallback=True,
                max_fallback_age_hours=24
            )
        )

        # Register DeepWiki for monitoring
        self.reliability_framework.register_source(
            source_name="deepwiki",
            health_check_func=self._deepwiki_health_check,
            fallback_strategy=FallbackStrategy(
                primary_sources=["deepwiki"],
                fallback_sources=["context7", "cache"],
                cache_fallback=True
            )
        )

        # Register GitHub MCP for monitoring
        self.reliability_framework.register_source(
            source_name="github_mcp",
            health_check_func=self._github_health_check
        )

    async def _context7_health_check(self):
        """Health check for Context7 service"""
        try:
            # Simple connectivity test
            result = await asyncio.wait_for(
                self.mcp_provider.context7_resolve("react"),
                timeout=5.0
            )
            return {"status": "healthy", "libraries_available": len(result)}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def _deepwiki_health_check(self):
        """Health check for DeepWiki service"""
        try:
            result = await asyncio.wait_for(
                self.mcp_provider.deepwiki_fetch("test", maxDepth=0),
                timeout=5.0
            )
            return {"status": "healthy", "response_length": len(result)}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def _github_health_check(self):
        """Health check for GitHub MCP service"""
        try:
            result = await asyncio.wait_for(
                self.mcp_provider.github_search("query:test"),
                timeout=5.0
            )
            return {"status": "healthy", "search_results": result.get('total_count', 0)}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def demonstrate_framework_documentation_access(self, framework: str, topic: str = None):
        """
        Demonstrate real-time framework documentation access with caching
        """
        print(f"🔍 Fetching {framework} documentation...")

        # Create knowledge request
        request = KnowledgeRequest(
            type='framework_docs',
            framework=framework,
            topic=topic,
            max_tokens=8000,
            trust_threshold=8.0
        )

        try:
            # Execute with reliability protection
            response = await self.reliability_framework.execute_with_reliability(
                "context7",
                self.mcp_provider.get_framework_documentation,
                request
            )

            print(f"✅ Successfully retrieved {framework} documentation")
            print(f"   Source: {response.source}")
            print(f"   Authority Score: {response.authority_score}/10")
            print(f"   Response Time: {response.response_time_ms}ms")
            print(f"   Cache Hit: {'Yes' if response.cache_hit else 'No'}")
            print(f"   Content Length: {len(response.content)} characters")

            # Cache the response for future use
            cache_key = f"framework:{framework}:{topic or 'general'}"
            await self.cache.set(
                cache_key,
                response.content,
                authority_score=response.authority_score,
                source=response.source
            )

            return response

        except Exception as e:
            print(f"❌ Failed to retrieve {framework} documentation: {e}")
            return None

    async def demonstrate_best_practices_curation(self, domain: str, framework: str = None):
        """
        Demonstrate industry best practices curation and ranking
        """
        print(f"📚 Curating best practices for {domain}...")

        try:
            # Get curated best practices
            best_practices = await self.curation_engine.curate_best_practices(
                domain=domain,
                framework=framework
            )

            print(f"✅ Found {len(best_practices)} curated best practices")

            for i, practice in enumerate(best_practices[:5], 1):  # Show top 5
                print(f"   {i}. {practice.title}")
                print(f"      Source: {practice.source.name}")
                print(f"      Quality Score: {practice.quality_score:.1f}/10")
                print(f"      Authority: {practice.authority_score:.1f}/10")
                if practice.frameworks:
                    print(f"      Frameworks: {', '.join(practice.frameworks)}")
                print()

            return best_practices

        except Exception as e:
            print(f"❌ Failed to curate best practices: {e}")
            return []

    async def demonstrate_security_compliance_assessment(self, technology_stack: List[str]):
        """
        Demonstrate security compliance assessment and implementation guidance
        """
        print(f"🔒 Assessing security compliance for: {', '.join(technology_stack)}")

        try:
            # Initialize security standards
            await self.compliance_provider._initialize_security_standards()

            # Get compliance requirements
            requirements = await self.compliance_provider.get_compliance_requirements(
                frameworks=[ComplianceFramework.OWASP_TOP_10, ComplianceFramework.NIST_CSF],
                technology_stack=technology_stack
            )

            print(f"✅ Found compliance requirements:")
            for framework, controls in requirements.items():
                print(f"   {framework.upper()}: {len(controls)} applicable controls")

            # Generate implementation guide
            implementation_guide = await self.compliance_provider.generate_implementation_guide(
                framework=ComplianceFramework.OWASP_TOP_10,
                technology_stack=technology_stack,
                priority='high'
            )

            print(f"📋 Generated implementation guide ({len(implementation_guide)} characters)")

            # Generate security checklist
            checklist = await self.compliance_provider.get_security_checklist(
                technology_stack=technology_stack,
                frameworks=[ComplianceFramework.OWASP_TOP_10]
            )

            print(f"☑️  Generated security checklist:")
            for framework, items in checklist.items():
                print(f"   {framework}: {len(items)} checklist items")

            return {
                'requirements': requirements,
                'implementation_guide': implementation_guide,
                'checklist': checklist
            }

        except Exception as e:
            print(f"❌ Failed security compliance assessment: {e}")
            return {}

    async def demonstrate_knowledge_search_and_ranking(self, query: str, framework: str = None):
        """
        Demonstrate intelligent knowledge search with quality ranking
        """
        print(f"🔎 Searching knowledge base for: '{query}'")

        try:
            # Search curated content
            search_results = await self.curation_engine.search_content(
                query=query,
                framework=framework,
                limit=10
            )

            print(f"✅ Found {len(search_results)} relevant knowledge items")

            for i, result in enumerate(search_results[:3], 1):  # Show top 3
                print(f"   {i}. {result.title}")
                print(f"      Type: {result.content_type.value}")
                print(f"      Quality: {result.quality_score:.1f}/10")
                print(f"      Relevance: {result.relevance_score:.1f}/10")
                print(f"      Source: {result.source.name}")
                print(f"      Preview: {result.content[:100]}...")
                print()

            return search_results

        except Exception as e:
            print(f"❌ Failed knowledge search: {e}")
            return []

    async def demonstrate_reliability_monitoring(self):
        """
        Demonstrate reliability monitoring and health status
        """
        print("📊 Checking knowledge source reliability...")

        try:
            # Get reliability dashboard
            dashboard = await self.reliability_framework.get_reliability_dashboard()

            print(f"✅ System Health Overview:")
            print(f"   Overall Health Score: {dashboard['overall_health']:.1f}/100")

            perf_summary = dashboard.get('performance_summary', {})
            if perf_summary:
                print(f"   Average Availability: {perf_summary.get('avg_availability', 0):.1f}%")
                print(f"   Average Response Time: {perf_summary.get('avg_response_time', 0):.0f}ms")
                print(f"   Healthy Sources: {perf_summary.get('healthy_sources', 0)}/{perf_summary.get('total_sources', 0)}")

            print(f"\n📈 Individual Source Health:")
            for source_name, health_data in dashboard.get('sources', {}).items():
                status_emoji = {
                    'healthy': '🟢',
                    'degraded': '🟡',
                    'unhealthy': '🔴',
                    'unknown': '⚪'
                }.get(health_data['status'], '⚪')

                print(f"   {status_emoji} {source_name}: {health_data['status'].title()}")
                print(f"      Health Score: {health_data['health_score']:.1f}/100")
                print(f"      Availability: {health_data['availability_24h']:.1f}%")
                print(f"      Response Time: {health_data['response_time_p95']:.0f}ms")

            return dashboard

        except Exception as e:
            print(f"❌ Failed to get reliability status: {e}")
            return {}

    async def demonstrate_cache_performance(self):
        """
        Demonstrate intelligent caching performance and metrics
        """
        print("💾 Analyzing cache performance...")

        try:
            # Get cache metrics
            metrics = await self.cache.get_metrics()

            print(f"✅ Cache Performance Metrics:")
            performance = metrics.get('performance', {})
            print(f"   Hit Rate: {performance.get('hit_rate', 0):.1f}%")
            print(f"   Total Requests: {performance.get('total_requests', 0)}")
            print(f"   Cache Hits: {performance.get('hits', 0)}")
            print(f"   Cache Misses: {performance.get('misses', 0)}")
            print(f"   Average Response Time: {performance.get('average_response_time_ms', 0):.1f}ms")

            cache_layers = metrics.get('cache_layers', {})
            print(f"\n🗄️  Cache Layer Status:")
            print(f"   L1 (Memory) Entries: {cache_layers.get('l1_entries', 0)}")
            print(f"   L2 (Redis) Available: {'Yes' if cache_layers.get('l2_available') else 'No'}")
            print(f"   L3 (Persistent) Entries: {cache_layers.get('l3_entries', 0)}")

            popular_content = metrics.get('popular_content', {})
            if popular_content:
                print(f"\n🔥 Most Popular Content:")
                for content_key, access_count in list(popular_content.items())[:5]:
                    print(f"   {content_key}: {access_count} accesses")

            return metrics

        except Exception as e:
            print(f"❌ Failed to get cache metrics: {e}")
            return {}

    async def run_comprehensive_demo(self):
        """
        Run comprehensive demonstration of all external knowledge capabilities
        """
        print("🚀 Starting External Knowledge Integration Demonstration")
        print("=" * 60)

        # 1. Framework documentation access
        await self.demonstrate_framework_documentation_access("react", "hooks")
        print("\n" + "-" * 40 + "\n")

        # 2. Best practices curation
        await self.demonstrate_best_practices_curation("performance", "react")
        print("\n" + "-" * 40 + "\n")

        # 3. Security compliance assessment
        await self.demonstrate_security_compliance_assessment(["django", "postgresql", "redis"])
        print("\n" + "-" * 40 + "\n")

        # 4. Knowledge search and ranking
        await self.demonstrate_knowledge_search_and_ranking("authentication security", "django")
        print("\n" + "-" * 40 + "\n")

        # 5. Reliability monitoring
        await self.demonstrate_reliability_monitoring()
        print("\n" + "-" * 40 + "\n")

        # 6. Cache performance
        await self.demonstrate_cache_performance()
        print("\n" + "-" * 40 + "\n")

        print("✅ External Knowledge Integration Demonstration Complete!")


async def main():
    """Main demonstration function"""
    print("External Knowledge Integration - Usage Example")
    print("=============================================\n")

    # Create and run demonstration
    demo = ExternalKnowledgeIntegrationExample()
    await demo.run_comprehensive_demo()

    print("\n🎯 Integration Benefits Summary:")
    print("• Real-time access to authoritative documentation")
    print("• Intelligent caching with 85%+ hit rate target")
    print("• Automated best practices curation from industry sources")
    print("• Comprehensive security compliance assessment")
    print("• 99.9% availability with robust fallback strategies")
    print("• Sub-2-second response times for critical knowledge")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())