#!/usr/bin/env python3
"""
Spike Test Runner

This script runs only spike tests for quick validation and debugging.
It allows testing spike test configuration without running the full test suite.

Author: Performance Testing Automation
Date: 2024
"""

import logging
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from jmeter_runner import JMeterRunner
from test_duration_optimizer import TestDurationOptimizer

logger = logging.getLogger(__name__)


class SpikeTestRunner:
    """Run only spike tests for quick validation"""

    def __init__(self):
        self.jmeter_runner = JMeterRunner()
        self.optimizer = TestDurationOptimizer()
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)

    def run_spike_tests(self, profile_name: str = "medium") -> List[Dict[str, Any]]:
        """Run only spike tests with specified profile"""
        try:
            logger.info(f"Running spike tests with {profile_name} profile...")

            # Apply duration profile
            if not self.optimizer.apply_duration_profile(profile_name):
                logger.error(f"Failed to apply {profile_name} profile")
                return []

            # Generate JMeter templates
            from jmeter_template_generator import JMeterTemplateGenerator

            generator = JMeterTemplateGenerator()
            generator.generate_all_templates()

            # Get spike test cases from config
            config = self.optimizer.config
            product_listing = config.get("test_scenarios", {}).get(
                "product_listing", {}
            )
            spike_test_cases = product_listing.get("spike_test_cases", [])

            test_results = []

            # Run each spike test
            for test_case in spike_test_cases:
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

            logger.info(f"Completed {len(test_results)} spike test executions")
            return test_results

        except Exception as e:
            logger.error(f"Failed to run spike tests: {e}")
            return []

    def print_spike_test_config(self):
        """Print current spike test configuration"""
        config = self.optimizer.config
        product_listing = config.get("test_scenarios", {}).get("product_listing", {})
        spike_test_cases = product_listing.get("spike_test_cases", [])

        print("\n🔍 Current Spike Test Configuration:")
        print("=" * 60)

        for test_case in spike_test_cases:
            if test_case.get("enabled", False):
                print(f"\n📋 {test_case['name']}:")
                print(f"   Description: {test_case['description']}")

                baseline = test_case.get("baseline", {})
                spike = test_case.get("spike", {})
                recovery = test_case.get("recovery", {})

                print(
                    f"   Baseline: {baseline.get('threads', 0)} threads, {baseline.get('duration', 0)}s"
                )
                print(
                    f"   Spike: {spike.get('threads', 0)} threads, {spike.get('duration', 0)}s"
                )
                print(
                    f"   Recovery: {recovery.get('threads', 0)} threads, {recovery.get('duration', 0)}s"
                )
                print(
                    f"   Total Duration: {baseline.get('duration', 0) + spike.get('duration', 0) + recovery.get('duration', 0)}s"
                )

    def print_test_results(self, results: List[Dict[str, Any]]):
        """Print spike test results"""
        print("\n📊 Spike Test Results:")
        print("=" * 60)

        for result in results:
            test_name = result.get("test_name", "Unknown")
            status = result.get("status", "UNKNOWN")
            avg_response_time = result.get("avg_response_time", 0)
            throughput = result.get("throughput", 0)
            error_rate = result.get("error_rate", 0)
            total_requests = result.get("total_requests", 0)

            print(f"\n🔹 {test_name}:")
            print(f"   Status: {status}")
            print(f"   Total Requests: {total_requests}")
            print(f"   Avg Response Time: {avg_response_time:.2f}ms")
            print(f"   Throughput: {throughput:.2f} req/sec")
            print(f"   Error Rate: {error_rate:.2f}%")

            if result.get("error_message"):
                print(f"   Error: {result['error_message']}")


def main():
    """Main function for spike test runner"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    runner = SpikeTestRunner()

    print("🎯 Spike Test Runner")
    print("=" * 60)

    # Show current configuration
    runner.print_spike_test_config()

    # Ask user for profile
    print("\n📋 Available Profiles:")
    print("1. quick (15 seconds)")
    print("2. short (5 minutes)")
    print("3. medium (15 minutes)")
    print("4. long (30 minutes)")
    print("5. extended (60 minutes)")

    choice = input("\nSelect profile (1-5) or press Enter for medium: ").strip()

    profile_map = {
        "1": "quick",
        "2": "short",
        "3": "medium",
        "4": "long",
        "5": "extended",
    }

    profile_name = profile_map.get(choice, "medium")
    print(f"\n🚀 Running spike tests with {profile_name} profile...")

    # Run spike tests
    start_time = time.time()
    results = runner.run_spike_tests(profile_name)
    end_time = time.time()
    actual_duration = end_time - start_time

    # Print results
    runner.print_test_results(results)

    print(
        f"\n⏱️  Actual execution time: ~{actual_duration:.1f} seconds ({actual_duration/60:.1f} minutes)"
    )
    print(f"✅ Spike tests completed!")


if __name__ == "__main__":
    main()
