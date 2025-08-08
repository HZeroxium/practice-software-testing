#!/usr/bin/env python3
"""
Performance Testing Automation Orchestrator

This script orchestrates the complete performance testing workflow for Product Listing scenario:
1. Generate JMeter test plans dynamically from configuration
2. Execute JMeter test plans for multiple data-driven test cases
3. Generate bug reports based on results
4. Update test case results
5. Update the main performance testing report
6. Clean up old reports

Author: Performance Testing Automation
Date: 2024
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from jmeter_runner import JMeterRunner
from report_generator import ReportGenerator
from report_cleaner import ReportCleaner
from config_manager import ConfigManager
from jmeter_template_generator import JMeterTemplateGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("performance_testing.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

# Force UTF-8 encoding for console output
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
logger = logging.getLogger(__name__)


class PerformanceTestingOrchestrator:
    """Main orchestrator for performance testing automation"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.scripts_dir = self.base_dir / "scripts"
        self.data_dir = self.base_dir / "data"
        self.results_dir = self.base_dir / "results"
        self.report_dir = self.base_dir / "report"
        self.config_dir = self.base_dir / "config"
        self.config_file = self.config_dir / "test_config.json"

        # Ensure directories exist
        self.results_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)

        # Initialize components
        self.config_manager = ConfigManager(str(self.config_file))
        self.template_generator = JMeterTemplateGenerator(str(self.config_file))
        self.jmeter_runner = JMeterRunner(
            scripts_dir=str(self.scripts_dir),
            results_dir=str(self.results_dir),
            config_file=str(self.config_file),
        )
        self.report_generator = ReportGenerator(
            data_dir=str(self.data_dir), results_dir=str(self.results_dir)
        )
        self.report_cleaner = ReportCleaner(
            results_dir=str(self.results_dir),
            keep_recent=self._get_keep_recent_from_config(),
        )

    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        logger.info("Checking prerequisites...")

        # Check if JMeter is available
        if not self.jmeter_runner._find_jmeter_home():
            logger.error(
                "JMeter not found. Please install JMeter and set JMETER_HOME environment variable."
            )
            return False

        # Check if data files exist
        required_data_files = [
            "StudentID_TestCases.csv",  # Still need CSV for reading initial data
        ]

        for data_file in required_data_files:
            data_path = self.data_dir / data_file
            if not data_path.exists():
                logger.error(f"Required data file not found: {data_path}")
                return False

        # Check if main report file exists
        main_report_file = self.report_dir / "StudentID_PerformanceTesting.md"
        if not main_report_file.exists():
            logger.error(f"Main report file not found: {main_report_file}")
            return False

        logger.info("All prerequisites met successfully")
        return True

    def generate_jmeter_templates(self) -> bool:
        """Generate JMeter test templates from configuration"""
        try:
            logger.info("Generating JMeter test templates...")
            self.template_generator.generate_all_templates()
            logger.info("JMeter templates generated successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to generate JMeter templates: {e}")
            return False

    def _get_keep_recent_from_config(self) -> int:
        """Get keep_recent_reports value from configuration"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            return config.get("reporting", {}).get("keep_recent_reports", 2)
        except Exception:
            return 2

    def _should_cleanup_reports(self) -> bool:
        """Check if cleanup is enabled in configuration"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            return config.get("reporting", {}).get("cleanup_old_results", True)
        except Exception:
            return True

    def run_jmeter_tests(self) -> List[Dict]:
        """Run all JMeter tests for Product Listing scenario"""
        try:
            logger.info("Starting JMeter test execution...")

            # Load configuration to get test cases
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            product_listing_config = config.get("test_scenarios", {}).get(
                "product_listing", {}
            )
            if not product_listing_config.get("enabled", False):
                logger.warning("Product Listing scenario is disabled")
                return []

            test_results = []

            # Run load test cases
            for test_case in product_listing_config.get("load_test_cases", []):
                if test_case.get("enabled", False):
                    logger.info(f"Running load test: {test_case['name']}")
                    result = self.jmeter_runner.run_test(
                        test_name=test_case["name"],
                        jmx_file=f"{test_case['name']}.jmx",
                        expected_response_time=test_case.get(
                            "expected_response_time", 2000
                        ),
                        expected_throughput=test_case.get("expected_throughput", 25),
                        expected_error_rate=test_case.get("expected_error_rate", 1.0),
                    )
                    result["test_type"] = "load"
                    result["test_case"] = test_case
                    test_results.append(result)

            # Run stress test cases
            for test_case in product_listing_config.get("stress_test_cases", []):
                if test_case.get("enabled", False):
                    logger.info(f"Running stress test: {test_case['name']}")
                    result = self.jmeter_runner.run_test(
                        test_name=test_case["name"],
                        jmx_file=f"{test_case['name']}.jmx",
                        expected_response_time=test_case.get(
                            "expected_response_time", 5000
                        ),
                        expected_throughput=test_case.get("expected_throughput", 15),
                        expected_error_rate=test_case.get("expected_error_rate", 5.0),
                    )
                    result["test_type"] = "stress"
                    result["test_case"] = test_case
                    test_results.append(result)

            # Run spike test cases
            for test_case in product_listing_config.get("spike_test_cases", []):
                if test_case.get("enabled", False):
                    logger.info(f"Running spike test: {test_case['name']}")
                    result = self.jmeter_runner.run_test(
                        test_name=test_case["name"],
                        jmx_file=f"{test_case['name']}.jmx",
                        expected_response_time=test_case.get(
                            "expected_response_time", 3000
                        ),
                        expected_throughput=test_case.get("expected_throughput", 20),
                        expected_error_rate=test_case.get("expected_error_rate", 2.0),
                    )
                    result["test_type"] = "spike"
                    result["test_case"] = test_case
                    test_results.append(result)

            logger.info(f"Completed {len(test_results)} test executions")
            return test_results

        except Exception as e:
            logger.error(f"Failed to run JMeter tests: {e}")
            return []

    def generate_reports(self, test_results: List[Dict]) -> Dict:
        """Generate reports based on test results"""
        try:
            logger.info("Generating reports...")

            # Generate bug reports and update test cases
            report_data = self.report_generator.generate_reports(test_results)

            # Clean up old reports if enabled
            if self._should_cleanup_reports():
                logger.info("Cleaning up old reports...")
                self.report_cleaner.run_cleanup()

            logger.info("Reports generated successfully")
            return report_data

        except Exception as e:
            logger.error(f"Failed to generate reports: {e}")
            return {}

    def update_main_report(self, results: Dict) -> bool:
        """Update the main performance testing report"""
        try:
            logger.info("Updating main performance testing report...")

            main_report_file = self.report_dir / "StudentID_PerformanceTesting.md"
            if not main_report_file.exists():
                logger.error(f"Main report file not found: {main_report_file}")
                return False

            # Read current content
            with open(main_report_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Update test execution section
            content = self._update_test_execution_section(content, results)

            # Update bugs found section
            content = self._update_bugs_found_section(content, results)

            # Update self assessment section
            content = self._update_self_assessment(content, results)

            # Write updated content
            with open(main_report_file, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info("Main report updated successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to update main report: {e}")
            return False

    def _update_test_execution_section(self, content: str, results: Dict) -> str:
        """Update the test execution section in the main report"""
        try:
            # Find the test execution section
            start_marker = "## Test Execution"
            end_marker = "## Bugs Found"

            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker)

            if start_idx == -1 or end_idx == -1:
                logger.warning("Could not find test execution section markers")
                return content

            # Generate new test execution content
            new_section = f"{start_marker}\n\n"
            new_section += "### Product Listing Performance Test Results\n\n"

            if results.get("test_results"):
                new_section += "| Test Case | Test Type | Status | Response Time (ms) | Throughput (req/sec) | Error Rate (%) |\n"
                new_section += "|-----------|-----------|--------|-------------------|---------------------|----------------|\n"

                for result in results["test_results"]:
                    test_case = result.get("test_case", {})
                    test_name = test_case.get("name", "Unknown")
                    test_type = result.get("test_type", "Unknown")
                    status = result.get("status", "UNKNOWN")
                    response_time = result.get("avg_response_time", 0)
                    throughput = result.get("throughput", 0)
                    error_rate = result.get("error_rate", 0)

                    new_section += f"| {test_name} | {test_type.title()} | {status} | {response_time:.2f} | {throughput:.2f} | {error_rate:.2f} |\n"
            else:
                new_section += "No test results available.\n"

            new_section += "\n"

            # Replace the section
            before_section = content[:start_idx]
            after_section = content[end_idx:]
            updated_content = before_section + new_section + after_section

            return updated_content

        except Exception as e:
            logger.error(f"Error updating test execution section: {e}")
            return content

    def _update_bugs_found_section(self, content: str, results: Dict) -> str:
        """Update the bugs found section in the main report"""
        try:
            # Find the bugs found section
            start_marker = "## Bugs Found"
            end_marker = "## Self Assessment"

            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker)

            if start_idx == -1 or end_idx == -1:
                logger.warning("Could not find bugs found section markers")
                return content

            # Generate new bugs found content
            new_section = f"{start_marker}\n\n"

            if results.get("bugs_found"):
                new_section += "### Performance Issues Identified\n\n"
                new_section += "| Bug ID | Summary | Priority | Affected Feature |\n"
                new_section += "|--------|---------|----------|-------------------|\n"

                for bug in results["bugs_found"]:
                    bug_id = bug.get("bug_id", "Unknown")
                    summary = bug.get("summary", "Unknown")
                    priority = bug.get("priority", "Unknown")
                    feature = bug.get("affected_feature", "Product Listing")

                    new_section += (
                        f"| {bug_id} | {summary} | {priority} | {feature} |\n"
                    )
            else:
                new_section += "No performance issues identified during testing.\n"

            new_section += "\n"

            # Replace the section
            before_section = content[:start_idx]
            after_section = content[end_idx:]
            updated_content = before_section + new_section + after_section

            return updated_content

        except Exception as e:
            logger.error(f"Error updating bugs found section: {e}")
            return content

    def _update_self_assessment(self, content: str, results: Dict) -> str:
        """Update the self assessment section in the main report"""
        try:
            # Find the self assessment section
            start_marker = "## Self Assessment"

            start_idx = content.find(start_marker)
            if start_idx == -1:
                logger.warning("Could not find self assessment section marker")
                return content

            # Generate new self assessment content
            new_section = f"{start_marker}\n\n"

            # Calculate overall metrics
            total_tests = len(results.get("test_results", []))
            passed_tests = len(
                [
                    r
                    for r in results.get("test_results", [])
                    if r.get("status") == "PASS"
                ]
            )
            failed_tests = total_tests - passed_tests

            new_section += f"### Test Execution Summary\n\n"
            new_section += f"- **Total Test Cases Executed**: {total_tests}\n"
            new_section += f"- **Passed Tests**: {passed_tests}\n"
            new_section += f"- **Failed Tests**: {failed_tests}\n"
            new_section += f"- **Success Rate**: {(passed_tests/total_tests*100):.1f}% (if total > 0)\n\n"

            new_section += f"### Performance Assessment\n\n"

            if results.get("bugs_found"):
                new_section += (
                    f"- **Performance Issues Found**: {len(results['bugs_found'])}\n"
                )
                new_section += f"- **Critical Issues**: {len([b for b in results['bugs_found'] if b.get('priority') == 'Critical'])}\n"
                new_section += f"- **High Priority Issues**: {len([b for b in results['bugs_found'] if b.get('priority') == 'High'])}\n"
            else:
                new_section += "- **Performance Issues Found**: 0\n"
                new_section += "- **All performance criteria met successfully**\n"

            new_section += "\n### Recommendations\n\n"

            if failed_tests > 0:
                new_section += "- Review and optimize Product Listing API endpoints\n"
                new_section += "- Consider implementing caching mechanisms\n"
                new_section += "- Monitor database query performance\n"
            else:
                new_section += "- Current performance meets requirements\n"
                new_section += "- Continue monitoring under production load\n"
                new_section += "- Consider load testing with higher user volumes\n"

            new_section += "\n"

            # Replace the section and everything after it
            before_section = content[:start_idx]
            updated_content = before_section + new_section

            return updated_content

        except Exception as e:
            logger.error(f"Error updating self assessment section: {e}")
            return content

    def generate_final_summary(self, results: Dict) -> None:
        """Generate a final summary of the test execution"""
        try:
            logger.info("Generating final summary...")

            summary_file = self.results_dir / "test_execution_summary.json"
            summary_data = {
                "execution_timestamp": datetime.now().isoformat(),
                "total_tests": len(results.get("test_results", [])),
                "passed_tests": len(
                    [
                        r
                        for r in results.get("test_results", [])
                        if r.get("status") == "PASS"
                    ]
                ),
                "failed_tests": len(
                    [
                        r
                        for r in results.get("test_results", [])
                        if r.get("status") == "FAIL"
                    ]
                ),
                "bugs_found": len(results.get("bugs_found", [])),
                "test_results": results.get("test_results", []),
                "bugs": results.get("bugs_found", []),
            }

            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Final summary saved to: {summary_file}")

            # Print summary to console
            print("\n" + "=" * 60)
            print("PERFORMANCE TESTING EXECUTION SUMMARY")
            print("=" * 60)
            print(f"Total Tests Executed: {summary_data['total_tests']}")
            print(f"Passed Tests: {summary_data['passed_tests']}")
            print(f"Failed Tests: {summary_data['failed_tests']}")
            print(f"Bugs Found: {summary_data['bugs_found']}")
            print(
                f"Success Rate: {(summary_data['passed_tests']/summary_data['total_tests']*100):.1f}%"
                if summary_data["total_tests"] > 0
                else "Success Rate: N/A"
            )
            print("=" * 60)

        except Exception as e:
            logger.error(f"Failed to generate final summary: {e}")

    def run_complete_workflow(self) -> bool:
        """Run the complete performance testing workflow"""
        try:
            logger.info("Starting complete performance testing workflow...")

            # Step 1: Check prerequisites
            if not self.check_prerequisites():
                logger.error("Prerequisites check failed")
                return False

            # Step 2: Generate JMeter templates
            if not self.generate_jmeter_templates():
                logger.error("JMeter template generation failed")
                return False

            # Step 3: Run JMeter tests
            test_results = self.run_jmeter_tests()
            if not test_results:
                logger.warning("No test results obtained")
                test_results = []

            # Step 4: Generate reports
            report_data = self.generate_reports(test_results)
            report_data["test_results"] = (
                test_results  # Ensure test results are included
            )

            # Step 5: Update main report
            if not self.update_main_report(report_data):
                logger.error("Failed to update main report")
                return False

            # Step 6: Generate final summary
            self.generate_final_summary(report_data)

            logger.info("Complete performance testing workflow finished successfully")
            return True

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return False


def main():
    """Main function to run the performance testing orchestrator"""
    try:
        orchestrator = PerformanceTestingOrchestrator()
        success = orchestrator.run_complete_workflow()

        if success:
            print("\n✅ Performance testing completed successfully!")
            print("📊 Check the following files for results:")
            print(f"   - Test Cases: {orchestrator.data_dir}/StudentID_TestCases.xlsx")
            print(f"   - Bug Report: {orchestrator.data_dir}/StudentID_BugReport.xlsx")
            print(
                f"   - Main Report: {orchestrator.report_dir}/StudentID_PerformanceTesting.md"
            )
            print(f"   - Results: {orchestrator.results_dir}/")
        else:
            print("\n❌ Performance testing failed!")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        print(f"\n❌ Execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
