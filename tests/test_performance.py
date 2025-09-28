"""
Performance Testing for Large Configurations

Tests system performance, memory usage, and scalability with large configurations.
"""

import pytest
import tempfile
import time
import psutil
import os
import threading
import concurrent.futures
from pathlib import Path
from unittest.mock import patch
import yaml
import gc
import resource
from typing import List, Dict, Any

from src.claude_config.mcp_processor import MCPProcessor
from src.claude_config.composer import AgentComposer
from src.claude_config.validator import ConfigValidator


class PerformanceProfiler:
    """Helper class for performance profiling."""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.start_time = None
        self.start_memory = None
        self.start_cpu_time = None
        
    def start(self):
        """Start profiling."""
        gc.collect()  # Force garbage collection
        self.start_time = time.time()
        self.start_memory = self.process.memory_info().rss
        self.start_cpu_time = self.process.cpu_times().user
        
    def stop(self):
        """Stop profiling and return metrics."""
        end_time = time.time()
        end_memory = self.process.memory_info().rss
        end_cpu_time = self.process.cpu_times().user
        
        return {
            "wall_time": end_time - self.start_time,
            "memory_delta": end_memory - self.start_memory,
            "memory_peak": self.process.memory_info().rss,
            "cpu_time": end_cpu_time - self.start_cpu_time,
            "memory_percent": self.process.memory_percent()
        }


