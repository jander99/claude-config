"""
Agent Composer - Core generation engine for generating Claude Code agents.

This module handles the generation of agents from unified YAML configurations
using Jinja2 templates to generate complete agent markdown files and 
data-driven global CLAUDE.md coordination guides.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel, Field


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
    traits: List[str] = Field(default_factory=list)
    custom_instructions: str = ""
    coordination_overrides: Dict[str, str] = Field(default_factory=dict)
    
    # Enhanced structured fields for data-driven agent behavior
    context_priming: Optional[str] = ""
    quality_criteria: Dict[str, Any] = Field(default_factory=dict)
    decision_frameworks: Dict[str, Any] = Field(default_factory=dict)
    boundaries: Dict[str, Any] = Field(default_factory=dict)
    common_failures: Dict[str, Any] = Field(default_factory=dict)




class AgentComposer:
    """Agent composition engine for building Claude Code agents from unified configurations."""
    
    def __init__(self, 
                 data_dir: Path = None, 
                 template_dir: Path = None,
                 output_dir: Path = None):
        """Initialize the composer with directory paths and enhanced capabilities."""
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
        """Generate complete agent markdown from unified configuration."""
        # Load traits referenced by the agent
        traits = [self.load_trait(trait) for trait in agent_config.traits]
        
        # Get the agent template
        template = self.jinja_env.get_template('agent.md.j2')
        
        # Render the agent with context
        render_context = {
            'agent': agent_config,
            'traits': traits
        }
        
        return template.render(**render_context)
    

    def build_agent(self, agent_name: str) -> Path:
        """Build a single agent from unified configuration."""
        logger.info(f"Building agent: {agent_name}")
        
        # Use unified format
        agent_config = self.load_agent(agent_name)
        agent_content = self.compose_agent(agent_config)
        output_name = agent_config.name
        
        # Ensure output directory exists
        agents_dir = self.output_dir / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        
        # Write agent file
        output_path = agents_dir / f"{output_name}.md"
        with open(output_path, 'w') as f:
            f.write(agent_content)
        
        logger.info(f"Agent {agent_name} built successfully: {output_path}")
        return output_path
    
    
    def build_all_agents(self) -> List[Path]:
        """Build all agents found in the personas directory."""
        personas_dir = self.data_dir / "personas"
        if not personas_dir.exists():
            return []
        
        built_agents = []
        
        # Process all agent files
        for persona_file in personas_dir.glob("*.yaml"):
            if persona_file.stem not in ["config"]:
                agent_name = persona_file.stem
                try:
                    agent_path = self.build_agent(agent_name)
                    built_agents.append(agent_path)
                except Exception as e:
                    print(f"Error building {agent_name}: {e}")
        
        return built_agents
    
    def load_all_agents(self) -> List[AgentConfig]:
        """Load all agent configurations from the personas directory."""
        personas_dir = self.data_dir / "personas"
        if not personas_dir.exists():
            return []
        
        agents = []
        for persona_file in personas_dir.glob("*.yaml"):
            if persona_file.stem not in ["config"]:
                try:
                    agent = self.load_agent(persona_file.stem)
                    agents.append(agent)
                except Exception as e:
                    logger.warning(f"Failed to load agent {persona_file.stem}: {e}")
        
        return agents
    
    def compose_global_claude_md(self) -> str:
        """Generate global CLAUDE.md from all agent configurations."""
        from datetime import datetime
        
        # Load all agents
        agents = self.load_all_agents()
        
        # Sort agents by tier and name for consistent output
        tier_order = {"haiku": 1, "sonnet": 2, "opus": 3}
        agents.sort(key=lambda a: (tier_order.get(a.model, 2), a.name))
        
        # Get the global template
        template = self.jinja_env.get_template('global-claude.md.j2')
        
        # Render the global configuration
        return template.render(
            agents=agents,
            timestamp=datetime.now(),
            agent_count=len(agents)
        )