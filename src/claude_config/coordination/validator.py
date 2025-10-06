"""
Main coordination validation orchestrator.

Coordinates cycle detection, consistency checking, and trait validation
to provide comprehensive validation of agent coordination patterns.
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import yaml
import logging

from .cycle_detector import CircularDependencyDetector, CoordinationCycle
from .consistency import ConsistencyValidator, ConsistencyIssue

logger = logging.getLogger(__name__)


@dataclass
class ValidationReport:
    """Comprehensive validation report for agent coordination."""
    is_valid: bool
    cycles: List[CoordinationCycle] = field(default_factory=list)
    consistency_issues: List[ConsistencyIssue] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def has_errors(self) -> bool:
        """Check if report has any errors."""
        return bool(self.errors or self.cycles or
                   any(issue.severity == 'error' for issue in self.consistency_issues))

    def has_warnings(self) -> bool:
        """Check if report has any warnings."""
        return bool(self.warnings or
                   any(issue.severity == 'warning' for issue in self.consistency_issues))

    def summary(self) -> str:
        """Generate a summary string of the validation report."""
        lines = []

        if self.is_valid:
            lines.append("✅ Coordination validation PASSED")
        else:
            lines.append("❌ Coordination validation FAILED")

        # Cycles
        if self.cycles:
            lines.append(f"\n🔄 Circular Dependencies: {len(self.cycles)}")
            for cycle in self.cycles:
                lines.append(f"  - {cycle}")

        # Consistency issues by severity
        errors = [i for i in self.consistency_issues if i.severity == 'error']
        warnings = [i for i in self.consistency_issues if i.severity == 'warning']
        info = [i for i in self.consistency_issues if i.severity == 'info']

        if errors:
            lines.append(f"\n❌ Errors: {len(errors)}")
            for issue in errors[:5]:  # Show first 5
                lines.append(f"  - {issue.description}")
            if len(errors) > 5:
                lines.append(f"  ... and {len(errors) - 5} more")

        if warnings:
            lines.append(f"\n⚠️  Warnings: {len(warnings)}")
            for issue in warnings[:5]:
                lines.append(f"  - {issue.description}")
            if len(warnings) > 5:
                lines.append(f"  ... and {len(warnings) - 5} more")

        if info:
            lines.append(f"\nℹ️  Info: {len(info)}")

        # General errors/warnings
        if self.errors:
            lines.append(f"\n❌ General Errors: {len(self.errors)}")
            for error in self.errors[:3]:
                lines.append(f"  - {error}")

        if self.warnings:
            lines.append(f"\n⚠️  General Warnings: {len(self.warnings)}")
            for warning in self.warnings[:3]:
                lines.append(f"  - {warning}")

        return "\n".join(lines)


class CoordinationValidator:
    """
    Main orchestrator for coordination validation.

    Coordinates cycle detection, consistency validation, and trait checking
    to provide comprehensive validation of agent coordination patterns.
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the coordination validator.

        Args:
            data_dir: Path to data directory containing agent configurations
        """
        self.data_dir = data_dir or Path("data")
        self.cycle_detector = CircularDependencyDetector()
        self.consistency_validator = ConsistencyValidator()

    def build_coordination_graph(
        self,
        agent_configs: Dict[str, Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """
        Build coordination graph from agent configurations.

        Args:
            agent_configs: Dictionary of agent configurations

        Returns:
            Adjacency list representation of coordination graph
        """
        graph = {}

        for agent_name, config in agent_configs.items():
            coordinated_agents = []

            # Extract coordination from custom_coordination
            custom_coord = config.get('custom_coordination', {})
            for coord_key, coord_desc in custom_coord.items():
                # Parse coordination description to extract agent names
                # Looking for patterns like "coordinates with ai-engineer"
                words = coord_desc.lower().split()
                for i, word in enumerate(words):
                    if word in ['coordinates', 'handoff', 'delegates'] and i + 2 < len(words):
                        if words[i + 1] in ['with', 'to']:
                            potential_agent = words[i + 2].rstrip('.,;:')
                            if potential_agent in agent_configs:
                                coordinated_agents.append(potential_agent)

            # Extract coordination from trait imports
            imports = config.get('imports', {})
            coordination_traits = imports.get('coordination', [])

            # Common coordination patterns from traits
            if 'qa-testing-handoff' in coordination_traits:
                if 'qa-engineer' in agent_configs:
                    coordinated_agents.append('qa-engineer')

            if 'documentation-handoff' in coordination_traits:
                if 'technical-writer' in agent_configs:
                    coordinated_agents.append('technical-writer')

            if 'version-control-coordination' in coordination_traits:
                if 'git-helper' in agent_configs:
                    coordinated_agents.append('git-helper')

            # Remove duplicates while preserving order
            seen = set()
            unique_coordinated = []
            for agent in coordinated_agents:
                if agent not in seen:
                    seen.add(agent)
                    unique_coordinated.append(agent)

            graph[agent_name] = unique_coordinated

        return graph

    def extract_agent_metadata(
        self,
        agent_configs: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Extract relevant metadata from agent configurations.

        Args:
            agent_configs: Dictionary of agent configurations

        Returns:
            Dictionary of agent metadata
        """
        metadata = {}

        for agent_name, config in agent_configs.items():
            metadata[agent_name] = {
                'imports': config.get('imports', {}),
                'custom_coordination': config.get('custom_coordination', {}),
                'proactive_activation': config.get('proactive_activation', {}),
                'model': config.get('model', 'sonnet')
            }

        return metadata

    def extract_agent_traits(
        self,
        agent_configs: Dict[str, Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """
        Extract trait imports from agent configurations.

        Args:
            agent_configs: Dictionary of agent configurations

        Returns:
            Dictionary mapping agent names to their trait lists
        """
        traits = {}

        for agent_name, config in agent_configs.items():
            all_traits = []
            imports = config.get('imports', {})

            for category, trait_list in imports.items():
                all_traits.extend(trait_list)

            traits[agent_name] = all_traits

        return traits

    def find_entry_points(
        self,
        agent_configs: Dict[str, Dict[str, Any]],
        coordination_graph: Optional[Dict[str, List[str]]] = None
    ) -> List[str]:
        """
        Find entry point agents (those with file patterns or no incoming edges).

        Entry points are agents that can be activated through:
        1. File pattern matching (proactive_activation.file_patterns)
        2. Direct user invocation (no incoming coordination edges)
        3. Always-available agents (git-helper, technical-writer)

        Args:
            agent_configs: Dictionary of agent configurations
            coordination_graph: Optional coordination graph to check for incoming edges

        Returns:
            List of agent names that are entry points
        """
        entry_points = []

        # Always-available agents that users can invoke directly
        always_available = {'git-helper', 'technical-writer'}

        # Build set of agents with incoming coordination edges
        agents_with_incoming = set()
        if coordination_graph:
            for source_agent, target_agents in coordination_graph.items():
                agents_with_incoming.update(target_agents)

        for agent_name, config in agent_configs.items():
            # Check for file pattern triggers
            proactive = config.get('proactive_activation', {})
            file_patterns = proactive.get('file_patterns', [])
            has_file_patterns = bool(file_patterns)

            # Check if agent has no incoming coordination edges
            has_no_incoming = agent_name not in agents_with_incoming

            # Check if agent is always available
            is_always_available = agent_name in always_available

            # Agent is an entry point if it has file patterns, no incoming edges, or is always available
            if has_file_patterns or has_no_incoming or is_always_available:
                entry_points.append(agent_name)

        return entry_points

    def validate_coordination(
        self,
        agent_configs: Dict[str, Dict[str, Any]]
    ) -> ValidationReport:
        """
        Perform comprehensive coordination validation.

        Args:
            agent_configs: Dictionary of agent configurations

        Returns:
            ValidationReport with all validation results

        Example:
            >>> validator = CoordinationValidator()
            >>> configs = {
            ...     'python-engineer': {
            ...         'imports': {'coordination': ['qa-testing-handoff']},
            ...         'custom_coordination': {}
            ...     },
            ...     'qa-engineer': {
            ...         'imports': {'coordination': ['standard-safety-protocols']},
            ...         'custom_coordination': {}
            ...     }
            ... }
            >>> report = validator.validate_coordination(configs)
            >>> report.is_valid
            True
        """
        report = ValidationReport(is_valid=True)

        try:
            # Build coordination graph
            coordination_graph = self.build_coordination_graph(agent_configs)
            logger.debug(f"Built coordination graph with {len(coordination_graph)} agents")

            # Extract metadata and traits
            agent_metadata = self.extract_agent_metadata(agent_configs)
            agent_traits = self.extract_agent_traits(agent_configs)
            defined_agents = set(agent_configs.keys())
            entry_points = self.find_entry_points(agent_configs, coordination_graph)

            # 1. Detect cycles
            cycles = self.cycle_detector.detect_cycles(coordination_graph)
            report.cycles = cycles

            if cycles:
                report.errors.append(f"Found {len(cycles)} circular dependencies")
                logger.error(f"Circular dependencies detected: {len(cycles)}")

            # 2. Validate consistency
            consistency_issues = self.consistency_validator.validate_all(
                coordination_graph=coordination_graph,
                agent_metadata=agent_metadata,
                agent_traits=agent_traits,
                defined_agents=defined_agents,
                entry_points=entry_points
            )
            report.consistency_issues = consistency_issues

            # Categorize consistency issues
            for issue in consistency_issues:
                if issue.severity == 'error':
                    report.errors.append(f"{issue.issue_type}: {issue.description}")
                elif issue.severity == 'warning':
                    report.warnings.append(f"{issue.issue_type}: {issue.description}")
                else:
                    report.info.append(f"{issue.issue_type}: {issue.description}")

            # Determine overall validity
            report.is_valid = not report.has_errors()

            logger.info(f"Validation complete: {len(cycles)} cycles, "
                       f"{len(consistency_issues)} consistency issues")

        except Exception as e:
            report.is_valid = False
            report.errors.append(f"Validation failed: {str(e)}")
            logger.exception("Coordination validation failed")

        return report

    def load_and_validate(self, agent_names: Optional[List[str]] = None) -> ValidationReport:
        """
        Load agent configurations from disk and validate.

        Args:
            agent_names: Optional list of specific agents to validate.
                        If None, validates all agents.

        Returns:
            ValidationReport with validation results
        """
        personas_dir = self.data_dir / "personas"
        if not personas_dir.exists():
            return ValidationReport(
                is_valid=False,
                errors=[f"Personas directory not found: {personas_dir}"]
            )

        agent_configs = {}

        # Load configurations
        if agent_names is None:
            # Load all agents
            for yaml_file in personas_dir.glob("*.yaml"):
                if yaml_file.stem not in ["config"]:
                    try:
                        with open(yaml_file, 'r') as f:
                            config = yaml.safe_load(f)
                            agent_configs[yaml_file.stem] = config
                    except Exception as e:
                        logger.warning(f"Failed to load {yaml_file.stem}: {e}")
        else:
            # Load specific agents
            for agent_name in agent_names:
                yaml_file = personas_dir / f"{agent_name}.yaml"
                if yaml_file.exists():
                    try:
                        with open(yaml_file, 'r') as f:
                            config = yaml.safe_load(f)
                            agent_configs[agent_name] = config
                    except Exception as e:
                        logger.warning(f"Failed to load {agent_name}: {e}")

        return self.validate_coordination(agent_configs)
