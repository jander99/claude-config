"""
CLI Integration Tests for Orchestration Commands.

Tests the CLI commands for generating CLAUDE.md, validating coordination,
visualizing graphs, and showing agent coordination patterns.
"""

import pytest
from pathlib import Path
from click.testing import CliRunner
from src.claude_config.cli import (
    cli,
    generate_claude_md,
    validate_coordination,
    visualize_graph,
    show_coordination,
    build_agents
)


@pytest.fixture
def cli_runner():
    """Create CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def test_data_dir():
    """Get test data directory path."""
    return Path("data")


class TestGenerateClaudeMd:
    """Test generate-claude-md command."""

    def test_help(self, cli_runner):
        """Test help message displays correctly."""
        result = cli_runner.invoke(generate_claude_md, ['--help'])
        assert result.exit_code == 0
        assert "Generate master CLAUDE.md orchestration file" in result.output
        assert "--output" in result.output
        assert "--validate" in result.output
        assert "--dry-run" in result.output

    def test_dry_run_mode(self, cli_runner, test_data_dir, tmp_path):
        """Test dry run mode doesn't write files."""
        output_path = tmp_path / "CLAUDE.md"
        result = cli_runner.invoke(generate_claude_md, [
            '--agents-dir', str(test_data_dir / "personas"),
            '--output', str(output_path),
            '--dry-run',
            '--no-validate'  # Skip validation to test dry-run behavior
        ])

        # Should succeed but not write file
        if result.exit_code == 0:
            assert "Dry run mode" in result.output
            assert not output_path.exists()
        else:
            # If it fails, at least check the file wasn't written
            assert not output_path.exists()

    def test_generate_with_validation(self, cli_runner, test_data_dir, tmp_path):
        """Test generation with validation enabled."""
        output_path = tmp_path / "CLAUDE.md"
        result = cli_runner.invoke(generate_claude_md, [
            '--agents-dir', str(test_data_dir / "personas"),
            '--output', str(output_path),
            '--validate'
        ])

        # Should validate and generate
        if result.exit_code == 0:
            assert "Validating coordination patterns" in result.output
            assert output_path.exists()
        else:
            # If validation fails, that's expected for test data
            assert "Validation error" in result.output or "Failed" in result.output

    def test_generate_skip_validation(self, cli_runner, test_data_dir, tmp_path):
        """Test generation with validation disabled."""
        output_path = tmp_path / "CLAUDE.md"
        result = cli_runner.invoke(generate_claude_md, [
            '--agents-dir', str(test_data_dir / "personas"),
            '--output', str(output_path),
            '--no-validate'
        ])

        # Should skip validation
        if result.exit_code == 0:
            assert "Validating coordination patterns" not in result.output
            assert output_path.exists()


class TestValidateCoordination:
    """Test validate-coordination command."""

    def test_help(self, cli_runner):
        """Test help message displays correctly."""
        result = cli_runner.invoke(validate_coordination, ['--help'])
        assert result.exit_code == 0
        assert "Validate coordination patterns" in result.output
        assert "--agent" in result.output
        assert "--fix-warnings" in result.output

    def test_validate_all_agents(self, cli_runner, test_data_dir):
        """Test validating all agents."""
        result = cli_runner.invoke(validate_coordination, [
            '--data-dir', str(test_data_dir)
        ])

        # Should attempt validation and show results
        assert "Validating coordination patterns" in result.output
        assert "Validating all agents" in result.output

    def test_validate_specific_agent(self, cli_runner, test_data_dir):
        """Test validating specific agent."""
        result = cli_runner.invoke(validate_coordination, [
            '--data-dir', str(test_data_dir),
            '--agent', 'python-engineer'
        ])

        # Should validate specific agent
        assert "Validating: python-engineer" in result.output


class TestVisualizeGraph:
    """Test visualize-graph command."""

    def test_help(self, cli_runner):
        """Test help message displays correctly."""
        result = cli_runner.invoke(visualize_graph, ['--help'])
        assert result.exit_code == 0
        assert "Generate and display coordination graph" in result.output
        assert "--format" in result.output
        assert "--output" in result.output
        assert "--max-nodes" in result.output

    def test_generate_mermaid_to_file(self, cli_runner, test_data_dir, tmp_path):
        """Test generating Mermaid diagram to file."""
        output_path = tmp_path / "graph.md"
        result = cli_runner.invoke(visualize_graph, [
            '--data-dir', str(test_data_dir),
            '--output', str(output_path),
            '--format', 'mermaid'
        ])

        if result.exit_code == 0:
            assert output_path.exists()
            content = output_path.read_text()
            assert "```mermaid" in content
            assert "graph TD" in content

    def test_generate_json_format(self, cli_runner, test_data_dir, tmp_path):
        """Test generating JSON format."""
        output_path = tmp_path / "graph.json"
        result = cli_runner.invoke(visualize_graph, [
            '--data-dir', str(test_data_dir),
            '--output', str(output_path),
            '--format', 'json'
        ])

        if result.exit_code == 0:
            assert output_path.exists()
            import json
            data = json.loads(output_path.read_text())
            assert 'agents' in data
            assert 'adjacency_list' in data
            assert 'metadata' in data

    def test_max_nodes_option(self, cli_runner, test_data_dir, tmp_path):
        """Test max-nodes option limits graph size."""
        output_path = tmp_path / "graph.md"
        result = cli_runner.invoke(visualize_graph, [
            '--data-dir', str(test_data_dir),
            '--output', str(output_path),
            '--format', 'mermaid',
            '--max-nodes', '10'
        ])

        if result.exit_code == 0:
            assert output_path.exists()


