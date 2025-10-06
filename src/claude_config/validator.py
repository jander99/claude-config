"""
Enhanced YAML validator for Claude Config Generator.

Comprehensive validation for agent configurations, traits, and MCP server configurations.
Includes syntax validation, schema validation, and security checks.
Enhanced with coordination schema validation for multi-agent orchestration.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml
from pydantic import BaseModel, ValidationError

from .composer import TraitConfig, AgentConfig


class ValidationResult(BaseModel):
    """Enhanced validation result with warnings support."""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []


class CoordinationValidator:
    """Validates coordination schema for multi-agent orchestration."""

    VALID_CONFIDENCE_LEVELS = {"high", "medium", "low"}
    VALID_COORDINATION_MODES = {"automatic", "suggest", "manual"}

    def __init__(self, data_dir: Path):
        """Initialize coordination validator with data directory."""
        self.data_dir = data_dir
        self._agent_names: Optional[set] = None

    def get_all_agent_names(self) -> set:
        """Get list of all valid agent names from personas directory."""
        if self._agent_names is None:
            personas_dir = self.data_dir / "personas"
            if personas_dir.exists():
                self._agent_names = {
                    f.stem for f in personas_dir.glob("*.yaml")
                    if f.stem != "config"
                }
            else:
                self._agent_names = set()
        return self._agent_names

    def validate_coordination(self, coordination_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate coordination schema structure.

        Expected structure:
        coordination:
          triggers:
            inbound: [{"pattern": str, "confidence": "high|medium|low"}]
            outbound: [{"trigger": str, "agents": [str], "mode": "automatic|suggest|manual"}]
          relationships:
            parallel: [agent_name]
            delegates_to: [agent_name]
            exclusive_from: [agent_name]
          task_patterns: [{"pattern": str, "decomposition": {agent: subtask}}]
        """
        errors = []
        warnings = []

        if not isinstance(coordination_data, dict):
            errors.append("Coordination section must be a dictionary")
            return ValidationResult(is_valid=False, errors=errors)

        # Validate triggers section (optional)
        if "triggers" in coordination_data:
            trigger_errors, trigger_warnings = self._validate_triggers(coordination_data["triggers"])
            errors.extend(trigger_errors)
            warnings.extend(trigger_warnings)

        # Validate relationships section (optional)
        if "relationships" in coordination_data:
            rel_errors, rel_warnings = self._validate_relationships(coordination_data["relationships"])
            errors.extend(rel_errors)
            warnings.extend(rel_warnings)

        # Validate task_patterns section (optional)
        if "task_patterns" in coordination_data:
            pattern_errors, pattern_warnings = self._validate_task_patterns(coordination_data["task_patterns"])
            errors.extend(pattern_errors)
            warnings.extend(pattern_warnings)

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _validate_triggers(self, triggers_data: Dict[str, Any]) -> tuple[List[str], List[str]]:
        """Validate triggers section structure."""
        errors = []
        warnings = []

        if not isinstance(triggers_data, dict):
            errors.append("Triggers section must be a dictionary")
            return errors, warnings

        # Validate inbound triggers
        if "inbound" in triggers_data:
            if not isinstance(triggers_data["inbound"], list):
                errors.append("triggers.inbound must be a list")
            else:
                for i, trigger in enumerate(triggers_data["inbound"]):
                    if not isinstance(trigger, dict):
                        errors.append(f"triggers.inbound[{i}] must be a dictionary")
                        continue

                    if "pattern" not in trigger:
                        errors.append(f"triggers.inbound[{i}] missing required field 'pattern'")
                    elif not isinstance(trigger["pattern"], str):
                        errors.append(f"triggers.inbound[{i}].pattern must be a string")

                    if "confidence" not in trigger:
                        warnings.append(f"triggers.inbound[{i}] missing recommended field 'confidence' (defaults to 'medium')")
                    elif trigger["confidence"] not in self.VALID_CONFIDENCE_LEVELS:
                        errors.append(f"triggers.inbound[{i}].confidence must be one of {self.VALID_CONFIDENCE_LEVELS}")

        # Validate outbound triggers
        if "outbound" in triggers_data:
            if not isinstance(triggers_data["outbound"], list):
                errors.append("triggers.outbound must be a list")
            else:
                for i, trigger in enumerate(triggers_data["outbound"]):
                    if not isinstance(trigger, dict):
                        errors.append(f"triggers.outbound[{i}] must be a dictionary")
                        continue

                    if "trigger" not in trigger:
                        errors.append(f"triggers.outbound[{i}] missing required field 'trigger'")
                    elif not isinstance(trigger["trigger"], str):
                        errors.append(f"triggers.outbound[{i}].trigger must be a string")

                    if "agents" not in trigger:
                        errors.append(f"triggers.outbound[{i}] missing required field 'agents'")
                    elif not isinstance(trigger["agents"], list):
                        errors.append(f"triggers.outbound[{i}].agents must be a list")
                    else:
                        # Validate agent names
                        valid_agents = self.get_all_agent_names()
                        for agent in trigger["agents"]:
                            if not isinstance(agent, str):
                                errors.append(f"triggers.outbound[{i}].agents must contain strings")
                            elif valid_agents and agent not in valid_agents:
                                warnings.append(f"triggers.outbound[{i}] references unknown agent '{agent}'")

                    if "mode" not in trigger:
                        warnings.append(f"triggers.outbound[{i}] missing recommended field 'mode' (defaults to 'suggest')")
                    elif trigger["mode"] not in self.VALID_COORDINATION_MODES:
                        errors.append(f"triggers.outbound[{i}].mode must be one of {self.VALID_COORDINATION_MODES}")

        return errors, warnings

    def _validate_relationships(self, relationships_data: Dict[str, Any]) -> tuple[List[str], List[str]]:
        """Validate relationships section structure."""
        errors = []
        warnings = []

        if not isinstance(relationships_data, dict):
            errors.append("Relationships section must be a dictionary")
            return errors, warnings

        valid_agents = self.get_all_agent_names()
        relationship_types = ["parallel", "delegates_to", "exclusive_from"]

        for rel_type in relationship_types:
            if rel_type in relationships_data:
                if not isinstance(relationships_data[rel_type], list):
                    errors.append(f"relationships.{rel_type} must be a list")
                    continue

                for i, agent_name in enumerate(relationships_data[rel_type]):
                    if not isinstance(agent_name, str):
                        errors.append(f"relationships.{rel_type}[{i}] must be a string (agent name)")
                    elif valid_agents and agent_name not in valid_agents:
                        warnings.append(f"relationships.{rel_type} references unknown agent '{agent_name}'")

        # Check for conflicting relationships
        if "parallel" in relationships_data and "exclusive_from" in relationships_data:
            parallel_set = set(relationships_data["parallel"])
            exclusive_set = set(relationships_data["exclusive_from"])
            conflicts = parallel_set & exclusive_set
            if conflicts:
                warnings.append(f"Agents listed in both parallel and exclusive_from: {conflicts}")

        return errors, warnings

    def _validate_task_patterns(self, task_patterns_data: List[Any]) -> tuple[List[str], List[str]]:
        """Validate task_patterns section structure."""
        errors = []
        warnings = []

        if not isinstance(task_patterns_data, list):
            errors.append("task_patterns must be a list")
            return errors, warnings

        valid_agents = self.get_all_agent_names()

        for i, pattern in enumerate(task_patterns_data):
            if not isinstance(pattern, dict):
                errors.append(f"task_patterns[{i}] must be a dictionary")
                continue

            if "pattern" not in pattern:
                errors.append(f"task_patterns[{i}] missing required field 'pattern'")
            elif not isinstance(pattern["pattern"], str):
                errors.append(f"task_patterns[{i}].pattern must be a string")

            if "decomposition" not in pattern:
                errors.append(f"task_patterns[{i}] missing required field 'decomposition'")
            elif not isinstance(pattern["decomposition"], dict):
                errors.append(f"task_patterns[{i}].decomposition must be a dictionary")
            else:
                # Validate decomposition agent names and subtasks
                for agent_name, subtask in pattern["decomposition"].items():
                    if not isinstance(agent_name, str):
                        errors.append(f"task_patterns[{i}].decomposition keys must be agent names (strings)")
                    elif valid_agents and agent_name not in valid_agents:
                        warnings.append(f"task_patterns[{i}].decomposition references unknown agent '{agent_name}'")

                    if not isinstance(subtask, str):
                        errors.append(f"task_patterns[{i}].decomposition[{agent_name}] must be a string (subtask description)")

        return errors, warnings