class TestMCPPerformance:
    """Test MCP processing performance with large configurations."""

    @pytest.fixture
    def large_mcp_dataset(self):
        """Create large dataset of MCP server configurations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Generate 100 MCP server configurations
            for i in range(100):
                config = {
                    "name": f"performance-server-{i:03d}",
                    "display_name": f"Performance Test Server {i}",
                    "description": f"Performance testing MCP server number {i} with detailed configuration",
                    "category": "development" if i % 3 == 0 else "productivity" if i % 3 == 1 else "research",
                    "server": {
                        "command": "npx" if i % 2 == 0 else "node",
                        "args": ["-y", f"@test/server-{i}", "--port", str(3000 + i)],
                        "timeout": 30 + (i % 60)
                    },
                    "environment": {
                        "variables": {
                            f"API_TOKEN_{j}": {
                                "source": "env",
                                "variable": f"PERF_API_TOKEN_{i}_{j}",
                                "required": j < 3,
                                "description": f"API token {j} for server {i}"
                            } for j in range(20)  # 20 env vars per server
                        },
                        "secrets": [f"API_TOKEN_{j}" for j in range(5)],  # First 5 are secrets
                        "validation": {
                            "required": [f"API_TOKEN_{j}" for j in range(3)],
                            "optional": [f"API_TOKEN_{j}" for j in range(3, 20)]
                        }
                    },
                    "metadata": {
                        "version": f"{i // 10}.{i % 10}.0",
                        "tags": [f"tag-{j}" for j in range(10)],
                        "personas": {
                            "suitable_for": ["python-engineer", "qa-engineer", "data-engineer"],
                            "enhancement_areas": ["testing", "performance", "scalability"],
                            "use_cases": [f"Use case {j} for server {i}" for j in range(5)]
                        },
                        "documentation": {
                            "url": f"https://docs.example.com/server-{i}",
                            "examples": [f"example{j}.py" for j in range(3)]
                        }
                    },
                    "security": {
                        "trust_level": "trusted" if i % 4 == 0 else "experimental",
                        "permissions": [f"network.server{i}.com", f"file.read./data/{i}"],
                        "data_access": [f"dataset-{i}", f"logs-{i}"],
                        "network_access": i % 2 == 0,
                        "sandboxed": i % 3 == 0
                    },
                    "development": {
                        "status": "stable" if i % 5 == 0 else "experimental",
                        "last_tested": f"2024-01-{(i % 28) + 1:02d}",
                        "known_issues": [f"Issue {j} for server {i}" for j in range(i % 3)],
                        "dependencies": ["node.js", "npm"] + [f"dep-{j}" for j in range(i % 5)],
                        "testing": {
                            "unit_tests": i % 2 == 0,
                            "integration_tests": i % 3 == 0,
                            "test_coverage": 80 + (i % 20)
                        }
                    }
                }

                with open(mcp_dir / f"performance-server-{i:03d}.yaml", 'w') as f:
                    yaml.dump(config, f)

            yield data_dir

    def test_mcp_loading_performance(self, large_mcp_dataset):
        """Test performance of loading many MCP configurations."""
        profiler = PerformanceProfiler()
        profiler.start()
        
        processor = MCPProcessor(large_mcp_dataset)
        
        # Load all servers
        all_servers = processor.load_all_mcp_servers()
        
        metrics = profiler.stop()
        
        # Verify all servers loaded
        assert len(all_servers) == 100
        
        # Performance assertions
        assert metrics["wall_time"] < 10.0, f"Loading took {metrics['wall_time']:.2f}s, expected < 10s"
        assert metrics["memory_delta"] < 100 * 1024 * 1024, f"Memory increase {metrics['memory_delta'] / 1024 / 1024:.2f}MB, expected < 100MB"
        
        print(f"Loading Performance: {metrics['wall_time']:.2f}s, {metrics['memory_delta'] / 1024 / 1024:.2f}MB")

    def test_mcp_validation_performance(self, large_mcp_dataset):
        """Test performance of validating many MCP configurations."""
        # Set up environment variables for validation
        env_vars = {}
        for i in range(100):
            for j in range(3):  # Only required variables
                env_vars[f"PERF_API_TOKEN_{i}_{j}"] = f"token_{i}_{j}"

        with patch.dict(os.environ, env_vars):
            profiler = PerformanceProfiler()
            profiler.start()
            
            processor = MCPProcessor(large_mcp_dataset)
            
            # Validate all servers
            validation_results = processor.validate_all_mcp_servers()
            
            metrics = profiler.stop()
            
            # Verify validation results
            assert len(validation_results) == 100
            valid_count = sum(1 for result in validation_results.values() if result.is_valid)
            assert valid_count >= 90, f"Only {valid_count}/100 servers validated successfully"
            
            # Performance assertions
            assert metrics["wall_time"] < 30.0, f"Validation took {metrics['wall_time']:.2f}s, expected < 30s"
            assert metrics["memory_delta"] < 200 * 1024 * 1024, f"Memory increase {metrics['memory_delta'] / 1024 / 1024:.2f}MB, expected < 200MB"
            
            print(f"Validation Performance: {metrics['wall_time']:.2f}s, {metrics['memory_delta'] / 1024 / 1024:.2f}MB")

    def test_mcp_processing_performance(self, large_mcp_dataset):
        """Test performance of processing many MCP configurations for Claude Code."""
        # Set up environment
        env_vars = {}
        for i in range(100):
            for j in range(20):
                env_vars[f"PERF_API_TOKEN_{i}_{j}"] = f"token_{i}_{j}"

        with patch.dict(os.environ, env_vars):
            profiler = PerformanceProfiler()
            profiler.start()
            
            processor = MCPProcessor(large_mcp_dataset)
            
            # Process all servers for Claude Code
            claude_configs = processor.process_all_for_claude_code()
            
            metrics = profiler.stop()
            
            # Verify processing results
            assert len(claude_configs) == 100
            
            # Verify structure of processed configs
            for server_name, config in claude_configs.items():
                assert "command" in config
                assert "env" in config
                assert "_metadata" in config
            
            # Performance assertions
            assert metrics["wall_time"] < 60.0, f"Processing took {metrics['wall_time']:.2f}s, expected < 60s"
            assert metrics["memory_delta"] < 300 * 1024 * 1024, f"Memory increase {metrics['memory_delta'] / 1024 / 1024:.2f}MB, expected < 300MB"
            
            print(f"Processing Performance: {metrics['wall_time']:.2f}s, {metrics['memory_delta'] / 1024 / 1024:.2f}MB")

    def test_concurrent_mcp_processing(self, large_mcp_dataset):
        """Test concurrent processing of MCP configurations."""
        env_vars = {}
        for i in range(100):
            for j in range(3):
                env_vars[f"PERF_API_TOKEN_{i}_{j}"] = f"token_{i}_{j}"

        def process_batch(batch_start, batch_size):
            """Process a batch of servers."""
            with patch.dict(os.environ, env_vars):
                processor = MCPProcessor(large_mcp_dataset)
                
                results = {}
                for i in range(batch_start, min(batch_start + batch_size, 100)):
                    server_name = f"performance-server-{i:03d}"
                    try:
                        server_def = processor.load_mcp_server(server_name)
                        claude_config = processor.process_for_claude_code(server_def)
                        results[server_name] = claude_config
                    except Exception as e:
                        results[server_name] = {"error": str(e)}
                
                return results

        profiler = PerformanceProfiler()
        profiler.start()
        
        # Process in parallel batches
        batch_size = 25
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(process_batch, i, batch_size)
                for i in range(0, 100, batch_size)
            ]
            
            all_results = {}
            for future in concurrent.futures.as_completed(futures):
                batch_results = future.result()
                all_results.update(batch_results)
        
        metrics = profiler.stop()
        
        # Verify all servers processed
        assert len(all_results) == 100
        
        # Count successful processing
        success_count = sum(1 for result in all_results.values() if "error" not in result)
        assert success_count >= 90, f"Only {success_count}/100 servers processed successfully"
        
        # Performance should be better than sequential
        assert metrics["wall_time"] < 45.0, f"Concurrent processing took {metrics['wall_time']:.2f}s, expected < 45s"
        
        print(f"Concurrent Processing Performance: {metrics['wall_time']:.2f}s, {success_count}/100 successful")


class TestAgentComposerPerformance:
    """Test agent composition performance with large datasets."""

    @pytest.fixture
    def large_agent_dataset(self):
        """Create large dataset of agent configurations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            
            # Create directory structure
            personas_dir = data_dir / "data/personas"
            traits_dir = data_dir / "data/traits"
            templates_dir = data_dir / "src/claude_config/templates"
            
            personas_dir.mkdir(parents=True)
            (traits_dir / "coordination").mkdir(parents=True)
            (traits_dir / "tools").mkdir(parents=True)
            (traits_dir / "enhancement").mkdir(parents=True)
            templates_dir.mkdir(parents=True)

            # Create 50 agent configurations
            for i in range(50):
                agent_config = {
                    "name": f"perf-agent-{i:02d}",
                    "display_name": f"Performance Agent {i}",
                    "description": f"Performance testing agent {i} with comprehensive configuration",
                    "model": "sonnet" if i % 3 == 0 else "haiku" if i % 3 == 1 else "opus",
                    "expertise": [f"Expertise {j}" for j in range(10)],
                    "responsibilities": [f"Responsibility {j}" for j in range(8)],
                    "imports": {
                        "coordination": [f"coord-trait-{j % 5}" for j in range(3)],
                        "tools": [f"tools-trait-{j % 3}" for j in range(2)],
                        "enhancement": [f"enhancement-trait-{j % 2}" for j in range(1)]
                    },
                    "context_priming": f"Performance agent {i} mindset with detailed context and extensive background information for testing",
                    "proactive_triggers": {
                        "file_patterns": [f"*.{ext}" for ext in ["py", "js", "ts", "java", "cpp"]],
                        "project_indicators": [f"framework-{j}" for j in range(5)]
                    },
                    "implementation_patterns": [f"Pattern {j} for agent {i}" for j in range(10)],
                    "professional_standards": [f"Standard {j}" for j in range(8)],
                    "integration_guidelines": [f"Guideline {j}" for j in range(6)],
                    "performance_benchmarks": [f"Benchmark {j}: < {100 + j * 10}ms" for j in range(5)],
                    "troubleshooting_guides": [f"Troubleshooting guide {j}" for j in range(4)],
                    "tool_configurations": [f"config-{j}.yaml" for j in range(3)]
                }
                
                with open(personas_dir / f"perf-agent-{i:02d}.yaml", 'w') as f:
                    yaml.dump(agent_config, f)

            # Create trait files
            trait_configs = {
                "coordination": [
                    (f"coord-trait-{i}.yaml", {
                        "name": f"coord_trait_{i}",
                        "category": "coordination",
                        "description": f"Coordination trait {i}",
                        "implementation": {
                            "patterns": [f"Pattern {j}" for j in range(5)],
                            "protocols": [f"Protocol {j}" for j in range(3)]
                        }
                    }) for i in range(5)
                ],
                "tools": [
                    (f"tools-trait-{i}.yaml", {
                        "name": f"tools_trait_{i}",
                        "category": "tools",
                        "description": f"Tools trait {i}",
                        "implementation": {
                            "frameworks": [f"Framework {j}" for j in range(8)],
                            "tools": [f"Tool {j}" for j in range(12)]
                        }
                    }) for i in range(3)
                ],
                "enhancement": [
                    (f"enhancement-trait-{i}.yaml", {
                        "name": f"enhancement_trait_{i}",
                        "category": "enhancement",
                        "description": f"Enhancement trait {i}",
                        "implementation": {
                            "optimizations": [f"Optimization {j}" for j in range(6)],
                            "enhancements": [f"Enhancement {j}" for j in range(4)]
                        }
                    }) for i in range(2)
                ]
            }
            
            for category, traits in trait_configs.items():
                for filename, config in traits:
                    with open(traits_dir / category / filename, 'w') as f:
                        yaml.dump(config, f)

            # Create template
            template_content = """# {{ agent.display_name }}

{{ agent.description }}

## Model: {{ agent.model }}

## Expertise
{% for expertise in agent.expertise %}
- {{ expertise }}
{% endfor %}

## Responsibilities
{% for responsibility in agent.responsibilities %}
- {{ responsibility }}
{% endfor %}

{% if traits %}
## Imported Traits
{% for category, trait_list in traits.items() %}
### {{ category|title }}
{% for trait in trait_list %}
#### {{ trait.name }}
{{ trait.description }}

{% if trait.implementation %}
{% for key, value in trait.implementation.items() %}
**{{ key|title }}:**
{% if value is iterable and value is not string %}
{% for item in value %}
- {{ item }}
{% endfor %}
{% else %}
- {{ value }}
{% endif %}
{% endfor %}
{% endif %}
{% endfor %}
{% endfor %}
{% endif %}

## Context Priming
{{ agent.context_priming }}

## Proactive Triggers
{% if agent.proactive_triggers %}
### File Patterns
{% for pattern in agent.proactive_triggers.file_patterns %}
- {{ pattern }}
{% endfor %}

### Project Indicators
{% for indicator in agent.proactive_triggers.project_indicators %}
- {{ indicator }}
{% endfor %}
{% endif %}

## Implementation Patterns
{% for pattern in agent.implementation_patterns %}
- {{ pattern }}
{% endfor %}

## Professional Standards
{% for standard in agent.professional_standards %}
- {{ standard }}
{% endfor %}
"""
            
            with open(templates_dir / "agent.md.j2", 'w') as f:
                f.write(template_content)

            yield data_dir

    def test_agent_loading_performance(self, large_agent_dataset):
        """Test performance of loading many agent configurations."""
        profiler = PerformanceProfiler()
        profiler.start()
        
        composer = AgentComposer(large_agent_dataset)
        
        # Load all agents
        loaded_agents = {}
        for i in range(50):
            agent_name = f"perf-agent-{i:02d}"
            agent_config = composer.load_agent(agent_name)
            loaded_agents[agent_name] = agent_config
        
        metrics = profiler.stop()
        
        # Verify all agents loaded
        assert len(loaded_agents) == 50
        
        # Performance assertions
        assert metrics["wall_time"] < 5.0, f"Agent loading took {metrics['wall_time']:.2f}s, expected < 5s"
        assert metrics["memory_delta"] < 150 * 1024 * 1024, f"Memory increase {metrics['memory_delta'] / 1024 / 1024:.2f}MB, expected < 150MB"
        
        print(f"Agent Loading Performance: {metrics['wall_time']:.2f}s, {metrics['memory_delta'] / 1024 / 1024:.2f}MB")

    def test_trait_processing_performance(self, large_agent_dataset):
        """Test performance of trait processing and merging."""
        profiler = PerformanceProfiler()
        profiler.start()
        
        composer = AgentComposer(large_agent_dataset)
        
        # Process all agents with trait resolution
        processed_agents = {}
        for i in range(50):
            agent_name = f"perf-agent-{i:02d}"
            agent_config = composer.load_agent(agent_name)
            
            # Process traits
            resolved_traits = {}
            for category, trait_names in agent_config.get("imports", {}).items():
                resolved_traits[category] = []
                for trait_name in trait_names:
                    trait_config = composer.load_trait(f"{category}/{trait_name}")
                    resolved_traits[category].append(trait_config)
            
            processed_agents[agent_name] = {
                "agent": agent_config,
                "traits": resolved_traits
            }
        
        metrics = profiler.stop()
        
        # Verify processing
        assert len(processed_agents) == 50
        
        # Check trait resolution
        for agent_name, data in processed_agents.items():
            assert "traits" in data
            assert len(data["traits"]) > 0
        
        # Performance assertions
        assert metrics["wall_time"] < 10.0, f"Trait processing took {metrics['wall_time']:.2f}s, expected < 10s"
        assert metrics["memory_delta"] < 200 * 1024 * 1024, f"Memory increase {metrics['memory_delta'] / 1024 / 1024:.2f}MB, expected < 200MB"
        
        print(f"Trait Processing Performance: {metrics['wall_time']:.2f}s, {metrics['memory_delta'] / 1024 / 1024:.2f}MB")

    def test_agent_composition_performance(self, large_agent_dataset):
        """Test performance of complete agent composition process."""
        profiler = PerformanceProfiler()
        profiler.start()
        
        composer = AgentComposer(large_agent_dataset)
        
        # Compose all agents
        composed_agents = {}
        for i in range(50):
            agent_name = f"perf-agent-{i:02d}"
            composed_agent = composer.compose_agent(agent_name)
            composed_agents[agent_name] = composed_agent
        
        metrics = profiler.stop()
        
        # Verify composition
        assert len(composed_agents) == 50
        
        # Check composed content
        for agent_name, content in composed_agents.items():
            assert len(content) > 1000  # Should have substantial content
            assert f"Performance Agent" in content
            assert "## Expertise" in content
            assert "## Traits" in content or "trait" in content.lower()
        
        # Performance assertions
        assert metrics["wall_time"] < 20.0, f"Agent composition took {metrics['wall_time']:.2f}s, expected < 20s"
        assert metrics["memory_delta"] < 300 * 1024 * 1024, f"Memory increase {metrics['memory_delta'] / 1024 / 1024:.2f}MB, expected < 300MB"
        
        print(f"Agent Composition Performance: {metrics['wall_time']:.2f}s, {metrics['memory_delta'] / 1024 / 1024:.2f}MB")


