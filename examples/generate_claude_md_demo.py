"""
Demo script showing CLAUDE.md generation from example agents.

Creates 3 sample agents and generates CLAUDE.md with coordination patterns.
"""

import sys
from pathlib import Path
import yaml
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.claude_config.generator import ClaudeMdGenerator


def create_example_agents(personas_dir: Path):
    """Create 3 example agents for demonstration."""

    python_engineer = {
        'name': 'python-engineer',
        'display_name': 'Python Engineer',
        'model': 'sonnet',
        'description': 'Expert Python developer specializing in web frameworks and data processing',
        'expertise': [
            'FastAPI, Django, Flask development',
            'Data processing with pandas and numpy',
            'Testing with pytest',
            'Python packaging and deployment'
        ],
        'responsibilities': [
            'Backend API development',
            'Data pipeline creation',
            'Python package management',
            'Code quality and testing'
        ],
        'imports': {
            'coordination': [
                'standard-safety-protocols',
                'qa-testing-handoff',
                'documentation-handoff',
                'version-control-coordination'
            ],
            'tools': ['python-development-stack']
        },
        'custom_coordination': {
            'ml_handoff': 'For ML-related Python development, coordinates with ai-engineer',
            'data_pipeline': 'For large-scale data processing, coordinates with data-engineer'
        },
        'proactive_activation': {
            'file_patterns': ['*.py', 'pyproject.toml', 'requirements.txt'],
            'project_indicators': ['FastAPI', 'Django', 'Flask', 'pytest']
        },
        'when_to_use': 'Building web applications, REST APIs, data processing pipelines, or general Python development'
    }

    qa_engineer = {
        'name': 'qa-engineer',
        'display_name': 'QA Engineer',
        'model': 'sonnet',
        'description': 'Quality assurance specialist focused on test automation and comprehensive testing strategies',
        'expertise': [
            'Test automation across multiple languages',
            'Pytest, JUnit, Jest, Cypress',
            'Integration and E2E testing',
            'CI/CD pipeline testing',
            'Performance testing'
        ],
        'responsibilities': [
            'Test strategy development',
            'Test automation implementation',
            'Quality assurance validation',
            'Testing framework selection',
            'CI/CD test integration'
        ],
        'imports': {
            'coordination': [
                'standard-safety-protocols',
                'documentation-handoff',
                'version-control-coordination'
            ]
        },
        'custom_coordination': {
            'performance_testing': 'Coordinates with performance-engineer for load testing',
            'security_testing': 'Coordinates with security-engineer for security test validation'
        },
        'proactive_activation': {
            'file_patterns': ['test_*.py', '*_test.py', '*.test.js', '*.spec.ts'],
            'project_indicators': ['pytest', 'jest', 'cypress', 'junit']
        },
        'when_to_use': 'Developing test strategies, implementing test automation, or validating quality requirements'
    }

    technical_writer = {
        'name': 'technical-writer',
        'display_name': 'Technical Writer',
        'model': 'haiku',
        'description': 'Documentation specialist creating clear, comprehensive technical documentation',
        'expertise': [
            'API documentation',
            'User guides and tutorials',
            'README and contribution guides',
            'Documentation tooling (MkDocs, Sphinx)',
            'Markdown and reStructuredText'
        ],
        'responsibilities': [
            'API documentation generation',
            'User-facing documentation',
            'Developer documentation',
            'Documentation review and quality',
            'Documentation structure design'
        ],
        'imports': {
            'coordination': [
                'standard-safety-protocols',
                'version-control-coordination'
            ]
        },
        'custom_coordination': {},
        'proactive_activation': {
            'file_patterns': ['*.md', 'docs/**/*', 'README*', 'CONTRIBUTING*'],
            'project_indicators': ['MkDocs', 'Sphinx', 'documentation']
        },
        'when_to_use': 'Creating or updating documentation, API guides, or user-facing content'
    }

    # Write agent YAML files
    agents = [python_engineer, qa_engineer, technical_writer]
    for agent in agents:
        agent_file = personas_dir / f"{agent['name']}.yaml"
        with open(agent_file, 'w') as f:
            yaml.dump(agent, f, default_flow_style=False, sort_keys=False)

    return agents


