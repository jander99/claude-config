#!/usr/bin/env python3
"""
Comprehensive quality validation runner for Stream C1.

Executes all validation pipelines and generates detailed reports.
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.test_enhanced_validation import EnhancedValidationFramework
from tests.test_content_pipelines import ContentValidationPipeline
from tests.test_cross_agent_integration import CrossAgentIntegrationFramework


class QualityValidationRunner:
    """Comprehensive quality validation orchestrator."""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path("data")
        self.start_time = None
        self.validation_results = {}

    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run complete validation suite."""
        print("🚀 Starting Stream C1 Quality Validation Pipeline")
        print("=" * 60)

        self.start_time = time.time()

        # Initialize frameworks
        enhanced_validator = EnhancedValidationFramework(self.data_dir)
        content_pipeline = ContentValidationPipeline(self.data_dir)
        integration_framework = CrossAgentIntegrationFramework(self.data_dir)

        validation_summary = {
            "timestamp": datetime.now().isoformat(),
            "pipeline_version": "Stream C1 v1.0",
            "phases": {},
            "overall_status": "UNKNOWN",
            "total_runtime": 0,
            "recommendations": []
        }

        try:
            # Phase 1: Basic Validation
            print("\n📋 Phase 1: Basic Validation")
            print("-" * 30)
            phase1_results = self._run_basic_validation(enhanced_validator)
            validation_summary["phases"]["basic_validation"] = phase1_results

            # Phase 2: Content Pipeline Validation
            print("\n📝 Phase 2: Content Pipeline Validation")
            print("-" * 40)
            phase2_results = self._run_content_validation(content_pipeline)
            validation_summary["phases"]["content_validation"] = phase2_results

            # Phase 3: Integration Testing
            print("\n🔗 Phase 3: Cross-Agent Integration Testing")
            print("-" * 45)
            phase3_results = self._run_integration_testing(integration_framework)
            validation_summary["phases"]["integration_testing"] = phase3_results

            # Phase 4: Quality Gates
            print("\n🎯 Phase 4: Quality Gates Validation")
            print("-" * 35)
            phase4_results = self._run_quality_gates(content_pipeline)
            validation_summary["phases"]["quality_gates"] = phase4_results

            # Calculate overall status
            validation_summary["overall_status"] = self._calculate_overall_status(validation_summary)
            validation_summary["total_runtime"] = time.time() - self.start_time

            # Generate recommendations
            validation_summary["recommendations"] = self._generate_recommendations(validation_summary)

        except Exception as e:
            validation_summary["overall_status"] = "ERROR"
            validation_summary["error"] = str(e)
            validation_summary["total_runtime"] = time.time() - self.start_time

        return validation_summary

    def _run_basic_validation(self, validator: EnhancedValidationFramework) -> Dict[str, Any]:
        """Run basic validation tests."""
        results = {
            "agent_content_validation": None,
            "trait_content_validation": None,
            "code_examples_validation": None,
            "status": "UNKNOWN"
        }

        try:
            # Agent content validation
            print("  🔍 Validating agent content...")
            agent_errors = []
            personas_dir = self.data_dir / "personas"

            if personas_dir.exists():
                for agent_file in personas_dir.glob("*.yaml"):
                    agent_name = agent_file.stem
                    result = validator.validate_agent_content(agent_name)
                    if not result.is_valid:
                        agent_errors.extend([f"{agent_name}: {error}" for error in result.errors])

            results["agent_content_validation"] = {
                "passed": len(agent_errors) == 0,
                "errors": agent_errors
            }

            # Trait content validation
            print("  🧩 Validating trait content...")
            trait_errors = []
            traits_dir = Path("src/claude_config/traits")

            if traits_dir.exists():
                for category_dir in traits_dir.iterdir():
                    if category_dir.is_dir():
                        for trait_file in category_dir.glob("*.md"):
                            trait_name = trait_file.stem
                            result = validator.validate_trait_content(category_dir.name, trait_name)
                            if not result.is_valid:
                                trait_errors.extend([f"{category_dir.name}/{trait_name}: {error}" for error in result.errors])

            results["trait_content_validation"] = {
                "passed": len(trait_errors) == 0,
                "errors": trait_errors
            }

            # Code examples validation
            print("  💻 Validating code examples...")
            code_errors = []

            if personas_dir.exists():
                for agent_file in personas_dir.glob("*.yaml"):
                    agent_name = agent_file.stem
                    result = validator.validate_code_examples(agent_name)
                    if not result.is_valid:
                        code_errors.extend([f"{agent_name}: {error}" for error in result.errors])

            results["code_examples_validation"] = {
                "passed": len(code_errors) == 0,
                "errors": code_errors
            }

            # Overall status
            all_passed = all(
                results[key]["passed"] for key in results if key != "status" and results[key]
            )
            results["status"] = "PASSED" if all_passed else "FAILED"

        except Exception as e:
            results["status"] = "ERROR"
            results["error"] = str(e)

        return results

    def _run_content_validation(self, pipeline: ContentValidationPipeline) -> Dict[str, Any]:
        """Run content validation pipeline."""
        results = {
            "yaml_syntax": None,
            "structure_validation": None,
            "generation_pipeline": None,
            "status": "UNKNOWN"
        }

        try:
            # YAML syntax validation
            print("  📄 Running YAML syntax validation...")
            yaml_report = pipeline.run_yaml_syntax_pipeline()
            results["yaml_syntax"] = {
                "passed": yaml_report["failed"] == 0,
                "details": f"{yaml_report['passed']}/{yaml_report['total_files']} files passed",
                "errors": yaml_report["errors"]
            }

            # Structure validation
            print("  🏗️  Running structure validation...")
            structure_report = pipeline.run_structure_validation_pipeline()
            results["structure_validation"] = {
                "passed": structure_report["failed"] == 0,
                "details": f"{structure_report['passed']}/{structure_report['total_agents']} agents passed",
                "errors": structure_report["errors"]
            }

            # Generation pipeline
            print("  ⚙️  Running generation pipeline...")
            generation_report = pipeline.run_generation_pipeline()
            results["generation_pipeline"] = {
                "passed": generation_report["failed"] == 0,
                "details": f"{generation_report['generated']}/{generation_report['total_agents']} agents generated",
                "errors": generation_report["errors"],
                "output_stats": generation_report.get("output_stats", {})
            }

            # Overall status
            all_passed = all(
                results[key]["passed"] for key in results if key != "status" and results[key]
            )
            results["status"] = "PASSED" if all_passed else "FAILED"

        except Exception as e:
            results["status"] = "ERROR"
            results["error"] = str(e)

        return results

    def _run_integration_testing(self, framework: CrossAgentIntegrationFramework) -> Dict[str, Any]:
        """Run cross-agent integration testing."""
        results = {
            "coordination_analysis": None,
            "tier_consistency": None,
            "trait_coordination": None,
            "expertise_coverage": None,
            "generation_consistency": None,
            "status": "UNKNOWN"
        }

        try:
            # Coordination analysis
            print("  🤝 Analyzing coordination patterns...")
            coordination_analysis = framework.analyze_coordination_patterns()
            results["coordination_analysis"] = {
                "passed": coordination_analysis["total_agents"] > 20,
                "details": f"Analyzed {coordination_analysis['total_agents']} agents",
                "data": coordination_analysis
            }

            # Tier consistency
            print("  🎚️  Validating tier consistency...")
            tier_errors = framework.validate_tier_consistency()
            results["tier_consistency"] = {
                "passed": len(tier_errors) == 0,
                "errors": tier_errors
            }

            # Trait coordination
            print("  🧩 Validating trait coordination...")
            trait_errors = framework.validate_trait_coordination()
            results["trait_coordination"] = {
                "passed": len(trait_errors) == 0,
                "errors": trait_errors
            }

            # Expertise coverage
            print("  🎯 Validating expertise coverage...")
            expertise_errors = framework.validate_expertise_coverage()
            results["expertise_coverage"] = {
                "passed": len(expertise_errors) == 0,
                "errors": expertise_errors
            }

            # Generation consistency
            print("  ⚙️  Testing generation consistency...")
            gen_success, gen_errors = framework.test_agent_generation_consistency()
            results["generation_consistency"] = {
                "passed": gen_success,
                "errors": gen_errors
            }

            # Overall status
            all_passed = all(
                results[key]["passed"] for key in results if key != "status" and results[key]
            )
            results["status"] = "PASSED" if all_passed else "FAILED"

        except Exception as e:
            results["status"] = "ERROR"
            results["error"] = str(e)

        return results

    def _run_quality_gates(self, pipeline: ContentValidationPipeline) -> Dict[str, Any]:
        """Run quality gates validation."""
        results = {"status": "UNKNOWN"}

        try:
            print("  🚪 Running quality gates...")
            quality_report = pipeline.run_quality_gates_pipeline()
            results = {
                "passed": quality_report["overall_passed"],
                "gates": quality_report["gates"],
                "status": "PASSED" if quality_report["overall_passed"] else "FAILED"
            }

        except Exception as e:
            results["status"] = "ERROR"
            results["error"] = str(e)

        return results

    def _calculate_overall_status(self, validation_summary: Dict[str, Any]) -> str:
        """Calculate overall validation status."""
        phases = validation_summary.get("phases", {})

        for phase_name, phase_results in phases.items():
            if phase_results.get("status") == "ERROR":
                return "ERROR"
            elif phase_results.get("status") == "FAILED":
                return "FAILED"

        return "PASSED"

    def _generate_recommendations(self, validation_summary: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on validation results."""
        recommendations = []

        phases = validation_summary.get("phases", {})

        for phase_name, phase_results in phases.items():
            if phase_results.get("status") == "FAILED":
                if phase_name == "basic_validation":
                    recommendations.append("Fix agent content validation errors before proceeding")
                    recommendations.append("Review trait content structure and completeness")
                elif phase_name == "content_validation":
                    recommendations.append("Resolve YAML syntax errors in agent configurations")
                    recommendations.append("Ensure all agents meet structural requirements")
                elif phase_name == "integration_testing":
                    recommendations.append("Review cross-agent coordination patterns")
                    recommendations.append("Validate trait usage consistency across agents")
                elif phase_name == "quality_gates":
                    recommendations.append("Address quality gate failures before deployment")

        if validation_summary["overall_status"] == "PASSED":
            recommendations.append("✅ All validations passed - system ready for deployment")
            recommendations.append("Consider running performance benchmarks")

        return recommendations

    def generate_report(self, validation_summary: Dict[str, Any], output_file: Path = None) -> str:
        """Generate detailed validation report."""
        if output_file is None:
            output_file = Path("validation_report.json")

        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(validation_summary, f, indent=2)

        # Generate text summary
        summary_lines = [
            f"🔍 Stream C1 Quality Validation Report",
            f"Generated: {validation_summary['timestamp']}",
            f"Runtime: {validation_summary['total_runtime']:.2f}s",
            f"Overall Status: {validation_summary['overall_status']}",
            "",
            "📊 Phase Results:",
        ]

        for phase_name, phase_results in validation_summary.get("phases", {}).items():
            status_emoji = "✅" if phase_results.get("status") == "PASSED" else "❌"
            summary_lines.append(f"  {status_emoji} {phase_name}: {phase_results.get('status')}")

        if validation_summary.get("recommendations"):
            summary_lines.extend([
                "",
                "💡 Recommendations:",
            ])
            for rec in validation_summary["recommendations"]:
                summary_lines.append(f"  • {rec}")

        summary_text = "\n".join(summary_lines)

        # Save text summary
        summary_file = output_file.with_suffix('.txt')
        with open(summary_file, 'w') as f:
            f.write(summary_text)

        return summary_text


def main():
    """Main execution function."""
    print("🚀 Stream C1: Testing Framework & Quality Validation")
    print("=" * 60)

    # Create output directory
    output_dir = Path("validation-reports")
    output_dir.mkdir(exist_ok=True)

    # Run validation
    runner = QualityValidationRunner()
    validation_summary = runner.run_comprehensive_validation()

    # Generate report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"validation_report_{timestamp}.json"
    summary_text = runner.generate_report(validation_summary, report_file)

    # Print summary
    print("\n" + "=" * 60)
    print(summary_text)
    print(f"\n📄 Detailed report saved to: {report_file}")

    # Exit with appropriate code
    if validation_summary["overall_status"] == "PASSED":
        print("\n🎉 Stream C1 validation completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Stream C1 validation failed: {validation_summary['overall_status']}")
        sys.exit(1)


if __name__ == "__main__":
    main()