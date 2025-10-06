"""
Command Line Interface for Claude Config Generator.

Provides commands for building, validating, and managing Claude Code
agent configurations.
"""

import sys
from pathlib import Path
from typing import List, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown

from .composer import AgentComposer
from .validator import ConfigValidator
from .generator.claude_md_generator import ClaudeMdGenerator
from .coordination.validator import CoordinationValidator


console = Console()


@click.group()
@click.version_option()
def cli():
    """Claude Code Configuration Generator
    
    Generate Claude Code agent configurations from YAML persona definitions
    using the unified AgentComposer system.
    """
    pass


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path),
              default="data", help="Data directory path")
@click.option("--output-dir", "-o", type=click.Path(path_type=Path),
              default="dist", help="Output directory path")
@click.option("--agent", "-a", multiple=True, help="Build specific agents only")
@click.option("--validate", is_flag=True, help="Validate configurations before building")
@click.option("--with-orchestration", is_flag=True, help="Also generate CLAUDE.md orchestration file")
def build_agents(data_dir: Path, output_dir: Path, agent: List[str], validate: bool, with_orchestration: bool):
    """Build agent configurations from persona definitions."""

    if validate:
        console.print("🔍 Validating configurations...", style="yellow")
        validator = ConfigValidator(data_dir)
        if not validator.validate_all():
            console.print("❌ Validation failed. Aborting build.", style="red")
            sys.exit(1)
        console.print("✅ Validation passed!", style="green")
    
    # Initialize composer
    composer = AgentComposer(data_dir=data_dir, output_dir=output_dir)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        if agent:
            # Build specific agents
            task = progress.add_task("Building specific agents...", total=len(agent))
            built_agents = []
            
            for agent_name in agent:
                try:
                    agent_path = composer.build_agent(agent_name)
                    built_agents.append(agent_path)
                    console.print(f"✅ Built {agent_name}", style="green")
                except Exception as e:
                    console.print(f"❌ Failed to build {agent_name}: {e}", style="red")
                progress.advance(task)
        else:
            # Build all agents
            task = progress.add_task("Building all agents...", total=None)
            built_agents = composer.build_all_agents()
    
    # Display results
    if built_agents:
        table = Table(title="Built Agents")
        table.add_column("Agent", style="cyan")
        table.add_column("Output Path", style="green")

        for agent_path in built_agents:
            table.add_row(agent_path.stem, str(agent_path))

        console.print(table)
        console.print(f"\n✅ Successfully built {len(built_agents)} agents", style="green")
    else:
        console.print("⚠️  No agents were built", style="yellow")

    # Generate orchestration file if requested
    if with_orchestration:
        console.print("\n🔨 Generating CLAUDE.md orchestration file...", style="blue")
        try:
            generator = ClaudeMdGenerator(data_dir=data_dir, output_dir=output_dir)
            output_path = generator.generate_claude_md()
            console.print(f"✅ CLAUDE.md generated: {output_path}", style="green")
        except Exception as e:
            console.print(f"❌ Failed to generate CLAUDE.md: {e}", style="red")
            sys.exit(1)


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path),
              default="data", help="Data directory path")
def validate(data_dir: Path):
    """Validate agent configurations."""
    console.print("🔍 Validating configurations...", style="yellow")

    validator = ConfigValidator(data_dir)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Validating...", total=None)

        # Validate agent configurations
        is_valid = validator.validate_all()
        if is_valid:
            console.print("✅ All configurations are valid!", style="green")
        else:
            console.print("❌ Validation failed. Check errors above.", style="red")
            sys.exit(1)

        progress.advance(task)


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path), 
              default="data", help="Data directory path")
def list_agents(data_dir: Path):
    """List available agent personas and compositions."""
    personas_dir = data_dir / "personas"
    
    if not personas_dir.exists():
        console.print("❌ No personas directory found", style="red")
        return
    
    table = Table(title="Available Agent Personas")
    table.add_column("Name", style="cyan")
    table.add_column("File", style="green")
    table.add_column("Status", style="yellow")
    
    for persona_file in personas_dir.glob("*.yaml"):
        if persona_file.stem != "config":
            status = "✅ Ready" if persona_file.exists() else "❌ Missing"
            table.add_row(persona_file.stem, persona_file.name, status)
    
    console.print(table)


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path), 
              default="data", help="Data directory path")
@click.option("--template-dir", "-t", type=click.Path(exists=True, path_type=Path), 
              default="src/claude_config/templates", help="Template directory path")
@click.option("--output", "-o", type=click.Path(path_type=Path), 
              default="dist/CLAUDE.md", help="Output file path")
