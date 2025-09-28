"""
Cross-agent integration testing framework.

Tests coordination patterns, trait inheritance, and agent ecosystem consistency.
"""

import pytest
import yaml
import tempfile
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple
from claude_config.composer import AgentComposer
from claude_config.validator import ConfigValidator


class CrossAgentIntegrationFramework:
    """Framework for testing cross-agent integration patterns."""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path("data")
        self.traits_dir = Path("src/claude_config/traits")
        self.composer = AgentComposer(self.data_dir)
        self.validator = ConfigValidator(self.data_dir)

    def analyze_coordination_patterns(self) -> Dict[str, Any]:
        """Analyze coordination patterns across agents."""
        coordination_analysis = {
            "total_agents": 0,
            "coordination_patterns": {},
            "trait_usage": {},
            "model_distribution": {"haiku": [], "sonnet": [], "opus": []},
            "expertise_overlap": {},
            "responsibility_gaps": []
        }

        personas_dir = self.data_dir / "personas"
        if not personas_dir.exists():
            return coordination_analysis

        for agent_file in personas_dir.glob("*.yaml"):
            try:
                with open(agent_file, 'r') as f:
                    agent_data = yaml.safe_load(f)

                agent_name = agent_file.stem
                coordination_analysis["total_agents"] += 1

                # Model distribution
                model = agent_data.get('model', 'sonnet')
                if model in coordination_analysis["model_distribution"]:
                    coordination_analysis["model_distribution"][model].append(agent_name)

                # Trait usage analysis
                if 'imports' in agent_data:
                    for category, traits in agent_data['imports'].items():
                        for trait in traits:
                            trait_key = f"{category}/{trait}"
                            if trait_key not in coordination_analysis["trait_usage"]:
                                coordination_analysis["trait_usage"][trait_key] = []
                            coordination_analysis["trait_usage"][trait_key].append(agent_name)

                # Expertise overlap analysis
                if 'expertise' in agent_data:
                    for expertise in agent_data['expertise']:
                        expertise_lower = expertise.lower()
                        if expertise_lower not in coordination_analysis["expertise_overlap"]:
                            coordination_analysis["expertise_overlap"][expertise_lower] = []
                        coordination_analysis["expertise_overlap"][expertise_lower].append(agent_name)

                # Coordination pattern detection
                if 'coordination' in agent_data.get('imports', {}):
                    coord_traits = agent_data['imports']['coordination']
                    for trait in coord_traits:
                        if trait not in coordination_analysis["coordination_patterns"]:
                            coordination_analysis["coordination_patterns"][trait] = []
                        coordination_analysis["coordination_patterns"][trait].append(agent_name)

            except Exception as e:
                print(f"Error analyzing {agent_file}: {e}")

        return coordination_analysis

    def validate_tier_consistency(self) -> List[str]:
        """Validate model tier consistency and appropriateness."""
        errors = []

        # Expected tier distributions (approximate)
        expected_tiers = {
            "haiku": ["git-helper", "technical-writer"],  # Efficiency agents
            "opus": [  # Strategic agents
                "sr-architect", "sr-ai-researcher", "sr-quant-analyst",
                "integration-architect", "subagent-generator"
            ]
        }

        personas_dir = self.data_dir / "personas"
        if not personas_dir.exists():
            return ["No personas directory found"]

        for tier, expected_agents in expected_tiers.items():
            for expected_agent in expected_agents:
                agent_file = personas_dir / f"{expected_agent}.yaml"
                if agent_file.exists():
                    try:
                        with open(agent_file, 'r') as f:
                            agent_data = yaml.safe_load(f)

                        actual_model = agent_data.get('model', 'sonnet')
                        if actual_model != tier:
                            errors.append(
                                f"Agent {expected_agent} should be {tier} tier, "
                                f"but is {actual_model}"
                            )
                    except Exception as e:
                        errors.append(f"Error checking {expected_agent}: {e}")

        return errors

    def validate_trait_coordination(self) -> List[str]:
        """Validate trait coordination across agents."""
        errors = []

        # Essential coordination traits that should be widely used
        essential_traits = [
            "coordination/standard-safety-protocols",
            "coordination/qa-testing-handoff",
            "coordination/version-control-coordination"
        ]

        coordination_analysis = self.analyze_coordination_patterns()

        for trait in essential_traits:
            if trait not in coordination_analysis["trait_usage"]:
                errors.append(f"Essential trait {trait} is not used by any agent")
            else:
                usage_count = len(coordination_analysis["trait_usage"][trait])
                if usage_count < 3:  # Should be used by at least 3 agents
                    errors.append(
                        f"Essential trait {trait} only used by {usage_count} agents "
                        f"(minimum 3 recommended)"
                    )

        return errors

    def validate_expertise_coverage(self) -> List[str]:
        """Validate that expertise areas have appropriate coverage."""
        errors = []

        coordination_analysis = self.analyze_coordination_patterns()
        expertise_overlap = coordination_analysis["expertise_overlap"]

        # Critical expertise areas that should have multiple agents
        critical_expertise = [
            "testing", "security", "performance", "documentation",
            "python", "javascript", "api", "database"
        ]

        for expertise in critical_expertise:
            # Check for exact or partial matches
            coverage_count = 0
            covering_agents = []

            for exp_key, agents in expertise_overlap.items():
                if expertise.lower() in exp_key or exp_key in expertise.lower():
                    coverage_count += len(agents)
                    covering_agents.extend(agents)

            if coverage_count == 0:
                errors.append(f"No agents cover critical expertise: {expertise}")
            elif coverage_count == 1:
                errors.append(
                    f"Only one agent covers critical expertise {expertise}: "
                    f"{covering_agents[0]}"
                )

        return errors

    def test_agent_generation_consistency(self) -> Tuple[bool, List[str]]:
        """Test that all agents generate consistently."""
        errors = []

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            try:
                composer = AgentComposer(
                    data_dir=self.data_dir,
                    output_dir=output_dir
                )

                personas_dir = self.data_dir / "personas"
                if not personas_dir.exists():
                    return False, ["No personas directory found"]

                generation_stats = {}

                for agent_file in personas_dir.glob("*.yaml"):
                    agent_name = agent_file.stem

                    try:
                        output_path = composer.build_agent(agent_name)

                        if output_path and output_path.exists():
                            with open(output_path, 'r') as f:
                                content = f.read()

                            stats = {
                                "file_size": len(content),
                                "line_count": len(content.splitlines()),
                                "word_count": len(content.split()),
                                "has_coordination_section": "## Coordination" in content,
                                "has_expertise_section": "## Expertise" in content
                            }
                            generation_stats[agent_name] = stats

                            # Validate minimum content requirements
                            if stats["file_size"] < 3000:  # Minimum 3KB
                                errors.append(
                                    f"Agent {agent_name} output too small: "
                                    f"{stats['file_size']} bytes"
                                )

                            if stats["line_count"] < 100:  # Minimum 100 lines
                                errors.append(
                                    f"Agent {agent_name} insufficient content: "
                                    f"{stats['line_count']} lines"
                                )

                        else:
                            errors.append(f"Failed to generate agent: {agent_name}")

                    except Exception as e:
                        errors.append(f"Generation error for {agent_name}: {e}")

                # Consistency checks across all generated agents
                if generation_stats:
                    sizes = [stats["file_size"] for stats in generation_stats.values()]
                    avg_size = sum(sizes) / len(sizes)
                    min_size = min(sizes)
                    max_size = max(sizes)

                    # Check for extreme variations (may indicate problems)
                    if max_size > avg_size * 3:  # More than 3x average
                        outliers = [
                            name for name, stats in generation_stats.items()
                            if stats["file_size"] > avg_size * 3
                        ]
                        errors.append(f"Unusually large agents: {', '.join(outliers)}")

                    if min_size < avg_size * 0.3:  # Less than 30% of average
                        outliers = [
                            name for name, stats in generation_stats.items()
                            if stats["file_size"] < avg_size * 0.3
                        ]
                        errors.append(f"Unusually small agents: {', '.join(outliers)}")

            except Exception as e:
                errors.append(f"Integration test setup error: {e}")

        return len(errors) == 0, errors

    def validate_development_workflows(self) -> List[str]:
        """Validate common development workflow patterns."""
        errors = []

        # Common development workflows and expected agent coordination
        workflows = {
            "full_stack_development": [
                "frontend-engineer", "python-engineer", "database-engineer",
                "devops-engineer", "security-engineer", "qa-engineer"
            ],
            "ai_ml_pipeline": [
                "ai-researcher", "ai-engineer", "data-engineer",
                "python-engineer", "performance-engineer"
            ],
            "mobile_development": [
                "mobile-engineer", "python-engineer", "database-engineer",
                "security-engineer", "qa-engineer"
            ]
        }

        personas_dir = self.data_dir / "personas"
        if not personas_dir.exists():
            return ["No personas directory found"]

        existing_agents = set(f.stem for f in personas_dir.glob("*.yaml"))

        for workflow, required_agents in workflows.items():
            missing_agents = set(required_agents) - existing_agents
            if missing_agents:
                errors.append(
                    f"Workflow {workflow} missing agents: {', '.join(missing_agents)}"
                )

        return errors


