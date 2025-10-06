"""
Consistency validation for agent coordination patterns.

Validates bidirectional consistency, trait compatibility, and reachability
in the agent coordination graph.
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class ConsistencyIssue:
    """Represents a consistency issue in agent coordination."""
    issue_type: str  # 'bidirectional', 'trait_compatibility', 'unreachable', 'missing_agent'
    severity: str  # 'error', 'warning', 'info'
    agents_involved: List[str]
    description: str
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable representation of the issue."""
        agents_str = ", ".join(self.agents_involved)
        msg = f"[{self.severity.upper()}] {self.issue_type}: {self.description}"
        if self.agents_involved:
            msg += f" (Agents: {agents_str})"
        if self.suggestion:
            msg += f"\n  Suggestion: {self.suggestion}"
        return msg


class ConsistencyValidator:
    """
    Validates consistency of agent coordination patterns.

    Checks:
    1. Bidirectional consistency: If A→B then B should know about A
    2. Trait compatibility: Coordinating agents have compatible traits
    3. Reachability: All agents are reachable from some entry point
    4. Missing agents: Referenced agents actually exist
    """

    def __init__(self):
        """Initialize the consistency validator."""
        self.issues: List[ConsistencyIssue] = []

    def validate_bidirectional_consistency(
        self,
        coordination_graph: Dict[str, List[str]],
        agent_metadata: Optional[Dict[str, Dict]] = None
    ) -> List[ConsistencyIssue]:
        """
        Validate bidirectional consistency in coordination patterns.

        If agent A coordinates with agent B, then B should have some awareness
        of A (either in its coordination patterns or trait imports).

        Args:
            coordination_graph: Adjacency list of agent coordination
            agent_metadata: Optional metadata about agents including trait imports

        Returns:
            List of ConsistencyIssue objects for bidirectional inconsistencies.

        Example:
            >>> validator = ConsistencyValidator()
            >>> graph = {
            ...     'python-engineer': ['qa-engineer'],
            ...     'qa-engineer': []
            ... }
            >>> issues = validator.validate_bidirectional_consistency(graph)
            >>> len(issues) > 0
            True
        """
        issues = []
        agent_metadata = agent_metadata or {}

        for source_agent, target_agents in coordination_graph.items():
            for target_agent in target_agents:
                # Check if target agent has reverse reference
                reverse_exists = False

                # Check in coordination graph
                if source_agent in coordination_graph.get(target_agent, []):
                    reverse_exists = True

                # Check in agent metadata (trait imports, custom coordination)
                if not reverse_exists and target_agent in agent_metadata:
                    metadata = agent_metadata[target_agent]

                    # Check trait imports for coordination patterns
                    imports = metadata.get('imports', {})
                    coord_traits = imports.get('coordination', [])

                    # Check custom coordination patterns
                    custom_coord = metadata.get('custom_coordination', {})

                    # If target has coordination traits or custom patterns, consider it aware
                    if coord_traits or custom_coord:
                        reverse_exists = True

                if not reverse_exists:
                    issues.append(ConsistencyIssue(
                        issue_type='bidirectional',
                        severity='warning',
                        agents_involved=[source_agent, target_agent],
                        description=f"{source_agent} coordinates with {target_agent}, "
                                  f"but {target_agent} has no awareness of {source_agent}",
                        suggestion=f"Add bidirectional coordination or trait import to {target_agent}"
                    ))

        return issues

    def validate_trait_compatibility(
        self,
        coordination_graph: Dict[str, List[str]],
        agent_traits: Dict[str, List[str]]
    ) -> List[ConsistencyIssue]:
        """
        Validate that coordinating agents have compatible traits.

        Args:
            coordination_graph: Adjacency list of agent coordination
            agent_traits: Dictionary mapping agent names to their imported traits

        Returns:
            List of ConsistencyIssue objects for trait incompatibilities.

        Example:
            >>> validator = ConsistencyValidator()
            >>> graph = {'python-engineer': ['frontend-engineer']}
            >>> traits = {
            ...     'python-engineer': ['python-development-stack'],
            ...     'frontend-engineer': ['javascript-development-stack']
            ... }
            >>> issues = validator.validate_trait_compatibility(graph, traits)
        """
        issues = []

        # Common trait categories that should align
        coordination_traits = {
            'qa-testing-handoff',
            'documentation-handoff',
            'version-control-coordination',
            'standard-safety-protocols'
        }

        for source_agent, target_agents in coordination_graph.items():
            source_traits = set(agent_traits.get(source_agent, []))

            for target_agent in target_agents:
                target_traits = set(agent_traits.get(target_agent, []))

                # Check if they share at least one coordination trait
                shared_coord_traits = source_traits.intersection(target_traits).intersection(coordination_traits)

                if not shared_coord_traits and coordination_traits.intersection(source_traits):
                    issues.append(ConsistencyIssue(
                        issue_type='trait_compatibility',
                        severity='info',
                        agents_involved=[source_agent, target_agent],
                        description=f"{source_agent} and {target_agent} coordinate but share no "
                                  f"common coordination traits",
                        suggestion="Consider adding shared coordination traits for consistency"
                    ))

        return issues

    def find_unreachable_agents(
        self,
        coordination_graph: Dict[str, List[str]],
        entry_points: Optional[List[str]] = None
    ) -> List[ConsistencyIssue]:
        """
        Find agents that are unreachable from any entry point.

        Args:
            coordination_graph: Adjacency list of agent coordination
            entry_points: Optional list of entry point agents (e.g., agents with file patterns)
                         If not provided, all agents with no incoming edges are considered entry points.

        Returns:
            List of ConsistencyIssue objects for unreachable agents.
        """
        issues = []

        # If no entry points provided, find agents with no incoming edges
        if entry_points is None:
            all_targets = set()
            for targets in coordination_graph.values():
                all_targets.update(targets)

            entry_points = [agent for agent in coordination_graph.keys()
                          if agent not in all_targets]

        if not entry_points:
            # No entry points means isolated graph
            return [ConsistencyIssue(
                issue_type='unreachable',
                severity='error',
                agents_involved=list(coordination_graph.keys()),
                description="No entry points found - coordination graph is isolated",
                suggestion="Add file patterns or proactive triggers to at least one agent"
            )]

        # Perform BFS from all entry points to find reachable agents
        reachable = set()
        queue = list(entry_points)

        while queue:
            current = queue.pop(0)
            if current in reachable:
                continue

            reachable.add(current)
            queue.extend(coordination_graph.get(current, []))

        # Find unreachable agents
        all_agents = set(coordination_graph.keys())
        unreachable = all_agents - reachable

        for agent in unreachable:
            issues.append(ConsistencyIssue(
                issue_type='unreachable',
                severity='warning',
                agents_involved=[agent],
                description=f"Agent {agent} is unreachable from any entry point",
                suggestion="Add coordination from reachable agents or make this an entry point"
            ))

        return issues

    def validate_agent_existence(
        self,
        coordination_graph: Dict[str, List[str]],
        defined_agents: Set[str]
    ) -> List[ConsistencyIssue]:
        """
        Validate that all referenced agents exist.

        Args:
            coordination_graph: Adjacency list of agent coordination
            defined_agents: Set of agent names that are actually defined

        Returns:
            List of ConsistencyIssue objects for missing agents.
        """
        issues = []

        for source_agent, target_agents in coordination_graph.items():
            # Check if source agent exists
            if source_agent not in defined_agents:
                issues.append(ConsistencyIssue(
                    issue_type='missing_agent',
                    severity='error',
                    agents_involved=[source_agent],
                    description=f"Source agent {source_agent} is not defined",
                    suggestion=f"Create {source_agent}.yaml or remove from coordination graph"
                ))

            # Check if target agents exist
            for target_agent in target_agents:
                if target_agent not in defined_agents:
                    issues.append(ConsistencyIssue(
                        issue_type='missing_agent',
                        severity='error',
                        agents_involved=[source_agent, target_agent],
                        description=f"{source_agent} references undefined agent {target_agent}",
                        suggestion=f"Create {target_agent}.yaml or remove from {source_agent}'s coordination"
                    ))

        return issues

    def validate_all(
        self,
        coordination_graph: Dict[str, List[str]],
        agent_metadata: Optional[Dict[str, Dict]] = None,
        agent_traits: Optional[Dict[str, List[str]]] = None,
        defined_agents: Optional[Set[str]] = None,
        entry_points: Optional[List[str]] = None
    ) -> List[ConsistencyIssue]:
        """
        Run all consistency validations.

        Args:
            coordination_graph: Adjacency list of agent coordination
            agent_metadata: Optional metadata about agents
            agent_traits: Optional trait imports for agents
            defined_agents: Optional set of defined agent names
            entry_points: Optional list of entry point agents

        Returns:
            Combined list of all consistency issues.
        """
        all_issues = []

        # Validate agent existence first
        if defined_agents is not None:
            all_issues.extend(self.validate_agent_existence(coordination_graph, defined_agents))

        # Only proceed with other validations if agents exist
        if not any(issue.issue_type == 'missing_agent' and issue.severity == 'error'
                  for issue in all_issues):

            # Bidirectional consistency
            all_issues.extend(self.validate_bidirectional_consistency(
                coordination_graph, agent_metadata
            ))

            # Trait compatibility
            if agent_traits is not None:
                all_issues.extend(self.validate_trait_compatibility(
                    coordination_graph, agent_traits
                ))

            # Unreachable agents
            all_issues.extend(self.find_unreachable_agents(
                coordination_graph, entry_points
            ))

        return all_issues
