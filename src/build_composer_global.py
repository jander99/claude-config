#!/usr/bin/env python3
"""
Composer-based Global CLAUDE.md Builder

Uses the AgentComposer system to generate global CLAUDE.md from actual agent data
instead of hardcoded templates.
"""

from pathlib import Path
import sys
import logging

# Add the claude_config module to path
sys.path.append(str(Path(__file__).parent))

from claude_config.composer import AgentComposer

def main():
    """Generate global CLAUDE.md using the composer system."""
    print("🌍 Building data-driven global CLAUDE.md configuration...")
    
    # Initialize composer
    data_dir = Path("data")
    output_dir = Path("dist/global")
    
    composer = AgentComposer(
        data_dir=data_dir,
        output_dir=output_dir
    )
    
    try:
        # Generate configuration using actual agent data
        config_content = composer.compose_global_claude_md()
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save configuration
        output_file = output_dir / "CLAUDE.md"
        output_file.write_text(config_content, encoding="utf-8")
        
        # Get agent statistics
        agents = composer.load_all_agents()
        agent_count = len(agents)
        
        print(f"✅ Data-driven global configuration generated!")
        print(f"📁 Output: {output_file}")
        print(f"🤖 Agents processed: {agent_count}")
        print(f"🧩 Uses actual agent data from YAML files")
        print(f"📋 To install: cp {output_file} ~/.claude/CLAUDE.md")
        print(f"🔄 Then restart Claude Code to apply coordination")
        
    except Exception as e:
        print(f"❌ Error generating global configuration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.WARNING)
    main()