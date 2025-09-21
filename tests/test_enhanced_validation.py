"""
Enhanced validation tests for comprehensive agent and trait validation.

Tests cover content validation, trait integration, code examples, and quality gates.
"""

import pytest
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any
from claude_config.validator import ConfigValidator, ValidationResult
from claude_config.composer import AgentComposer


class EnhancedValidationFramework:
    """Enhanced validation framework for comprehensive testing."""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path("data")
        self.traits_dir = Path("src/claude_config/traits")
        self.validator = ConfigValidator(self.data_dir)
        self.composer = AgentComposer(self.data_dir)

    def validate_agent_content(self, agent_name: str) -> ValidationResult:
        """Validate agent content quality and completeness."""
        errors = []

        try:
            agent_config = self.composer.load_agent(agent_name)

            # Content completeness checks
            if not agent_config.description or len(agent_config.description.strip()) < 50:
                errors.append(f"Description too short: {len(agent_config.description)} chars")

            if not agent_config.expertise or len(agent_config.expertise) < 3:
                errors.append("Insufficient expertise areas (minimum 3)")

            if not agent_config.responsibilities or len(agent_config.responsibilities) < 3:
                errors.append("Insufficient responsibilities (minimum 3)")

            # Check for model tier appropriateness
            valid_models = ["haiku", "sonnet", "opus"]
            if hasattr(agent_config, 'model') and agent_config.model not in valid_models:
                errors.append(f"Invalid model tier: {agent_config.model}")

            # Validate trait references
            if hasattr(agent_config, 'imports') and agent_config.imports:
                trait_errors = self._validate_trait_imports(agent_config.imports)
                errors.extend(trait_errors)

            return ValidationResult(is_valid=len(errors) == 0, errors=errors)

        except Exception as e:
            return ValidationResult(is_valid=False, errors=[f"Content validation error: {e}"])

    def _validate_trait_imports(self, imports: Dict[str, List[str]]) -> List[str]:
        """Validate trait import structure and references."""
        errors = []

        for category, traits in imports.items():
            if not isinstance(traits, list):
                errors.append(f"Invalid trait category format: {category}")
                continue

            for trait in traits:
                # Check if trait file exists
                trait_file = self.traits_dir / category / f"{trait}.md"
                if not trait_file.exists():
                    errors.append(f"Missing trait file: {trait_file}")

        return errors

    def validate_code_examples(self, agent_name: str) -> ValidationResult:
        """Validate code examples in agent configurations."""
        errors = []

        try:
            agent_path = self.data_dir / "personas" / f"{agent_name}.yaml"
            with open(agent_path, 'r') as f:
                content = f.read()

            # Find code blocks in YAML content
            code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)

            for language, code in code_blocks:
                if language:
                    validation_error = self._validate_code_syntax(language, code)
                    if validation_error:
                        errors.append(validation_error)

            return ValidationResult(is_valid=len(errors) == 0, errors=errors)

        except Exception as e:
            return ValidationResult(is_valid=False, errors=[f"Code validation error: {e}"])

    def _validate_code_syntax(self, language: str, code: str) -> str:
        """Basic syntax validation for code examples."""
        # Basic checks for common issues
        if language.lower() in ['python', 'py']:
            # Check for obvious Python syntax issues
            if code.count('(') != code.count(')'):
                return f"Unmatched parentheses in Python code"
            if code.count('{') != code.count('}'):
                return f"Unmatched braces in Python code"

        elif language.lower() in ['javascript', 'js', 'typescript', 'ts']:
            # Check for obvious JS/TS syntax issues
            if code.count('(') != code.count(')'):
                return f"Unmatched parentheses in {language} code"
            if code.count('{') != code.count('}'):
                return f"Unmatched braces in {language} code"

        return None

    def validate_trait_content(self, trait_category: str, trait_name: str) -> ValidationResult:
        """Validate trait content and structure."""
        errors = []

        try:
            trait_file = self.traits_dir / trait_category / f"{trait_name}.md"

            if not trait_file.exists():
                return ValidationResult(is_valid=False, errors=[f"Trait file not found: {trait_file}"])

            with open(trait_file, 'r') as f:
                content = f.read()

            # Content structure checks
            if not content.strip():
                errors.append("Empty trait content")

            if len(content.strip()) < 200:
                errors.append(f"Trait content too short: {len(content)} chars")

            # Check for required sections
            required_sections = ['##', '###']
            has_sections = any(section in content for section in required_sections)
            if not has_sections:
                errors.append("Missing structured sections in trait")

            return ValidationResult(is_valid=len(errors) == 0, errors=errors)

        except Exception as e:
            return ValidationResult(is_valid=False, errors=[f"Trait validation error: {e}"])

    def validate_cross_agent_consistency(self) -> ValidationResult:
        """Validate consistency across all agents."""
        errors = []

        try:
            personas_dir = self.data_dir / "personas"
            agent_files = list(personas_dir.glob("*.yaml"))

            model_distribution = {"haiku": 0, "sonnet": 0, "opus": 0}
            trait_usage = {}

            for agent_file in agent_files:
                try:
                    with open(agent_file, 'r') as f:
                        data = yaml.safe_load(f)

                    # Track model distribution
                    model = data.get('model', 'sonnet')
                    if model in model_distribution:
                        model_distribution[model] += 1

                    # Track trait usage
                    if 'imports' in data:
                        for category, traits in data['imports'].items():
                            for trait in traits:
                                trait_key = f"{category}/{trait}"
                                trait_usage[trait_key] = trait_usage.get(trait_key, 0) + 1

                except Exception as e:
                    errors.append(f"Error processing {agent_file.name}: {e}")

            # Validate model distribution (should have agents in all tiers)
            if model_distribution["haiku"] == 0:
                errors.append("No Haiku-tier agents found")
            if model_distribution["sonnet"] == 0:
                errors.append("No Sonnet-tier agents found")
            if model_distribution["opus"] == 0:
                errors.append("No Opus-tier agents found")

            # Check for unused traits
            expected_traits = self._get_all_available_traits()
            unused_traits = set(expected_traits) - set(trait_usage.keys())
            if unused_traits:
                errors.append(f"Unused traits: {', '.join(unused_traits)}")

            return ValidationResult(is_valid=len(errors) == 0, errors=errors)

        except Exception as e:
            return ValidationResult(is_valid=False, errors=[f"Cross-agent validation error: {e}"])

    def _get_all_available_traits(self) -> List[str]:
        """Get list of all available traits."""
        traits = []

        for category_dir in self.traits_dir.iterdir():
            if category_dir.is_dir():
                for trait_file in category_dir.glob("*.md"):
                    trait_name = trait_file.stem
                    traits.append(f"{category_dir.name}/{trait_name}")

        return traits


