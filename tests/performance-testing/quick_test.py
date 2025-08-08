#!/usr/bin/env python3
"""
Quick Test Script for Performance Testing

This script sets up a quick test configuration and runs the complete
performance testing workflow for the Product Listing scenario.

Author: Performance Testing Automation
Date: 2024
"""

import json
import logging
import sys
import time
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from run_performance_tests import PerformanceTestingOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("quick_test.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def setup_test_config(profile_name: str = "short"):
    """Set up a test configuration using duration optimizer"""
    from test_duration_optimizer import TestDurationOptimizer

    config_file = Path("config/test_config.json")

    # Ensure config directory exists
    config_file.parent.mkdir(exist_ok=True)

    # Use duration optimizer to apply specified profile
    optimizer = TestDurationOptimizer(str(config_file))
    success = optimizer.apply_duration_profile(profile_name)

    if success:
        logger.info(
            f"{profile_name.title()} test configuration saved to: {config_file}"
        )
        return config_file, optimizer
    else:
        logger.error(f"Failed to create {profile_name} test configuration")
        return None, None


def main():
    """Main function to run test with specified profile"""
    try:
        # Default profile is "short" but can be changed
        profile_name = "medium"  # Change this to test different profiles

        # Ask user what type of test to run
        print("🎯 Quick Test Runner")
        print("=" * 60)
        print("1. Run all tests (load + stress + spike)")
        print("2. Run only spike tests (for debugging)")
        print("3. Run only load tests")
        print("4. Run only stress tests")

        choice = input(
            "\nSelect test type (1-4) or press Enter for all tests: "
        ).strip()

        if choice == "2":
            # Run only spike tests
            from spike_test_runner import SpikeTestRunner

            runner = SpikeTestRunner()

            print(f"\n🚀 Running Spike Tests with {profile_name.title()} Profile")
            print("=" * 60)

            # Show current configuration
            runner.print_spike_test_config()

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

        else:
            # Run all tests (original logic)
            print(
                f"Starting {profile_name.title()} Performance Test for Product Listing Scenario"
            )
            print("=" * 60)

            # Set up test configuration
            logger.info(f"Setting up {profile_name} test configuration...")
            config_file, optimizer = setup_test_config(profile_name)

            if not config_file:
                print(f"\n❌ Failed to set up {profile_name} test configuration!")
                sys.exit(1)

            # Get execution time estimate
            estimate = optimizer.estimate_execution_time()
            total_minutes = estimate.get("total_time_minutes", 0)

            # Initialize orchestrator
            logger.info("Initializing performance testing orchestrator...")
            orchestrator = PerformanceTestingOrchestrator()

            # Run complete workflow with real-time counter
            logger.info("Running complete performance testing workflow...")
            start_time = time.time()
            success = orchestrator.run_complete_workflow()
            end_time = time.time()
            actual_duration = end_time - start_time

            if success:
                print(f"\n✅ {profile_name.title()} test completed successfully!")
                print("📊 Generated artifacts:")
                print(
                    f"   - Test Cases: {orchestrator.data_dir}/StudentID_TestCases.xlsx"
                )
                print(
                    f"   - Bug Report: {orchestrator.data_dir}/StudentID_BugReport.xlsx"
                )
                print(
                    f"   - Main Report: {orchestrator.report_dir}/StudentID_PerformanceTesting.md"
                )
                print(f"   - Results: {orchestrator.results_dir}/")
                print(f"\n⏱️  Estimated execution time: ~{total_minutes:.1f} minutes")
                print(
                    f"⏱️  Actual execution time: ~{actual_duration:.1f} seconds ({actual_duration/60:.1f} minutes)"
                )
                print("🎯 All 6 test cases executed (2 load + 2 stress + 2 spike)")
            else:
                print(f"\n❌ {profile_name.title()} test failed!")
                sys.exit(1)

    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