def create_minimal_template(template_dir: Path):
    """Create a minimal CLAUDE.md template for demonstration."""

    template_content = """# Global Claude Code Agent Delegation System

**Generated**: {{ timestamp.strftime('%Y-%m-%d %H:%M:%S') }}
**Source**: {{ agent_count }} specialized agents
**Version**: 4.0 - Orchestration-Aware Delegation

⚠️ **AUTO-GENERATED** - Do not edit manually

---

## 🎯 Agent Detection Matrix

| **Pattern** | **Agent** | **Enforcement** |
|-------------|-----------|----------------|
{% for trigger, agents_list in rules.entry_point_mapping.items() %}
| {{ trigger }} | `{{ agents_list[0] }}` | STANDARD |
{% endfor %}

---

## 🔄 Coordination Workflows

{% for task_type, agent_sequence in rules.task_decomposition.items() %}
### {{ task_type }}:
```
{% for agent in agent_sequence %}{{ agent }}{{ " → " if not loop.last }}{% endfor %}
```
{% endfor %}

---

## 📊 Coordination Graph

{{ mermaid_graph }}

**Statistics:**
- Total Agents: {{ optimization_stats.total_agents }}
- Entry Points: {{ optimization_stats.entry_points }}
- Cached Paths: {{ optimization_stats.cached_paths }}
- Optimization Time: {{ optimization_stats.optimization_time_ms }}ms

---

{{ agent_directory }}

---

## 💰 Cost Optimization

**Tier 1 (Haiku):** {% for agent in agents if agent.model == 'haiku' %}`{{ agent.name }}`{{ ", " if not loop.last }}{% endfor %}

**Tier 2 (Sonnet):** {% for agent in agents if agent.model == 'sonnet' %}`{{ agent.name }}`{{ ", " if not loop.last }}{% endfor %}

**Tier 3 (Opus):** {% for agent in agents if agent.model == 'opus' %}`{{ agent.name }}`{{ ", " if not loop.last }}{% endfor %}

---

*Generated by claude-config v4.0*
"""

    template_file = template_dir / 'CLAUDE.md.j2'
    with open(template_file, 'w') as f:
        f.write(template_content)


def main():
    """Run the demo generation."""
    print("🚀 CLAUDE.md Generation Demo\n")
    print("Creating temporary workspace...")

    # Create temporary directories
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        data_dir = tmpdir / "data"
        personas_dir = data_dir / "personas"
        template_dir = tmpdir / "templates"
        output_dir = tmpdir / "output"

        personas_dir.mkdir(parents=True)
        template_dir.mkdir(parents=True)
        output_dir.mkdir(parents=True)

        print("✅ Workspace created\n")

        # Create example agents
        print("Creating 3 example agents...")
        agents = create_example_agents(personas_dir)
        print(f"✅ Created: {', '.join(a['name'] for a in agents)}\n")

        # Create template
        print("Creating CLAUDE.md template...")
        create_minimal_template(template_dir)
        print("✅ Template created\n")

        # Initialize generator
        print("Initializing ClaudeMdGenerator...")
        generator = ClaudeMdGenerator(
            data_dir=data_dir,
            template_dir=template_dir,
            output_dir=output_dir
        )
        print("✅ Generator initialized\n")

        # Generate CLAUDE.md
        print("Generating CLAUDE.md...")
        print("Note: Skipping validation for demo (minimal agent set)")
        import time
        start = time.time()

        output_path = generator.generate_claude_md(validate=False)

        elapsed = time.time() - start
        print(f"✅ Generated in {elapsed*1000:.1f}ms\n")

        # Display generated content
        print("=" * 80)
        print("GENERATED CLAUDE.MD CONTENT:")
        print("=" * 80)
        with open(output_path, 'r') as f:
            content = f.read()
            print(content)
        print("=" * 80)

        # Copy to examples directory for inspection
        examples_output = Path(__file__).parent / "example_CLAUDE.md"
        shutil.copy(output_path, examples_output)
        print(f"\n✅ Example saved to: {examples_output}")

        # Show statistics
        print("\n📊 Generation Statistics:")
        print(f"   - Agents Processed: {len(agents)}")
        print(f"   - Generation Time: {elapsed*1000:.1f}ms")
        print(f"   - Output Size: {len(content)} characters")
        print(f"   - Template: CLAUDE.md.j2")

        print("\n✨ Demo complete!")


if __name__ == '__main__':
    main()
