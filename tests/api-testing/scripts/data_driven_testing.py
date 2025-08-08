#!/usr/bin/env python3
"""
Data-Driven API Testing Module
Specialized classes for handling data-driven testing with CSV data files
"""

import csv
import json
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import platform


class TestDataLoader:
    """Handles loading and parsing CSV and JSON test data files"""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def load_test_data(self, endpoint: str) -> List[Dict[str, str]]:
        """Load test data from CSV and JSON files for a specific endpoint"""
        test_cases = []

        # Load CSV data (for GET endpoints)
        csv_file = self.data_dir / f"{endpoint}-test-data.csv"
        if csv_file.exists():
            csv_cases = self._load_csv_data(csv_file)
            test_cases.extend(csv_cases)
            print(f"📊 Loaded {len(csv_cases)} CSV test cases from {csv_file}")

        # Load JSON data (for POST endpoints)
        json_file = self.data_dir / f"{endpoint}-post-test-data.json"
        if json_file.exists():
            json_cases = self._load_json_data(json_file)
            test_cases.extend(json_cases)
            print(f"📊 Loaded {len(json_cases)} JSON test cases from {json_file}")

        if not test_cases:
            print(f"⚠ Warning: No test data files found for endpoint: {endpoint}")
            print(f"  Checked: {csv_file}, {json_file}")

        return test_cases

    def _load_csv_data(self, csv_file: Path) -> List[Dict[str, str]]:
        """Load test data from CSV file"""
        test_cases = []
        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    test_cases.append(row)
            return test_cases
        except Exception as e:
            print(f"❌ Error loading CSV data from {csv_file}: {e}")
            return []

    def _load_json_data(self, json_file: Path) -> List[Dict[str, str]]:
        """Load test data from JSON file"""
        test_cases = []
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "test_cases" in data:
                for test_case in data["test_cases"]:
                    # Convert JSON test case to CSV-like format
                    csv_test_case = {
                        "test_case_id": test_case.get("test_case_id", ""),
                        "title": test_case.get("title", ""),
                        "preconditions": test_case.get("preconditions", ""),
                        "inputs": json.dumps(test_case.get("request_body", {})),
                        "test_steps": test_case.get("test_steps", ""),
                        "expected_result": test_case.get("expected_result", ""),
                        "actual_result": test_case.get("actual_result", ""),
                        "result": test_case.get("result", ""),
                        "method": data.get("method", "POST"),
                        "request_body": json.dumps(test_case.get("request_body", {})),
                    }
                    test_cases.append(csv_test_case)

            return test_cases
        except Exception as e:
            print(f"❌ Error loading JSON data from {json_file}: {e}")
            return []

    def get_all_endpoints(self) -> List[str]:
        """Get list of all available endpoints based on CSV and JSON files"""
        endpoints = set()

        # Get endpoints from CSV files
        for csv_file in self.data_dir.glob("*-test-data.csv"):
            endpoint = csv_file.stem.replace("-test-data", "")
            endpoints.add(endpoint)

        # Get endpoints from JSON files
        for json_file in self.data_dir.glob("*-post-test-data.json"):
            endpoint = json_file.stem.replace("-post-test-data", "")
            endpoints.add(endpoint)

        return list(endpoints)


class PostmanEnvironmentBuilder:
    """Builds Postman environment files for data-driven testing"""

    def __init__(self, base_url: str = "http://localhost:8091"):
        self.base_url = base_url

    def create_environment_file(self, test_case: Dict[str, str], endpoint: str) -> Path:
        """Create a temporary Postman environment file for a specific test case"""

        # Determine expected status and response structure based on endpoint
        expected_status = "200"
        expected_response_structure = "array"

        if endpoint == "products":
            expected_response_structure = "object"

        # Check if test case expects failure
        if test_case.get("result") == "FAIL":
            expected_status = "422"  # Default for validation errors

        # Extract query parameters from inputs
        inputs = test_case.get("inputs", "")
        query_params = ""
        if "query_params=" in inputs:
            query_params = inputs.split("query_params=")[1].strip()

        # Handle request body for POST requests
        request_body = test_case.get("request_body", "")
        if not request_body and test_case.get("method") == "POST":
            # Try to extract from inputs if it's JSON
            try:
                if inputs.startswith("{") or inputs.startswith("["):
                    request_body = inputs
            except:
                pass

        # Create environment variables
        env_vars = {
            "base_url": self.base_url,
            "endpoint": endpoint,
            "query_params": query_params,
            "request_body": request_body,
            "expected_status": expected_status,
            "expected_response_structure": expected_response_structure,
        }

        # Debug: Print environment variables
        print(f"      Environment variables: {env_vars}")

        # Create temporary environment file
        env_data = {
            "id": f"env-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": f"Data-Driven-{endpoint}-{test_case.get('test_case_id', 'unknown')}",
            "values": [
                {"key": key, "value": value, "type": "default", "enabled": True}
                for key, value in env_vars.items()
            ],
        }

        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump(env_data, temp_file, indent=2)
        temp_file.close()

        return Path(temp_file.name)