@pytest.fixture
def enhanced_validator():
    """Create enhanced validation framework."""
    return EnhancedValidationFramework()


def test_all_agents_content_validation(enhanced_validator):
    """Test content validation for all agents."""
    personas_dir = Path("data/personas")
    if not personas_dir.exists():
        pytest.skip("No personas directory found")

    agent_files = list(personas_dir.glob("*.yaml"))
    failures = []

    for agent_file in agent_files:
        agent_name = agent_file.stem
        result = enhanced_validator.validate_agent_content(agent_name)

        if not result.is_valid:
            failures.append(f"{agent_name}: {', '.join(result.errors)}")

    assert len(failures) == 0, f"Content validation failures:\n" + "\n".join(failures)


def test_all_agents_code_examples(enhanced_validator):
    """Test code examples in all agents."""
    personas_dir = Path("data/personas")
    if not personas_dir.exists():
        pytest.skip("No personas directory found")

    agent_files = list(personas_dir.glob("*.yaml"))
    failures = []

    for agent_file in agent_files:
        agent_name = agent_file.stem
        result = enhanced_validator.validate_code_examples(agent_name)

        if not result.is_valid:
            failures.append(f"{agent_name}: {', '.join(result.errors)}")

    assert len(failures) == 0, f"Code validation failures:\n" + "\n".join(failures)


def test_all_traits_content_validation(enhanced_validator):
    """Test content validation for all traits."""
    traits_dir = Path("src/claude_config/traits")
    if not traits_dir.exists():
        pytest.skip("No traits directory found")

    failures = []

    for category_dir in traits_dir.iterdir():
        if category_dir.is_dir():
            for trait_file in category_dir.glob("*.md"):
                trait_name = trait_file.stem
                result = enhanced_validator.validate_trait_content(category_dir.name, trait_name)

                if not result.is_valid:
                    failures.append(f"{category_dir.name}/{trait_name}: {', '.join(result.errors)}")

    assert len(failures) == 0, f"Trait validation failures:\n" + "\n".join(failures)


def test_cross_agent_consistency(enhanced_validator):
    """Test consistency across all agents."""
    result = enhanced_validator.validate_cross_agent_consistency()
    assert result.is_valid, f"Cross-agent consistency failures: {', '.join(result.errors)}"


def test_trait_import_validation(enhanced_validator):
    """Test that all trait imports are valid."""
    personas_dir = Path("data/personas")
    if not personas_dir.exists():
        pytest.skip("No personas directory found")

    agent_files = list(personas_dir.glob("*.yaml"))
    failures = []

    for agent_file in agent_files:
        agent_name = agent_file.stem
        try:
            with open(agent_file, 'r') as f:
                data = yaml.safe_load(f)

            if 'imports' in data:
                trait_errors = enhanced_validator._validate_trait_imports(data['imports'])
                if trait_errors:
                    failures.append(f"{agent_name}: {', '.join(trait_errors)}")

        except Exception as e:
            failures.append(f"{agent_name}: Error loading YAML: {e}")

    assert len(failures) == 0, f"Trait import validation failures:\n" + "\n".join(failures)