def build_claude(data_dir: Path, template_dir: Path, output: Path):
    """Build global CLAUDE.md configuration file from all agents."""
    console.print("🔨 Building global CLAUDE.md configuration...", style="blue")
    
    try:
        composer = AgentComposer(
            data_dir=data_dir,
            template_dir=template_dir,
            output_dir=output.parent
        )
        
        # Generate global CLAUDE.md content
        global_content = composer.compose_global_claude_md()
        
        # Ensure output directory exists
        output.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the global configuration
        with open(output, 'w') as f:
            f.write(global_content)
        
        console.print(f"✅ Global CLAUDE.md built successfully: {output}", style="green")
        
    except Exception as e:
        console.print(f"❌ Failed to build global CLAUDE.md: {e}", style="red")
        sys.exit(1)


# Add backwards compatibility alias
@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path),
              default="data", help="Data directory path")
@click.option("--output-dir", "-o", type=click.Path(path_type=Path),
              default="dist", help="Output directory path")
@click.option("--agent", "-a", multiple=True, help="Build specific agents only")
@click.option("--validate", is_flag=True, help="Validate configurations before building")
@click.option("--with-orchestration", is_flag=True, help="Also generate CLAUDE.md orchestration file")
def build(data_dir: Path, output_dir: Path, agent: List[str], validate: bool, with_orchestration: bool):
    """Build agent configurations (alias for build-agents)."""
    # Call build_agents with the same parameters
    from click import Context
    ctx = Context(build_agents)
    ctx.invoke(build_agents, data_dir=data_dir, output_dir=output_dir, agent=agent,
               validate=validate, with_orchestration=with_orchestration)


@cli.command()
@click.option("--output-dir", "-o", type=click.Path(path_type=Path),
              default="dist", help="Output directory to install from")
@click.option("--target", "-t", type=click.Path(path_type=Path),
              help="Target directory (defaults to ~/.claude)")
@click.option("--dry-run", is_flag=True, help="Show what would be installed without doing it")
@click.option("--no-clean", is_flag=True, help="Skip cleaning agents directory before install")
def install(output_dir: Path, target: Optional[Path], dry_run: bool, no_clean: bool):
    """Install generated configurations to Claude Code directory.

    By default, this performs a clean installation that removes existing
    agents before installing new ones. Use --no-clean to preserve existing
    agents and only overwrite matching files.
    """
    import shutil

    if not target:
        target = Path.home() / ".claude"

    if not output_dir.exists():
        console.print(f"❌ Output directory {output_dir} does not exist. Run 'build' first.", style="red")
        sys.exit(1)

    console.print(f"📦 Installing from {output_dir} to {target}", style="blue")

    if dry_run:
        console.print("🔍 Dry run mode - no changes will be made", style="yellow")

    # Ensure target directory exists
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    # Clean agents directory if requested (default behavior)
    agents_dir = target / "agents"
    cleaned_files = []

    if not no_clean and agents_dir.exists():
        console.print("🧹 Cleaning existing agents directory...", style="yellow")

        if dry_run:
            # Show what would be cleaned
            for agent_file in agents_dir.glob("*.md"):
                console.print(f"Would remove: agents/{agent_file.name}", style="dim red")
                cleaned_files.append(f"agents/{agent_file.name}")
        else:
            # Actually clean the agents directory
            for agent_file in agents_dir.glob("*.md"):
                agent_file.unlink()
                cleaned_files.append(f"agents/{agent_file.name}")
                console.print(f"🗑️  Removed: agents/{agent_file.name}", style="dim")

    # Copy new files
    copied_files = []
    for item in output_dir.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(output_dir)
            dest_path = target / rel_path

            if dry_run:
                console.print(f"Would copy: {rel_path}", style="dim green")
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)
                copied_files.append(rel_path)

    # Summary
    if not dry_run:
        if cleaned_files and not no_clean:
            console.print(f"🗑️  Cleaned {len(cleaned_files)} existing agents", style="yellow")
        console.print(f"✅ Installed {len(copied_files)} files to {target}", style="green")
    else:
        if cleaned_files and not no_clean:
            console.print(f"Would clean {len(cleaned_files)} existing agents", style="yellow")
        console.print(f"Would install {len(list(output_dir.rglob('*')))} items", style="yellow")


@cli.command()
@click.option("--output", "-o", type=click.Path(path_type=Path),
              help="Output path for CLAUDE.md (default: ~/.claude/CLAUDE.md)")
@click.option("--agents-dir", "-a", type=click.Path(exists=True, path_type=Path),
              default="data/personas", help="Directory containing agent YAML files")
