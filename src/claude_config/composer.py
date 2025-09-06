"""
Agent Composer - Core composition engine for generating Claude Code agents.

This module handles the composition of agents from personas, traits, and content
using Jinja2 templates to generate complete agent markdown files.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel, Field


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
    persona: str
    traits: List[str] = Field(default_factory=list)
    custom_instructions: str = ""
    coordination_overrides: Dict[str, str] = Field(default_factory=dict)


class AgentComposer:
    """Main composition engine for generating Claude Code agents."""
    
    def __init__(self, 
                 data_dir: Path = None, 
                 template_dir: Path = None,
                 output_dir: Path = None):
        """Initialize the composer with directory paths."""
        self.data_dir = data_dir or Path("data")
        self.template_dir = template_dir or Path("src/claude_config/templates")
        self.output_dir = output_dir or Path("dist")
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
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
        """Generate complete agent markdown from unified agent configuration."""
        # Load traits
        traits = [self.load_trait(trait) for trait in agent_config.traits]
        
        # Load content sections
        content_sections = {}
        for section_name, content_path in agent_config.content_sections.items():
            content_sections[section_name] = self.load_content(content_path)
        
        # Get the agent template
        template = self.jinja_env.get_template('agent.md.j2')
        
        # Render the complete agent
        return template.render(
            agent=agent_config,
            traits=traits,
            content_sections=content_sections
        )

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
        """Build a single agent and save to output directory."""
        try:
            # Try new unified format first
            agent_config = self.load_agent(agent_name)
            agent_content = self.compose_agent(agent_config)
            output_name = agent_config.name
        except (FileNotFoundError, TypeError):
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
        
        return output_path
    
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