class ConfigValidator:
    """Enhanced YAML and schema validator with MCP support and coordination validation."""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path("data")
        self.coordination_validator = CoordinationValidator(self.data_dir)
    
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
        """Validate agent has required fields and optional coordination schema."""
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
            warnings = []

            if 'traits' in data:
                for trait in data['traits']:
                    trait_path = self.data_dir / "traits" / f"{trait}.yaml"
                    if not trait_path.exists():
                        errors.append(f"Missing trait: {trait}")

            # Validate coordination schema if present (optional)
            if 'coordination' in data:
                coord_result = self.coordination_validator.validate_coordination(data['coordination'])
                errors.extend(coord_result.errors)
                warnings.extend(coord_result.warnings)

            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings
            )

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
        """Validate all configurations with warnings display."""
        print("Validating configurations...")
        overall_valid = True

        # Validate agents in alphabetical order
        personas_dir = self.data_dir / "personas"
        if personas_dir.exists():
            persona_files = sorted(personas_dir.glob("*.yaml"), key=lambda p: p.stem)
            for persona_file in persona_files:
                if persona_file.stem != "config":
                    result = self.validate_agent(persona_file.stem)
                    if result.is_valid:
                        print(f"✅ {persona_file.stem}")
                        if result.warnings:
                            for warning in result.warnings:
                                print(f"   ⚠️  {warning}")
                    else:
                        print(f"❌ {persona_file.stem}: {', '.join(result.errors)}")
                        overall_valid = False

        # Validate traits in alphabetical order
        traits_dir = self.data_dir / "traits"
        if traits_dir.exists():
            trait_files = sorted(traits_dir.rglob("*.yaml"), key=lambda p: str(p.relative_to(traits_dir).with_suffix('')))
            for trait_file in trait_files:
                trait_name = str(trait_file.relative_to(traits_dir).with_suffix(''))
                result = self.validate_trait(trait_name)
                if result.is_valid:
                    print(f"✅ trait: {trait_name}")
                else:
                    print(f"❌ trait: {trait_name}: {', '.join(result.errors)}")
                    overall_valid = False

        return overall_valid