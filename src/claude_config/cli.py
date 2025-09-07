"""
Command Line Interface for Claude Config Generator.

Provides commands for building, validating, and managing Claude Code
agent configurations.
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import yaml
import json

from .composer import AgentComposer
from .validator import ConfigValidator

# Import trait inheritance components
try:
    from .inheritance.resolver import TraitResolver
    from .inheritance.compositor import TraitCompositor
    from .inheritance.schema import TraitReference
    INHERITANCE_AVAILABLE = True
except ImportError:
    INHERITANCE_AVAILABLE = False

# Import pattern resolver
try:
    import sys
    sys.path.append(str(Path("data/patterns/schemas")))
    from pattern_resolver import PatternResolver
    PATTERNS_AVAILABLE = True
except ImportError:
    PATTERNS_AVAILABLE = False


console = Console()


def _validate_inheritance_and_patterns(data_dir: Path, use_inheritance: bool, use_patterns: bool) -> bool:
    """Validate trait inheritance and pattern resolution setup."""
    try:
        if use_inheritance and INHERITANCE_AVAILABLE:
            trait_paths = [data_dir / "traits"]
            resolver = TraitResolver(trait_paths)
            
            # Basic validation - check if trait directory exists and has valid traits
            if not (data_dir / "traits").exists():
                console.print("❌ Traits directory not found", style="red")
                return False
                
            # Test loading available traits
            available_traits = resolver.get_available_traits()
            console.print(f"📊 Found {sum(len(traits) for traits in available_traits.values())} traits", style="green")
        
        if use_patterns and PATTERNS_AVAILABLE:
            patterns_dir = data_dir / "patterns"
            if not patterns_dir.exists():
                console.print("❌ Patterns directory not found", style="red")
                return False
            
            pattern_resolver = PatternResolver(patterns_dir)
            pattern_resolver.load_all_patterns()
            console.print(f"📊 Loaded {len(pattern_resolver.loaded_patterns)} patterns", style="green")
        
        return True
    except Exception as e:
        console.print(f"❌ Inheritance/pattern validation error: {e}", style="red")
        return False


def _display_build_statistics(console: Console, built_agents: List[Path], composer: AgentComposer) -> None:
    """Display statistics about trait inheritance and pattern resolution."""
    if hasattr(composer, 'trait_statistics'):
        stats = composer.trait_statistics
        table = Table(title="Trait Inheritance Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green")
        
        table.add_row("Traits Resolved", str(stats.get('traits_resolved', 0)))
        table.add_row("Patterns Applied", str(stats.get('patterns_applied', 0)))
        table.add_row("Dependencies Resolved", str(stats.get('dependencies_resolved', 0)))
        
        console.print(table)


def _display_enhanced_build_results(console: Console, build_result: Dict[str, Any]) -> None:
    """Display enhanced build results with comprehensive information."""
    if build_result['success']:
        console.print("✅ Enhanced build completed successfully!", style="green")
        
        # Build statistics
        stats = build_result.get('build_statistics', {})
        stats_table = Table(title="Build Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("Build Mode", build_result['build_mode'])
        stats_table.add_row("Validation Level", build_result['validation_level'])
        stats_table.add_row("Duration", f"{stats.get('duration', 0):.2f}s")
        stats_table.add_row("Agents Built", str(stats.get('agents_built', 0)))
        stats_table.add_row("Agents Failed", str(stats.get('agents_failed', 0)))
        
        if stats.get('traits_resolved', 0) > 0:
            stats_table.add_row("Traits Resolved", str(stats['traits_resolved']))
        if stats.get('patterns_applied', 0) > 0:
            stats_table.add_row("Patterns Applied", str(stats['patterns_applied']))
        
        console.print(stats_table)
        
        # Built agents
        if build_result['agents_built']:
            agents_table = Table(title="Successfully Built Agents")
            agents_table.add_column("Agent", style="cyan")
            agents_table.add_column("Output Path", style="green")
            
            for agent_result in build_result['agents_built']:
                agents_table.add_row(agent_result['name'], agent_result['output_path'])
            
            console.print(agents_table)
        
        # Validation summary
        validation = build_result.get('validation_summary', {})
        if validation.get('warning_count', 0) > 0:
            console.print(f"⚠️  {validation['warning_count']} validation warnings", style="yellow")
    else:
        console.print("❌ Enhanced build failed!", style="red")
        console.print(f"Reason: {build_result['failure_reason']}", style="red")
        
        # Show validation errors
        validation = build_result.get('validation_summary', {})
        if validation.get('errors'):
            console.print("\nValidation Errors:", style="red")
            for error in validation['errors'][:5]:  # Show first 5 errors
                console.print(f"  • {error}", style="dim red")
            
            if len(validation['errors']) > 5:
                console.print(f"  ... and {len(validation['errors']) - 5} more errors", style="dim red")


def _legacy_build_process(data_dir: Path, output_dir: Path, agent: List[str], use_inheritance: bool, 
                         use_patterns: bool, debug_traits: bool, validate: bool) -> None:
    """Execute legacy build process for backwards compatibility."""
    # Check system availability
    if use_inheritance and not INHERITANCE_AVAILABLE:
        console.print("⚠️  Trait inheritance system not available. Falling back to basic composition.", style="yellow")
        use_inheritance = False
    
    if use_patterns and not PATTERNS_AVAILABLE:
        console.print("⚠️  Pattern resolution system not available. Falling back to basic composition.", style="yellow")
        use_patterns = False
    
    if validate:
        console.print("🔍 Validating configurations...", style="yellow")
        validator = ConfigValidator(data_dir)
        if not validator.validate_all():
            console.print("❌ Validation failed. Aborting build.", style="red")
            sys.exit(1)
        
        # Additional validation for trait inheritance and patterns
        if use_inheritance or use_patterns:
            console.print("🔍 Validating trait inheritance and patterns...", style="yellow")
            if not _validate_inheritance_and_patterns(data_dir, use_inheritance, use_patterns):
                console.print("❌ Trait/pattern validation failed. Aborting build.", style="red")
                sys.exit(1)
        
        console.print("✅ Validation passed!", style="green")
    
    # Initialize composer with enhanced capabilities
    composer = AgentComposer(data_dir=data_dir, output_dir=output_dir)
    
    # Configure enhanced features
    if use_inheritance:
        console.print("🧬 Enabling trait inheritance system...", style="blue")
    if use_patterns:
        console.print("📋 Enabling pattern resolution...", style="blue")
    if debug_traits:
        console.print("🔧 Debug mode enabled for trait resolution", style="dim")
    
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
        
        # Display inheritance and pattern statistics
        if use_inheritance or use_patterns:
            _display_build_statistics(console, built_agents, composer)
        
        console.print(f"\n✅ Successfully built {len(built_agents)} agents", style="green")
    else:
        console.print("⚠️  No agents were built", style="yellow")


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
@click.option("--use-inheritance", is_flag=True, default=True, help="Use trait inheritance system")
@click.option("--use-patterns", is_flag=True, default=True, help="Use pattern library")
@click.option("--debug-traits", is_flag=True, help="Debug trait resolution process")
@click.option("--mode", type=click.Choice(['development', 'production', 'testing', 'ci_cd']), 
              default='development', help="Build mode with different optimizations")
@click.option("--validation-level", type=click.Choice(['relaxed', 'standard', 'strict', 'pedantic']),
              default='standard', help="Validation strictness level")
def build(data_dir: Path, output_dir: Path, agent: List[str], validate: bool, 
          use_inheritance: bool, use_patterns: bool, debug_traits: bool,
          mode: str, validation_level: str):
    """Build agent configurations with trait inheritance and pattern resolution."""
    
    # Import enhanced build system
    try:
        from .build_modes import BuildConfiguration, BuildMode, ValidationLevel, EnhancedBuildEngine
        ENHANCED_BUILD_AVAILABLE = True
    except ImportError:
        ENHANCED_BUILD_AVAILABLE = False
        console.print("⚠️  Enhanced build system not available. Using legacy build.", style="yellow")
    
    # Use enhanced build system if available
    if ENHANCED_BUILD_AVAILABLE:
        # Create build configuration from CLI options
        build_mode = BuildMode(mode)
        val_level = ValidationLevel(validation_level)
        
        config = BuildConfiguration(
            mode=build_mode,
            validation_level=val_level,
            use_trait_inheritance=use_inheritance,
            use_pattern_resolution=use_patterns,
            enable_debugging=debug_traits,
            fail_fast=(val_level in [ValidationLevel.STRICT, ValidationLevel.PEDANTIC])
        )
        
        console.print(f"🚀 Starting enhanced build in {mode} mode with {validation_level} validation", style="blue")
        
        # Initialize and run enhanced build engine
        engine = EnhancedBuildEngine(config, data_dir, output_dir)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Building with enhanced system...", total=None)
            
            agent_list = list(agent) if agent else None
            build_result = engine.validate_and_build(agent_list)
            
            progress.advance(task)
        
        # Display enhanced results
        _display_enhanced_build_results(console, build_result)
        
        # Exit with appropriate code
        if not build_result['success']:
            sys.exit(1)
    else:
        # Legacy build system fallback
        console.print("📦 Using legacy build system", style="yellow")
        _legacy_build_process(data_dir, output_dir, agent, use_inheritance, use_patterns, debug_traits, validate)


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
@click.option("--detailed", is_flag=True, help="Show detailed trait information")
@click.option("--category", "-c", help="Filter by trait category")
def list_traits(data_dir: Path, detailed: bool, category: Optional[str]):
    """List available traits with inheritance information."""
    traits_dir = data_dir / "traits"
    
    if not traits_dir.exists():
        console.print("❌ No traits directory found", style="red")
        return
    
    if INHERITANCE_AVAILABLE:
        # Use trait resolver for enhanced listing
        trait_paths = [traits_dir]
        resolver = TraitResolver(trait_paths)
        
        try:
            available_traits = resolver.get_available_traits()
            
            if category:
                available_traits = {category: available_traits.get(category, [])}
            
            for cat_name, trait_names in available_traits.items():
                if not trait_names:
                    continue
                
                console.print(f"\n[bold cyan]{cat_name.title()} Traits[/bold cyan]")
                
                table = Table()
                table.add_column("Name", style="cyan")
                if detailed:
                    table.add_column("Version", style="yellow")
                    table.add_column("Dependencies", style="dim")
                    table.add_column("Description", style="green")
                
                for trait_name in trait_names:
                    try:
                        if detailed:
                            trait_def = resolver.load_trait(trait_name)
                            deps = ", ".join(trait_def.dependencies) if trait_def.dependencies else "None"
                            table.add_row(
                                trait_name,
                                trait_def.version,
                                deps,
                                trait_def.description[:50] + "..." if len(trait_def.description) > 50 else trait_def.description
                            )
                        else:
                            table.add_row(trait_name)
                    except Exception as e:
                        if detailed:
                            table.add_row(trait_name, "Error", str(e), "Failed to load")
                        else:
                            table.add_row(trait_name)
                
                console.print(table)
        except Exception as e:
            console.print(f"❌ Error loading traits: {e}", style="red")
    else:
        # Fallback to basic file listing
        table = Table(title="Available Traits")
        table.add_column("Name", style="cyan")
        table.add_column("Category", style="yellow")
        table.add_column("File", style="green")
        
        for trait_file in traits_dir.rglob("*.yaml"):
            # Get relative path for nested traits
            rel_path = trait_file.relative_to(traits_dir)
            trait_name = str(rel_path.with_suffix(''))
            cat = rel_path.parent.name if rel_path.parent.name != "." else "root"
            
            if not category or cat == category:
                table.add_row(trait_name, cat, trait_file.name)
        
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


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path), 
              default="data", help="Data directory path")
@click.option("--trait", "-t", help="Validate specific trait")
@click.option("--agent", "-a", help="Validate traits for specific agent")
def validate_traits(data_dir: Path, trait: Optional[str], agent: Optional[str]):
    """Validate trait inheritance configurations."""
    if not INHERITANCE_AVAILABLE:
        console.print("❌ Trait inheritance system not available", style="red")
        sys.exit(1)
    
    traits_dir = data_dir / "traits"
    if not traits_dir.exists():
        console.print("❌ No traits directory found", style="red")
        sys.exit(1)
    
    resolver = TraitResolver([traits_dir])
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        if trait:
            # Validate specific trait
            task = progress.add_task(f"Validating trait {trait}...", total=None)
            try:
                trait_def = resolver.load_trait(trait)
                deps = resolver.resolve_dependencies(trait_def)
                
                console.print(f"✅ Trait '{trait}' is valid", style="green")
                if deps:
                    console.print(f"📋 Dependencies: {[d.name for d in deps]}", style="dim")
                
            except Exception as e:
                console.print(f"❌ Trait '{trait}' validation failed: {e}", style="red")
                sys.exit(1)
        
        elif agent:
            # Validate traits for specific agent
            task = progress.add_task(f"Validating agent {agent} traits...", total=None)
            
            personas_dir = data_dir / "personas"
            agent_file = personas_dir / f"{agent}.yaml"
            
            if not agent_file.exists():
                console.print(f"❌ Agent definition not found: {agent_file}", style="red")
                sys.exit(1)
            
            try:
                with open(agent_file, 'r') as f:
                    agent_data = yaml.safe_load(f)
                
                trait_names = agent_data.get('traits', [])
                if not trait_names:
                    console.print(f"⚠️  Agent '{agent}' has no traits defined", style="yellow")
                    return
                
                trait_refs = [TraitReference(name=name) for name in trait_names]
                all_traits = resolver.resolve_trait_chain(trait_refs)
                
                console.print(f"✅ Agent '{agent}' trait configuration is valid", style="green")
                console.print(f"📋 Resolved {len(all_traits)} traits total", style="dim")
                
            except Exception as e:
                console.print(f"❌ Agent '{agent}' trait validation failed: {e}", style="red")
                sys.exit(1)
        
        else:
            # Validate all traits
            task = progress.add_task("Validating all traits...", total=None)
            try:
                available_traits = resolver.get_available_traits()
                total_traits = sum(len(traits) for traits in available_traits.values())
                
                errors = []
                for category, trait_names in available_traits.items():
                    for trait_name in trait_names:
                        try:
                            resolver.load_trait(trait_name)
                        except Exception as e:
                            errors.append(f"{trait_name}: {e}")
                
                if errors:
                    console.print(f"❌ Found {len(errors)} trait validation errors:", style="red")
                    for error in errors:
                        console.print(f"  • {error}", style="dim")
                    sys.exit(1)
                else:
                    console.print(f"✅ All {total_traits} traits are valid", style="green")
                
            except Exception as e:
                console.print(f"❌ Trait validation failed: {e}", style="red")
                sys.exit(1)


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path), 
              default="data", help="Data directory path")
def list_patterns(data_dir: Path):
    """List available patterns from the pattern library."""
    patterns_dir = data_dir / "patterns"
    
    if not patterns_dir.exists():
        console.print("❌ No patterns directory found", style="red")
        return
    
    if PATTERNS_AVAILABLE:
        try:
            pattern_resolver = PatternResolver(patterns_dir)
            pattern_resolver.load_all_patterns()
            
            if not pattern_resolver.loaded_patterns:
                console.print("⚠️  No patterns found", style="yellow")
                return
            
            # Group patterns by type
            pattern_types = {}
            for pattern_name, pattern_data in pattern_resolver.loaded_patterns.items():
                pattern_type = pattern_data.get('type', 'unknown')
                if pattern_type not in pattern_types:
                    pattern_types[pattern_type] = []
                pattern_types[pattern_type].append((pattern_name, pattern_data))
            
            for pattern_type, patterns in pattern_types.items():
                console.print(f"\n[bold cyan]{pattern_type.title()} Patterns[/bold cyan]")
                
                table = Table()
                table.add_column("Name", style="cyan")
                table.add_column("Version", style="yellow") 
                table.add_column("Description", style="green")
                
                for pattern_name, pattern_data in patterns:
                    table.add_row(
                        pattern_name,
                        pattern_data.get('version', '1.0.0'),
                        pattern_data.get('description', 'No description')[:60] + "..."
                        if len(pattern_data.get('description', '')) > 60
                        else pattern_data.get('description', 'No description')
                    )
                
                console.print(table)
                
        except Exception as e:
            console.print(f"❌ Error loading patterns: {e}", style="red")
    else:
        # Fallback to basic file listing
        table = Table(title="Available Pattern Files")
        table.add_column("Type", style="cyan")
        table.add_column("Name", style="yellow")
        table.add_column("File", style="green")
        
        pattern_dirs = ["workflows", "coordination", "procedures", "templates"]
        for pattern_dir in pattern_dirs:
            pattern_path = patterns_dir / pattern_dir
            if pattern_path.exists():
                for pattern_file in pattern_path.glob("*.yaml"):
                    table.add_row(pattern_dir, pattern_file.stem, pattern_file.name)
        
        console.print(table)


@cli.command()
@click.option("--data-dir", "-d", type=click.Path(exists=True, path_type=Path), 
              default="data", help="Data directory path")
@click.option("--trait", "-t", required=True, help="Trait to analyze")
@click.option("--show-implementation", is_flag=True, help="Show trait implementation")
def analyze_trait(data_dir: Path, trait: str, show_implementation: bool):
    """Analyze a specific trait and its dependencies."""
    if not INHERITANCE_AVAILABLE:
        console.print("❌ Trait inheritance system not available", style="red")
        sys.exit(1)
    
    traits_dir = data_dir / "traits"
    resolver = TraitResolver([traits_dir])
    
    try:
        trait_def = resolver.load_trait(trait)
        
        # Basic information
        info_table = Table(title=f"Trait Analysis: {trait}")
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="green")
        
        info_table.add_row("Name", trait_def.name)
        info_table.add_row("Version", trait_def.version)
        info_table.add_row("Category", trait_def.category)
        info_table.add_row("Description", trait_def.description)
        
        console.print(info_table)
        
        # Dependencies
        if trait_def.dependencies:
            deps_table = Table(title="Dependencies")
            deps_table.add_column("Dependency", style="yellow")
            deps_table.add_column("Status", style="green")
            
            for dep_name in trait_def.dependencies:
                try:
                    resolver.load_trait(dep_name)
                    status = "✅ Available"
                except Exception:
                    status = "❌ Missing"
                
                deps_table.add_row(dep_name, status)
            
            console.print(deps_table)
        
        # Parameters
        if trait_def.parameters:
            params_table = Table(title="Parameters")
            params_table.add_column("Parameter", style="cyan")
            params_table.add_column("Type", style="yellow")
            params_table.add_column("Required", style="green")
            params_table.add_column("Default", style="dim")
            
            for param_name, param_def in trait_def.parameters.items():
                params_table.add_row(
                    param_name,
                    param_def.type,
                    "Yes" if param_def.required else "No",
                    str(param_def.default) if param_def.default is not None else "None"
                )
            
            console.print(params_table)
        
        # Implementation
        if show_implementation and trait_def.implementation:
            console.print(f"\n[bold cyan]Implementation:[/bold cyan]")
            panel = Panel(trait_def.implementation, title="Trait Implementation", border_style="dim")
            console.print(panel)
            
    except Exception as e:
        console.print(f"❌ Failed to analyze trait '{trait}': {e}", style="red")
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()