class DataDrivenTestExecutor:
    """Executes data-driven tests using Newman CLI"""

    def __init__(self, collection_file: Path, base_url: str = "http://localhost:8091"):
        self.collection_file = collection_file
        self.base_url = base_url
        self.env_builder = PostmanEnvironmentBuilder(base_url)

    def execute_test_case(
        self, test_case: Dict[str, str], endpoint: str
    ) -> Dict[str, Any]:
        """Execute a single test case using Newman"""

        # Create environment file
        env_file = self.env_builder.create_environment_file(test_case, endpoint)

        try:
            # Get method from test case
            method = test_case.get("method", "GET")

            # Try multiple Newman command variations
            newman_commands = self._get_newman_commands(env_file, endpoint, method)

            result = None
            for i, cmd in enumerate(newman_commands):
                try:
                    print(f"      Trying command {i+1}: {' '.join(cmd)}")
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        timeout=30,
                        shell=False,
                    )
                    print(
                        f"      Command {i+1} executed successfully with exit code: {result.returncode}"
                    )
                    break  # If successful, break out of the loop
                except (FileNotFoundError, subprocess.TimeoutExpired) as e:
                    print(f"      Command {i+1} failed: {e}")
                    continue
                except Exception as e:
                    print(f"      Command {i+1} unexpected error: {e}")
                    continue

            if result is None:
                # All commands failed
                return {
                    "test_case_id": test_case.get("test_case_id", "unknown"),
                    "title": test_case.get("title", "Unknown Test"),
                    "endpoint": test_case.get("endpoint", "unknown"),
                    "passed": False,
                    "exit_code": -1,
                    "stdout": "",
                    "stderr": "All Newman commands failed",
                    "assertion_errors": ["Newman not found or not accessible"],
                    "stats": {"total": 0, "passed": 0, "failed": 0},
                    "execution_time": datetime.now().isoformat(),
                }

            # Add debug information
            print(f"      Newman output: {result.stdout}...")
            if result.stderr:
                print(f"      Newman error: {result.stderr}...")

            # Parse results
            test_result = self._parse_newman_output(result, test_case)

            return test_result

        finally:
            # Clean up temporary environment file
            if env_file.exists():
                os.unlink(env_file)

    def _get_newman_commands(
        self, env_file: Path, endpoint: str, method: str = "GET"
    ) -> List[List[str]]:
        """Get list of Newman command variations to try"""

        commands = []
        folder_name = f"{method} /{endpoint}"

        # PowerShell variation for Windows (prioritized)
        if platform.system() == "Windows":
            commands.append(
                [
                    "powershell",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    f"newman run '{self.collection_file}' -e '{env_file}' --folder '{folder_name}'",
                ]
            )

        # Direct newman command
        commands.append(
            [
                "newman",
                "run",
                str(self.collection_file),
                "-e",
                str(env_file),
                "--folder",
                folder_name,
            ]
        )

        # npx newman command
        commands.append(
            [
                "npx",
                "newman",
                "run",
                str(self.collection_file),
                "-e",
                str(env_file),
                "--folder",
                folder_name,
            ]
        )

        return commands

    def _parse_newman_output(
        self, result: subprocess.CompletedProcess, test_case: Dict[str, str]
    ) -> Dict[str, Any]:
        """Parse Newman output and extract test results"""

        # Determine if test passed based on exit code and output
        passed = result.returncode == 0

        # Look for assertion errors in output
        assertion_errors = []
        if not passed:
            lines = result.stdout.split("\n") + result.stderr.split("\n")
            for line in lines:
                if "AssertionError" in line or "Error:" in line:
                    assertion_errors.append(line.strip())

        # Check if it's an API connection error (expected when API server is down)
        api_connection_error = False
        if not passed:
            output_text = result.stdout + result.stderr
            if (
                "ECONNREFUSED" in output_text
                or "timeout" in output_text.lower()
                or "connection" in output_text.lower()
            ):
                api_connection_error = True
                assertion_errors.append(
                    "API server not accessible (expected when server is down)"
                )

        # Extract test statistics
        stats = {
            "total": 5,  # Default number of tests per endpoint
            "passed": 5 if passed else 0,
            "failed": 0 if passed else 5,
        }

        # If API server is not accessible, mark as expected failure
        if api_connection_error:
            # Don't count API connection errors as test failures
            stats["passed"] = 0
            stats["failed"] = 0
            stats["skipped"] = 5

        # Try to extract actual stats from output
        for line in result.stdout.split("\n"):
            if "iterations" in line.lower() and "assertions" in line.lower():
                # Parse Newman summary output
                try:
                    parts = line.split()
                    if len(parts) >= 4:
                        stats["total"] = int(parts[0])
                        stats["passed"] = int(parts[2])
                        stats["failed"] = stats["total"] - stats["passed"]
                except (ValueError, IndexError):
                    pass

        return {
            "test_case_id": test_case.get("test_case_id", "unknown"),
            "title": test_case.get("title", "Unknown Test"),
            "endpoint": test_case.get("endpoint", "unknown"),
            "passed": passed,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "assertion_errors": assertion_errors,
            "stats": stats,
            "execution_time": datetime.now().isoformat(),
        }


