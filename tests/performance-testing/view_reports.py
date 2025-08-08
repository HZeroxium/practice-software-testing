#!/usr/bin/env python3
"""
Report Viewer for Performance Testing

This script helps view all generated report artifacts from performance testing.

Author: Performance Testing Automation
Date: 2024
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ReportViewer:
    """View and analyze performance testing reports"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.results_dir = self.base_dir / "results"
        self.data_dir = self.base_dir / "data"
        self.report_dir = self.base_dir / "report"

    def show_execution_summary(self):
        """Show the test execution summary"""
        logger.info("=" * 80)
        logger.info("PERFORMANCE TESTING EXECUTION SUMMARY")
        logger.info("=" * 80)

        summary_file = self.results_dir / "test_execution_summary.json"
        if not summary_file.exists():
            logger.error("Test execution summary not found!")
            return

        try:
            with open(summary_file, "r") as f:
                summary = json.load(f)

            logger.info(f"Execution Time: {summary.get('execution_time', 'N/A')}")
            logger.info(f"Total Tests: {summary.get('total_tests', 0)}")
            logger.info(f"Successful Tests: {summary.get('successful_tests', 0)}")
            logger.info(f"Failed Tests: {summary.get('failed_tests', 0)}")

            logger.info("\n" + "=" * 60)
            logger.info("DETAILED TEST RESULTS")
            logger.info("=" * 60)

            for result in summary.get("test_results", []):
                test_name = result.get("test_name", "Unknown")
                test_type = result.get("test_type", "Unknown")
                success = result.get("success", False)
                total_requests = result.get("total_requests", 0)
                successful_requests = result.get("successful_requests", 0)
                failed_requests = result.get("failed_requests", 0)
                avg_response_time = result.get("average_response_time", 0)
                throughput = result.get("throughput", 0)
                error_rate = result.get("error_rate", 0)

                logger.info(f"\n{test_name} ({test_type.upper()}):")
                logger.info(f"  Status: {'PASSED' if success else 'FAILED'}")
                logger.info(f"  Total Requests: {total_requests}")
                logger.info(f"  Successful: {successful_requests}")
                logger.info(f"  Failed: {failed_requests}")
                logger.info(f"  Average Response Time: {avg_response_time:.2f} ms")
                logger.info(f"  Throughput: {throughput:.2f} req/s")
                logger.info(f"  Error Rate: {error_rate:.2f}%")

        except Exception as e:
            logger.error(f"Error reading execution summary: {e}")

    def show_html_reports(self):
        """Show available HTML reports"""
        logger.info("\n" + "=" * 80)
        logger.info("JMETER HTML REPORTS")
        logger.info("=" * 80)

        html_dirs = list(self.results_dir.glob("*_report"))
        if not html_dirs:
            logger.warning("No HTML report directories found!")
            return

        for html_dir in html_dirs:
            index_file = html_dir / "index.html"
            if index_file.exists():
                logger.info(f"📊 {html_dir.name}:")
                logger.info(f"   📁 Directory: {html_dir}")
                logger.info(f"   🌐 Open: {index_file}")
                logger.info(
                    f"   📅 Created: {datetime.fromtimestamp(html_dir.stat().st_mtime)}"
                )
            else:
                logger.warning(f"⚠️  {html_dir.name}: index.html not found")

    def show_csv_reports(self):
        """Show CSV report files"""
        logger.info("\n" + "=" * 80)
        logger.info("CSV REPORT FILES")
        logger.info("=" * 80)

        # Test Cases
        test_cases_file = self.data_dir / "StudentID_TestCases.csv"
        if test_cases_file.exists():
            logger.info(f"📋 Test Cases: {test_cases_file}")
            logger.info(
                f"   📅 Modified: {datetime.fromtimestamp(test_cases_file.stat().st_mtime)}"
            )

        # Bug Report
        bug_report_file = self.data_dir / "StudentID_BugReport.csv"
        if bug_report_file.exists():
            logger.info(f"🐛 Bug Report: {bug_report_file}")
            logger.info(
                f"   📅 Modified: {datetime.fromtimestamp(bug_report_file.stat().st_mtime)}"
            )

        # Main Report
        main_report_file = self.report_dir / "StudentID_PerformanceTesting.md"
        if main_report_file.exists():
            logger.info(f"📄 Main Report: {main_report_file}")
            logger.info(
                f"   📅 Modified: {datetime.fromtimestamp(main_report_file.stat().st_mtime)}"
            )

    def show_jtl_files(self):
        """Show JTL result files"""
        logger.info("\n" + "=" * 80)
        logger.info("JMETER JTL RESULT FILES")
        logger.info("=" * 80)

        jtl_files = list(self.results_dir.glob("*.jtl"))
        if not jtl_files:
            logger.warning("No JTL files found!")
            return

        for jtl_file in sorted(
            jtl_files, key=lambda x: x.stat().st_mtime, reverse=True
        ):
            logger.info(f"📊 {jtl_file.name}:")
            logger.info(f"   📁 File: {jtl_file}")
            logger.info(
                f"   📅 Created: {datetime.fromtimestamp(jtl_file.stat().st_mtime)}"
            )
            logger.info(f"   📏 Size: {jtl_file.stat().st_size:,} bytes")

    def show_log_files(self):
        """Show log files"""
        logger.info("\n" + "=" * 80)
        logger.info("LOG FILES")
        logger.info("=" * 80)

        log_files = list(self.results_dir.glob("*.log"))
        if not log_files:
            logger.warning("No log files found!")
            return

        for log_file in sorted(
            log_files, key=lambda x: x.stat().st_mtime, reverse=True
        ):
            logger.info(f"📝 {log_file.name}:")
            logger.info(f"   📁 File: {log_file}")
            logger.info(
                f"   📅 Created: {datetime.fromtimestamp(log_file.stat().st_mtime)}"
            )
            logger.info(f"   📏 Size: {log_file.stat().st_size:,} bytes")

    def show_quick_guide(self):
        """Show quick guide for viewing reports"""
        logger.info("\n" + "=" * 80)
        logger.info("QUICK GUIDE - HOW TO VIEW REPORTS")
        logger.info("=" * 80)

        logger.info("🌐 HTML Reports (JMeter Dashboard):")
        logger.info("   1. Navigate to results directory")
        logger.info("   2. Open any *_report folder")
        logger.info("   3. Open index.html in your browser")
        logger.info("   4. View graphs, tables, and detailed results")

        logger.info("\n📊 CSV Reports:")
        logger.info("   1. Open StudentID_TestCases.csv in Excel/LibreOffice")
        logger.info("   2. Open StudentID_BugReport.csv for bug details")
        logger.info("   3. Use filters to analyze specific test results")

        logger.info("\n📄 Main Report:")
        logger.info("   1. Open StudentID_PerformanceTesting.md")
        logger.info("   2. View comprehensive analysis and findings")
        logger.info("   3. Check self-assessment and recommendations")

        logger.info("\n📝 JTL Files (Raw JMeter Data):")
        logger.info("   1. Use JMeter GUI to load .jtl files")
        logger.info("   2. View detailed request/response data")
        logger.info("   3. Analyze individual transaction details")

    def show_all_reports(self):
        """Show all available reports"""
        self.show_execution_summary()
        self.show_html_reports()
        self.show_csv_reports()
        self.show_jtl_files()
        self.show_log_files()
        self.show_quick_guide()


def main():
    """Main execution function"""
    try:
        viewer = ReportViewer()
        viewer.show_all_reports()

        logger.info("\n" + "=" * 80)
        logger.info("REPORT VIEWING COMPLETED")
        logger.info("=" * 80)
        logger.info(
            "💡 Tip: Use the file paths above to open reports in your preferred applications"
        )

    except Exception as e:
        logger.error(f"Error viewing reports: {e}")


if __name__ == "__main__":
    main()
