"""
Simplified YAML validator for Claude Config Generator.

Basic validation for agent configurations - syntax and required fields only.
"""

from pathlib import Path
from typing import List
import yaml
from pydantic import BaseModel, ValidationError

from .composer import TraitConfig, AgentConfig


class ValidationResult(BaseModel):
    """Simple validation result."""
    is_valid: bool
    errors: List[str] = []


class ConfigValidator:
    """Basic YAML and schema validator."""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path("data")
    
    def validate_yaml_file(self, file_path: Path) -> ValidationResult:
        """Check if YAML file can be loaded."""
        if not file_path.exists():
            return ValidationResult(is_valid=False, errors=[f"File not found: {file_path}"])
        
        try:
            with open(file_path, 'r') as f:
                yaml.safe_load(f)
            return ValidationResult(is_valid=True)
        except yaml.YAMLError as e:
            return ValidationResult(is_valid=False, errors=[f"Invalid YAML: {e}"])
    
    def validate_agent(self, agent_name: str) -> ValidationResult:
        """Validate agent has required fields."""
        agent_path = self.data_dir / "personas" / f"{agent_name}.yaml"
        
        # Check YAML syntax first
        yaml_result = self.validate_yaml_file(agent_path)
        if not yaml_result.is_valid:
            return yaml_result
        
        try:
            with open(agent_path, 'r') as f:
                data = yaml.safe_load(f)
            
            # Try to create AgentConfig - this validates required fields
            AgentConfig(**data)
            
            # Check trait references if they exist
            errors = []
            if 'traits' in data:
                for trait in data['traits']:
                    trait_path = self.data_dir / "traits" / f"{trait}.yaml"
                    if not trait_path.exists():
                        errors.append(f"Missing trait: {trait}")
            
            return ValidationResult(is_valid=len(errors) == 0, errors=errors)
            
        except ValidationError as e:
            return ValidationResult(is_valid=False, errors=[f"Invalid agent structure: {e}"])
        except Exception as e:
            return ValidationResult(is_valid=False, errors=[f"Validation error: {e}"])
    
    def validate_trait(self, trait_name: str) -> ValidationResult:
        """Basic trait validation."""
        trait_path = self.data_dir / "traits" / f"{trait_name}.yaml"
        
        yaml_result = self.validate_yaml_file(trait_path)
        if not yaml_result.is_valid:
            return yaml_result
        
        try:
            with open(trait_path, 'r') as f:
                data = yaml.safe_load(f)
            TraitConfig(**data)
            return ValidationResult(is_valid=True)
        except ValidationError as e:
            return ValidationResult(is_valid=False, errors=[f"Invalid trait: {e}"])
    
    def validate_all(self) -> bool:
        """Validate all configurations."""
        print("Validating configurations...")
        overall_valid = True
        
        # Validate agents
        personas_dir = self.data_dir / "personas"
        if personas_dir.exists():
            for persona_file in personas_dir.glob("*.yaml"):
                if persona_file.stem != "config":
                    result = self.validate_agent(persona_file.stem)
                    if result.is_valid:
                        print(f"✅ {persona_file.stem}")
                    else:
                        print(f"❌ {persona_file.stem}: {', '.join(result.errors)}")
                        overall_valid = False
        
        # Validate traits
        traits_dir = self.data_dir / "traits"
        if traits_dir.exists():
            for trait_file in traits_dir.rglob("*.yaml"):
                trait_name = str(trait_file.relative_to(traits_dir).with_suffix(''))
                result = self.validate_trait(trait_name)
                if result.is_valid:
                    print(f"✅ trait: {trait_name}")
                else:
                    print(f"❌ trait: {trait_name}: {', '.join(result.errors)}")
                    overall_valid = False
        
        return overall_valid