@pytest.fixture
def integration_framework():
    """Create cross-agent integration framework."""
    return CrossAgentIntegrationFramework()


def test_coordination_patterns_analysis(integration_framework):
    """Test coordination patterns across all agents."""
    analysis = integration_framework.analyze_coordination_patterns()

    assert analysis["total_agents"] > 20, f"Expected >20 agents, found {analysis['total_agents']}"

    # Should have agents in all model tiers
    assert len(analysis["model_distribution"]["haiku"]) > 0, "No Haiku tier agents found"
    assert len(analysis["model_distribution"]["sonnet"]) > 0, "No Sonnet tier agents found"
    assert len(analysis["model_distribution"]["opus"]) > 0, "No Opus tier agents found"

    # Should have coordination patterns
    assert len(analysis["coordination_patterns"]) > 0, "No coordination patterns found"


def test_tier_consistency_validation(integration_framework):
    """Test model tier consistency across agents."""
    errors = integration_framework.validate_tier_consistency()
    assert len(errors) == 0, f"Tier consistency errors: {errors}"


def test_expertise_coverage_validation(integration_framework):
    """Test expertise area coverage across agents."""
    errors = integration_framework.validate_expertise_coverage()
    assert len(errors) == 0, f"Expertise coverage errors: {errors}"