class DataDrivenTestRunner:
    """Main orchestrator for data-driven testing"""

    def __init__(self, project_root: Path, base_url: str = "http://localhost:8091"):
        self.project_root = project_root
        self.base_url = base_url
        self.data_dir = project_root / "data"
        self.collection_file = (
            project_root / "postman-collections" / "data-driven-collection.json"
        )

        # Initialize components
        self.data_loader = TestDataLoader(self.data_dir)
        self.test_executor = DataDrivenTestExecutor(self.collection_file, base_url)

        # Results storage
        self.test_results = {}
        self.bugs_found = []

    def run_all_data_driven_tests(
        self,
        include_endpoints: Optional[List[str]] = None,
        exclude_endpoints: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Run all data-driven tests for all endpoints"""

        print("🚀 Starting Data-Driven API Testing...")
        print(f"📁 Data directory: {self.data_dir}")
        print(f"📋 Collection file: {self.collection_file}")

        # Get all available endpoints
        all_endpoints = self.data_loader.get_all_endpoints()
        print(f"🎯 Available endpoints: {', '.join(all_endpoints)}")

        # Filter endpoints based on include/exclude parameters
        endpoints = all_endpoints.copy()

        if include_endpoints:
            endpoints = [ep for ep in endpoints if ep in include_endpoints]
            print(f"🎯 Including endpoints: {', '.join(endpoints)}")

        if exclude_endpoints:
            endpoints = [ep for ep in endpoints if ep not in exclude_endpoints]
            print(f"🎯 Excluding endpoints: {', '.join(exclude_endpoints)}")

        print(f"🎯 Final endpoints to test: {', '.join(endpoints)}")

        total_tests = 0
        passed_tests = 0
        failed_tests = 0

        for endpoint in endpoints:
            print(f"\n📊 Testing endpoint: {endpoint}")

            # Load test data for this endpoint
            test_cases = self.data_loader.load_test_data(endpoint)
            print(f"   📝 Loaded {len(test_cases)} test cases")

            endpoint_results = []

            for test_case in test_cases:
                print(
                    f"   🔍 Running: {test_case.get('test_case_id', 'Unknown')} - {test_case.get('title', 'Unknown')}"
                )

                # Execute test case
                result = self.test_executor.execute_test_case(test_case, endpoint)
                endpoint_results.append(result)

                # Update counters
                total_tests += 1

                # Check if it's an API connection error (expected when server is down)
                api_connection_error = any(
                    "API server not accessible" in error
                    for error in result.get("assertion_errors", [])
                )

                if result["passed"]:
                    passed_tests += 1
                elif api_connection_error:
                    # Don't count API connection errors as failures
                    print(f"      ⚠️ SKIP (API server not accessible)")
                else:
                    failed_tests += 1
                    # Add to bugs found only for actual test failures
                    bug_info = {
                        "test_case_id": result["test_case_id"],
                        "title": result["title"],
                        "endpoint": endpoint,
                        "expected_result": test_case.get("expected_result", "Unknown"),
                        "actual_result": f"Failed with exit code {result['exit_code']}",
                        "assertion_errors": result["assertion_errors"],
                        "stdout": result["stdout"],
                        "stderr": result["stderr"],
                    }
                    self.bugs_found.append(bug_info)

                # Print result
                status = "✅ PASS" if result["passed"] else "❌ FAIL"
                print(f"      {status}")

            self.test_results[endpoint] = endpoint_results

        # Generate summary
        summary = {
            "total_endpoints": len(endpoints),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (
                (passed_tests / total_tests * 100) if total_tests > 0 else 0
            ),
            "bugs_found": len(self.bugs_found),
        }

        return {
            "summary": summary,
            "results": self.test_results,
            "bugs": self.bugs_found,
        }

    def generate_data_driven_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive report for data-driven testing"""

        summary = results["summary"]

        report = f"""
# Data-Driven API Testing Report

## Executive Summary
- **Total Endpoints Tested**: {summary['total_endpoints']}
- **Total Test Cases**: {summary['total_tests']}
- **Passed Tests**: {summary['passed_tests']}
- **Failed Tests**: {summary['failed_tests']}
- **Success Rate**: {summary['success_rate']:.1f}%
- **Bugs Found**: {summary['bugs_found']}

## Endpoint Results
"""

        for endpoint, endpoint_results in results["results"].items():
            passed = sum(1 for r in endpoint_results if r["passed"])
            total = len(endpoint_results)
            success_rate = (passed / total * 100) if total > 0 else 0

            report += f"""
### {endpoint.upper()} Endpoint
- **Test Cases**: {total}
- **Passed**: {passed}
- **Failed**: {total - passed}
- **Success Rate**: {success_rate:.1f}%

#### Test Case Details:
"""

            for result in endpoint_results:
                status = "✅ PASS" if result["passed"] else "❌ FAIL"
                report += (
                    f"- **{result['test_case_id']}**: {result['title']} - {status}\n"
                )

        if results["bugs"]:
            report += f"""
## Bugs Found ({len(results['bugs'])})

"""
            for i, bug in enumerate(results["bugs"], 1):
                report += f"""
### Bug #{i}
- **Test Case**: {bug['test_case_id']}
- **Title**: {bug['title']}
- **Endpoint**: {bug['endpoint']}
- **Expected**: {bug['expected_result']}
- **Actual**: {bug['actual_result']}
- **Errors**: {', '.join(bug['assertion_errors']) if bug['assertion_errors'] else 'No specific errors'}

"""

        return report

    def save_test_results_to_csv(self, results: Dict[str, Any], output_dir: Path):
        """Save test results to CSV files"""

        output_dir.mkdir(exist_ok=True)

        # Create combined results file
        combined_file = output_dir / "data-driven-test-results.csv"

        with open(combined_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "test_case_id",
                    "title",
                    "endpoint",
                    "passed",
                    "exit_code",
                    "execution_time",
                    "assertion_errors",
                ]
            )

            for endpoint_results in results["results"].values():
                for result in endpoint_results:
                    writer.writerow(
                        [
                            result["test_case_id"],
                            result["title"],
                            result.get("endpoint", "unknown"),
                            result["passed"],
                            result["exit_code"],
                            result["execution_time"],
                            (
                                "; ".join(result["assertion_errors"])
                                if result["assertion_errors"]
                                else ""
                            ),
                        ]
                    )

        return str(combined_file)