@click.option("--validate/--no-validate", default=True,
              help="Run validation before generation")
@click.option("--no-optimize", is_flag=True,
              help="Skip graph optimization")
@click.option("--dry-run", is_flag=True,
              help="Show what would be generated without writing")
def generate_claude_md(
    output: Optional[Path],
    agents_dir: Path,
    validate: bool,
    no_optimize: bool,
    dry_run: bool
):
    """Generate master CLAUDE.md orchestration file from agent configurations.

    This command processes all agent YAML files, extracts coordination patterns,
    validates the coordination graph, and generates the master CLAUDE.md file
    that Claude Code uses for agent delegation decisions.

    Examples:
        # Generate to default location (~/.claude/CLAUDE.md)
        make generate-claude-md

        # Generate to custom location
        python -m claude_config.cli generate-claude-md --output dist/CLAUDE.md

        # Skip validation (not recommended)
        python -m claude_config.cli generate-claude-md --no-validate

        # Dry run to preview
        python -m claude_config.cli generate-claude-md --dry-run
    """
    import time

    # Set default output path
    if output is None:
        output = Path.home() / ".claude" / "CLAUDE.md"

    console.print("🔨 Generating CLAUDE.md orchestration file...", style="blue")

    try:
        # Initialize generator
        data_dir = agents_dir.parent
        start_time = time.time()

        generator = ClaudeMdGenerator(
            data_dir=data_dir,
            output_dir=output.parent
        )

        # Load agents
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Loading agent configurations...", total=None)
            agents = generator.load_all_agents()
            progress.update(task, completed=True)

        if not agents:
            console.print("❌ No agent configurations found", style="red")
            sys.exit(1)

        console.print(f"✅ Loaded {len(agents)} agent configurations", style="green")

        # Validate if requested
        if validate:
            console.print("\n🔍 Validating coordination patterns...", style="yellow")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Validating coordination...", total=None)
                report = generator.validate_before_generation(agents)
                progress.update(task, completed=True)

            if report.has_warnings():
                console.print(f"⚠️  {len(report.warnings)} validation warnings", style="yellow")

        # Build graph
        console.print("\n📊 Building coordination graph...", style="blue")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Building graph...", total=None)
            graph = generator.build_coordination_graph(agents)
            progress.update(task, completed=True)

        # Display graph stats
        stats = graph.optimization_result.optimization_stats
        stats_table = Table(title="Coordination Graph Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")

        stats_table.add_row("Total Agents", str(len(graph.adjacency_list)))
        stats_table.add_row("Entry Points", str(len([a for a in agents if graph.is_entry_point(a.name)])))
        stats_table.add_row("Coordination Edges", str(stats.get('total_edges', 0)))
        stats_table.add_row("Cached Paths", str(stats.get('cached_paths', 0)))

        console.print(stats_table)

        # Generate file
        if dry_run:
            console.print("\n🔍 Dry run mode - file will not be written", style="yellow")
        else:
            console.print(f"\n✍️  Writing to {output}...", style="blue")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Generating CLAUDE.md...", total=None)
                output_path = generator.generate_claude_md(
                    output_path=output,
                    validate=False  # Already validated
                )
                progress.update(task, completed=True)

            elapsed = time.time() - start_time
            console.print(f"\n✅ CLAUDE.md generated successfully in {elapsed*1000:.0f}ms", style="green")
            console.print(f"📄 Output: {output_path}", style="cyan")

    except ValueError as e:
        console.print(f"\n❌ Validation error: {e}", style="red")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n❌ Generation failed: {e}", style="red")
        import traceback
        console.print(traceback.format_exc(), style="dim red")
        sys.exit(1)


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path),
              default="data", help="Data directory path")
@click.option("--agent", "-a", help="Validate specific agent only")
@click.option("--fix-warnings", is_flag=True,
              help="Attempt to fix common validation warnings")
