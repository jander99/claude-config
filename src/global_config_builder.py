#!/usr/bin/env python3
"""
Global CLAUDE.md Configuration Builder

Composes global Claude Code configurations from base rules, user profiles, 
and environment overrides to generate personalized global CLAUDE.md files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import sys


@dataclass
class GlobalConfigSpec:
    """Specification for building global configuration."""
    profile: str
    environment: str
    base_path: Path = field(default_factory=lambda: Path("data/global"))
    output_path: Path = field(default_factory=lambda: Path("dist/global"))
    

@dataclass 
class ConfigSection:
    """Represents a section of configuration with content and metadata."""
    name: str
    content: str
    priority: int = 0  # Higher priority sections override lower priority
    source: str = ""   # Track where this section came from


class GlobalConfigBuilder:
    """Builds personalized global CLAUDE.md configurations."""
    
    def __init__(self, spec: GlobalConfigSpec):
        self.spec = spec
        self.base_path = spec.base_path
        self.output_path = spec.output_path
        
    def build_global_config(self) -> str:
        """Build complete global CLAUDE.md configuration."""
        print(f"🌍 Building global configuration for profile '{self.spec.profile}' in environment '{self.spec.environment}'")
        
        # Load all configuration components
        base_config = self._load_base_configuration()
        profile_config = self._load_profile_configuration()
        env_config = self._load_environment_configuration()
        
        # Compose final configuration
        return self._compose_global_claude_md(base_config, profile_config, env_config)
        
    def _load_base_configuration(self) -> Dict[str, Any]:
        """Load non-negotiable base enforcement rules."""
        print("📋 Loading base enforcement rules...")
        
        base_sections = {}
        base_dir = self.base_path / "base"
        
        if not base_dir.exists():
            raise FileNotFoundError(f"Base configuration directory not found: {base_dir}")
            
        for md_file in base_dir.glob("*.md"):
            section_name = md_file.stem.replace("-", "_")
            content = md_file.read_text(encoding="utf-8")
            base_sections[section_name] = ConfigSection(
                name=section_name,
                content=content,
                priority=100,  # Highest priority - cannot be overridden
                source=f"base/{md_file.name}"
            )
            
        return base_sections
        
    def _load_profile_configuration(self) -> Dict[str, Any]:
        """Load user profile preferences."""
        print(f"👤 Loading profile configuration: {self.spec.profile}")
        
        profile_file = self.base_path / "profiles" / f"{self.spec.profile}.yaml"
        
        if not profile_file.exists():
            print(f"⚠️  Profile file not found: {profile_file}. Using default settings.")
            return {}
            
        with open(profile_file, 'r') as f:
            return yaml.safe_load(f)
            
    def _load_environment_configuration(self) -> Dict[str, Any]:
        """Load environment-specific overrides."""
        print(f"🌐 Loading environment configuration: {self.spec.environment}")
        
        env_file = self.base_path / "environments" / f"{self.spec.environment}.yaml"
        
        if not env_file.exists():
            print(f"⚠️  Environment file not found: {env_file}. Using default settings.")
            return {}
            
        with open(env_file, 'r') as f:
            return yaml.safe_load(f)
            
    def _compose_global_claude_md(self, base_config: Dict[str, Any], 
                                  profile_config: Dict[str, Any], 
                                  env_config: Dict[str, Any]) -> str:
        """Compose the final global CLAUDE.md configuration."""
        print("🔧 Composing final global configuration...")
        
        # Build configuration context for template rendering
        config_context = {
            'profile': profile_config,
            'environment': env_config,
            'timestamp': self._get_timestamp(),
        }
        
        # Start with base sections (highest priority)
        sections = []
        
        # Add header
        sections.append(self._generate_header(config_context))
        
        # Add base enforcement rules (mandatory)
        for section in base_config.values():
            sections.append(section.content)
            
        # Add profile-specific enhancements
        if profile_config:
            sections.append(self._generate_profile_section(profile_config))
            
        # Add environment-specific overrides
        if env_config:
            sections.append(self._generate_environment_section(env_config))
            
        # Add footer with metadata
        sections.append(self._generate_footer(config_context))
        
        return "\n\n---\n\n".join(sections)
        
    def _generate_header(self, context: Dict[str, Any]) -> str:
        """Generate configuration header."""
        profile_name = context['profile'].get('display_name', 'Default') if context['profile'] else 'Default'
        env_name = context['environment'].get('display_name', 'Default') if context['environment'] else 'Default'
        
        return f"""# Global Claude Code Configuration
# Generated: {context['timestamp']}
# Profile: {profile_name}
# Environment: {env_name}

**GLOBAL ENFORCEMENT**: This configuration establishes universal agent delegation protocols for ALL Claude Code sessions on this machine.

## 🎯 Configuration Summary

