"""
CLAUDE.md Generator - Creates master orchestration file from agent YAML definitions.

This module processes agent coordination patterns and generates the global CLAUDE.md
file that Claude Code uses for agent delegation decisions.
"""

from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple
from datetime import datetime
import logging
import time
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader

from ..composer import AgentComposer, AgentConfig
from ..coordination.validator import CoordinationValidator, ValidationReport
from ..coordination.optimizer import GraphOptimizer, OptimizationResult

logger = logging.getLogger(__name__)


class CoordinationGraph:
    """Represents the agent coordination graph with metadata."""

    def __init__(
        self,
        adjacency_list: Dict[str, List[str]],
        agent_metadata: Dict[str, Dict[str, Any]],
        optimization_result: OptimizationResult
    ):
        """
        Initialize coordination graph.

        Args:
            adjacency_list: Adjacency list representation of graph
            agent_metadata: Metadata for each agent
            optimization_result: Pre-computed optimization data
        """
        self.adjacency_list = adjacency_list
        self.agent_metadata = agent_metadata
        self.optimization_result = optimization_result

    def get_agent_tier(self, agent_name: str) -> str:
        """Get the tier (haiku/sonnet/opus) for an agent."""
        metadata = self.agent_metadata.get(agent_name, {})
        return metadata.get('model', 'sonnet')

    def get_coordination_targets(self, agent_name: str) -> List[str]:
        """Get direct coordination targets for an agent."""
        return self.adjacency_list.get(agent_name, [])

    def get_all_reachable(self, agent_name: str) -> Set[str]:
        """Get all agents reachable from the given agent."""
        return self.optimization_result.get_all_descendants(agent_name)

    def is_entry_point(self, agent_name: str) -> bool:
        """Check if agent is an entry point (has file patterns)."""
        agent_info = self.optimization_result.get_agent_info(agent_name)
        return agent_info.get('is_entry_point', False) if agent_info else False


class OrchestrationRules:
    """Extracted orchestration rules from coordination graph."""

    def __init__(self):
        """Initialize empty orchestration rules."""
        self.mandatory_delegation: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        self.automatic_handoffs: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        self.parallel_patterns: List[Dict[str, Any]] = []
        self.task_decomposition: Dict[str, List[str]] = defaultdict(list)
        self.entry_point_mapping: Dict[str, List[str]] = defaultdict(list)

    def add_mandatory_delegation(
        self,
        trigger: str,
        agent: str,
        reason: str
    ) -> None:
        """Add a mandatory delegation rule."""
        self.mandatory_delegation[trigger].append((agent, reason))

    def add_automatic_handoff(
        self,
        source_agent: str,
        target_agent: str,
        condition: str
    ) -> None:
        """Add an automatic handoff rule."""
        self.automatic_handoffs[source_agent].append((target_agent, condition))

    def add_parallel_pattern(
        self,
        scenario: str,
        agents: List[str],
        coordination_strategy: str
    ) -> None:
        """Add a parallel execution pattern."""
        self.parallel_patterns.append({
            'scenario': scenario,
            'agents': agents,
            'coordination_strategy': coordination_strategy
        })

    def add_task_decomposition(
        self,
        task_type: str,
        agent_sequence: List[str]
    ) -> None:
        """Add a task decomposition pattern."""
        self.task_decomposition[task_type] = agent_sequence

    def add_entry_point(
        self,
        pattern: str,
        agents: List[str]
    ) -> None:
        """Add entry point mapping."""
        self.entry_point_mapping[pattern] = agents


