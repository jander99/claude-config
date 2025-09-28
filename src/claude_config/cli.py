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

from .composer import AgentComposer
from .validator import ConfigValidator


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
def build_agents(data_dir: Path, output_dir: Path, agent: List[str], validate: bool):
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
def build(data_dir: Path, output_dir: Path, agent: List[str], validate: bool):
    """Build agent configurations (alias for build-agents)."""
    # Call build_agents with the same parameters
    from click import Context
    ctx = Context(build_agents)
    ctx.invoke(build_agents, data_dir=data_dir, output_dir=output_dir, agent=agent, validate=validate)


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




def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()