"""
Circular dependency detection for agent coordination graphs.

Implements Tarjan's algorithm for finding strongly connected components (SCCs)
to detect circular dependencies in agent coordination patterns.
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class CoordinationCycle:
    """Represents a circular dependency in the coordination graph."""
    agents: List[str]
    cycle_type: str  # 'direct' or 'transitive'

    def __str__(self) -> str:
        """Return a readable representation of the cycle."""
        cycle_str = " -> ".join(self.agents)
        return f"{self.cycle_type.capitalize()} cycle: {cycle_str} -> {self.agents[0]}"

    def __hash__(self) -> int:
        """Make cycle hashable for set operations."""
        return hash((frozenset(self.agents), self.cycle_type))

    def __eq__(self, other) -> bool:
        """Compare cycles based on agent sets, not order."""
        if not isinstance(other, CoordinationCycle):
            return False
        return (frozenset(self.agents) == frozenset(other.agents) and
                self.cycle_type == other.cycle_type)


class CircularDependencyDetector:
    """
    Detects circular dependencies in agent coordination graphs using Tarjan's algorithm.

    Tarjan's algorithm finds strongly connected components (SCCs) in directed graphs
    in O(V + E) time complexity, where V is vertices and E is edges.
    """

    def __init__(self):
        """Initialize the cycle detector."""
        self._index_counter = 0
        self._stack: List[str] = []
        self._lowlinks: Dict[str, int] = {}
        self._index: Dict[str, int] = {}
        self._on_stack: Set[str] = set()
        self._sccs: List[Set[str]] = []

    def detect_cycles(self, coordination_graph: Dict[str, List[str]]) -> List[CoordinationCycle]:
        """
        Detect all circular dependencies in the coordination graph.

        Args:
            coordination_graph: Adjacency list representation where keys are agent names
                              and values are lists of agents they coordinate with.

        Returns:
            List of CoordinationCycle objects representing detected cycles.
            Empty list if no cycles are found.

        Example:
            >>> detector = CircularDependencyDetector()
            >>> graph = {
            ...     'python-engineer': ['qa-engineer'],
            ...     'qa-engineer': ['technical-writer'],
            ...     'technical-writer': ['python-engineer']
            ... }
            >>> cycles = detector.detect_cycles(graph)
            >>> len(cycles) > 0
            True
        """
        # Reset state for new detection
        self._reset_state()

        # Run Tarjan's algorithm on each unvisited node
        for agent in coordination_graph.keys():
            if agent not in self._index:
                self._strongconnect(agent, coordination_graph)

        # Convert SCCs to CoordinationCycle objects
        cycles = []
        for scc in self._sccs:
            if len(scc) > 1:
                # Multiple agents in SCC = cycle
                cycle_agents = list(scc)
                cycle_type = 'direct' if len(scc) == 2 else 'transitive'
                cycles.append(CoordinationCycle(agents=cycle_agents, cycle_type=cycle_type))
            elif len(scc) == 1:
                # Check for self-loop
                agent = list(scc)[0]
                if agent in coordination_graph.get(agent, []):
                    cycles.append(CoordinationCycle(agents=[agent], cycle_type='self'))

        return cycles

    def _strongconnect(self, agent: str, graph: Dict[str, List[str]]) -> None:
        """
        Tarjan's algorithm recursive helper for finding SCCs.

        Args:
            agent: Current agent being processed
            graph: Full coordination graph
        """
        # Set the depth index for this agent
        self._index[agent] = self._index_counter
        self._lowlinks[agent] = self._index_counter
        self._index_counter += 1
        self._stack.append(agent)
        self._on_stack.add(agent)

        # Consider successors of this agent
        for successor in graph.get(agent, []):
            if successor not in self._index:
                # Successor not yet visited; recurse on it
                self._strongconnect(successor, graph)
                self._lowlinks[agent] = min(self._lowlinks[agent], self._lowlinks[successor])
            elif successor in self._on_stack:
                # Successor is on stack and hence in the current SCC
                self._lowlinks[agent] = min(self._lowlinks[agent], self._index[successor])

        # If agent is a root node, pop the stack and generate an SCC
        if self._lowlinks[agent] == self._index[agent]:
            scc = set()
            while True:
                successor = self._stack.pop()
                self._on_stack.remove(successor)
                scc.add(successor)
                if successor == agent:
                    break
            self._sccs.append(scc)

    def _reset_state(self) -> None:
        """Reset internal state for new cycle detection."""
        self._index_counter = 0
        self._stack = []
        self._lowlinks = {}
        self._index = {}
        self._on_stack = set()
        self._sccs = []

    def has_cycles(self, coordination_graph: Dict[str, List[str]]) -> bool:
        """
        Check if the coordination graph has any cycles.

        Args:
            coordination_graph: Adjacency list representation

        Returns:
            True if cycles are detected, False otherwise.
        """
        cycles = self.detect_cycles(coordination_graph)
        return len(cycles) > 0

    def get_cycle_paths(self, cycle: CoordinationCycle,
                       coordination_graph: Dict[str, List[str]]) -> List[List[str]]:
        """
        Get all possible paths through a cycle.

        Args:
            cycle: The cycle to analyze
            coordination_graph: Full coordination graph

        Returns:
            List of paths, where each path is a list of agent names.
        """
        if cycle.cycle_type == 'self':
            return [[cycle.agents[0], cycle.agents[0]]]

        # For larger cycles, find actual paths using DFS
        paths = []
        cycle_agents = set(cycle.agents)

        def dfs_path(current: str, target: str, visited: Set[str], path: List[str]) -> None:
            """DFS to find paths from current to target within cycle."""
            for neighbor in coordination_graph.get(current, []):
                if neighbor == target and len(path) > 1:
                    # Found a path back to target, complete the cycle
                    paths.append(path + [target])
                    return
                elif neighbor in cycle_agents and neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs_path(neighbor, target, visited, path)
                    path.pop()
                    visited.remove(neighbor)

        # Find paths from first agent back to itself
        start_agent = cycle.agents[0]
        dfs_path(start_agent, start_agent, {start_agent}, [start_agent])

        return paths if paths else [cycle.agents + [cycle.agents[0]]]