class TestMemoryUsage:
    """Test memory usage patterns and potential leaks."""

    def test_memory_usage_stability(self):
        """Test that memory usage remains stable across multiple operations."""
        initial_memory = psutil.Process(os.getpid()).memory_info().rss
        
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create and process many small configurations
            for iteration in range(10):
                # Create configs
                for i in range(10):
                    config = {
                        "name": f"memory-test-{iteration}-{i}",
                        "display_name": f"Memory Test {iteration}-{i}",
                        "description": "Memory test server",
                        "category": "development",
                        "server": {"command": "test", "args": []},
                        "security": {"trust_level": "trusted", "network_access": False},
                        "development": {"status": "stable"}
                    }
                    
                    with open(mcp_dir / f"memory-test-{iteration}-{i}.yaml", 'w') as f:
                        yaml.dump(config, f)

                # Process configs
                processor = MCPProcessor(data_dir)
                results = processor.process_all_for_claude_code()
                
                # Clean up
                for i in range(10):
                    (mcp_dir / f"memory-test-{iteration}-{i}.yaml").unlink()
                
                # Force garbage collection
                del processor, results
                gc.collect()

        final_memory = psutil.Process(os.getpid()).memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be minimal
        assert memory_increase < 50 * 1024 * 1024, f"Memory increased by {memory_increase / 1024 / 1024:.2f}MB, expected < 50MB"

    def test_large_configuration_memory_efficiency(self):
        """Test memory efficiency with very large configurations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create one very large configuration
            large_config = {
                "name": "memory-intensive-server",
                "display_name": "Memory Intensive Server",
                "description": "Server with large configuration for memory testing",
                "category": "development",
                "server": {"command": "node", "args": ["server.js"]},
                "environment": {
                    "variables": {
                        f"VAR_{i}": {
                            "source": "env",
                            "variable": f"SOURCE_VAR_{i}",
                            "required": i < 100,
                            "description": f"Variable {i} with detailed description and extensive metadata"
                        } for i in range(1000)  # 1000 environment variables
                    },
                    "secrets": [f"VAR_{i}" for i in range(50)],
                    "validation": {
                        "required": [f"VAR_{i}" for i in range(100)],
                        "optional": [f"VAR_{i}" for i in range(100, 1000)]
                    }
                },
                "metadata": {
                    "version": "1.0.0",
                    "tags": [f"tag-{i}" for i in range(100)],
                    "personas": {
                        "suitable_for": [f"agent-{i}" for i in range(50)],
                        "enhancement_areas": [f"area-{i}" for i in range(30)],
                        "use_cases": [f"Use case {i} with detailed description" for i in range(100)]
                    }
                },
                "security": {"trust_level": "trusted", "network_access": True},
                "development": {
                    "status": "experimental",
                    "known_issues": [f"Issue {i} with detailed description" for i in range(50)],
                    "dependencies": [f"dependency-{i}" for i in range(20)]
                }
            }

            with open(mcp_dir / "memory-intensive-server.yaml", 'w') as f:
                yaml.dump(large_config, f)

            profiler = PerformanceProfiler()
            profiler.start()
            
            # Process the large configuration
            processor = MCPProcessor(data_dir)
            server_def = processor.load_mcp_server("memory-intensive-server")
            
            # Set up environment for validation
            env_vars = {f"SOURCE_VAR_{i}": f"value_{i}" for i in range(100)}
            with patch.dict(os.environ, env_vars):
                validation_result = processor.validate_mcp_server("memory-intensive-server")
                claude_config = processor.process_for_claude_code(server_def)
            
            metrics = profiler.stop()
            
            # Verify processing succeeded
            assert validation_result.is_valid
            assert len(claude_config["env"]) >= 100
            
            # Memory usage should be reasonable even for large configs
            assert metrics["memory_delta"] < 500 * 1024 * 1024, f"Memory increase {metrics['memory_delta'] / 1024 / 1024:.2f}MB, expected < 500MB"
            assert metrics["wall_time"] < 15.0, f"Processing took {metrics['wall_time']:.2f}s, expected < 15s"


@pytest.mark.slow
class TestScalabilityLimits:
    """Test system behavior at scalability limits."""

    def test_maximum_concurrent_operations(self):
        """Test maximum number of concurrent operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create test configuration
            config = {
                "name": "concurrent-test-server",
                "display_name": "Concurrent Test Server",
                "description": "Server for concurrent testing",
                "category": "development",
                "server": {"command": "test", "args": []},
                "environment": {
                    "variables": {
                        "TEST_VAR": {
                            "source": "env",
                            "variable": "CONCURRENT_TEST_VAR",
                            "required": True
                        }
                    }
                },
                "security": {"trust_level": "trusted", "network_access": False},
                "development": {"status": "stable"}
            }
            
            with open(mcp_dir / "concurrent-test-server.yaml", 'w') as f:
                yaml.dump(config, f)

            def process_server():
                """Process server in thread."""
                with patch.dict(os.environ, {"CONCURRENT_TEST_VAR": "test_value"}):
                    processor = MCPProcessor(data_dir)
                    server_def = processor.load_mcp_server("concurrent-test-server")
                    return processor.process_for_claude_code(server_def)

            # Test with increasing thread counts
            for thread_count in [10, 25, 50, 100]:
                profiler = PerformanceProfiler()
                profiler.start()
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
                    futures = [executor.submit(process_server) for _ in range(thread_count)]
                    results = [future.result() for future in concurrent.futures.as_completed(futures)]
                
                metrics = profiler.stop()
                
                assert len(results) == thread_count
                assert all("command" in result for result in results)
                
                # Performance should degrade gracefully
                print(f"Concurrent threads: {thread_count}, Time: {metrics['wall_time']:.2f}s, Memory: {metrics['memory_delta'] / 1024 / 1024:.2f}MB")

    def test_stress_testing_limits(self):
        """Test system behavior under stress conditions."""
        process = psutil.Process(os.getpid())
        
        # Monitor system resources
        initial_memory = process.memory_info().rss
        initial_cpu_percent = process.cpu_percent()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create many configurations rapidly
            for batch in range(10):
                start_time = time.time()
                
                # Create 50 configs
                for i in range(50):
                    config = {
                        "name": f"stress-test-{batch}-{i}",
                        "display_name": f"Stress Test {batch}-{i}",
                        "description": "Stress test configuration",
                        "category": "development",
                        "server": {"command": "test", "args": []},
                        "environment": {
                            "variables": {
                                f"VAR_{j}": f"value_{j}" for j in range(10)
                            }
                        },
                        "security": {"trust_level": "trusted", "network_access": False},
                        "development": {"status": "experimental"}
                    }
                    
                    with open(mcp_dir / f"stress-test-{batch}-{i}.yaml", 'w') as f:
                        yaml.dump(config, f)

                # Process all configs
                processor = MCPProcessor(data_dir)
                results = processor.process_all_for_claude_code()
                
                # Clean up
                for i in range(50):
                    (mcp_dir / f"stress-test-{batch}-{i}.yaml").unlink()
                
                batch_time = time.time() - start_time
                current_memory = process.memory_info().rss
                
                print(f"Stress batch {batch}: {batch_time:.2f}s, Memory: {(current_memory - initial_memory) / 1024 / 1024:.2f}MB")
                
                # System should remain responsive
                assert batch_time < 10.0, f"Batch {batch} took {batch_time:.2f}s, too slow"
                assert current_memory - initial_memory < 1024 * 1024 * 1024, "Memory usage too high"  # < 1GB


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "not slow"])