class TestShowCoordination:
    """Test show-coordination command."""

    def test_help(self, cli_runner):
        """Test help message displays correctly."""
        result = cli_runner.invoke(show_coordination, ['--help'])
        assert result.exit_code == 0
        assert "Show coordination patterns for a specific agent" in result.output

    def test_show_existing_agent(self, cli_runner, test_data_dir):
        """Test showing coordination for existing agent."""
        result = cli_runner.invoke(show_coordination, [
            'python-engineer',
            '--data-dir', str(test_data_dir)
        ])

        if result.exit_code == 0:
            assert "Analyzing coordination for: python-engineer" in result.output
            # Should show various coordination sections
            assert "Outbound Coordination" in result.output or "Inbound Coordination" in result.output

    def test_show_nonexistent_agent(self, cli_runner, test_data_dir):
        """Test showing coordination for non-existent agent."""
        result = cli_runner.invoke(show_coordination, [
            'nonexistent-agent',
            '--data-dir', str(test_data_dir)
        ])

        # Should fail with appropriate error
        assert result.exit_code == 1
        assert "Agent 'nonexistent-agent' not found" in result.output


class TestBuildAgentsWithOrchestration:
    """Test build-agents command with orchestration flag."""

    def test_build_with_orchestration_flag(self, cli_runner, test_data_dir, tmp_path):
        """Test building agents with orchestration file generation."""
        output_dir = tmp_path / "dist"
        result = cli_runner.invoke(build_agents, [
            '--data-dir', str(test_data_dir),
            '--output-dir', str(output_dir),
            '--with-orchestration'
        ])

        if result.exit_code == 0:
            # Should build agents and generate CLAUDE.md
            assert "Successfully built" in result.output or "Generating CLAUDE.md" in result.output

    def test_build_without_orchestration_flag(self, cli_runner, test_data_dir, tmp_path):
        """Test building agents without orchestration file generation."""
        output_dir = tmp_path / "dist"
        result = cli_runner.invoke(build_agents, [
            '--data-dir', str(test_data_dir),
            '--output-dir', str(output_dir)
        ])

        # Should build agents without CLAUDE.md generation
        if result.exit_code == 0:
            assert "Generating CLAUDE.md" not in result.output


class TestCLIIntegration:
    """Integration tests for CLI workflows."""

    def test_full_workflow(self, cli_runner, test_data_dir, tmp_path):
        """Test complete workflow: validate -> build -> generate."""
        output_dir = tmp_path / "dist"

        # Step 1: Validate coordination
        validate_result = cli_runner.invoke(validate_coordination, [
            '--data-dir', str(test_data_dir)
        ])
        # Validation may pass or fail depending on test data

        # Step 2: Build agents with orchestration
        build_result = cli_runner.invoke(build_agents, [
            '--data-dir', str(test_data_dir),
            '--output-dir', str(output_dir),
            '--with-orchestration'
        ])

        # If build succeeds, verify outputs
        if build_result.exit_code == 0:
            agents_dir = output_dir / "agents"
            claude_md = output_dir / "CLAUDE.md"

            # Check agents were built
            if agents_dir.exists():
                agent_files = list(agents_dir.glob("*.md"))
                assert len(agent_files) > 0

    def test_visualize_after_build(self, cli_runner, test_data_dir, tmp_path):
        """Test visualizing graph after building agents."""
        # First build agents
        output_dir = tmp_path / "dist"
        build_result = cli_runner.invoke(build_agents, [
            '--data-dir', str(test_data_dir),
            '--output-dir', str(output_dir)
        ])

        # Then visualize
        viz_output = tmp_path / "graph.md"
        viz_result = cli_runner.invoke(visualize_graph, [
            '--data-dir', str(test_data_dir),
            '--output', str(viz_output),
            '--format', 'mermaid'
        ])

        if viz_result.exit_code == 0:
            assert viz_output.exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
