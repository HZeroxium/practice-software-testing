#!/usr/bin/env python3
"""
API Testing Runner for The Toolshop Application
Executes tests using Newman CLI and generates comprehensive reports
"""

import os
import sys
import json
import csv
import subprocess
import argparse
import time
import platform
from datetime import datetime
from pathlib import Path
import requests
from typing import Dict, List, Any, Optional

# Import the report generator
from report_generator import ReportGenerator

# Import data-driven testing components
from data_driven_testing import DataDrivenTestRunner


class APITestRunner:
    def __init__(self, base_url: str = "http://localhost:8091", ci_mode: bool = False):
        self.base_url = base_url
        self.ci_mode = ci_mode
        self.project_root = Path(__file__).parent.parent
        self.reports_dir = self.project_root / "reports"
        self.test_results_dir = self.reports_dir / "test-results"
        self.bug_reports_dir = self.reports_dir / "bug-reports"

        # Create directories if they don't exist
        self.reports_dir.mkdir(exist_ok=True)
        self.test_results_dir.mkdir(exist_ok=True)
        self.bug_reports_dir.mkdir(exist_ok=True)

        # Test collections
        self.collections = {
            "brands": "postman-collections/brands-collection.json",
            "products": "postman-collections/products-collection.json",
            "categories": "postman-collections/categories-collection.json",
        }

        # Initialize results storage
        self.test_results = {}
        self.bugs_found = []

    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        try:
            # Check Newman - try multiple approaches for Windows
            newman_found = False

            # Try direct newman command
            try:
                result = subprocess.run(
                    ["newman", "--version"], capture_output=True, text=True, check=True
                )
                print(f"✓ Newman version: {result.stdout.strip()}")
                newman_found = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

            # Try with npx (for Windows)
            if not newman_found:
                try:
                    result = subprocess.run(
                        ["npx", "newman", "--version"],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    print(f"✓ Newman version (via npx): {result.stdout.strip()}")
                    newman_found = True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass

            # Try with PowerShell (for Windows)
            if not newman_found and platform.system() == "Windows":
                try:
                    result = subprocess.run(
                        ["powershell", "-Command", "newman --version"],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    print(f"✓ Newman version (via PowerShell): {result.stdout.strip()}")
                    newman_found = True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass

            if not newman_found:
                print("❌ Newman is not installed or not in PATH")
                print("  Install Newman: npm install -g newman")
                return False

            # Check if API is accessible
            try:
                response = requests.get(f"{self.base_url}/brands", timeout=5)
                print(f"✓ API is accessible at {self.base_url}")
            except requests.exceptions.RequestException as e:
                print(f"⚠ Warning: API not accessible at {self.base_url}: {e}")
                print("  Make sure the API server is running before executing tests.")
                print("  Expected endpoints: /brands, /products, /categories")

            return True
        except Exception as e:
            print(f"❌ Error checking dependencies: {e}")
            return False

    def count_tests_in_collection(self, collection_file: Path) -> int:
        """Count the number of test cases in a Postman collection"""
        try:
            with open(collection_file, "r", encoding="utf-8") as f:
                collection_data = json.load(f)

            test_count = 0
            if "item" in collection_data:
                for item in collection_data["item"]:
                    if "item" in item:  # Folder
                        for sub_item in item["item"]:
                            if "event" in sub_item:
                                for event in sub_item["event"]:
                                    if event.get("listen") == "test":
                                        test_count += 1
                    elif "event" in item:  # Single request
                        for event in item["event"]:
                            if event.get("listen") == "test":
                                test_count += 1

            return test_count
        except Exception as e:
            print(f"⚠ Warning: Could not count tests in {collection_file}: {e}")
            return 0

    def run_collection(
        self, collection_name: str, collection_path: str
    ) -> Dict[str, Any]:
        """Run a single Postman collection using Newman"""
        print(f"\n🔍 Running {collection_name} collection...")

        collection_file = self.project_root / collection_path
        if not collection_file.exists():
            print(f"❌ Collection file not found: {collection_file}")
            return {"error": "Collection file not found"}

        # Count tests in collection
        expected_test_count = self.count_tests_in_collection(collection_file)

        # Prepare Newman command - use PowerShell for Windows
        if platform.system() == "Windows":
            # Use PowerShell command for Windows
            cmd = [
                "powershell",
                "-Command",
                f"newman run '{collection_file}' --environment '{self.project_root}/postman-collections/environment.json' --reporters cli --reporter-json-export '{self.test_results_dir}/{collection_name}-results.json' --timeout-request 10000 --timeout-script 10000",
            ]
        else:
            cmd = [
                "newman",
                "run",
                str(collection_file),
                "--environment",
                str(self.project_root / "postman-collections" / "environment.json"),
                "--reporters",
                "cli",
                "--reporter-json-export",
                str(self.test_results_dir / f"{collection_name}-results.json"),
                "--reporter-cli-no-summary",
                "--timeout-request",
                "10000",
                "--timeout-script",
                "10000",
            ]

        # Add CI-specific options
        if self.ci_mode:
            cmd.extend(
                [
                    "--reporter-json-export",
                    str(self.test_results_dir / f"{collection_name}-ci-results.json"),
                ]
            )

        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                encoding="utf-8",
                errors="ignore",
            )
            execution_time = time.time() - start_time

            # Parse results
            test_result = {
                "collection": collection_name,
                "execution_time": execution_time,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "expected_test_count": expected_test_count,
            }

            # Try to parse JSON results if available
            json_result_file = self.test_results_dir / f"{collection_name}-results.json"
            if json_result_file.exists():
                try:
                    with open(json_result_file, "r") as f:
                        json_results = json.load(f)
                    test_result["json_results"] = json_results

                    # Extract test statistics
                    if "run" in json_results:
                        run_stats = json_results["run"]["stats"]
                        test_result["stats"] = {
                            "total": run_stats.get("assertions", {}).get("total", 0),
                            "passed": run_stats.get("assertions", {}).get("passed", 0),
                            "failed": run_stats.get("assertions", {}).get("failed", 0),
                            "skipped": run_stats.get("assertions", {}).get(
                                "skipped", 0
                            ),
                        }

                        # Extract failed tests for bug reporting
                        if "executions" in json_results["run"]:
                            for execution in json_results["run"]["executions"]:
                                if execution.get("assertions"):
                                    for assertion in execution["assertions"]:
                                        if assertion.get("error"):
                                            self.bugs_found.append(
                                                {
                                                    "collection": collection_name,
                                                    "test_name": execution.get(
                                                        "item", {}
                                                    ).get("name", "Unknown"),
                                                    "error": assertion["error"].get(
                                                        "message", "Unknown error"
                                                    ),
                                                    "timestamp": datetime.now().isoformat(),
                                                }
                                            )
                except json.JSONDecodeError as e:
                    print(f"⚠ Warning: Could not parse JSON results: {e}")

            # If JSON file doesn't exist, try to extract bugs from stdout
            if not json_result_file.exists() and result.returncode != 0:
                # Parse stdout to extract failed assertions
                stdout_lines = result.stdout.split("\n")
                current_test = "Unknown"

                for line in stdout_lines:
                    # Look for test names (lines starting with →)
                    if line.strip().startswith("→"):
                        current_test = line.strip().split("→")[1].strip()
                    # Look for failed assertions (lines with numbers and "AssertionError")
                    elif "AssertionError" in line and any(
                        char.isdigit() for char in line
                    ):
                        # Extract error message
                        error_msg = line.strip()
                        if error_msg:
                            self.bugs_found.append(
                                {
                                    "collection": collection_name,
                                    "test_name": current_test,
                                    "error": error_msg,
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )

            # If no JSON results but collection succeeded, use expected test count
            if test_result["success"] and "stats" not in test_result:
                test_result["stats"] = {
                    "total": expected_test_count,
                    "passed": expected_test_count,  # Assume all passed if no JSON output
                    "failed": 0,
                    "skipped": 0,
                }
                print(
                    f"✅ {collection_name} collection completed successfully ({expected_test_count} tests)"
                )
            elif test_result["success"]:
                print(f"✅ {collection_name} collection completed successfully")
            else:
                # Even if failed, we know how many tests were expected
                test_result["stats"] = {
                    "total": expected_test_count,
                    "passed": 0,
                    "failed": expected_test_count,
                    "skipped": 0,
                }
                print(
                    f"❌ {collection_name} collection failed ({expected_test_count} tests)"
                )
                print(f"   Error: {result.stderr}")

            return test_result

        except Exception as e:
            print(f"❌ Error running {collection_name} collection: {e}")
            return {"error": str(e), "collection": collection_name}

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test collections"""
        print("🚀 Starting API Test Execution")
        print(f"📅 Test run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"💻 Platform: {platform.system()} {platform.release()}")

        overall_results = {
            "start_time": datetime.now().isoformat(),
            "base_url": self.base_url,
            "platform": f"{platform.system()} {platform.release()}",
            "collections": {},
            "summary": {
                "total_collections": len(self.collections),
                "passed_collections": 0,
                "failed_collections": 0,
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
            },
        }

        for collection_name, collection_path in self.collections.items():
            result = self.run_collection(collection_name, collection_path)
            overall_results["collections"][collection_name] = result

            if result.get("success", False):
                overall_results["summary"]["passed_collections"] += 1
                if "stats" in result:
                    stats = result["stats"]
                    overall_results["summary"]["total_tests"] += stats["total"]
                    overall_results["summary"]["passed_tests"] += stats["passed"]
                    overall_results["summary"]["failed_tests"] += stats["failed"]
            else:
                overall_results["summary"]["failed_collections"] += 1
                # Even for failed collections, count the expected tests
                if "stats" in result:
                    stats = result["stats"]
                    overall_results["summary"]["total_tests"] += stats["total"]
                    overall_results["summary"]["failed_tests"] += stats["failed"]

        overall_results["end_time"] = datetime.now().isoformat()
        overall_results["bugs_found"] = self.bugs_found

        # Save overall results
        results_file = self.test_results_dir / "overall-results.json"
        with open(results_file, "w") as f:
            json.dump(overall_results, f, indent=2)

        return overall_results

    def generate_bug_report(self) -> str:
        """Generate bug report in CSV format"""
        if not self.bugs_found:
            print("✅ No bugs found during testing")
            return ""

        bug_report_file = (
            self.bug_reports_dir
            / f"bug-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"
        )

        with open(bug_report_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "BugID",
                    "Summary",
                    "Steps To Reproduce",
                    "Actual vs Expected Result",
                    "Screenshot",
                    "Priority",
                    "Affected Feature / Version",
                ]
            )

            for i, bug in enumerate(self.bugs_found, 1):
                writer.writerow(
                    [
                        f"BUG-{i:03d}",
                        f"Test failure in {bug['collection']} collection: {bug['test_name']}",
                        f"1. Run {bug['collection']} collection; 2. Execute {bug['test_name']} test",
                        f"Expected: Test should pass; Actual: {bug['error']}",
                        "Screenshot not available for API tests",
                        "Medium" if "timeout" in bug["error"].lower() else "High",
                        f"{bug['collection']} API / sprint5",
                    ]
                )

        print(f"📊 Bug report generated: {bug_report_file}")
        return str(bug_report_file)

    def generate_test_summary(self, results: Dict[str, Any]) -> str:
        """Generate test execution summary"""
        summary_file = (
            self.test_results_dir
            / f"test-summary-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        )

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("API TESTING SUMMARY REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Test Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Base URL: {self.base_url}\n")
            f.write(f"Platform: {results['platform']}\n")
            f.write("\n")

            f.write("COLLECTION RESULTS:\n")
            f.write("-" * 30 + "\n")

            for collection_name, result in results["collections"].items():
                status = "PASSED" if result.get("success", False) else "FAILED"
                f.write(f"{collection_name.upper()}: {status}\n")

                if "stats" in result:
                    stats = result["stats"]
                    f.write(
                        f"  Tests: {stats['total']} total, {stats['passed']} passed, {stats['failed']} failed\n"
                    )

                if "execution_time" in result:
                    f.write(
                        f"  Execution Time: {result['execution_time']:.2f} seconds\n"
                    )

                f.write("\n")

            f.write("OVERALL SUMMARY:\n")
            f.write("-" * 30 + "\n")
            summary = results["summary"]
            f.write(
                f"Collections: {summary['passed_collections']}/{summary['total_collections']} passed\n"
            )
            f.write(
                f"Tests: {summary['passed_tests']}/{summary['total_tests']} passed\n"
            )
            f.write(f"Bugs Found: {len(self.bugs_found)}\n")

            if self.bugs_found:
                f.write("\nBUGS FOUND:\n")
                f.write("-" * 30 + "\n")
                for i, bug in enumerate(self.bugs_found, 1):
                    f.write(
                        f"{i}. {bug['collection']} - {bug['test_name']}: {bug['error']}\n"
                    )

        print(f"📋 Test summary generated: {summary_file}")
        return str(summary_file)

    def create_environment_file(self):
        """Create Newman environment file"""
        env_file = self.project_root / "postman-collections" / "environment.json"
        env_file.parent.mkdir(exist_ok=True)

        environment = {
            "id": "api-testing-env",
            "name": "API Testing Environment",
            "values": [{"key": "base_url", "value": self.base_url, "enabled": True}],
        }

        with open(env_file, "w") as f:
            json.dump(environment, f, indent=2)

        print(f"🌍 Environment file created: {env_file}")


def main():
    parser = argparse.ArgumentParser(description="API Testing Runner for The Toolshop")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8091",
        help="Base URL for the API (default: http://localhost:8091)",
    )
    parser.add_argument(
        "--ci", action="store_true", help="Run in CI/CD mode with additional reporting"
    )
    parser.add_argument(
        "--check-deps", action="store_true", help="Only check dependencies"
    )
    parser.add_argument(
        "--data-driven",
        action="store_true",
        help="Run data-driven tests using CSV files",
    )
    parser.add_argument(
        "--mode",
        choices=["standard", "data-driven", "both"],
        default="standard",
        help="Testing mode: standard (default), data-driven, or both",
    )
    parser.add_argument(
        "--endpoints",
        nargs="+",
        help="Specific endpoints to test (e.g., brands products categories). Default: all endpoints",
    )
    parser.add_argument(
        "--exclude-endpoints",
        nargs="+",
        help="Endpoints to exclude from testing (e.g., categories)",
    )

    args = parser.parse_args()

    # Determine testing mode
    if args.data_driven:
        testing_mode = "data-driven"
    else:
        testing_mode = args.mode

    runner = APITestRunner(base_url=args.base_url, ci_mode=args.ci)

    if args.check_deps:
        runner.check_dependencies()
        return

    print("🔧 Checking dependencies...")
    if not runner.check_dependencies():
        sys.exit(1)

    print("🌍 Creating environment file...")
    runner.create_environment_file()

    # Initialize data-driven test runner if needed
    data_driven_results = None
    if testing_mode in ["data-driven", "both"]:
        print("🚀 Starting Data-Driven API Testing...")
        data_driven_runner = DataDrivenTestRunner(runner.project_root, args.base_url)
        data_driven_results = data_driven_runner.run_all_data_driven_tests(
            include_endpoints=args.endpoints, exclude_endpoints=args.exclude_endpoints
        )

        # Save data-driven results
        if data_driven_results:
            results_dir = runner.project_root / "reports" / "test-results"
            csv_file = data_driven_runner.save_test_results_to_csv(
                data_driven_results, results_dir
            )
            print(f"📊 Data-driven results saved: {csv_file}")

        # Run standard tests if needed
    if testing_mode in ["standard", "both"]:
        print("🚀 Starting Standard API Testing...")
        results = runner.run_all_tests()
    else:
        # Create empty results for data-driven only mode
        results = {
            "summary": {
                "total_collections": 0,
                "passed_collections": 0,
                "failed_collections": 0,
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
            },
            "collections": {},
            "platform": platform.system(),
            "base_url": args.base_url,
        }

    print("📊 Generating comprehensive reports...")
    bug_report = runner.generate_bug_report()
    test_summary = runner.generate_test_summary(results)

    # Initialize report generator and generate all artifacts
    report_generator = ReportGenerator(runner.project_root)
    report_results = report_generator.generate_all_reports(
        results, bug_report, data_driven_results
    )

    # Print final summary
    print("\n" + "=" * 60)
    print("TEST EXECUTION COMPLETED")
    print("=" * 60)

    # Standard test results
    if testing_mode in ["standard", "both"]:
        summary = results["summary"]
        print(f"📊 Standard Tests:")
        print(
            f"   Collections: {summary['passed_collections']}/{summary['total_collections']} passed"
        )
        print(f"   Tests: {summary['passed_tests']}/{summary['total_tests']} passed")
        print(f"   Bugs Found: {len(runner.bugs_found)}")
        if bug_report:
            print(f"   Bug Report: {bug_report}")

    # Data-driven test results
    if testing_mode in ["data-driven", "both"] and data_driven_results:
        dd_summary = data_driven_results["summary"]
        print(f"📊 Data-Driven Tests:")
        print(f"   Endpoints: {dd_summary['total_endpoints']}")
        print(f"   Test Cases: {dd_summary['total_tests']}")
        print(f"   Passed: {dd_summary['passed_tests']}")
        print(f"   Failed: {dd_summary['failed_tests']}")
        print(f"   Success Rate: {dd_summary['success_rate']:.1f}%")
        print(f"   Bugs Found: {dd_summary['bugs_found']}")

    print(f"📋 Reports written to README.md and StudentID_APITesting.md")
    print("📊 Excel Files Generated:")
    for excel_file in report_results["excel_files"]:
        print(f"  - {excel_file}")

    # Exit with appropriate code
    has_failures = False

    if testing_mode in ["standard", "both"]:
        if results["summary"]["failed_collections"] > 0:
            has_failures = True

    if testing_mode in ["data-driven", "both"] and data_driven_results:
        if data_driven_results["summary"]["failed_tests"] > 0:
            has_failures = True

    if has_failures:
        print("❌ Some tests failed!")
        sys.exit(1)
    else:
        print("✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
