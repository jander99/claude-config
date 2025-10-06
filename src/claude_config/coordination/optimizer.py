"""
Graph optimization for coordination patterns.

Pre-computes transitive relationships, builds indices for fast lookups,
and generates decision trees for common coordination scenarios.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """Results from graph optimization."""
    transitive_closure: Dict[str, Set[str]] = field(default_factory=dict)
    agent_index: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    common_paths: Dict[Tuple[str, str], List[str]] = field(default_factory=dict)
    entry_point_paths: Dict[str, List[List[str]]] = field(default_factory=dict)
    optimization_stats: Dict[str, Any] = field(default_factory=dict)

    def get_all_descendants(self, agent: str) -> Set[str]:
        """Get all agents reachable from the given agent."""
        return self.transitive_closure.get(agent, set())

    def get_path(self, source: str, target: str) -> Optional[List[str]]:
        """Get cached path between two agents."""
        return self.common_paths.get((source, target))

    def get_agent_info(self, agent: str) -> Optional[Dict[str, Any]]:
        """Get indexed information about an agent."""
        return self.agent_index.get(agent)


class GraphOptimizer:
    """
    Optimizes coordination graph for runtime performance.

    Performs:
    1. Transitive closure computation (pre-compute all reachable agents)
    2. Path caching for common coordination patterns
    3. Agent indexing for fast lookups
    4. Decision tree generation for common scenarios
    """

    def __init__(self):
        """Initialize the graph optimizer."""
        self.optimization_cache: Optional[OptimizationResult] = None

    def compute_transitive_closure(
        self,
        coordination_graph: Dict[str, List[str]]
    ) -> Dict[str, Set[str]]:
        """
        Compute transitive closure of the coordination graph.

        Uses Floyd-Warshall algorithm to find all reachable agents
        from each agent in O(V^3) time.

        Args:
            coordination_graph: Adjacency list representation

        Returns:
            Dictionary mapping each agent to set of all reachable agents

        Example:
            >>> optimizer = GraphOptimizer()
            >>> graph = {
            ...     'python-engineer': ['qa-engineer'],
            ...     'qa-engineer': ['technical-writer'],
            ...     'technical-writer': []
            ... }
            >>> closure = optimizer.compute_transitive_closure(graph)
            >>> 'technical-writer' in closure['python-engineer']
            True
        """
        agents = list(coordination_graph.keys())
        n = len(agents)
        agent_to_idx = {agent: i for i, agent in enumerate(agents)}

        # Initialize reachability matrix
        reachable = [[False] * n for _ in range(n)]

        # Set direct edges
        for i, agent in enumerate(agents):
            reachable[i][i] = True  # Agent can reach itself
            for target in coordination_graph.get(agent, []):
                if target in agent_to_idx:
                    j = agent_to_idx[target]
                    reachable[i][j] = True

        # Floyd-Warshall for transitive closure
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    reachable[i][j] = reachable[i][j] or (reachable[i][k] and reachable[k][j])

        # Convert to dictionary format
        closure = {}
        for i, agent in enumerate(agents):
            reachable_agents = {agents[j] for j in range(n)
                              if reachable[i][j] and i != j}
            closure[agent] = reachable_agents

        logger.debug(f"Computed transitive closure for {n} agents")
        return closure

    def build_agent_index(
        self,
        coordination_graph: Dict[str, List[str]],
        agent_metadata: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Build fast lookup index for agent information.

        Args:
            coordination_graph: Adjacency list representation
            agent_metadata: Agent metadata including traits, patterns, etc.

        Returns:
            Indexed agent information for fast lookups
        """
        index = {}

        for agent in coordination_graph.keys():
            metadata = agent_metadata.get(agent, {})

            # Compute in-degree and out-degree
            out_degree = len(coordination_graph.get(agent, []))
            in_degree = sum(1 for targets in coordination_graph.values()
                          if agent in targets)

            index[agent] = {
                'out_degree': out_degree,
                'in_degree': in_degree,
                'is_entry_point': in_degree == 0,
                'is_terminal': out_degree == 0,
                'model': metadata.get('model', 'sonnet'),
                'traits': metadata.get('imports', {}).get('coordination', []),
                'file_patterns': metadata.get('proactive_activation', {}).get('file_patterns', [])
            }

        logger.debug(f"Built agent index for {len(index)} agents")
        return index

    def cache_common_paths(
        self,
        coordination_graph: Dict[str, List[str]],
        max_path_length: int = 5
    ) -> Dict[Tuple[str, str], List[str]]:
        """
        Pre-compute and cache common coordination paths using BFS.

        Args:
            coordination_graph: Adjacency list representation
            max_path_length: Maximum path length to cache

        Returns:
            Dictionary mapping (source, target) to shortest path
        """
        paths = {}

        def bfs_path(start: str, end: str) -> Optional[List[str]]:
            """Find shortest path using BFS."""
            if start == end:
                return [start]

            visited = {start}
            queue = [(start, [start])]

            while queue:
                current, path = queue.pop(0)

                if len(path) > max_path_length:
                    continue

                for neighbor in coordination_graph.get(current, []):
                    if neighbor == end:
                        return path + [neighbor]

                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

            return None

        # Cache paths between all pairs of agents
        agents = list(coordination_graph.keys())
        for source in agents:
            for target in agents:
                if source != target:
                    path = bfs_path(source, target)
                    if path:
                        paths[(source, target)] = path

        logger.debug(f"Cached {len(paths)} common paths")
        return paths

    def generate_entry_point_paths(
        self,
        coordination_graph: Dict[str, List[str]],
        entry_points: List[str]
    ) -> Dict[str, List[List[str]]]:
        """
        Generate all paths from entry points for fast orchestration decisions.

        Args:
            coordination_graph: Adjacency list representation
            entry_points: List of entry point agents

        Returns:
            Dictionary mapping entry points to all possible coordination paths
        """
        entry_paths = {}

        def dfs_all_paths(
            current: str,
            visited: Set[str],
            path: List[str],
            max_depth: int = 5
        ) -> List[List[str]]:
            """DFS to find all paths from current node."""
            paths = []

            if len(path) >= max_depth:
                return paths

            for neighbor in coordination_graph.get(current, []):
                if neighbor not in visited:
                    new_visited = visited | {neighbor}
                    new_path = path + [neighbor]
                    paths.append(new_path)

                    # Continue DFS
                    deeper_paths = dfs_all_paths(neighbor, new_visited, new_path, max_depth)
                    paths.extend(deeper_paths)

            return paths

        for entry_point in entry_points:
            paths = dfs_all_paths(entry_point, {entry_point}, [entry_point])
            entry_paths[entry_point] = paths

        logger.debug(f"Generated paths for {len(entry_points)} entry points")
        return entry_paths

    def optimize(
        self,
        coordination_graph: Dict[str, List[str]],
        agent_metadata: Dict[str, Dict[str, Any]],
        entry_points: Optional[List[str]] = None
    ) -> OptimizationResult:
        """
        Perform full graph optimization.

        Args:
            coordination_graph: Adjacency list representation
            agent_metadata: Agent metadata
            entry_points: Optional list of entry point agents

        Returns:
            OptimizationResult with all optimization data
        """
        import time
        start_time = time.time()

        # 1. Compute transitive closure
        transitive_closure = self.compute_transitive_closure(coordination_graph)

        # 2. Build agent index
        agent_index = self.build_agent_index(coordination_graph, agent_metadata)

        # 3. Cache common paths
        common_paths = self.cache_common_paths(coordination_graph)

        # 4. Generate entry point paths
        if entry_points is None:
            entry_points = [agent for agent, info in agent_index.items()
                          if info['is_entry_point']]

        entry_point_paths = self.generate_entry_point_paths(
            coordination_graph, entry_points
        )

        # Calculate statistics
        optimization_time = time.time() - start_time
        stats = {
            'total_agents': len(coordination_graph),
            'entry_points': len(entry_points),
            'cached_paths': len(common_paths),
            'optimization_time_ms': round(optimization_time * 1000, 2),
            'avg_out_degree': sum(len(targets) for targets in coordination_graph.values()) / len(coordination_graph),
            'max_transitive_reach': max(len(agents) for agents in transitive_closure.values()) if transitive_closure else 0
        }

        result = OptimizationResult(
            transitive_closure=transitive_closure,
            agent_index=agent_index,
            common_paths=common_paths,
            entry_point_paths=entry_point_paths,
            optimization_stats=stats
        )

        self.optimization_cache = result
        logger.info(f"Graph optimization complete in {stats['optimization_time_ms']}ms")

        return result

    def suggest_optimizations(
        self,
        coordination_graph: Dict[str, List[str]],
        optimization_result: OptimizationResult
    ) -> List[str]:
        """
        Suggest optimizations based on graph analysis.

        Args:
            coordination_graph: Adjacency list representation
            optimization_result: Results from optimization

        Returns:
            List of optimization suggestions
        """
        suggestions = []
        agent_index = optimization_result.agent_index

        # Find bottleneck agents (high in-degree)
        high_in_degree = [(agent, info['in_degree'])
                         for agent, info in agent_index.items()
                         if info['in_degree'] > 5]

        if high_in_degree:
            high_in_degree.sort(key=lambda x: x[1], reverse=True)
            agent, degree = high_in_degree[0]
            suggestions.append(
                f"Agent '{agent}' has high in-degree ({degree}). "
                f"Consider splitting responsibilities or adding intermediate agents."
            )

        # Find long coordination chains
        long_chains = [(key, len(path)) for key, path in optimization_result.common_paths.items()
                      if len(path) > 4]

        if long_chains:
            long_chains.sort(key=lambda x: x[1], reverse=True)
            (source, target), length = long_chains[0]
            suggestions.append(
                f"Long coordination chain from '{source}' to '{target}' ({length} hops). "
                f"Consider direct coordination or intermediate delegation."
            )

        # Find isolated entry points
        isolated_entry = [agent for agent, info in agent_index.items()
                         if info['is_entry_point'] and info['out_degree'] == 0]

        if isolated_entry:
            suggestions.append(
                f"Isolated entry points found: {', '.join(isolated_entry[:3])}. "
                f"Consider adding coordination patterns."
            )

        # Check for balanced model usage
        model_counts = defaultdict(int)
        for info in agent_index.values():
            model_counts[info['model']] += 1

        if model_counts.get('opus', 0) > len(agent_index) * 0.3:
            suggestions.append(
                f"High opus usage ({model_counts['opus']} agents). "
                f"Consider using sonnet for standard coordination tasks."
            )

        return suggestions
