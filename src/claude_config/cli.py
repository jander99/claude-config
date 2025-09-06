"""
Command Line Interface for Claude Config Generator.

Provides commands for building, validating, and managing Claude Code
agent configurations.
"""

import sys
from pathlib import Path
from typing import Optional, List
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .composer import AgentComposer
from .validator import ConfigValidator


console = Console()


@click.group()
@click.version_option()
def cli():
    """Claude Code Configuration Generator
    
    A composable system for generating Claude Code agent configurations
    through personas, traits, and content composition.
    """
    pass


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path), 
              default="data", help="Data directory path")
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), 
              default="dist", help="Output directory path")
@click.option("--agent", "-a", multiple=True, help="Build specific agents only")
@click.option("--validate", is_flag=True, help="Validate configurations before building")
def build(data_dir: Path, output_dir: Path, agent: List[str], validate: bool):
    """Build agent configurations from compositions."""
    
    if validate:
        console.print("🔍 Validating configurations...", style="yellow")
        validator = ConfigValidator(data_dir)
        if not validator.validate_all():
            console.print("❌ Validation failed. Aborting build.", style="red")
            sys.exit(1)
        console.print("✅ Validation passed!", style="green")
    
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
        is_valid = validator.validate_all()
        progress.advance(task)
    
    if is_valid:
        console.print("✅ All configurations are valid!", style="green")
    else:
        console.print("❌ Validation failed. Check errors above.", style="red")
        sys.exit(1)


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
def list_traits(data_dir: Path):
    """List available traits."""
    traits_dir = data_dir / "traits"
    
    if not traits_dir.exists():
        console.print("❌ No traits directory found", style="red")
        return
    
    table = Table(title="Available Traits")
    table.add_column("Name", style="cyan")
    table.add_column("Category", style="yellow")
    table.add_column("File", style="green")
    
    for trait_file in traits_dir.rglob("*.yaml"):
        # Get relative path for nested traits
        rel_path = trait_file.relative_to(traits_dir)
        trait_name = str(rel_path.with_suffix(''))
        category = rel_path.parent.name if rel_path.parent.name != "." else "root"
        
        table.add_row(trait_name, category, trait_file.name)
    
    console.print(table)


@cli.command()
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), 
              default="dist", help="Output directory to install from")
@click.option("--target", "-t", type=click.Path(path_type=Path), 
              help="Target directory (defaults to ~/.claude)")
@click.option("--dry-run", is_flag=True, help="Show what would be installed without doing it")
def install(output_dir: Path, target: Optional[Path], dry_run: bool):
    """Install generated configurations to Claude Code directory."""
    import shutil
    import os
    
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
    
    # Copy files
    copied_files = []
    for item in output_dir.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(output_dir)
            dest_path = target / rel_path
            
            if dry_run:
                console.print(f"Would copy: {rel_path}", style="dim")
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)
                copied_files.append(rel_path)
    
    if not dry_run:
        console.print(f"✅ Installed {len(copied_files)} files to {target}", style="green")
    else:
        console.print(f"Would install {len(list(output_dir.rglob('*')))} items", style="yellow")


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()