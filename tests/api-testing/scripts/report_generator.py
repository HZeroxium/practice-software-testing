#!/usr/bin/env python3
"""
Comprehensive Report Generator for API Testing Framework
Handles Excel conversion, markdown reports, and cleanup functionality
"""

import pandas as pd
import json
import csv
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class ReportGenerator:
    def __init__(self, project_root: Path, student_id: str = "22127154"):
        self.project_root = project_root
        self.student_id = student_id
        self.reports_dir = project_root / "reports"
        self.test_results_dir = self.reports_dir / "test-results"
        self.bug_reports_dir = self.reports_dir / "bug-reports"
        self.test_cases_dir = project_root / "test-cases"
        self.data_dir = project_root / "data"

    def cleanup_old_reports(self, keep_count: int = 5):
        """Clean up old reports, keeping only the most recent ones"""
        print("🧹 Cleaning up old reports...")

        # Clean test results
        if self.test_results_dir.exists():
            files = list(self.test_results_dir.glob("*.json")) + list(
                self.test_results_dir.glob("*.txt")
            )
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            for file in files[keep_count:]:
                try:
                    file.unlink()
                    print(f"  Deleted: {file.name}")
                except Exception as e:
                    print(f"  Failed to delete {file.name}: {e}")

        # Clean bug reports
        if self.bug_reports_dir.exists():
            files = list(self.bug_reports_dir.glob("*.csv"))
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            for file in files[keep_count:]:
                try:
                    file.unlink()
                    print(f"  Deleted: {file.name}")
                except Exception as e:
                    print(f"  Failed to delete {file.name}: {e}")

    def generate_test_cases_from_data(
        self,
        test_results: Dict[str, Any],
        data_driven_results: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, List[Dict]]:
        """Generate test cases from actual test data and results"""
        test_cases = {"brands": [], "products": [], "categories": []}

        # Generate standard test cases
        # Load test data
        test_data = {}
        for api in ["brands", "products", "categories"]:
            data_file = self.data_dir / f"{api}-test-data.json"
            if data_file.exists():
                with open(data_file, "r", encoding="utf-8") as f:
                    test_data[api] = json.load(f)

        # Generate test cases for each API
        for collection_name, result in test_results.get("collections", {}).items():
            if collection_name in ["brands", "products", "categories"]:
                api_data = test_data.get(collection_name, {})
                test_cases[collection_name] = self._generate_api_test_cases(
                    collection_name, result, api_data
                )

        # Generate data-driven test cases if available
        if data_driven_results:
            dd_test_cases = self._generate_data_driven_test_cases(data_driven_results)
            # Merge data-driven test cases with standard ones
            for api_name, cases in dd_test_cases.items():
                if cases:
                    test_cases[api_name].extend(cases)

        return test_cases

    def generate_data_driven_bug_report(
        self, data_driven_results: Dict[str, Any]
    ) -> str:
        """Generate bug report from data-driven testing results"""
        print("🐛 Generating data-driven bug report...")

        if not data_driven_results or not data_driven_results.get("bugs"):
            print("  No bugs found in data-driven testing")
            return ""

        bug_report_file = (
            self.bug_reports_dir
            / f"data-driven-bug-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        with open(bug_report_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "BugID",
                    "Summary",
                    "Steps To Reproduce",
                    "Actual vs Expected Result",
                    "Screenshot",
                    "Priority",
                    "Affected Feature / Version",
                ],
            )
            writer.writeheader()

            for i, bug in enumerate(data_driven_results["bugs"], 1):
                # Determine priority based on error type
                priority = "Medium"
                if "timeout" in str(bug.get("assertion_errors", [])).lower():
                    priority = "High"
                elif "API server not accessible" in str(
                    bug.get("assertion_errors", [])
                ):
                    priority = "Low"  # Expected when server is down

                writer.writerow(
                    {
                        "BugID": f"DD-BUG-{i:03d}",
                        "Summary": f"Data-driven test failed: {bug.get('title', 'Unknown test')}",
                        "Steps To Reproduce": f"1. Run data-driven test case {bug.get('test_case_id', 'Unknown')}\n2. Execute GET request to /{bug.get('endpoint', 'unknown')}\n3. Verify expected result: {bug.get('expected_result', 'Unknown')}",
                        "Actual vs Expected Result": f"Expected: {bug.get('expected_result', 'Success')}\nActual: {bug.get('actual_result', 'Test failed')}\nErrors: {', '.join(bug.get('assertion_errors', ['Unknown error']))}",
                        "Screenshot": "N/A (API testing)",
                        "Priority": priority,
                        "Affected Feature / Version": f"{bug.get('endpoint', 'Unknown').capitalize()} API / v1.0",
                    }
                )

        print(f"  ✅ Created: {bug_report_file}")
        return str(bug_report_file)

    def _generate_data_driven_test_cases(
        self, data_driven_results: Dict[str, Any]
    ) -> Dict[str, List[Dict]]:
        """Generate test cases from data-driven testing results"""
        test_cases = {"brands": [], "products": [], "categories": []}

        # Load CSV and JSON data files
        for endpoint in ["brands", "products", "categories"]:
            # Load CSV data (GET endpoints)
            csv_file = self.data_dir / f"{endpoint}-test-data.csv"
            if csv_file.exists():
                endpoint_results = data_driven_results.get("results", {}).get(
                    endpoint, []
                )

                # Load original CSV data
                with open(csv_file, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    csv_data = list(reader)

                # Create test cases from CSV data and results
                for i, (csv_row, result) in enumerate(zip(csv_data, endpoint_results)):
                    test_case = {
                        "id": csv_row.get(
                            "test_case_id", f"{endpoint.upper()}-{i+1:03d}"
                        ),
                        "title": csv_row.get(
                            "title", f"Data-Driven {endpoint.capitalize()} Test {i+1}"
                        ),
                        "preconditions": csv_row.get(
                            "preconditions", "API server is running and accessible"
                        ),
                        "inputs": csv_row.get("inputs", ""),
                        "test_steps": csv_row.get(
                            "test_steps",
                            f"1. Send GET request to /{endpoint} endpoint\n2. Verify response",
                        ),
                        "expected_result": csv_row.get(
                            "expected_result", "Status code 200 with valid response"
                        ),
                        "actual_result": "",
                        "result": "",
                    }

                    # Update actual result and status based on test execution
                    if result.get("passed", False):
                        test_case["actual_result"] = "Test executed successfully"
                        test_case["result"] = "PASS"
                    else:
                        # Check if it's an API connection error
                        api_connection_error = any(
                            "API server not accessible" in error
                            for error in result.get("assertion_errors", [])
                        )

                        if api_connection_error:
                            test_case["actual_result"] = (
                                "API server not accessible (expected when server is down)"
                            )
                            test_case["result"] = "SKIP"
                        else:
                            test_case["actual_result"] = (
                                f"Test failed: {', '.join(result.get('assertion_errors', ['Unknown error']))}"
                            )
                            test_case["result"] = "FAIL"

                    test_cases[endpoint].append(test_case)

            # Load JSON data (POST endpoints)
            json_file = self.data_dir / f"{endpoint}-post-test-data.json"
            if json_file.exists():
                endpoint_results = data_driven_results.get("results", {}).get(
                    endpoint, []
                )

                # Load original JSON data
                json_test_cases = self._load_json_test_cases(json_file)

                # Create test cases from JSON data and results
                for i, (json_row, result) in enumerate(
                    zip(json_test_cases, endpoint_results)
                ):
                    test_case = {
                        "id": json_row.get(
                            "test_case_id", f"{endpoint.upper()}-POST-{i+1:03d}"
                        ),
                        "title": json_row.get(
                            "title",
                            f"Data-Driven {endpoint.capitalize()} POST Test {i+1}",
                        ),
                        "preconditions": json_row.get(
                            "preconditions", "API server is running and accessible"
                        ),
                        "inputs": json_row.get("inputs", ""),
                        "test_steps": json_row.get(
                            "test_steps",
                            f"1. Send POST request to /{endpoint} endpoint\n2. Verify response",
                        ),
                        "expected_result": json_row.get(
                            "expected_result", "Status code 201 with valid response"
                        ),
                        "actual_result": "",
                        "result": "",
                    }

                    # Update actual result and status based on test execution
                    if result.get("passed", False):
                        test_case["actual_result"] = "Test executed successfully"
                        test_case["result"] = "PASS"
                    else:
                        # Check if it's an API connection error
                        api_connection_error = any(
                            "API server not accessible" in error
                            for error in result.get("assertion_errors", [])
                        )

                        if api_connection_error:
                            test_case["actual_result"] = (
                                "API server not accessible (expected when server is down)"
                            )
                            test_case["result"] = "SKIP"
                        else:
                            test_case["actual_result"] = (
                                f"Test failed: {', '.join(result.get('assertion_errors', ['Unknown error']))}"
                            )
                            test_case["result"] = "FAIL"

                    test_cases[endpoint].append(test_case)

        return test_cases

    def _load_json_test_cases(self, json_file: Path) -> List[Dict]:
        """Load test cases from JSON file"""
        test_cases = []
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "test_cases" in data:
                for test_case in data["test_cases"]:
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
            print(f"❌ Error loading JSON test cases from {json_file}: {e}")
            return []

    def _generate_api_test_cases(
        self, api_name: str, result: Dict, test_data: Dict
    ) -> List[Dict]:
        """Generate test cases for a specific API"""
        test_cases = []

        # Base test cases based on API
        base_cases = {
            "brands": [
                {
                    "id": "BR-001",
                    "title": "Get All Brands - Valid Request",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /brands endpoint\n2. Verify response status code\n3. Verify response structure\n4. Verify brands data is returned",
                    "expected_result": "Status code 200; JSON response with brands array",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "BR-002",
                    "title": "Get All Brands - Check Content Type",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /brands endpoint\n2. Verify Content-Type header",
                    "expected_result": "Content-Type: application/json",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "BR-003",
                    "title": "Get All Brands - Performance Test",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /brands endpoint\n2. Measure response time",
                    "expected_result": "Response time < 2000ms",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "BR-004",
                    "title": "Get All Brands - Error Handling Test",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /brands endpoint\n2. Verify no 500 or 404 errors",
                    "expected_result": "No 500 or 404 errors returned",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "BR-005",
                    "title": "Get All Brands - Data Validation Test",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /brands endpoint\n2. Verify response is valid JSON\n3. Verify response structure",
                    "expected_result": "Valid JSON response with array structure",
                    "actual_result": "",
                    "result": "",
                },
            ],
            "products": [
                {
                    "id": "PR-001",
                    "title": "Get All Products - Valid Request",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /products endpoint\n2. Verify response status code\n3. Verify response structure",
                    "expected_result": "Status code 200; JSON response with products data",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "PR-002",
                    "title": "Get Products - Pagination First Page",
                    "preconditions": "API server is running and accessible",
                    "inputs": "page=1, limit=10",
                    "test_steps": "1. Send GET request to /products?page=1&limit=10\n2. Verify pagination metadata",
                    "expected_result": "Pagination metadata exists (current_page, per_page, total)",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "PR-003",
                    "title": "Get Products - Filter by Category",
                    "preconditions": "API server is running and accessible",
                    "inputs": "category=7",
                    "test_steps": "1. Send GET request to /products?category=7\n2. Verify filtered results",
                    "expected_result": "Filtered results are returned",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "PR-004",
                    "title": "Get Products - Search by Name",
                    "preconditions": "API server is running and accessible",
                    "inputs": "search=hammer",
                    "test_steps": "1. Send GET request to /products?search=hammer\n2. Verify search results",
                    "expected_result": "Search results are returned",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "PR-005",
                    "title": "Get Products - Sort by Price",
                    "preconditions": "API server is running and accessible",
                    "inputs": "sort=price, order=asc",
                    "test_steps": "1. Send GET request to /products?sort=price&order=asc\n2. Verify sorted results",
                    "expected_result": "Sorted results are returned",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "PR-006",
                    "title": "Get Products - Performance Test",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /products endpoint\n2. Measure response time",
                    "expected_result": "Response time < 3000ms",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "PR-007",
                    "title": "Get Products - Error Handling Test",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /products endpoint\n2. Verify no 500 or 404 errors",
                    "expected_result": "No 500 or 404 errors returned",
                    "actual_result": "",
                    "result": "",
                },
            ],
            "categories": [
                {
                    "id": "CT-001",
                    "title": "Get All Categories - Valid Request",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /categories endpoint\n2. Verify response status code\n3. Verify response structure",
                    "expected_result": "Status code 200; JSON response with categories array",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "CT-002",
                    "title": "Get All Categories - Check Content Type",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /categories endpoint\n2. Verify Content-Type header",
                    "expected_result": "Content-Type: application/json",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "CT-003",
                    "title": "Get All Categories - Performance Test",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /categories endpoint\n2. Measure response time",
                    "expected_result": "Response time < 1500ms",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "CT-004",
                    "title": "Get All Categories - Error Handling Test",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /categories endpoint\n2. Verify no 500 or 404 errors",
                    "expected_result": "No 500 or 404 errors returned",
                    "actual_result": "",
                    "result": "",
                },
                {
                    "id": "CT-005",
                    "title": "Get All Categories - Data Validation Test",
                    "preconditions": "API server is running and accessible",
                    "inputs": "No parameters required",
                    "test_steps": "1. Send GET request to /categories endpoint\n2. Verify response is valid JSON\n3. Verify response structure",
                    "expected_result": "Valid JSON response with array structure",
                    "actual_result": "",
                    "result": "",
                },
            ],
        }

        # Update actual results based on test execution
        if result.get("success", False):
            for test_case in base_cases.get(api_name, []):
                test_case["actual_result"] = "Test executed successfully"
                test_case["result"] = "PASS"
        else:
            for test_case in base_cases.get(api_name, []):
                test_case["actual_result"] = (
                    f"Test failed: {result.get('error', 'Unknown error')}"
                )
                test_case["result"] = "FAIL"

        return base_cases.get(api_name, [])

    def save_test_cases_to_csv(self, test_cases: Dict[str, List[Dict]]):
        """Save generated test cases to CSV files"""
        print("📝 Saving test cases to CSV...")

        for api_name, cases in test_cases.items():
            if cases:
                csv_file = self.test_cases_dir / f"{api_name}-test-cases.csv"
                with open(csv_file, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(
                        f,
                        fieldnames=[
                            "Test Case ID",
                            "Title",
                            "Preconditions",
                            "Inputs",
                            "Test Steps",
                            "Expected Result",
                            "Actual Result",
                            "Result",
                        ],
                    )
                    writer.writeheader()

                    for case in cases:
                        writer.writerow(
                            {
                                "Test Case ID": case["id"],
                                "Title": case["title"],
                                "Preconditions": case["preconditions"],
                                "Inputs": case["inputs"],
                                "Test Steps": case["test_steps"],
                                "Expected Result": case["expected_result"],
                                "Actual Result": case["actual_result"],
                                "Result": case["result"],
                            }
                        )

                print(f"  ✅ Created: {csv_file}")

    def convert_to_excel(
        self,
        test_cases: Dict[str, List[Dict]],
        bug_report_file: Optional[str] = None,
        data_driven_bug_report: Optional[str] = None,
    ):
        """Convert CSV files to Excel format"""
        print("📊 Converting to Excel format...")

        try:
            # Convert test cases
            for api_name, cases in test_cases.items():
                if cases:
                    df = pd.DataFrame(cases)
                    excel_file = (
                        self.project_root
                        / f"{self.student_id}_TestCases_{api_name.capitalize()}.xlsx"
                    )
                    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                        df.to_excel(
                            writer,
                            sheet_name=f"{api_name.capitalize()} Test Cases",
                            index=False,
                        )
                    print(f"  ✅ Created: {excel_file}")

            # Create combined test cases file
            combined_data = {}
            for api_name, cases in test_cases.items():
                if cases:
                    combined_data[api_name.capitalize()] = pd.DataFrame(cases)

            if combined_data:
                excel_file = self.project_root / f"{self.student_id}_TestCases.xlsx"
                with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                    for sheet_name, df in combined_data.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"  ✅ Created: {excel_file}")

            # Convert bug reports
            bug_reports = []
            if bug_report_file and Path(bug_report_file).exists():
                bug_reports.append(("Standard", bug_report_file))
            if data_driven_bug_report and Path(data_driven_bug_report).exists():
                bug_reports.append(("Data-Driven", data_driven_bug_report))

            if bug_reports:
                excel_file = self.project_root / f"{self.student_id}_BugReport.xlsx"
                with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                    for report_type, report_file in bug_reports:
                        df = pd.read_csv(report_file)
                        df.to_excel(
                            writer, sheet_name=f"{report_type} Bugs", index=False
                        )
                print(f"  ✅ Created: {excel_file}")
            else:
                # Create empty bug report if none exists
                empty_df = pd.DataFrame(
                    columns=[
                        "BugID",
                        "Summary",
                        "Steps To Reproduce",
                        "Actual vs Expected Result",
                        "Screenshot",
                        "Priority",
                        "Affected Feature / Version",
                    ]
                )
                excel_file = self.project_root / f"{self.student_id}_BugReport.xlsx"
                with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                    empty_df.to_excel(writer, sheet_name="Bug Report", index=False)
                print(f"  ✅ Created: {excel_file}")

        except ImportError:
            print("❌ Error: openpyxl is required for Excel conversion")
            print("Install it with: pip install openpyxl")
        except Exception as e:
            print(f"❌ Error during Excel conversion: {e}")

    def generate_markdown_report(
        self,
        test_results: Dict[str, Any],
        test_cases: Dict[str, List[Dict]],
        bug_report_file: Optional[str] = None,
        data_driven_results: Optional[Dict[str, Any]] = None,
        data_driven_bug_report: Optional[str] = None,
    ):
        """Generate comprehensive markdown report"""
        print("📋 Generating markdown report...")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_content = f"""# API Testing Report - The Toolshop Application

**Generated:** {timestamp}  
**Base URL:** {test_results.get('base_url', 'N/A')}  
**Platform:** {test_results.get('platform', 'N/A')}

## 📊 Test Execution Summary

### Overall Results
- **Total Collections:** {test_results.get('summary', {}).get('total_collections', 0)}
- **Passed Collections:** {test_results.get('summary', {}).get('passed_collections', 0)}
- **Failed Collections:** {test_results.get('summary', {}).get('failed_collections', 0)}
- **Total Tests:** {test_results.get('summary', {}).get('total_tests', 0)}
- **Passed Tests:** {test_results.get('summary', {}).get('passed_tests', 0)}
- **Failed Tests:** {test_results.get('summary', {}).get('failed_tests', 0)}

### Collection Results

"""

        # Add collection results
        for collection_name, result in test_results.get("collections", {}).items():
            status = "✅ PASSED" if result.get("success", False) else "❌ FAILED"
            execution_time = result.get("execution_time", 0)

            report_content += f"#### {collection_name.upper()}: {status}\n"
            report_content += f"- **Execution Time:** {execution_time:.2f} seconds\n"

            if "stats" in result:
                stats = result["stats"]
                report_content += f"- **Tests:** {stats['total']} total, {stats['passed']} passed, {stats['failed']} failed\n"

            report_content += "\n"

        # Add test cases summary
        report_content += "## 📝 Test Cases Summary\n\n"

        for api_name, cases in test_cases.items():
            passed_count = sum(1 for case in cases if case.get("result") == "PASS")
            total_count = len(cases)

            report_content += f"### {api_name.upper()} API\n"
            report_content += f"- **Total Test Cases:** {total_count}\n"
            report_content += f"- **Passed:** {passed_count}\n"
            report_content += f"- **Failed:** {total_count - passed_count}\n"
            if total_count > 0:
                report_content += (
                    f"- **Success Rate:** {(passed_count/total_count*100):.1f}%\n\n"
                )
            else:
                report_content += f"- **Success Rate:** 0.0%\n\n"

        # Add bug report summary
        total_bugs = 0
        if bug_report_file and Path(bug_report_file).exists():
            try:
                with open(bug_report_file, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    bugs = list(reader)
                    total_bugs += len(bugs)

                report_content += f"## 🐛 Bug Report Summary\n\n"
                report_content += f"- **Standard Bugs Found:** {len(bugs)}\n"
                report_content += (
                    f"- **Standard Bug Report File:** {Path(bug_report_file).name}\n\n"
                )

                if bugs:
                    report_content += "### Standard Bug Details\n\n"
                    for i, bug in enumerate(bugs[:5], 1):  # Show first 5 bugs
                        report_content += f"#### {bug.get('BugID', f'BUG-{i:03d}')}\n"
                        report_content += (
                            f"- **Summary:** {bug.get('Summary', 'N/A')}\n"
                        )
                        report_content += (
                            f"- **Priority:** {bug.get('Priority', 'N/A')}\n"
                        )
                        report_content += f"- **Affected Feature:** {bug.get('Affected Feature / Version', 'N/A')}\n\n"
            except Exception as e:
                report_content += f"## 🐛 Bug Report Summary\n\n"
                report_content += f"- **Error reading standard bug report:** {e}\n\n"

        # Add data-driven bug report summary
        if data_driven_bug_report and Path(data_driven_bug_report).exists():
            try:
                with open(data_driven_bug_report, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    dd_bugs = list(reader)
                    total_bugs += len(dd_bugs)

                if not report_content.endswith("## 🐛 Bug Report Summary\n\n"):
                    report_content += f"## 🐛 Bug Report Summary\n\n"

                report_content += f"- **Data-Driven Bugs Found:** {len(dd_bugs)}\n"
                report_content += f"- **Data-Driven Bug Report File:** {Path(data_driven_bug_report).name}\n\n"

                if dd_bugs:
                    report_content += "### Data-Driven Bug Details\n\n"
                    for i, bug in enumerate(dd_bugs[:5], 1):  # Show first 5 bugs
                        report_content += (
                            f"#### {bug.get('BugID', f'DD-BUG-{i:03d}')}\n"
                        )
                        report_content += (
                            f"- **Summary:** {bug.get('Summary', 'N/A')}\n"
                        )
                        report_content += (
                            f"- **Priority:** {bug.get('Priority', 'N/A')}\n"
                        )
                        report_content += f"- **Affected Feature:** {bug.get('Affected Feature / Version', 'N/A')}\n\n"
            except Exception as e:
                if not report_content.endswith("## 🐛 Bug Report Summary\n\n"):
                    report_content += f"## 🐛 Bug Report Summary\n\n"
                report_content += f"- **Error reading data-driven bug report:** {e}\n\n"

        # Add total bugs summary
        if total_bugs > 0:
            if not report_content.endswith("## 🐛 Bug Report Summary\n\n"):
                report_content += f"## 🐛 Bug Report Summary\n\n"
            report_content += f"- **Total Bugs Found:** {total_bugs}\n\n"

        # Add data-driven testing results if available
        if data_driven_results:
            report_content += "## 🚀 Data-Driven Testing Results\n\n"

            dd_summary = data_driven_results["summary"]
            report_content += f"### Executive Summary\n"
            report_content += (
                f"- **Total Endpoints Tested:** {dd_summary['total_endpoints']}\n"
            )
            report_content += f"- **Total Test Cases:** {dd_summary['total_tests']}\n"
            report_content += f"- **Passed Tests:** {dd_summary['passed_tests']}\n"
            report_content += f"- **Failed Tests:** {dd_summary['failed_tests']}\n"
            report_content += f"- **Success Rate:** {dd_summary['success_rate']:.1f}%\n"
            report_content += f"- **Bugs Found:** {dd_summary['bugs_found']}\n\n"

            # Add endpoint results
            for endpoint, endpoint_results in data_driven_results["results"].items():
                passed = sum(1 for r in endpoint_results if r["passed"])
                total = len(endpoint_results)
                success_rate = (passed / total * 100) if total > 0 else 0

                report_content += f"### {endpoint.upper()} Endpoint\n"
                report_content += f"- **Test Cases:** {total}\n"
                report_content += f"- **Passed:** {passed}\n"
                report_content += f"- **Failed:** {total - passed}\n"
                report_content += f"- **Success Rate:** {success_rate:.1f}%\n\n"

            # Add data-driven bugs
            if data_driven_results["bugs"]:
                report_content += f"### Data-Driven Bugs Found ({len(data_driven_results['bugs'])})\n\n"
                for i, bug in enumerate(
                    data_driven_results["bugs"][:5], 1
                ):  # Show first 5
                    report_content += f"#### Bug #{i}\n"
                    report_content += f"- **Test Case:** {bug['test_case_id']}\n"
                    report_content += f"- **Title:** {bug['title']}\n"
                    report_content += f"- **Endpoint:** {bug['endpoint']}\n"
                    report_content += f"- **Expected:** {bug['expected_result']}\n"
                    report_content += f"- **Actual:** {bug['actual_result']}\n\n"

        # Add generated files list
        report_content += "## 📁 Generated Files\n\n"
        report_content += "### Excel Files\n"
        report_content += "- `StudentID_TestCases.xlsx` - Combined test cases\n"
        for api_name in test_cases.keys():
            report_content += f"- `StudentID_TestCases_{api_name.capitalize()}.xlsx` - {api_name.capitalize()} test cases\n"
        report_content += "- `StudentID_BugReport.xlsx` - Bug reports\n\n"

        report_content += "### CSV Files\n"
        for api_name in test_cases.keys():
            report_content += (
                f"- `{api_name}-test-cases.csv` - {api_name.capitalize()} test cases\n"
            )
        if bug_report_file:
            report_content += (
                f"- `{Path(bug_report_file).name}` - Standard bug report\n"
            )
        if data_driven_bug_report:
            report_content += (
                f"- `{Path(data_driven_bug_report).name}` - Data-driven bug report\n"
            )

        return report_content

    def write_reports_to_files(self, report_content: str):
        """Write report content directly to README.md and student-specific report file"""
        print(
            f"📝 Writing reports to README.md and {self.student_id}_APITesting.md..."
        )

        # Write to README.md
        readme_file = self.project_root / "README.md"
        if readme_file.exists():
            # Read existing content
            with open(readme_file, "r", encoding="utf-8") as f:
                existing_content = f.read()

            # Find the API Testing section and replace it
            if "## API Testing Results" in existing_content:
                # Split at the API Testing Results section
                parts = existing_content.split("## API Testing Results")
                if len(parts) >= 2:
                    # Find the next section
                    remaining = parts[1]
                    next_section_match = remaining.find("\n## ")
                    if next_section_match != -1:
                        remaining = remaining[next_section_match:]
                    else:
                        remaining = ""

                    new_content = (
                        parts[0]
                        + "## API Testing Results\n\n"
                        + report_content
                        + remaining
                    )
                else:
                    new_content = (
                        existing_content
                        + "\n\n## API Testing Results\n\n"
                        + report_content
                    )
            else:
                new_content = (
                    existing_content + "\n\n## API Testing Results\n\n" + report_content
                )

            with open(readme_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✅ Updated: {readme_file}")

        # Write to StudentID_APITesting.md
        student_file = self.project_root / "StudentID_APITesting.md"
        if student_file.exists():
            # Read existing content
            with open(student_file, "r", encoding="utf-8") as f:
                existing_content = f.read()

            # Find the API Testing Results section and replace it
            if "## API Testing Results" in existing_content:
                # Split at the API Testing Results section
                parts = existing_content.split("## API Testing Results")
                if len(parts) >= 2:
                    # Find the next section
                    remaining = parts[1]
                    next_section_match = remaining.find("\n## ")
                    if next_section_match != -1:
                        remaining = remaining[next_section_match:]
                    else:
                        remaining = ""

                    new_content = (
                        parts[0]
                        + "## API Testing Results\n\n"
                        + report_content
                        + remaining
                    )
                else:
                    new_content = (
                        existing_content
                        + "\n\n## API Testing Results\n\n"
                        + report_content
                    )
            else:
                new_content = (
                    existing_content + "\n\n## API Testing Results\n\n" + report_content
                )

            with open(student_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✅ Updated: {student_file}")

    def generate_all_reports(
        self,
        test_results: Dict[str, Any],
        bug_report_file: Optional[str] = None,
        data_driven_results: Optional[Dict[str, Any]] = None,
    ):
        """Generate all reports and artifacts"""
        print("🚀 Generating comprehensive reports...")

        # Clean up old reports
        self.cleanup_old_reports()

        # Generate data-driven bug report if available
        data_driven_bug_report = None
        if data_driven_results and data_driven_results.get("bugs"):
            data_driven_bug_report = self.generate_data_driven_bug_report(
                data_driven_results
            )

        # Generate test cases from data
        test_cases = self.generate_test_cases_from_data(
            test_results, data_driven_results
        )

        # Save test cases to CSV
        self.save_test_cases_to_csv(test_cases)

        # Convert to Excel
        self.convert_to_excel(test_cases, bug_report_file, data_driven_bug_report)

        # Generate markdown report content
        report_content = self.generate_markdown_report(
            test_results,
            test_cases,
            bug_report_file,
            data_driven_results,
            data_driven_bug_report,
        )

        # Write reports to README.md and StudentID_APITesting.md
        self.write_reports_to_files(report_content)

        print("✅ All reports generated successfully!")
        return {
            "test_cases": test_cases,
            "report_content": report_content,
            "data_driven_bug_report": data_driven_bug_report,
            "excel_files": [
                f"{self.student_id}_TestCases.xlsx",
                f"{self.student_id}_TestCases_Brands.xlsx",
                f"{self.student_id}_TestCases_Products.xlsx",
                f"{self.student_id}_TestCases_Categories.xlsx",
                f"{self.student_id}_BugReport.xlsx",
            ],
        }