def validate_coordination(data_dir: Path, agent: Optional[str], fix_warnings: bool):
    """Validate coordination patterns in agent configurations.

    This command performs comprehensive validation of agent coordination patterns
    including cycle detection, consistency checking, and trait validation.

    Examples:
        # Validate all agents
        make validate-coordination

        # Validate specific agent
        python -m claude_config.cli validate-coordination --agent python-engineer

        # Attempt to fix warnings
        python -m claude_config.cli validate-coordination --fix-warnings
    """
    console.print("🔍 Validating coordination patterns...", style="blue")

    try:
        validator = CoordinationValidator(data_dir=data_dir)

        # Validate specific agent or all agents
        if agent:
            report = validator.load_and_validate(agent_names=[agent])
            console.print(f"\nValidating: {agent}", style="cyan")
        else:
            report = validator.load_and_validate()
            console.print("\nValidating all agents", style="cyan")

        # Display summary
        console.print("\n" + "="*60)
        console.print(report.summary())
        console.print("="*60)

        # Show detailed errors
        if report.cycles:
            console.print("\n🔄 Circular Dependencies Detected:", style="red bold")
            for cycle in report.cycles:
                console.print(f"  {cycle}", style="red")

        if report.consistency_issues:
            errors = [i for i in report.consistency_issues if i.severity == 'error']
            warnings = [i for i in report.consistency_issues if i.severity == 'warning']

            if errors:
                console.print("\n❌ Consistency Errors:", style="red bold")
                for issue in errors[:10]:
                    console.print(f"  [{issue.issue_type}] {issue.description}", style="red")
                if len(errors) > 10:
                    console.print(f"  ... and {len(errors) - 10} more errors", style="dim red")

            if warnings:
                console.print("\n⚠️  Consistency Warnings:", style="yellow bold")
                for issue in warnings[:10]:
                    console.print(f"  [{issue.issue_type}] {issue.description}", style="yellow")
                if len(warnings) > 10:
                    console.print(f"  ... and {len(warnings) - 10} more warnings", style="dim yellow")

        # Fix warnings if requested
        if fix_warnings and report.has_warnings():
            console.print("\n🔧 Attempting to fix warnings...", style="yellow")
            console.print("⚠️  Warning fix functionality not yet implemented", style="yellow")

        # Exit with appropriate code
        if report.is_valid:
            console.print("\n✅ Coordination validation PASSED", style="green bold")
            sys.exit(0)
        else:
            console.print("\n❌ Coordination validation FAILED", style="red bold")
            sys.exit(1)

    except Exception as e:
        console.print(f"\n❌ Validation error: {e}", style="red")
        import traceback
        console.print(traceback.format_exc(), style="dim red")
        sys.exit(1)


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path),
              default="data", help="Data directory path")
@click.option("--output", "-o", type=click.Path(path_type=Path),
              help="Save graph to file")
@click.option("--format", "-f", type=click.Choice(['mermaid', 'dot', 'json']),
              default='mermaid', help="Output format")
@click.option("--open", "open_browser", is_flag=True,
              help="Open visualization in browser (requires mermaid-cli)")
@click.option("--max-nodes", type=int, default=30,
              help="Maximum nodes to include in visualization")
def visualize_graph(
    data_dir: Path,
    output: Optional[Path],
    format: str,
    open_browser: bool,
    max_nodes: int
):
    """Generate and display coordination graph visualization.

    This command creates a visual representation of the agent coordination graph
    using Mermaid diagrams, Graphviz DOT format, or JSON.

    Examples:
        # Display Mermaid diagram in terminal
        make visualize-graph

        # Save Mermaid diagram to file
        python -m claude_config.cli visualize-graph --output coordination.md

        # Generate Graphviz DOT format
        python -m claude_config.cli visualize-graph --format dot --output graph.dot

        # Generate JSON representation
        python -m claude_config.cli visualize-graph --format json --output graph.json
    """
    console.print("📊 Generating coordination graph...", style="blue")

    try:
        generator = ClaudeMdGenerator(data_dir=data_dir)

        # Load agents and build graph
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Loading agents...", total=None)
            agents = generator.load_all_agents()
            progress.update(task, description="Building graph...")
            graph = generator.build_coordination_graph(agents)
            progress.update(task, completed=True)

        # Generate visualization
        if format == 'mermaid':
            diagram = generator.generate_mermaid_graph(graph, agents, max_nodes=max_nodes)

            if output:
                output.parent.mkdir(parents=True, exist_ok=True)
                with open(output, 'w') as f:
                    f.write(diagram)
                console.print(f"✅ Mermaid diagram saved to: {output}", style="green")
            else:
                # Display in terminal
                console.print("\n" + "="*60)
                console.print(Markdown(diagram))
                console.print("="*60)

        elif format == 'dot':
            console.print("⚠️  DOT format not yet implemented", style="yellow")
            console.print("Use mermaid format for now", style="dim")

        elif format == 'json':
            import json
            graph_data = {
                'agents': [agent.name for agent in agents],
                'adjacency_list': graph.adjacency_list,
                'metadata': graph.agent_metadata,
                'stats': graph.optimization_result.optimization_stats
            }

            if output:
                output.parent.mkdir(parents=True, exist_ok=True)
                with open(output, 'w') as f:
                    json.dump(graph_data, f, indent=2)
                console.print(f"✅ JSON graph saved to: {output}", style="green")
            else:
                console.print(json.dumps(graph_data, indent=2))

        # Open in browser if requested
        if open_browser and format == 'mermaid' and output:
            console.print("\n🌐 Opening in browser...", style="blue")
            console.print("⚠️  Browser opening not yet implemented", style="yellow")
            console.print("Please use mermaid.live or mermaid-cli to view", style="dim")

    except Exception as e:
        console.print(f"\n❌ Visualization failed: {e}", style="red")
        import traceback
        console.print(traceback.format_exc(), style="dim red")
        sys.exit(1)


