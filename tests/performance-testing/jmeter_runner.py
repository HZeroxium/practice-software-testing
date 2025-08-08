#!/usr/bin/env python3
"""
JMeter Test Runner for Performance Testing Automation

This script automates the execution of JMeter test plans and captures results
for the Product Listing performance testing scenario.

Author: Performance Testing Automation
Date: 2024
"""

import os
import sys
import subprocess
import time
import json
import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("jmeter_execution.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Data class to store test execution results"""

    test_name: str
    test_type: str  # load, stress, spike
    start_time: datetime
    end_time: datetime
    duration: float
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    min_response_time: float
    max_response_time: float
    throughput: float
    error_rate: float
    jtl_file: str
    log_file: str
    status: str  # PASS, FAIL
    error_message: Optional[str] = None


class JMeterRunner:
    """Main class for executing JMeter test plans"""

    def __init__(
        self,
        scripts_dir: str = "scripts",
        results_dir: str = "results",
        config_file: str = "config/test_config.json",
    ):
        self.scripts_dir = Path(scripts_dir)
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)

        # Load configuration
        self.config_file = Path(config_file)
        self.config = self._load_config()

        # JMeter configuration
        self.jmeter_home = self._find_jmeter_home()
        self.jmeter_bin = (
            self.jmeter_home / "bin" / "jmeter.bat"
            if os.name == "nt"
            else self.jmeter_home / "bin" / "jmeter"
        )

        self.results: List[TestResult] = []

    def _find_jmeter_home(self) -> Path:
        """Find JMeter installation directory"""
        # Common JMeter installation paths
        possible_paths = [
            Path("C:/apache-jmeter-5.6.3"),
            Path("C:/Program Files/Apache Software Foundation/Apache JMeter 5.6.3"),
            Path("C:/jmeter"),
            Path.home() / "apache-jmeter-5.6.3",
            Path("/opt/apache-jmeter-5.6.3"),
            Path("/usr/local/apache-jmeter-5.6.3"),
            # My JMeter installation path: C:\Users\ADMIN\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin
            Path("C:/Users/ADMIN/Downloads/apache-jmeter-5.6.3/apache-jmeter-5.6.3"),
        ]

        # Check environment variable first
        jmeter_home_env = os.environ.get("JMETER_HOME")
        if jmeter_home_env:
            jmeter_path = Path(jmeter_home_env)
            if jmeter_path.exists():
                logger.info(f"Found JMeter at: {jmeter_path}")
                return jmeter_path

        # Check possible paths
        for path in possible_paths:
            if path.exists():
                logger.info(f"Found JMeter at: {path}")
                return path

        # If not found, return None and let the caller handle it
        logger.warning("JMeter installation not found in common locations")
        return None

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_file}")
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return {}

    def _validate_environment(self) -> bool:
        """Validate that JMeter is available and working"""
        if not self.jmeter_home:
            logger.error("JMeter installation not found")
            return False

        if not self.jmeter_bin.exists():
            logger.error(f"JMeter binary not found at: {self.jmeter_bin}")
            return False

        # Test JMeter installation
        try:
            result = subprocess.run(
                [str(self.jmeter_bin), "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                logger.info(f"JMeter version: {result.stdout.strip()}")
                return True
            else:
                logger.error(f"JMeter test failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error testing JMeter installation: {e}")
            return False

    def run_test(
        self,
        test_name: str,
        jmx_file: str,
        expected_response_time: float = 2000,
        expected_throughput: float = 25,
        expected_error_rate: float = 1.0,
    ) -> Dict[str, Any]:
        """Run a single JMeter test and return results"""
        try:
            logger.info(f"Running test: {test_name}")

            # Validate environment
            if not self._validate_environment():
                return {
                    "test_name": test_name,
                    "status": "FAIL",
                    "error_message": "JMeter environment validation failed",
                    "avg_response_time": 0,
                    "throughput": 0,
                    "error_rate": 100,
                    "total_requests": 0,
                    "successful_requests": 0,
                    "failed_requests": 0,
                }

            # Check if JMX file exists
            jmx_path = self.scripts_dir / jmx_file
            if not jmx_path.exists():
                return {
                    "test_name": test_name,
                    "status": "FAIL",
                    "error_message": f"JMX file not found: {jmx_path}",
                    "avg_response_time": 0,
                    "throughput": 0,
                    "error_rate": 100,
                    "total_requests": 0,
                    "successful_requests": 0,
                    "failed_requests": 0,
                }

            # Generate output file names
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            jtl_file = self.results_dir / f"{test_name}_{timestamp}.jtl"
            log_file = self.results_dir / f"{test_name}_{timestamp}.log"
            html_report_dir = self.results_dir / f"{test_name}_{timestamp}_report"

            # Build JMeter command
            cmd = [
                str(self.jmeter_bin),
                "-n",  # Non-GUI mode
                "-t",
                str(jmx_path),  # Test plan file
                "-l",
                str(jtl_file),  # Results file
                "-e",  # Generate HTML report
                "-o",
                str(html_report_dir),  # HTML report directory
                "-j",
                str(log_file),  # Log file
            ]

            logger.info(f"Executing JMeter command: {' '.join(cmd)}")

            # Execute JMeter test
            start_time = datetime.now()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Parse results
            if result.returncode == 0:
                logger.info(f"Test {test_name} completed successfully")
                test_result = self._parse_jtl_results(
                    jtl_file,
                    test_name,
                    start_time,
                    end_time,
                    duration,
                    True,
                    None,
                    log_file,
                )

                # Determine status based on expected values
                status = "PASS"
                if (
                    test_result.average_response_time > expected_response_time
                    or test_result.throughput < expected_throughput
                    or test_result.error_rate > expected_error_rate
                ):
                    status = "FAIL"

                return {
                    "test_name": test_name,
                    "status": status,
                    "avg_response_time": test_result.average_response_time,
                    "throughput": test_result.throughput,
                    "error_rate": test_result.error_rate,
                    "total_requests": test_result.total_requests,
                    "successful_requests": test_result.successful_requests,
                    "failed_requests": test_result.failed_requests,
                    "min_response_time": test_result.min_response_time,
                    "max_response_time": test_result.max_response_time,
                    "duration": duration,
                    "jtl_file": str(jtl_file),
                    "log_file": str(log_file),
                    "html_report_dir": str(html_report_dir),
                }
            else:
                logger.error(
                    f"Test {test_name} failed with return code: {result.returncode}"
                )
                logger.error(f"Error output: {result.stderr}")
                return {
                    "test_name": test_name,
                    "status": "FAIL",
                    "error_message": f"JMeter execution failed: {result.stderr}",
                    "avg_response_time": 0,
                    "throughput": 0,
                    "error_rate": 100,
                    "total_requests": 0,
                    "successful_requests": 0,
                    "failed_requests": 0,
                }

        except subprocess.TimeoutExpired:
            logger.error(f"Test {test_name} timed out")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "error_message": "Test execution timed out",
                "avg_response_time": 0,
                "throughput": 0,
                "error_rate": 100,
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
            }
        except Exception as e:
            logger.error(f"Error running test {test_name}: {e}")
            return {
                "test_name": test_name,
                "status": "FAIL",
                "error_message": str(e),
                "avg_response_time": 0,
                "throughput": 0,
                "error_rate": 100,
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
            }

    def _parse_jtl_results(
        self,
        jtl_file: Path,
        test_name: str,
        start_time: datetime,
        end_time: datetime,
        duration: float,
        success: bool,
        error_message: Optional[str],
        log_file: Path,
    ) -> TestResult:
        """Parse JMeter JTL results file"""
        try:
            if not jtl_file.exists():
                logger.warning(f"JTL file not found: {jtl_file}")
                return TestResult(
                    test_name=test_name,
                    test_type="unknown",
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    total_requests=0,
                    successful_requests=0,
                    failed_requests=0,
                    average_response_time=0,
                    min_response_time=0,
                    max_response_time=0,
                    throughput=0,
                    error_rate=100,
                    jtl_file=str(jtl_file),
                    log_file=str(log_file),
                    status="FAIL",
                    error_message="JTL file not found",
                )

            # Parse JTL file
            response_times = []
            total_requests = 0
            successful_requests = 0
            failed_requests = 0

            with open(jtl_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_requests += 1
                    response_time = int(row.get("elapsed", 0))
                    response_times.append(response_time)

                    if row.get("success", "false").lower() == "true":
                        successful_requests += 1
                    else:
                        failed_requests += 1

            # Calculate metrics
            if response_times:
                average_response_time = sum(response_times) / len(response_times)
                min_response_time = min(response_times)
                max_response_time = max(response_times)
            else:
                average_response_time = 0
                min_response_time = 0
                max_response_time = 0

            throughput = successful_requests / duration if duration > 0 else 0
            error_rate = (
                (failed_requests / total_requests * 100) if total_requests > 0 else 100
            )

            # Determine test type from test name
            test_type = "unknown"
            if "load" in test_name.lower():
                test_type = "load"
            elif "stress" in test_name.lower():
                test_type = "stress"
            elif "spike" in test_name.lower():
                test_type = "spike"

            return TestResult(
                test_name=test_name,
                test_type=test_type,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                total_requests=total_requests,
                successful_requests=successful_requests,
                failed_requests=failed_requests,
                average_response_time=average_response_time,
                min_response_time=min_response_time,
                max_response_time=max_response_time,
                throughput=throughput,
                error_rate=error_rate,
                jtl_file=str(jtl_file),
                log_file=str(log_file),
                status="PASS" if success else "FAIL",
                error_message=error_message,
            )

        except Exception as e:
            logger.error(f"Error parsing JTL results: {e}")
            return TestResult(
                test_name=test_name,
                test_type="unknown",
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                average_response_time=0,
                min_response_time=0,
                max_response_time=0,
                throughput=0,
                error_rate=100,
                jtl_file=str(jtl_file),
                log_file=str(log_file),
                status="FAIL",
                error_message=f"Error parsing results: {e}",
            )

    def get_test_results(self) -> List[TestResult]:
        """Get all test results"""
        return self.results


def main():
    """Main function for testing JMeter runner"""
    try:
        runner = JMeterRunner()

        # Test environment validation
        if runner._validate_environment():
            print("✅ JMeter environment validated successfully")
        else:
            print("❌ JMeter environment validation failed")
            return

        # Test a single JMeter script if available
        test_scripts = list(runner.scripts_dir.glob("*.jmx"))
        if test_scripts:
            test_script = test_scripts[0]
            print(f"Testing with script: {test_script.name}")

            result = runner.run_test(
                test_name="test_run",
                jmx_file=test_script.name,
                expected_response_time=5000,
                expected_throughput=10,
                expected_error_rate=5.0,
            )

            print(f"Test result: {result}")
        else:
            print("No JMeter scripts found for testing")

    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()
