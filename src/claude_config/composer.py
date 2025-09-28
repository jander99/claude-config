"""
Agent Composer - Core generation engine for generating Claude Code agents.

This module handles the generation of agents from unified YAML configurations
using Jinja2 templates to generate complete agent markdown files and 
data-driven global CLAUDE.md coordination guides.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import yaml
import logging
import re
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel, Field



logger = logging.getLogger(__name__)


class TechnologyFramework(BaseModel):
    """Configuration for a technology framework."""
    name: str
    version: str = ""
    use_cases: List[str] = Field(default_factory=list)
    alternatives: List[str] = Field(default_factory=list)
    configuration: Optional[str] = None
    config_language: Optional[str] = None


class TechnologyStack(BaseModel):
    """Technology stack configuration."""
    primary_frameworks: List[TechnologyFramework] = Field(default_factory=list)
    essential_tools: Dict[str, List[str]] = Field(default_factory=dict)


class ImplementationPattern(BaseModel):
    """Implementation pattern with code examples."""
    pattern: str
    context: str
    code_example: Optional[str] = None
    language: str = "python"
    best_practices: List[str] = Field(default_factory=list)
    common_pitfalls: List[str] = Field(default_factory=list)


class ProfessionalStandards(BaseModel):
    """Professional standards and compliance."""
    security_frameworks: List[str] = Field(default_factory=list)
    industry_practices: List[str] = Field(default_factory=list)
    compliance_requirements: List[str] = Field(default_factory=list)


class IntegrationGuidelines(BaseModel):
    """Integration guidelines for various services."""
    api_integration: List[str] = Field(default_factory=list)
    database_integration: List[str] = Field(default_factory=list)
    third_party_services: List[str] = Field(default_factory=list)


class PerformanceBenchmarks(BaseModel):
    """Performance benchmarks and targets."""
    response_times: List[str] = Field(default_factory=list)
    throughput_targets: List[str] = Field(default_factory=list)
    resource_utilization: List[str] = Field(default_factory=list)


class TroubleshootingGuide(BaseModel):
    """Troubleshooting guide entry."""
    issue: str
    symptoms: List[str] = Field(default_factory=list)
    solutions: List[str] = Field(default_factory=list)
    prevention: List[str] = Field(default_factory=list)


class ToolConfiguration(BaseModel):
    """Tool configuration settings."""
    tool: str
    config_file: Optional[str] = None
    recommended_settings: Dict[str, Any] = Field(default_factory=dict)
    integration_notes: Optional[str] = None
    setup_commands: List[str] = Field(default_factory=list)
    format: str = "ini"


class TraitConfig(BaseModel):
    """Configuration for a reusable trait."""
    name: str
    category: str
    version: str = "1.0.0"
    description: str
    implementation: str
    coordination_patterns: List[Dict[str, Any]] = Field(default_factory=list)


class TraitContent(BaseModel):
    """Parsed trait content from markdown files."""
    name: str
    category: str
    description: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


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

    # Enhanced trait import support
    imports: Dict[str, List[str]] = Field(default_factory=dict)  # e.g., {"coordination": ["standard-safety"], "tools": ["python-ml-stack"]}
    custom_coordination: Dict[str, str] = Field(default_factory=dict)  # Agent-specific overrides
    custom_tools: List[ToolConfiguration] = Field(default_factory=list)  # Additional tools
    
    # Enhanced structured fields for data-driven agent behavior
    context_priming: Optional[str] = ""
    quality_criteria: Dict[str, Any] = Field(default_factory=dict)
    decision_frameworks: Dict[str, Any] = Field(default_factory=dict)
    boundaries: Dict[str, Any] = Field(default_factory=dict)
    common_failures: Dict[str, Any] = Field(default_factory=dict)
    
    # Rich content schema fields for comprehensive agent content
    technology_stack: Optional[TechnologyStack] = None
    implementation_patterns: List[ImplementationPattern] = Field(default_factory=list)
    professional_standards: Optional[ProfessionalStandards] = None
    integration_guidelines: Optional[IntegrationGuidelines] = None
    performance_benchmarks: Optional[PerformanceBenchmarks] = None
    troubleshooting_guides: List[TroubleshootingGuide] = Field(default_factory=list)
    tool_configurations: List[ToolConfiguration] = Field(default_factory=list)




class TraitProcessor:
    """Processes trait imports and merges content for agents."""

    def __init__(self, traits_dir: Path):
        """Initialize trait processor with traits directory."""
        self.traits_dir = traits_dir
        self._trait_cache: Dict[str, TraitContent] = {}

    def load_trait_markdown(self, trait_path: str) -> TraitContent:
        """Load and parse a trait markdown file."""
        if trait_path in self._trait_cache:
            return self._trait_cache[trait_path]

        # Support both category/trait-name and direct trait-name paths
        full_path = self.traits_dir / f"{trait_path}.md"
        if not full_path.exists():
            raise FileNotFoundError(f"Trait not found: {full_path}")

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse YAML frontmatter if present
        metadata = {}
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    if frontmatter:
                        metadata = yaml.safe_load(frontmatter)
                    content = parts[2].strip()
            except yaml.YAMLError:
                # If frontmatter parsing fails, treat as regular markdown
                pass

        # Extract trait name and category from path or metadata
        trait_name = metadata.get('name', trait_path.split('/')[-1])
        category = metadata.get('category', trait_path.split('/')[0] if '/' in trait_path else 'general')
        description = metadata.get('description', self._extract_description_from_content(content))

        trait_content = TraitContent(
            name=trait_name,
            category=category,
            description=description,
            content=content,
            metadata=metadata
        )

        self._trait_cache[trait_path] = trait_content
        return trait_content

    def _extract_description_from_content(self, content: str) -> str:
        """Extract description from content if no frontmatter description."""
        # Look for ## Description section
        desc_match = re.search(r'## Description\n\n(.+?)(?:\n## |\Z)', content, re.DOTALL)
        if desc_match:
            return desc_match.group(1).strip()

        # Fallback to first paragraph
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                return line

        return "No description available"

    def process_agent_imports(self, agent_config: AgentConfig) -> Dict[str, Any]:
        """Process trait imports for an agent and return merged content."""
        merged_content = {
            'coordination_traits': {},
            'tool_traits': {},
            'safety_traits': {},
            'enhancement_traits': {},
            'custom_coordination': agent_config.custom_coordination,
            'custom_tools': agent_config.custom_tools
        }

        # Process imports by category
        for category, trait_names in agent_config.imports.items():
            trait_content = {}

            for trait_name in trait_names:
                try:
                    trait_path = f"{category}/{trait_name}"
                    trait = self.load_trait_markdown(trait_path)
                    trait_content[trait_name] = {
                        'name': trait.name,
                        'description': trait.description,
                        'content': trait.content,
                        'metadata': trait.metadata
                    }
                except FileNotFoundError:
                    logger.warning(f"Trait not found: {trait_path} for agent {agent_config.name}")
                    trait_content[trait_name] = {
                        'name': trait_name,
                        'description': f"Missing trait: {trait_name}",
                        'content': f"<!-- Trait {trait_name} not found at {trait_path} -->",
                        'metadata': {}
                    }

            # Map category to appropriate content section
            if category == 'coordination':
                merged_content['coordination_traits'] = trait_content
            elif category == 'tools':
                merged_content['tool_traits'] = trait_content
            elif category == 'safety':
                merged_content['safety_traits'] = trait_content
            elif category == 'enhancement':
                merged_content['enhancement_traits'] = trait_content
            else:
                # Handle custom categories
                merged_content[f"{category}_traits"] = trait_content

        return merged_content


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

        # Initialize trait processor
        traits_dir = Path("src/claude_config/traits")
        self.trait_processor = TraitProcessor(traits_dir)

        # Initialize MCP processor

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
        # Load legacy traits referenced by the agent (for backward compatibility)
        legacy_traits = []
        if agent_config.traits:
            try:
                legacy_traits = [self.load_trait(trait) for trait in agent_config.traits]
            except Exception as e:
                logger.warning(f"Failed to load legacy traits for {agent_config.name}: {e}")

        # Process new trait imports
        imported_traits = {}
        if agent_config.imports:
            try:
                imported_traits = self.trait_processor.process_agent_imports(agent_config)
            except Exception as e:
                logger.error(f"Failed to process trait imports for {agent_config.name}: {e}")
                # Continue with empty imported traits rather than failing

        # Get the agent template
        template = self.jinja_env.get_template('agent.md.j2')

        # Render the agent with enhanced context
        render_context = {
            'agent': agent_config,
            'traits': legacy_traits,  # Legacy trait support
            'imported_traits': imported_traits,  # New trait import system
            'has_imports': bool(agent_config.imports),
            'has_legacy_traits': bool(agent_config.traits)
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
        
        # Process all agent files in alphabetical order
        persona_files = sorted(personas_dir.glob("*.yaml"), key=lambda p: p.stem)
        for persona_file in persona_files:
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