class ClaudeMdGenerator:
    """
    Generator for master CLAUDE.md orchestration file.

    Processes all agent YAML definitions, extracts coordination patterns,
    validates and optimizes the coordination graph, and generates the
    master CLAUDE.md file using Jinja2 templates.
    """

    def __init__(
        self,
        data_dir: Optional[Path] = None,
        template_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        """
        Initialize the CLAUDE.md generator.

        Args:
            data_dir: Directory containing agent YAML files
            template_dir: Directory containing Jinja2 templates
            output_dir: Directory for generated output
        """
        self.data_dir = data_dir or Path("data")
        self.template_dir = template_dir or Path("src/claude_config/templates")
        self.output_dir = output_dir or Path("dist")

        # Initialize composer for loading agents
        self.composer = AgentComposer(
            data_dir=self.data_dir,
            template_dir=self.template_dir,
            output_dir=self.output_dir
        )

        # Initialize validation and optimization
        self.validator = CoordinationValidator(data_dir=self.data_dir)
        self.optimizer = GraphOptimizer()

        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def load_all_agents(self) -> List[AgentConfig]:
        """
        Load all agent YAML files from data/personas/.

        Returns:
            List of AgentConfig objects

        Example:
            >>> generator = ClaudeMdGenerator()
            >>> agents = generator.load_all_agents()
            >>> len(agents) > 0
            True
        """
        return self.composer.load_all_agents()

    def build_coordination_graph(
        self,
        agents: List[AgentConfig]
    ) -> CoordinationGraph:
        """
        Build coordination graph from agent configurations.

        Args:
            agents: List of agent configurations

        Returns:
            CoordinationGraph with adjacency list and metadata

        Example:
            >>> generator = ClaudeMdGenerator()
            >>> agents = generator.load_all_agents()
            >>> graph = generator.build_coordination_graph(agents)
            >>> isinstance(graph, CoordinationGraph)
            True
        """
        # Convert agents to dict format for validator
        agent_configs = {agent.name: agent.model_dump() for agent in agents}

        # Build adjacency list using validator
        adjacency_list = self.validator.build_coordination_graph(agent_configs)

        # Extract metadata
        agent_metadata = self.validator.extract_agent_metadata(agent_configs)

        # Find entry points
        entry_points = self.validator.find_entry_points(agent_configs)

        # Optimize graph
        optimization_result = self.optimizer.optimize(
            coordination_graph=adjacency_list,
            agent_metadata=agent_metadata,
            entry_points=entry_points
        )

        logger.info(
            f"Built coordination graph: {len(adjacency_list)} agents, "
            f"{len(entry_points)} entry points, "
            f"{optimization_result.optimization_stats['cached_paths']} cached paths"
        )

        return CoordinationGraph(
            adjacency_list=adjacency_list,
            agent_metadata=agent_metadata,
            optimization_result=optimization_result
        )

    def extract_orchestration_rules(
        self,
        graph: CoordinationGraph,
        agents: List[AgentConfig]
    ) -> OrchestrationRules:
        """
        Extract orchestration rules from coordination graph.

        Args:
            graph: Coordination graph
            agents: List of agent configurations

        Returns:
            OrchestrationRules with delegation patterns
        """
        rules = OrchestrationRules()

        # Build agent lookup by name
        agent_lookup = {agent.name: agent for agent in agents}

        # Extract mandatory delegation from file patterns
        for agent in agents:
            if hasattr(agent, 'proactive_triggers'):
                triggers = agent.proactive_triggers
                if isinstance(triggers, dict):
                    file_patterns = triggers.get('file_patterns', [])
                else:
                    file_patterns = getattr(triggers, 'file_patterns', [])

                for pattern in file_patterns:
                    rules.add_mandatory_delegation(
                        trigger=pattern,
                        agent=agent.name,
                        reason=f"File pattern match: {pattern}"
                    )

                    # Add to entry point mapping
                    existing = rules.entry_point_mapping.get(pattern, [])
                    if agent.name not in existing:
                        rules.entry_point_mapping[pattern].append(agent.name)

        # Extract automatic handoffs from coordination graph
        for agent_name, targets in graph.adjacency_list.items():
            agent = agent_lookup.get(agent_name)
            if not agent:
                continue

            for target in targets:
                # Determine condition based on traits and custom coordination
                condition = self._determine_handoff_condition(
                    agent, target, agent_lookup
                )
                rules.add_automatic_handoff(agent_name, target, condition)

        # Extract parallel patterns from multi-target coordination
        parallel_scenarios = self._extract_parallel_scenarios(graph, agent_lookup)
        for scenario in parallel_scenarios:
            rules.add_parallel_pattern(**scenario)

        # Extract task decomposition from common paths
        task_patterns = self._extract_task_patterns(graph, agent_lookup)
        for task_type, sequence in task_patterns.items():
            rules.add_task_decomposition(task_type, sequence)

        logger.info(
            f"Extracted orchestration rules: "
            f"{len(rules.mandatory_delegation)} delegation triggers, "
            f"{len(rules.automatic_handoffs)} handoff patterns, "
            f"{len(rules.parallel_patterns)} parallel patterns"
        )

        return rules

    def _determine_handoff_condition(
        self,
        source_agent: AgentConfig,
        target_agent_name: str,
        agent_lookup: Dict[str, AgentConfig]
    ) -> str:
        """Determine the condition for automatic handoff."""
        # Check coordination traits
        imports = source_agent.imports
        coordination_traits = imports.get('coordination', [])

        # Map common coordination patterns to conditions
        if 'qa-testing-handoff' in coordination_traits and target_agent_name == 'qa-engineer':
            return "After feature development completion"

        if 'documentation-handoff' in coordination_traits and target_agent_name == 'technical-writer':
            return "For user-facing features and APIs"

        if 'version-control-coordination' in coordination_traits and target_agent_name == 'git-helper':
            return "For all version control operations"

        # Check custom coordination
        custom = source_agent.custom_coordination
        for key, desc in custom.items():
            if target_agent_name in desc.lower():
                return desc

        # Default condition
        return f"When {source_agent.name} requires {target_agent_name} expertise"

    def _extract_parallel_scenarios(
        self,
        graph: CoordinationGraph,
        agent_lookup: Dict[str, AgentConfig]
    ) -> List[Dict[str, Any]]:
        """Extract parallel execution scenarios from graph."""
        scenarios = []

        # Common parallel patterns
        patterns = {
            'Full-Stack Feature': {
                'agents': ['frontend-engineer', 'python-engineer', 'database-engineer'],
                'strategy': 'Simultaneous development with API contract'
            },
            'Security Review': {
                'agents': ['security-engineer', 'qa-engineer', 'sr-architect'],
                'strategy': 'Multi-perspective vulnerability assessment'
            },
            'Performance Optimization': {
                'agents': ['performance-engineer', 'database-engineer', 'devops-engineer'],
                'strategy': 'Coordinated optimization across stack layers'
            }
        }

        for scenario, config in patterns.items():
            # Only include if all agents exist
            if all(agent in agent_lookup for agent in config['agents']):
                scenarios.append({
                    'scenario': scenario,
                    'agents': config['agents'],
                    'coordination_strategy': config['strategy']
                })

        return scenarios

    def _extract_task_patterns(
        self,
        graph: CoordinationGraph,
        agent_lookup: Dict[str, AgentConfig]
    ) -> Dict[str, List[str]]:
        """Extract common task decomposition patterns from graph."""
        patterns = {}

        # Define common workflow patterns
        workflows = {
            'Web Application Development': [
                'frontend-engineer',
                'python-engineer',
                'database-engineer',
                'qa-engineer',
                'technical-writer',
                'git-helper'
            ],
            'ML/AI Development': [
                'ai-researcher',
                'ai-engineer',
                'data-engineer',
                'qa-engineer',
                'technical-writer'
            ],
            'Infrastructure Development': [
                'devops-engineer',
                'security-engineer',
                'database-engineer',
                'qa-engineer',
                'technical-writer'
            ]
        }

        # Filter workflows to only include agents that exist
        for workflow_name, agent_sequence in workflows.items():
            filtered_sequence = [
                agent for agent in agent_sequence
                if agent in agent_lookup
            ]
            if len(filtered_sequence) >= 3:  # Only include substantial workflows
                patterns[workflow_name] = filtered_sequence

        return patterns

    def generate_agent_directory(
        self,
        agents: List[AgentConfig],
        graph: CoordinationGraph
    ) -> str:
        """
        Generate agent directory markdown section.

        Args:
            agents: List of agent configurations
            graph: Coordination graph

        Returns:
            Markdown formatted agent directory
        """
        # Group agents by tier
        tiers = {'haiku': [], 'sonnet': [], 'opus': []}
        for agent in agents:
            tier = agent.model.lower()
            if tier in tiers:
                tiers[tier].append(agent)

        lines = ["## Agent Directory\n"]

        tier_names = {
            'haiku': 'Tier 1: Efficiency Agents (Haiku)',
            'sonnet': 'Tier 2: Specialist Agents (Sonnet)',
            'opus': 'Tier 3: Senior Agents (Opus)'
        }

        for tier, tier_agents in tiers.items():
            if not tier_agents:
                continue

            lines.append(f"### {tier_names[tier]}\n")

            # Sort agents alphabetically within tier
            tier_agents.sort(key=lambda a: a.name)

            for agent in tier_agents:
                lines.append(f"**{agent.name}** `model: {agent.model}`")
                lines.append(f"- {agent.description}")

                # Add coordination targets
                targets = graph.get_coordination_targets(agent.name)
                if targets:
                    lines.append(f"- Coordinates with: {', '.join(targets)}")

                # Add proactive triggers
                if hasattr(agent, 'proactive_triggers'):
                    triggers = agent.proactive_triggers
                    if isinstance(triggers, dict):
                        patterns = triggers.get('file_patterns', [])
                    else:
                        patterns = getattr(triggers, 'file_patterns', [])

                    if patterns:
                        pattern_str = ', '.join(patterns[:3])
                        if len(patterns) > 3:
                            pattern_str += f", ... ({len(patterns)} total)"
                        lines.append(f"- Proactive on: {pattern_str}")

                lines.append("")

        return "\n".join(lines)

    def generate_mermaid_graph(
        self,
        graph: CoordinationGraph,
        agents: List[AgentConfig],
        max_nodes: int = 30
    ) -> str:
        """
        Generate Mermaid diagram of coordination graph.

        Args:
            graph: Coordination graph
            agents: List of agent configurations
            max_nodes: Maximum nodes to include in diagram

        Returns:
            Mermaid diagram code
        """
        # Color coding by tier
        tier_colors = {
            'haiku': '#90EE90',  # Light green
            'sonnet': '#87CEEB',  # Sky blue
            'opus': '#FFB6C1'    # Light pink
        }

        # Limit nodes to entry points and their immediate descendants
        agent_info = graph.optimization_result.agent_index
        entry_agents = [
            agent for agent in agents
            if agent_info.get(agent.name, {}).get('is_entry_point', False)
        ]

        # Select top entry agents by out-degree
        entry_agents.sort(
            key=lambda a: agent_info.get(a.name, {}).get('out_degree', 0),
            reverse=True
        )
        selected_entries = entry_agents[:min(10, len(entry_agents))]

        # Build visible node set
        visible_nodes = set()
        for agent in selected_entries:
            visible_nodes.add(agent.name)
            # Add immediate targets
            for target in graph.get_coordination_targets(agent.name):
                visible_nodes.add(target)
                if len(visible_nodes) >= max_nodes:
                    break
            if len(visible_nodes) >= max_nodes:
                break

        # Build Mermaid diagram
        lines = ["```mermaid", "graph TD"]

        # Add nodes with styling
        agent_lookup = {agent.name: agent for agent in agents}
        for node in visible_nodes:
            agent = agent_lookup.get(node)
            if not agent:
                continue

            tier = agent.model.lower()
            color = tier_colors.get(tier, '#CCCCCC')
            label = agent.display_name or agent.name

            lines.append(f"    {node}[{label}]")
            lines.append(f"    style {node} fill:{color}")

        # Add edges
        for node in visible_nodes:
            targets = graph.get_coordination_targets(node)
            for target in targets:
                if target in visible_nodes:
                    # Check if it's a trait-based handoff (solid) or custom (dashed)
                    agent = agent_lookup.get(node)
                    if agent and target in ['qa-engineer', 'technical-writer', 'git-helper']:
                        # Automatic handoff (solid arrow)
                        lines.append(f"    {node} --> {target}")
                    else:
                        # Optional coordination (dashed arrow)
                        lines.append(f"    {node} -.-> {target}")

        lines.append("```")
        return "\n".join(lines)

    def validate_before_generation(
        self,
        agents: List[AgentConfig]
    ) -> ValidationReport:
        """
        Validate coordination patterns before generating CLAUDE.md.

        Args:
            agents: List of agent configurations

        Returns:
            ValidationReport with validation results

        Raises:
            ValueError: If validation fails with errors
        """
        agent_configs = {agent.name: agent.model_dump() for agent in agents}
        report = self.validator.validate_coordination(agent_configs)

        if not report.is_valid:
            logger.error(f"Coordination validation failed:\n{report.summary()}")
            raise ValueError(f"Coordination validation failed: {len(report.errors)} errors")

        if report.has_warnings():
            logger.warning(f"Validation warnings:\n{report.summary()}")

        logger.info(f"Coordination validation passed: {len(agents)} agents validated")
        return report

    def generate_claude_md(
        self,
        output_path: Optional[Path] = None,
        validate: bool = True
    ) -> Path:
        """
        Generate the master CLAUDE.md file.

        Args:
            output_path: Path for generated CLAUDE.md (default: dist/CLAUDE.md)
            validate: Whether to validate coordination before generation

        Returns:
            Path to generated CLAUDE.md file

        Raises:
            ValueError: If validation fails and validate=True

        Example:
            >>> generator = ClaudeMdGenerator()
            >>> output = generator.generate_claude_md()
            >>> output.exists()
            True
        """
        start_time = time.time()

        # Load all agents
        logger.info("Loading all agent configurations...")
        agents = self.load_all_agents()

        if not agents:
            raise ValueError("No agent configurations found")

        # Validate coordination patterns
        if validate:
            logger.info("Validating coordination patterns...")
            self.validate_before_generation(agents)

        # Build coordination graph
        logger.info("Building coordination graph...")
        graph = self.build_coordination_graph(agents)

        # Extract orchestration rules
        logger.info("Extracting orchestration rules...")
        rules = self.extract_orchestration_rules(graph, agents)

        # Generate agent directory
        logger.info("Generating agent directory...")
        agent_directory = self.generate_agent_directory(agents, graph)

        # Generate Mermaid diagram
        logger.info("Generating coordination diagram...")
        mermaid_graph = self.generate_mermaid_graph(graph, agents)

        # Get optimization suggestions
        suggestions = self.optimizer.suggest_optimizations(
            graph.adjacency_list,
            graph.optimization_result
        )

        # Prepare template context
        template_context = {
            'timestamp': datetime.now(),
            'agent_count': len(agents),
            'agents': agents,
            'graph': graph,
            'rules': rules,
            'agent_directory': agent_directory,
            'mermaid_graph': mermaid_graph,
            'optimization_stats': graph.optimization_result.optimization_stats,
            'suggestions': suggestions
        }

        # Render template
        logger.info("Rendering CLAUDE.md template...")
        template = self.jinja_env.get_template('CLAUDE.md.j2')
        content = template.render(**template_context)

        # Write output
        if output_path is None:
            output_path = self.output_dir / "CLAUDE.md"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        elapsed = time.time() - start_time
        logger.info(
            f"CLAUDE.md generated successfully in {elapsed*1000:.0f}ms: {output_path}"
        )

        return output_path
