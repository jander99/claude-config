#!/usr/bin/env python3
"""
Content Consolidation Script

Consolidates modular content files from data/content/personas/ into main YAML files.
This simplifies the system by eliminating the separate content directory structure.
"""

import os
import sys
from pathlib import Path
import yaml
import re

def consolidate_agent_content(agent_name: str, data_dir: Path):
    """Consolidate content files for a single agent into its main YAML file."""
    
    # Paths
    agent_yaml_path = data_dir / "personas" / f"{agent_name}.yaml"
    content_dir = data_dir / "content" / "personas" / agent_name
    
    if not agent_yaml_path.exists():
        print(f"❌ Agent YAML not found: {agent_yaml_path}")
        return False
        
    if not content_dir.exists():
        print(f"ℹ️  No content directory for {agent_name}")
        return True
    
    print(f"🔄 Consolidating {agent_name}...")
    
    # Read the YAML file
    with open(agent_yaml_path, 'r') as f:
        content = f.read()
    
    # Parse YAML to get content_sections
    try:
        data = yaml.safe_load(content)
    except Exception as e:
        print(f"❌ Failed to parse YAML for {agent_name}: {e}")
        return False
    
    if 'content_sections' not in data:
        print(f"ℹ️  No content_sections in {agent_name}")
        return True
    
    content_sections = data['content_sections']
    print(f"   Found {len(content_sections)} content sections")
    
    # Load each content file and prepare consolidated sections
    consolidated_sections = {}
    
    for section_name, relative_path in content_sections.items():
        # Remove "personas/" prefix if present
        if relative_path.startswith('personas/'):
            relative_path = relative_path[len('personas/'):]
        
        content_file = data_dir / "content" / "personas" / relative_path
        
        if content_file.exists():
            with open(content_file, 'r') as f:
                section_content = f.read().strip()
                consolidated_sections[section_name] = section_content
            print(f"   ✅ Loaded {section_name} from {content_file.name}")
        else:
            print(f"   ⚠️  Content file not found: {content_file}")
    
    # Remove content_sections from YAML and add consolidated sections
    if consolidated_sections:
        # Remove content_sections line
        content = re.sub(r'content_sections:\s*\n(?:  [^\n]+\n)*\n?', '', content)
        
        # Add consolidated sections at the end
        content += "\n# Consolidated Content Sections\n"
        for section_name, section_content in consolidated_sections.items():
            content += f"\n{section_name}: |\n"
            # Indent the content
            for line in section_content.split('\n'):
                content += f"  {line}\n" if line.strip() else "\n"
        
        # Write back the consolidated YAML
        with open(agent_yaml_path, 'w') as f:
            f.write(content)
        
        print(f"   ✅ Consolidated {len(consolidated_sections)} sections into {agent_name}.yaml")
        return True
    else:
        print(f"   ⚠️  No content to consolidate for {agent_name}")
        return True

def main():
    """Main consolidation process."""
    
    # Find the project root
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    
    if not data_dir.exists():
        print("❌ Data directory not found. Run from project root.")
        sys.exit(1)
    
    print("🧹 Starting content consolidation process...")
    
    # Get all agents with content_sections
    personas_dir = data_dir / "personas"
    agents_with_content = []
    
    for yaml_file in personas_dir.glob("*.yaml"):
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
                if 'content_sections' in data:
                    agents_with_content.append(yaml_file.stem)
        except Exception as e:
            print(f"⚠️  Error checking {yaml_file.name}: {e}")
    
    print(f"Found {len(agents_with_content)} agents with content sections:")
    for agent in agents_with_content:
        print(f"  - {agent}")
    
    # Consolidate each agent
    success_count = 0
    for agent_name in agents_with_content:
        if consolidate_agent_content(agent_name, data_dir):
            success_count += 1
        print()  # Add spacing
    
    print(f"✅ Consolidation complete: {success_count}/{len(agents_with_content)} agents processed")
    print("\nNext steps:")
    print("1. Review consolidated YAML files")
    print("2. Remove content_sections references from composer")
    print("3. Delete data/content/personas/ directory")
    print("4. Test the build system")

if __name__ == "__main__":
    main()