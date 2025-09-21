"""
Content validation pipelines for YAML syntax, structure, and quality validation.

Comprehensive pipeline testing for agent generation workflow.
"""

import pytest
import yaml
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Any
from claude_config.composer import AgentComposer
from claude_config.validator import ConfigValidator


class ContentValidationPipeline:
    """Pipeline for comprehensive content validation."""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path("data")
        self.validator = ConfigValidator(self.data_dir)
        self.composer = AgentComposer(self.data_dir)
        self.validation_reports = []

    def run_yaml_syntax_pipeline(self) -> Dict[str, Any]:
        """Pipeline for YAML syntax validation."""
        report = {
            "pipeline": "yaml_syntax",
            "total_files": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
        }

        personas_dir = self.data_dir / "personas"
        if personas_dir.exists():
            yaml_files = list(personas_dir.glob("*.yaml"))
            report["total_files"] = len(yaml_files)

            for yaml_file in yaml_files:
                try:
                    with open(yaml_file, 'r') as f:
                        yaml.safe_load(f)
                    report["passed"] += 1
                except yaml.YAMLError as e:
                    report["failed"] += 1
                    report["errors"].append({
                        "file": str(yaml_file),
                        "error": str(e)
                    })
                except Exception as e:
                    report["failed"] += 1
                    report["errors"].append({
                        "file": str(yaml_file),
                        "error": f"Unexpected error: {e}"
                    })

        self.validation_reports.append(report)
        return report

    def run_structure_validation_pipeline(self) -> Dict[str, Any]:
        """Pipeline for YAML structure validation."""
        report = {
            "pipeline": "structure_validation",
            "total_agents": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
        }

        personas_dir = self.data_dir / "personas"
        if personas_dir.exists():
            agent_files = list(personas_dir.glob("*.yaml"))
            report["total_agents"] = len(agent_files)

            for agent_file in agent_files:
                agent_name = agent_file.stem
                result = self.validator.validate_agent(agent_name)

                if result.is_valid:
                    report["passed"] += 1
                else:
                    report["failed"] += 1
                    report["errors"].append({
                        "agent": agent_name,
                        "errors": result.errors
                    })

        self.validation_reports.append(report)
        return report

    def run_generation_pipeline(self) -> Dict[str, Any]:
        """Pipeline for agent generation validation."""
        report = {
            "pipeline": "generation_validation",
            "total_agents": 0,
            "generated": 0,
            "failed": 0,
            "errors": [],
            "output_stats": {}
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            try:
                # Create composer with temporary output directory
                composer = AgentComposer(
                    data_dir=self.data_dir,
                    output_dir=output_dir
                )

                personas_dir = self.data_dir / "personas"
                if personas_dir.exists():
                    agent_files = list(personas_dir.glob("*.yaml"))
                    report["total_agents"] = len(agent_files)

                    for agent_file in agent_files:
                        agent_name = agent_file.stem

                        try:
                            output_path = composer.build_agent(agent_name)

                            if output_path and output_path.exists():
                                report["generated"] += 1

                                # Collect output statistics
                                with open(output_path, 'r') as f:
                                    content = f.read()

                                stats = {
                                    "file_size": len(content),
                                    "line_count": len(content.splitlines()),
                                    "word_count": len(content.split())
                                }
                                report["output_stats"][agent_name] = stats
                            else:
                                report["failed"] += 1
                                report["errors"].append({
                                    "agent": agent_name,
                                    "error": "Generation failed - no output file"
                                })

                        except Exception as e:
                            report["failed"] += 1
                            report["errors"].append({
                                "agent": agent_name,
                                "error": str(e)
                            })

            except Exception as e:
                report["errors"].append({
                    "agent": "composer_setup",
                    "error": f"Composer initialization failed: {e}"
                })

        self.validation_reports.append(report)
        return report

    def run_quality_gates_pipeline(self) -> Dict[str, Any]:
        """Pipeline for quality gates validation."""
        report = {
            "pipeline": "quality_gates",
            "gates": {},
            "overall_passed": True
        }

        # Gate 1: YAML Syntax Check
        yaml_report = self.run_yaml_syntax_pipeline()
        report["gates"]["yaml_syntax"] = {
            "passed": yaml_report["failed"] == 0,
            "details": f"{yaml_report['passed']}/{yaml_report['total_files']} files passed"
        }
        if not report["gates"]["yaml_syntax"]["passed"]:
            report["overall_passed"] = False

        # Gate 2: Structure Validation
        structure_report = self.run_structure_validation_pipeline()
        report["gates"]["structure_validation"] = {
            "passed": structure_report["failed"] == 0,
            "details": f"{structure_report['passed']}/{structure_report['total_agents']} agents passed"
        }
        if not report["gates"]["structure_validation"]["passed"]:
            report["overall_passed"] = False

        # Gate 3: Generation Success
        generation_report = self.run_generation_pipeline()
        report["gates"]["generation_success"] = {
            "passed": generation_report["failed"] == 0,
            "details": f"{generation_report['generated']}/{generation_report['total_agents']} agents generated"
        }
        if not report["gates"]["generation_success"]["passed"]:
            report["overall_passed"] = False

        # Gate 4: Output Quality (minimum file size)
        min_output_size = 5000  # Minimum 5KB per agent
        quality_failures = []
        for agent, stats in generation_report.get("output_stats", {}).items():
            if stats["file_size"] < min_output_size:
                quality_failures.append(f"{agent}: {stats['file_size']} bytes")

        report["gates"]["output_quality"] = {
            "passed": len(quality_failures) == 0,
            "details": f"Output quality check: {len(quality_failures)} failures" if quality_failures else "All outputs meet minimum size"
        }
        if quality_failures:
            report["gates"]["output_quality"]["failures"] = quality_failures
            report["overall_passed"] = False

        self.validation_reports.append(report)
        return report

    def generate_validation_summary(self) -> Dict[str, Any]:
        """Generate comprehensive validation summary."""
        summary = {
            "total_pipelines": len(self.validation_reports),
            "pipeline_results": self.validation_reports,
            "overall_status": "PASSED",
            "recommendations": []
        }

        # Check for any failures
        has_failures = False
        for report in self.validation_reports:
            if report.get("failed", 0) > 0 or not report.get("overall_passed", True):
                has_failures = True
                break

        if has_failures:
            summary["overall_status"] = "FAILED"
            summary["recommendations"] = [
                "Review failed validations in pipeline reports",
                "Fix YAML syntax errors before proceeding",
                "Ensure all required fields are present in agent configurations",
                "Verify trait references are valid"
            ]

        return summary


@pytest.fixture
def content_pipeline():
    """Create content validation pipeline."""
    return ContentValidationPipeline()


def test_yaml_syntax_pipeline(content_pipeline):
    """Test YAML syntax validation pipeline."""
    report = content_pipeline.run_yaml_syntax_pipeline()

    assert report["total_files"] > 0, "No YAML files found to validate"
    assert report["failed"] == 0, f"YAML syntax errors: {report['errors']}"


def test_structure_validation_pipeline(content_pipeline):
    """Test structure validation pipeline."""
    report = content_pipeline.run_structure_validation_pipeline()

    assert report["total_agents"] > 0, "No agents found to validate"
    assert report["failed"] == 0, f"Structure validation errors: {report['errors']}"


def test_generation_pipeline(content_pipeline):
    """Test agent generation pipeline."""
    report = content_pipeline.run_generation_pipeline()

    assert report["total_agents"] > 0, "No agents found for generation"
    assert report["failed"] == 0, f"Generation errors: {report['errors']}"
    assert report["generated"] == report["total_agents"], "Not all agents generated successfully"


def test_quality_gates_pipeline(content_pipeline):
    """Test complete quality gates pipeline."""
    report = content_pipeline.run_quality_gates_pipeline()

    assert report["overall_passed"], f"Quality gates failed: {json.dumps(report['gates'], indent=2)}"


def test_comprehensive_validation_summary(content_pipeline):
    """Test comprehensive validation summary generation."""
    # Run all pipelines
    content_pipeline.run_yaml_syntax_pipeline()
    content_pipeline.run_structure_validation_pipeline()
    content_pipeline.run_generation_pipeline()
    content_pipeline.run_quality_gates_pipeline()

    summary = content_pipeline.generate_validation_summary()

    assert summary["total_pipelines"] >= 4, "Not all pipelines were executed"
    assert summary["overall_status"] == "PASSED", f"Validation summary failed: {summary['recommendations']}"


class MinimumContentRequirements:
    """Validate minimum content requirements for enhanced agents."""

    @staticmethod
    def validate_agent_depth(agent_data: Dict[str, Any]) -> List[str]:
        """Validate agent meets minimum depth requirements."""
        errors = []

        # Check essential sections
        required_sections = [
            'name', 'display_name', 'description', 'expertise',
            'responsibilities', 'technology_stack'
        ]

        for section in required_sections:
            if section not in agent_data:
                errors.append(f"Missing required section: {section}")

        # Check content depth
        if 'expertise' in agent_data:
            if len(agent_data['expertise']) < 5:
                errors.append(f"Insufficient expertise areas: {len(agent_data['expertise'])} (minimum 5)")

        if 'responsibilities' in agent_data:
            if len(agent_data['responsibilities']) < 5:
                errors.append(f"Insufficient responsibilities: {len(agent_data['responsibilities'])} (minimum 5)")

        # Check description length
        if 'description' in agent_data:
            desc_length = len(agent_data['description'])
            if desc_length < 200:
                errors.append(f"Description too short: {desc_length} chars (minimum 200)")

        return errors


def test_minimum_content_requirements():
    """Test that all agents meet minimum content requirements."""
    personas_dir = Path("data/personas")
    if not personas_dir.exists():
        pytest.skip("No personas directory found")

    failures = []
    validator = MinimumContentRequirements()

    for agent_file in personas_dir.glob("*.yaml"):
        try:
            with open(agent_file, 'r') as f:
                agent_data = yaml.safe_load(f)

            errors = validator.validate_agent_depth(agent_data)
            if errors:
                failures.append(f"{agent_file.stem}: {', '.join(errors)}")

        except Exception as e:
            failures.append(f"{agent_file.stem}: Error loading YAML: {e}")

    assert len(failures) == 0, f"Content requirement failures:\n" + "\n".join(failures)