- **Profile**: {profile_name} - {context['profile'].get('description', 'Standard configuration') if context['profile'] else 'Standard configuration'}
- **Environment**: {env_name} - {context['environment'].get('description', 'Default environment') if context['environment'] else 'Default environment'}
- **Agent Count**: 26 specialized agents available
- **Enforcement Level**: Strict delegation with cost optimization"""

    def _generate_profile_section(self, profile_config: Dict[str, Any]) -> str:
        """Generate profile-specific configuration section."""
        sections = ["## 👤 Profile-Specific Configuration"]
        
        # Agent priorities
        if 'agent_priorities' in profile_config:
            sections.append("### Agent Priority Configuration")
            priorities = profile_config['agent_priorities']
            
            for level, agents in priorities.items():
                sections.append(f"**{level.upper()} Priority Agents:**")
                for agent in agents:
                    sections.append(f"- `{agent}` - Enhanced detection and reduced cost thresholds")
                    
        # Cost preferences
        if 'cost_preferences' in profile_config:
            cost_prefs = profile_config['cost_preferences']
            sections.append("### Cost Management")
            sections.append(f"- **Daily Budget**: ${cost_prefs.get('daily_budget', 50.0)}")
            sections.append(f"- **Session Budget**: ${cost_prefs.get('session_budget', 15.0)}")
            sections.append(f"- **Tier Preference**: {cost_prefs.get('tier_preference', 'balanced')}")
            sections.append(f"- **Escalation Threshold**: {cost_prefs.get('escalation_threshold', 3)} attempts")
            
        # Workflow preferences
        if 'workflow_preferences' in profile_config:
            workflow = profile_config['workflow_preferences']
            sections.append("### Workflow Preferences")
            sections.append(f"- **Testing Requirement**: {workflow.get('testing_requirement', 'standard')}")
            sections.append(f"- **Documentation Level**: {workflow.get('documentation_level', 'api_focused')}")
            sections.append(f"- **Git Workflow**: {workflow.get('git_workflow', 'feature_branches')}")
            sections.append(f"- **Deployment Strategy**: {workflow.get('deployment_strategy', 'containerized')}")
            
        return "\n".join(sections)
        
    def _generate_environment_section(self, env_config: Dict[str, Any]) -> str:
        """Generate environment-specific configuration section."""
        sections = ["## 🌐 Environment Configuration"]
        
        # Enforcement overrides
        if 'enforcement_overrides' in env_config:
            overrides = env_config['enforcement_overrides']
            sections.append("### Enforcement Adjustments")
            sections.append(f"- **Branch Protection**: {overrides.get('branch_protection', 'strict')}")
            sections.append(f"- **Context Verification**: {overrides.get('context_verification', 'strict')}")
            sections.append(f"- **Cost Monitoring**: {overrides.get('cost_monitoring', 'standard')}")
            
        # Cost overrides
        if 'cost_overrides' in env_config:
            cost_overrides = env_config['cost_overrides']
            sections.append("### Cost Adjustments")
            sections.append(f"- **Daily Budget Multiplier**: {cost_overrides.get('daily_budget_multiplier', 1.0)}x")
            sections.append(f"- **Session Budget Multiplier**: {cost_overrides.get('session_budget_multiplier', 1.0)}x")
            sections.append(f"- **Escalation Threshold**: {cost_overrides.get('escalation_threshold', 3)} attempts")
            
        return "\n".join(sections)
        
    def _generate_footer(self, context: Dict[str, Any]) -> str:
        """Generate configuration footer."""
        return f"""---

**CONFIGURATION METADATA**
- **Generated**: {context['timestamp']}
- **Builder Version**: 1.0
- **Profile**: {self.spec.profile}
- **Environment**: {self.spec.environment}
- **Source Repository**: claude-config
- **Authority Level**: GLOBAL SYSTEM CONFIGURATION

**USAGE INSTRUCTIONS**
1. Copy this file to `~/.claude/CLAUDE.md`
2. Restart Claude Code to apply global configuration  
3. Verify agent delegation is working with test development tasks
4. Monitor cost and effectiveness through session summaries

**OVERRIDE CONDITIONS**
- Project-specific CLAUDE.md files can extend but not reduce these requirements
- Emergency bypass available for critical production issues
- User explicit override with acknowledgment of protocol deviation"""

    def _get_timestamp(self) -> str:
        """Get current timestamp for configuration metadata."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def save_global_config(self, config_content: str) -> Path:
        """Save generated configuration to output directory."""
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        output_file = self.output_path / "CLAUDE.md"
        output_file.write_text(config_content, encoding="utf-8")
        
        print(f"✅ Global configuration saved to: {output_file}")
        return output_file


def main():
    """CLI entry point for building global configurations."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build global Claude Code configurations")
    parser.add_argument("--profile", default="developer", help="User profile (default: developer)")
    parser.add_argument("--environment", default="development", help="Environment (default: development)")
    parser.add_argument("--output", type=Path, help="Output directory (default: dist/global)")
    
    args = parser.parse_args()
    
    spec = GlobalConfigSpec(
        profile=args.profile,
        environment=args.environment
    )
    
    if args.output:
        spec.output_path = args.output
        
    try:
        builder = GlobalConfigBuilder(spec)
        config_content = builder.build_global_config()
        output_file = builder.save_global_config(config_content)
        
        print(f"🎉 Successfully built global configuration!")
        print(f"📁 Output: {output_file}")
        print(f"📋 To install: cp {output_file} ~/.claude/CLAUDE.md")
        
    except Exception as e:
        print(f"❌ Error building global configuration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()