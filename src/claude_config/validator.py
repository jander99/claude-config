"""
Configuration Validator for Claude Config Generator.

Validates agent compositions, personas, traits, and content files
to ensure they are correctly formatted and complete.
"""

from pathlib import Path
from typing import Dict, List, Set, Optional, Any
import yaml
from pydantic import BaseModel, ValidationError
from rich.console import Console
from rich.panel import Panel

from .composer import PersonaConfig, TraitConfig, AgentComposition, AgentConfig


console = Console()


class ValidationResult(BaseModel):
    """Result of a validation check."""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []


class ConfigValidator:
    """Validates agent configurations and compositions."""
    
    def __init__(self, data_dir: Path = None):
        """Initialize validator with data directory."""
        self.data_dir = data_dir or Path("data")
    
    def validate_yaml_file(self, file_path: Path) -> ValidationResult:
        """Validate that a file contains valid YAML."""
        result = ValidationResult(is_valid=True)
        
        if not file_path.exists():
            result.is_valid = False
            result.errors.append(f"File does not exist: {file_path}")
            return result
        
        try:
            with open(file_path, 'r') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            result.is_valid = False
            result.errors.append(f"Invalid YAML in {file_path}: {e}")
        
        return result
    
    def validate_agent(self, agent_name: str) -> ValidationResult:
        """Validate a unified agent configuration."""
        result = ValidationResult(is_valid=True)
        agent_path = self.data_dir / "personas" / f"{agent_name}.yaml"
        
        # Check YAML validity
        yaml_result = self.validate_yaml_file(agent_path)
        if not yaml_result.is_valid:
            return yaml_result
        
        # Validate agent structure
        try:
            with open(agent_path, 'r') as f:
                data = yaml.safe_load(f)
            
            agent = AgentConfig(**data)
            
            # Check that content sections exist
            for section_name, content_path in agent.content_sections.items():
                full_path = self.data_dir / "content" / content_path
                if not full_path.exists():
                    result.warnings.append(f"Content file missing: {content_path}")
            
            # Validate that referenced traits exist
            for trait in agent.traits:
                trait_path = self.data_dir / "traits" / f"{trait}.yaml"
                if not trait_path.exists():
                    result.errors.append(f"Referenced trait not found: {trait}")
                    result.is_valid = False
            
        except ValidationError as e:
            result.is_valid = False
            result.errors.append(f"Invalid agent structure in {agent_name}: {e}")
        except Exception as e:
            result.is_valid = False
            result.errors.append(f"Error validating agent {agent_name}: {e}")
        
        return result

    def validate_persona(self, persona_name: str) -> ValidationResult:
        """Validate a persona configuration. (Legacy method)"""
        result = ValidationResult(is_valid=True)
        persona_path = self.data_dir / "personas" / f"{persona_name}.yaml"
        
        # Check YAML validity
        yaml_result = self.validate_yaml_file(persona_path)
        if not yaml_result.is_valid:
            return yaml_result
        
        # Validate persona structure
        try:
            with open(persona_path, 'r') as f:
                data = yaml.safe_load(f)
            
            persona = PersonaConfig(**data)
            
            # Check that content sections exist
            for section_name, content_path in persona.content_sections.items():
                full_path = self.data_dir / "content" / content_path
                if not full_path.exists():
                    result.warnings.append(f"Content file missing: {content_path}")
            
        except ValidationError as e:
            result.is_valid = False
            result.errors.append(f"Invalid persona structure in {persona_name}: {e}")
        except Exception as e:
            result.is_valid = False
            result.errors.append(f"Error validating persona {persona_name}: {e}")
        
        return result
    
    def validate_trait(self, trait_name: str) -> ValidationResult:
        """Validate a trait configuration."""
        result = ValidationResult(is_valid=True)
        trait_path = self.data_dir / "traits" / f"{trait_name}.yaml"
        
        # Check YAML validity
        yaml_result = self.validate_yaml_file(trait_path)
        if not yaml_result.is_valid:
            return yaml_result
        
        # Validate trait structure
        try:
            with open(trait_path, 'r') as f:
                data = yaml.safe_load(f)
            
            trait = TraitConfig(**data)
            
            # Check that implementation is not empty
            if not trait.implementation.strip():
                result.warnings.append(f"Trait {trait_name} has empty implementation")
            
        except ValidationError as e:
            result.is_valid = False
            result.errors.append(f"Invalid trait structure in {trait_name}: {e}")
        except Exception as e:
            result.is_valid = False
            result.errors.append(f"Error validating trait {trait_name}: {e}")
        
        return result
    
    def validate_composition(self, composition_name: str) -> ValidationResult:
        """Validate an agent composition."""
        result = ValidationResult(is_valid=True)
        
        # Try composition-specific files first (e.g., python-engineer-composition.yaml)
        composition_path = self.data_dir / "personas" / f"{composition_name}-composition.yaml"
        if not composition_path.exists():
            # Fall back to regular persona files
            composition_path = self.data_dir / "personas" / f"{composition_name}.yaml"
        
        if not composition_path.exists():
            result.is_valid = False
            result.errors.append(f"Composition not found: {composition_name}")
            return result
        
        # Check YAML validity
        yaml_result = self.validate_yaml_file(composition_path)
        if not yaml_result.is_valid:
            return yaml_result
        
        try:
            with open(composition_path, 'r') as f:
                data = yaml.safe_load(f)
            
            composition = AgentComposition(**data)
            
            # Validate that referenced persona exists
            persona_path = self.data_dir / "personas" / f"{composition.persona}.yaml"
            if not persona_path.exists():
                result.errors.append(f"Referenced persona not found: {composition.persona}")
                result.is_valid = False
            
            # Validate that referenced traits exist
            for trait in composition.traits:
                trait_path = self.data_dir / "traits" / f"{trait}.yaml"
                if not trait_path.exists():
                    result.errors.append(f"Referenced trait not found: {trait}")
                    result.is_valid = False
            
        except ValidationError as e:
            result.is_valid = False
            result.errors.append(f"Invalid composition structure in {composition_name}: {e}")
        except Exception as e:
            result.is_valid = False
            result.errors.append(f"Error validating composition {composition_name}: {e}")
        
        return result
    
    def find_circular_dependencies(self) -> ValidationResult:
        """Check for circular dependencies in compositions."""
        result = ValidationResult(is_valid=True)
        # TODO: Implement circular dependency detection
        # This would be important if we have compositions that reference other compositions
        return result
    
    def validate_content_files(self) -> ValidationResult:
        """Validate that referenced content files exist and are readable."""
        result = ValidationResult(is_valid=True)
        
        content_dir = self.data_dir / "content"
        if not content_dir.exists():
            result.warnings.append("Content directory does not exist")
            return result
        
        # Check content files referenced by personas
        personas_dir = self.data_dir / "personas"
        if personas_dir.exists():
            for persona_file in personas_dir.glob("*.yaml"):
                try:
                    with open(persona_file, 'r') as f:
                        data = yaml.safe_load(f)
                    
                    if 'content_sections' in data:
                        for section_name, content_path in data['content_sections'].items():
                            full_path = content_dir / content_path
                            if not full_path.exists():
                                result.warnings.append(f"Missing content file: {content_path}")
                            elif not full_path.is_file():
                                result.errors.append(f"Content path is not a file: {content_path}")
                                result.is_valid = False
                
                except Exception as e:
                    result.warnings.append(f"Could not check content for {persona_file.name}: {e}")
        
        return result
    
    def validate_all(self) -> bool:
        """Validate all configurations and return overall validity."""
        overall_valid = True
        
        console.print("🔍 Validating Agent Configurations", style="bold blue")
        
        # Validate personas/agents
        personas_dir = self.data_dir / "personas"
        if personas_dir.exists():
            console.print("\n📝 Validating Personas:", style="bold")
            for persona_file in personas_dir.glob("*.yaml"):
                if persona_file.stem != "config" and not persona_file.stem.endswith("-composition"):
                    # Try unified agent validation first, fall back to legacy persona
                    try:
                        result = self.validate_agent(persona_file.stem)
                    except (ValidationError, KeyError):
                        result = self.validate_persona(persona_file.stem)
                    
                    self._print_validation_result(persona_file.stem, result, "persona")
                    if not result.is_valid:
                        overall_valid = False
        
        # Validate traits
        traits_dir = self.data_dir / "traits"
        if traits_dir.exists():
            console.print("\n🧩 Validating Traits:", style="bold")
            for trait_file in traits_dir.rglob("*.yaml"):
                trait_name = str(trait_file.relative_to(traits_dir).with_suffix(''))
                result = self.validate_trait(trait_name)
                self._print_validation_result(trait_name, result, "trait")
                if not result.is_valid:
                    overall_valid = False
        
        # Validate compositions
        console.print("\n🔧 Validating Compositions:", style="bold")
        if personas_dir.exists():
            for composition_file in personas_dir.glob("*-composition.yaml"):
                composition_name = composition_file.stem.replace("-composition", "")
                result = self.validate_composition(composition_name)
                self._print_validation_result(composition_name, result, "composition")
                if not result.is_valid:
                    overall_valid = False
        
        # Validate content files
        console.print("\n📄 Validating Content Files:", style="bold")
        content_result = self.validate_content_files()
        self._print_validation_result("Content Files", content_result, "content")
        if not content_result.is_valid:
            overall_valid = False
        
        # Check for circular dependencies
        console.print("\n🔄 Checking Dependencies:", style="bold")
        deps_result = self.find_circular_dependencies()
        self._print_validation_result("Dependencies", deps_result, "dependencies")
        if not deps_result.is_valid:
            overall_valid = False
        
        return overall_valid
    
    def _print_validation_result(self, name: str, result: ValidationResult, item_type: str):
        """Print validation result in a formatted way."""
        if result.is_valid:
            console.print(f"  ✅ {name}", style="green")
        else:
            console.print(f"  ❌ {name}", style="red")
        
        for error in result.errors:
            console.print(f"    🚫 {error}", style="red")
        
        for warning in result.warnings:
            console.print(f"    ⚠️  {warning}", style="yellow")