@cli.command()
@click.argument("agent_name")
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path),
              default="data", help="Data directory path")
def show_coordination(agent_name: str, data_dir: Path):
    """Show coordination patterns for a specific agent.

    Displays inbound/outbound coordination triggers, relationships,
    and connected agents.

    Examples:
        # Show coordination for python-engineer
        make show-coordination AGENT=python-engineer

        # Show coordination for qa-engineer
        make show-coordination AGENT=qa-engineer
    """
    console.print(f"🔍 Analyzing coordination for: {agent_name}", style="blue")

    try:
        generator = ClaudeMdGenerator(data_dir=data_dir)

        # Load agents and build graph
        agents = generator.load_all_agents()
        agent_lookup = {agent.name: agent for agent in agents}

        if agent_name not in agent_lookup:
            console.print(f"\n❌ Agent '{agent_name}' not found", style="red")
            console.print(f"Available agents: {', '.join(sorted(agent_lookup.keys()))}", style="dim")
            sys.exit(1)

        agent = agent_lookup[agent_name]
        graph = generator.build_coordination_graph(agents)

        # Display agent info
        console.print(f"\n{'='*60}")
        console.print(Panel(
            f"[bold cyan]{agent.display_name or agent.name}[/bold cyan]\n"
            f"[dim]{agent.description}[/dim]\n\n"
            f"Model: [yellow]{agent.model}[/yellow]",
            title=f"Agent: {agent_name}",
            border_style="blue"
        ))

        # Outbound coordination (who this agent coordinates with)
        targets = graph.get_coordination_targets(agent_name)
        if targets:
            console.print("\n📤 Outbound Coordination:", style="green bold")
            for target in targets:
                target_agent = agent_lookup.get(target)
                if target_agent:
                    console.print(
                        f"  → {target} ({target_agent.model}) - {target_agent.description[:60]}...",
                        style="green"
                    )
        else:
            console.print("\n📤 Outbound Coordination: None", style="dim")

        # Inbound coordination (who coordinates with this agent)
        inbound = [
            source for source, targets in graph.adjacency_list.items()
            if agent_name in targets
        ]
        if inbound:
            console.print("\n📥 Inbound Coordination:", style="blue bold")
            for source in inbound:
                source_agent = agent_lookup.get(source)
                if source_agent:
                    console.print(
                        f"  ← {source} ({source_agent.model}) - {source_agent.description[:60]}...",
                        style="blue"
                    )
        else:
            console.print("\n📥 Inbound Coordination: None", style="dim")

        # Coordination traits
        if agent.imports:
            coord_traits = agent.imports.get('coordination', [])
            if coord_traits:
                console.print("\n🔗 Coordination Traits:", style="yellow bold")
                for trait in coord_traits:
                    console.print(f"  - {trait}", style="yellow")

        # Custom coordination
        if agent.custom_coordination:
            console.print("\n⚙️  Custom Coordination:", style="magenta bold")
            for key, desc in agent.custom_coordination.items():
                console.print(f"  {key}: {desc}", style="magenta")

        # Proactive triggers
        if hasattr(agent, 'proactive_triggers'):
            triggers = agent.proactive_triggers
            if isinstance(triggers, dict):
                patterns = triggers.get('file_patterns', [])
            else:
                patterns = getattr(triggers, 'file_patterns', [])

            if patterns:
                console.print("\n🎯 Proactive Triggers:", style="cyan bold")
                for pattern in patterns[:10]:
                    console.print(f"  - {pattern}", style="cyan")
                if len(patterns) > 10:
                    console.print(f"  ... and {len(patterns) - 10} more patterns", style="dim cyan")

        console.print(f"\n{'='*60}\n")

    except Exception as e:
        console.print(f"\n❌ Analysis failed: {e}", style="red")
        import traceback
        console.print(traceback.format_exc(), style="dim red")
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()