def test_development_workflows_validation(integration_framework):
    """Test common development workflow support."""
    errors = integration_framework.validate_development_workflows()
    assert len(errors) == 0, f"Development workflow errors: {errors}"


class TraitIntegrationValidator:
    """Validator for trait integration across agents."""

    def __init__(self, data_dir: Path = None, traits_dir: Path = None):
        self.data_dir = data_dir or Path("data")
        self.traits_dir = traits_dir or Path("src/claude_config/traits")

    def validate_trait_file_consistency(self) -> List[str]:
        """Validate trait files exist and are consistent."""
        errors = []

        # Get all trait references from agents
        trait_references = set()
        personas_dir = self.data_dir / "personas"

        if personas_dir.exists():
            for agent_file in personas_dir.glob("*.yaml"):
                try:
                    with open(agent_file, 'r') as f:
                        agent_data = yaml.safe_load(f)

                    if 'imports' in agent_data:
                        for category, traits in agent_data['imports'].items():
                            for trait in traits:
                                trait_references.add(f"{category}/{trait}")

                except Exception as e:
                    errors.append(f"Error reading {agent_file}: {e}")

        # Check if referenced trait files exist
        for trait_ref in trait_references:
            trait_file = self.traits_dir / f"{trait_ref}.md"
            if not trait_file.exists():
                errors.append(f"Referenced trait file missing: {trait_file}")

        # Check for orphaned trait files (not referenced by any agent)
        available_traits = set()
        for category_dir in self.traits_dir.iterdir():
            if category_dir.is_dir():
                for trait_file in category_dir.glob("*.md"):
                    available_traits.add(f"{category_dir.name}/{trait_file.stem}")

        orphaned_traits = available_traits - trait_references
        if orphaned_traits:
            # This is a warning, not an error
            print(f"⚠️ Orphaned traits (not used by any agent): {', '.join(orphaned_traits)}")

        return errors


def test_trait_file_consistency():
    """Test trait file consistency across the system."""
    validator = TraitIntegrationValidator()
    errors = validator.validate_trait_file_consistency()
    assert len(errors) == 0, f"Trait file consistency errors: {errors}"