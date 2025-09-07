"""
Agent Composer - Core composition engine for generating Claude Code agents.

This module handles the composition of agents from personas, traits, and content
using Jinja2 templates to generate complete agent markdown files.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel, Field

# Trait inheritance system removed
INHERITANCE_AVAILABLE = False

# Import pattern resolver
try:
    import sys
    sys.path.append(str(Path("data/patterns/schemas")))
    from pattern_resolver import PatternResolver
    PATTERNS_AVAILABLE = True
except ImportError:
    PATTERNS_AVAILABLE = False

logger = logging.getLogger(__name__)


class TraitConfig(BaseModel):
    """Configuration for a reusable trait."""
    name: str
    category: str
    version: str = "1.0.0"
    description: str
    implementation: str
    coordination_patterns: List[Dict[str, Any]] = Field(default_factory=list)


class AgentConfig(BaseModel):
    """Unified agent configuration combining persona and composition."""
    name: str
    display_name: str
    model: str = "sonnet"
    description: str
    expertise: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    proactive_triggers: Dict[str, List[str]] = Field(default_factory=dict)
    content_sections: Dict[str, str] = Field(default_factory=dict)
    traits: List[str] = Field(default_factory=list)
    custom_instructions: str = ""
    coordination_overrides: Dict[str, str] = Field(default_factory=dict)


# Legacy models for backward compatibility during migration
class PersonaConfig(BaseModel):
    """Configuration for an agent persona."""
    name: str
    display_name: str
    model: str = "sonnet"
    description: str
    expertise: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    proactive_triggers: Dict[str, List[str]] = Field(default_factory=dict)
    content_sections: Dict[str, str] = Field(default_factory=dict)


class AgentComposition(BaseModel):
    """Complete agent composition definition."""
    name: str
    model: str = "sonnet"
    persona: Optional[str] = None
    traits: List[str] = Field(default_factory=list)
    custom_instructions: str = ""
    coordination_overrides: Dict[str, str] = Field(default_factory=dict)


class AgentComposer:
    """Enhanced composition engine with trait inheritance and pattern resolution."""
    
    def __init__(self, 
                 data_dir: Path = None, 
                 template_dir: Path = None,
                 output_dir: Path = None):
        """Initialize the composer with directory paths and enhanced capabilities."""
        self.data_dir = data_dir or Path("data")
        self.template_dir = template_dir or Path("src/claude_config/templates")
        self.output_dir = output_dir or Path("dist")
        
        # Enhanced features flags
        self.use_trait_inheritance = False
        self.use_pattern_resolution = False
        self.trait_debug_mode = False
        
        # Enhanced components
        self.trait_resolver = None
        self.trait_compositor = None
        self.pattern_resolver = None
        
        # Statistics tracking
        self.trait_statistics = {
            'traits_resolved': 0,
            'patterns_applied': 0,
            'dependencies_resolved': 0,
            'compositions_created': 0
        }
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Initialize enhanced features if available
        self._initialize_enhanced_features()
    
    def _initialize_enhanced_features(self):
        """Initialize trait inheritance and pattern resolution if available."""
        if INHERITANCE_AVAILABLE:
            trait_paths = [self.data_dir / "traits"]
            self.trait_resolver = TraitResolver(trait_paths)
            self.trait_compositor = TraitCompositor()
            logger.debug("Trait inheritance system initialized")
        
        if PATTERNS_AVAILABLE:
            patterns_dir = self.data_dir / "patterns"
            if patterns_dir.exists():
                self.pattern_resolver = PatternResolver(patterns_dir)
                self.pattern_resolver.load_all_patterns()
                logger.debug(f"Pattern resolver initialized with {len(self.pattern_resolver.loaded_patterns)} patterns")
    
    def enable_trait_inheritance(self):
        """Enable trait inheritance functionality."""
        if INHERITANCE_AVAILABLE and self.trait_resolver:
            self.use_trait_inheritance = True
            logger.info("Trait inheritance enabled")
        else:
            logger.warning("Cannot enable trait inheritance - components not available")
    
    def enable_pattern_resolution(self):
        """Enable pattern resolution functionality."""
        if PATTERNS_AVAILABLE and self.pattern_resolver:
            self.use_pattern_resolution = True
            logger.info("Pattern resolution enabled")
        else:
            logger.warning("Cannot enable pattern resolution - components not available")
    
    def enable_trait_debug(self):
        """Enable debug mode for trait resolution."""
        self.trait_debug_mode = True
        logger.info("Trait debug mode enabled")
    
    def load_agent(self, agent_name: str) -> AgentConfig:
        """Load a unified agent configuration from YAML."""
        agent_path = self.data_dir / "personas" / f"{agent_name}.yaml"
        if not agent_path.exists():
            raise FileNotFoundError(f"Agent not found: {agent_path}")
        
        with open(agent_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return AgentConfig(**data)

    def load_persona(self, persona_name: str) -> PersonaConfig:
        """Load a persona configuration from YAML. (Legacy method)"""
        persona_path = self.data_dir / "personas" / f"{persona_name}.yaml"
        if not persona_path.exists():
            raise FileNotFoundError(f"Persona not found: {persona_path}")
        
        with open(persona_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return PersonaConfig(**data)
    
    def load_trait(self, trait_name: str) -> TraitConfig:
        """Load a trait configuration from YAML."""
        # Handle nested trait names like "safety/branch-check"
        trait_path = self.data_dir / "traits" / f"{trait_name}.yaml"
        if not trait_path.exists():
            raise FileNotFoundError(f"Trait not found: {trait_path}")
        
        with open(trait_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return TraitConfig(**data)
    
    def load_content(self, content_path: str) -> str:
        """Load markdown content from the content directory."""
        full_path = self.data_dir / "content" / content_path
        if not full_path.exists():
            return f"<!-- Content not found: {content_path} -->"
        
        with open(full_path, 'r') as f:
            return f.read()
    
    def compose_agent(self, agent_config: AgentConfig) -> str:
        """Generate complete agent markdown with trait inheritance and pattern resolution."""
        # Enhanced trait processing with inheritance
        if self.use_trait_inheritance and agent_config.traits:
            traits, trait_composition = self._resolve_agent_traits(agent_config)
            self.trait_statistics['traits_resolved'] += len(traits)
            
            if self.trait_debug_mode:
                logger.info(f"Resolved {len(traits)} traits for agent {agent_config.name}")
                for trait in traits:
                    if hasattr(trait, 'name') and hasattr(trait, 'version'):
                        logger.debug(f"  - {trait.name} v{trait.version}")
        else:
            # Fallback to basic trait loading
            traits = [self.load_trait(trait) for trait in agent_config.traits]
            trait_composition = None
        
        # Enhanced content sections with pattern resolution
        content_sections = {}
        for section_name, content_path in agent_config.content_sections.items():
            content_sections[section_name] = self.load_content(content_path)
        
        # Apply pattern resolution if enabled
        if self.use_pattern_resolution:
            agent_dict = agent_config.dict()
            if 'patterns' in agent_dict or 'pattern_composition' in agent_dict:
                resolved_agent = self.pattern_resolver.inline_patterns_in_agent(agent_dict)
                agent_config = AgentConfig(**resolved_agent)
                self.trait_statistics['patterns_applied'] += len(resolved_agent.get('_resolved_patterns', {}))
        
        # Get the enhanced agent template
        template = self.jinja_env.get_template('agent.md.j2')
        
        # Render the complete agent with enhanced context
        render_context = {
            'agent': agent_config,
            'traits': traits,
            'content_sections': content_sections
        }
        
        # Add enhanced context if available
        if trait_composition:
            render_context['trait_composition'] = trait_composition
        
        if self.use_pattern_resolution and hasattr(agent_config, '_resolved_patterns'):
            render_context['resolved_patterns'] = getattr(agent_config, '_resolved_patterns', {})
        
        return template.render(**render_context)
    
    def _resolve_agent_traits(self, agent_config: AgentConfig) -> tuple:
        """Resolve agent traits using the inheritance system."""
        if not self.trait_resolver or not agent_config.traits:
            return [], None
        
        try:
            # Create trait references from agent configuration
            trait_refs = []
            for trait_name in agent_config.traits:
                if isinstance(trait_name, str):
                    trait_refs.append(TraitReference(name=trait_name))
                elif isinstance(trait_name, dict):
                    trait_refs.append(TraitReference(**trait_name))
            
            # Resolve the complete trait chain with dependencies
            resolved_traits = self.trait_resolver.resolve_trait_chain(trait_refs)
            self.trait_statistics['dependencies_resolved'] += len(resolved_traits) - len(trait_refs)
            
            # Create trait composition
            if self.trait_compositor:
                composition = self.trait_compositor.compose_traits(resolved_traits, trait_refs)
                self.trait_statistics['compositions_created'] += 1
                return resolved_traits, composition
            
            return resolved_traits, None
            
        except Exception as e:
            logger.error(f"Failed to resolve traits for agent {agent_config.name}: {e}")
            if self.trait_debug_mode:
                logger.exception("Trait resolution error details:")
            
            # Fallback to basic trait loading
            return [self.load_trait(trait) for trait in agent_config.traits if isinstance(trait, str)], None

    def compose_agent_legacy(self, composition: AgentComposition) -> str:
        """Generate complete agent markdown from composition. (Legacy method)"""
        # Load persona and traits
        persona = self.load_persona(composition.persona)
        traits = [self.load_trait(trait) for trait in composition.traits]
        
        # Load content sections
        content_sections = {}
        for section_name, content_path in persona.content_sections.items():
            content_sections[section_name] = self.load_content(content_path)
        
        # Get the agent template
        template = self.jinja_env.get_template('agent.md.j2')
        
        # Render the complete agent
        return template.render(
            composition=composition,
            persona=persona,
            traits=traits,
            content_sections=content_sections
        )
    
    def load_composition(self, composition_name: str) -> AgentComposition:
        """Load a composition configuration from YAML."""
        # Try composition-specific files first (e.g., python-engineer-composition.yaml)
        composition_path = self.data_dir / "personas" / f"{composition_name}-composition.yaml"
        if not composition_path.exists():
            # Fall back to regular persona files
            composition_path = self.data_dir / "personas" / f"{composition_name}.yaml"
        
        if not composition_path.exists():
            raise FileNotFoundError(f"Composition not found: {composition_name}")
        
        with open(composition_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return AgentComposition(**data)

    def build_agent(self, agent_name: str) -> Path:
        """Build a single agent with enhanced trait inheritance and pattern resolution."""
        logger.info(f"Building agent: {agent_name}")
        
        try:
            # Try new unified format first
            agent_config = self.load_agent(agent_name)
            agent_content = self.compose_agent(agent_config)
            output_name = agent_config.name
            
            # Enhanced output with metadata
            if self.use_trait_inheritance or self.use_pattern_resolution:
                agent_content = self._add_build_metadata(agent_content, agent_config)
                
        except (FileNotFoundError, TypeError) as e:
            logger.debug(f"Unified format failed for {agent_name}, trying legacy: {e}")
            # Fall back to legacy composition format
            composition = self.load_composition(agent_name)
            agent_content = self.compose_agent_legacy(composition)
            output_name = composition.name
        
        # Ensure output directory exists
        agents_dir = self.output_dir / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        
        # Write agent file
        output_path = agents_dir / f"{output_name}.md"
        with open(output_path, 'w') as f:
            f.write(agent_content)
        
        logger.info(f"Agent {agent_name} built successfully: {output_path}")
        return output_path
    
    def _add_build_metadata(self, content: str, agent_config: AgentConfig) -> str:
        """Add build metadata to agent content."""
        metadata_lines = [
            "<!-- Build Metadata -->",
            f"<!-- Agent: {agent_config.name} -->",
            f"<!-- Build System: Enhanced with trait inheritance and patterns -->",
        ]
        
        if self.use_trait_inheritance:
            metadata_lines.append(f"<!-- Traits Resolved: {self.trait_statistics['traits_resolved']} -->")
        
        if self.use_pattern_resolution:
            metadata_lines.append(f"<!-- Patterns Applied: {self.trait_statistics['patterns_applied']} -->")
        
        metadata_lines.append("<!-- End Build Metadata -->\n")
        
        return "\n".join(metadata_lines) + "\n\n" + content
    
    def build_all_agents(self) -> List[Path]:
        """Build all agents found in the personas directory."""
        personas_dir = self.data_dir / "personas"
        if not personas_dir.exists():
            return []
        
        built_agents = []
        processed_agents = set()
        
        # Process composition files first (they have priority)
        for composition_file in personas_dir.glob("*-composition.yaml"):
            agent_name = composition_file.stem.replace("-composition", "")
            if agent_name not in processed_agents:
                try:
                    agent_path = self.build_agent(agent_name)
                    built_agents.append(agent_path)
                    processed_agents.add(agent_name)
                except Exception as e:
                    print(f"Error building {agent_name}: {e}")
        
        # Then process regular persona files that don't have compositions
        for persona_file in personas_dir.glob("*.yaml"):
            if persona_file.stem not in ["config"] and not persona_file.stem.endswith("-composition"):
                agent_name = persona_file.stem
                if agent_name not in processed_agents:
                    try:
                        agent_path = self.build_agent(agent_name)
                        built_agents.append(agent_path)
                        processed_agents.add(agent_name)
                    except Exception as e:
                        print(f"Error building {agent_name}: {e}")
        
        return built_agents