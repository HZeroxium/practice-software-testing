#!/usr/bin/env python3
"""
Test Duration Optimizer

This module provides intelligent test duration optimization based on desired total execution time.
It automatically adjusts test parameters to achieve the target duration while maintaining test quality.

Author: Performance Testing Automation
Date: 2024
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TestDurationProfile:
    """Test duration profile for different execution modes"""

    name: str
    description: str
    total_duration_minutes: int
    load_test_duration: int
    stress_test_duration: int
    spike_test_duration: int
    threads_multiplier: float
    loops_multiplier: float


class TestDurationOptimizer:
    """Optimize test duration based on desired total execution time"""

    def __init__(self, config_file: str = "config/test_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()

        # Predefined duration profiles
        self.duration_profiles = {
            "quick": TestDurationProfile(
                name="Quick Test",
                description="Fast validation test (~15 seconds)",
                total_duration_minutes=0.25,
                load_test_duration=3,
                stress_test_duration=3,
                spike_test_duration=3,
                threads_multiplier=0.1,
                loops_multiplier=0.1,
            ),
            "short": TestDurationProfile(
                name="Short Test",
                description="Brief performance test (~5 minutes)",
                total_duration_minutes=5,
                load_test_duration=60,
                stress_test_duration=60,
                spike_test_duration=60,
                threads_multiplier=0.3,
                loops_multiplier=0.3,
            ),
            "medium": TestDurationProfile(
                name="Medium Test",
                description="Standard performance test (~15 minutes)",
                total_duration_minutes=15,
                load_test_duration=180,
                stress_test_duration=180,
                spike_test_duration=180,
                threads_multiplier=0.6,
                loops_multiplier=0.6,
            ),
            "long": TestDurationProfile(
                name="Long Test",
                description="Comprehensive performance test (~30 minutes)",
                total_duration_minutes=30,
                load_test_duration=360,
                stress_test_duration=360,
                spike_test_duration=360,
                threads_multiplier=1.0,
                loops_multiplier=1.0,
            ),
            "extended": TestDurationProfile(
                name="Extended Test",
                description="Extended performance test (~60 minutes)",
                total_duration_minutes=60,
                load_test_duration=720,
                stress_test_duration=720,
                spike_test_duration=720,
                threads_multiplier=1.5,
                loops_multiplier=1.5,
            ),
            "custom": TestDurationProfile(
                name="Custom Test",
                description="Custom duration test",
                total_duration_minutes=0,
                load_test_duration=0,
                stress_test_duration=0,
                spike_test_duration=0,
                threads_multiplier=1.0,
                loops_multiplier=1.0,
            ),
        }

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}

    def _save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False

    def get_available_profiles(self) -> List[str]:
        """Get list of available duration profiles"""
        return list(self.duration_profiles.keys())

    def apply_duration_profile(self, profile_name: str) -> bool:
        """Apply a predefined duration profile"""
        if profile_name not in self.duration_profiles:
            logger.error(f"Unknown profile: {profile_name}")
            return False

        profile = self.duration_profiles[profile_name]
        logger.info(f"Applying {profile.name} profile: {profile.description}")

        # Get current product listing configuration
        product_listing = self.config.get("test_scenarios", {}).get(
            "product_listing", {}
        )
        if not product_listing:
            logger.error("Product listing configuration not found")
            return False

        # Apply profile to load test cases
        for test_case in product_listing.get("load_test_cases", []):
            test_case["duration"] = profile.load_test_duration
            test_case["threads"] = max(
                1, int(test_case.get("threads", 10) * profile.threads_multiplier)
            )
            test_case["loops"] = max(
                1, int(test_case.get("loops", 1) * profile.loops_multiplier)
            )

        # Apply profile to stress test cases
        for test_case in product_listing.get("stress_test_cases", []):
            test_case["duration"] = profile.stress_test_duration
            test_case["threads"] = max(
                1, int(test_case.get("threads", 20) * profile.threads_multiplier)
            )
            test_case["loops"] = max(
                1, int(test_case.get("loops", 1) * profile.loops_multiplier)
            )

        # Apply profile to spike test cases
        for test_case in product_listing.get("spike_test_cases", []):
            test_case["duration"] = profile.spike_test_duration

            # Update baseline configuration
            test_case["baseline"]["threads"] = max(
                1,
                int(
                    test_case["baseline"].get("threads", 5) * profile.threads_multiplier
                ),
            )
            test_case["baseline"]["duration"] = int(
                profile.spike_test_duration * 0.3
            )  # 30% of total duration
            test_case["baseline"]["ramp_up"] = max(
                1, int(test_case["baseline"]["duration"] * 0.1)
            )

            # Update spike configuration
            test_case["spike"]["threads"] = max(
                1,
                int(test_case["spike"].get("threads", 20) * profile.threads_multiplier),
            )
            test_case["spike"]["duration"] = int(
                profile.spike_test_duration * 0.4
            )  # 40% of total duration
            test_case["spike"]["ramp_up"] = max(
                1, int(test_case["spike"]["duration"] * 0.1)
            )

            # Update recovery configuration
            test_case["recovery"]["threads"] = max(
                1,
                int(
                    test_case["recovery"].get("threads", 5) * profile.threads_multiplier
                ),
            )
            test_case["recovery"]["duration"] = int(
                profile.spike_test_duration * 0.3
            )  # 30% of total duration
            test_case["recovery"]["ramp_up"] = max(
                1, int(test_case["recovery"]["duration"] * 0.1)
            )

        # Save updated configuration
        return self._save_config(self.config)

    def optimize_for_duration(self, target_minutes: int) -> bool:
        """Optimize test configuration for a specific target duration"""
        logger.info(f"Optimizing test configuration for {target_minutes} minutes")

        # Calculate optimal parameters based on target duration
        total_test_cases = 6  # 2 load + 2 stress + 2 spike
        time_per_test = target_minutes * 60 / total_test_cases  # seconds per test

        # Get current product listing configuration
        product_listing = self.config.get("test_scenarios", {}).get(
            "product_listing", {}
        )
        if not product_listing:
            logger.error("Product listing configuration not found")
            return False

        # Calculate optimal threads and loops based on duration
        base_threads = max(1, int(target_minutes / 5))  # More threads for longer tests
        base_loops = max(1, int(target_minutes / 10))  # More loops for longer tests

        # Apply optimization to load test cases
        for test_case in product_listing.get("load_test_cases", []):
            test_case["duration"] = int(time_per_test * 0.8)  # 80% of time per test
            test_case["threads"] = max(1, base_threads)
            test_case["loops"] = max(1, base_loops)
            test_case["ramp_up"] = max(
                1, int(test_case["duration"] * 0.1)
            )  # 10% ramp-up

        # Apply optimization to stress test cases
        for test_case in product_listing.get("stress_test_cases", []):
            test_case["duration"] = int(
                time_per_test * 1.2
            )  # 120% of time per test (more intensive)
            test_case["threads"] = max(
                1, int(base_threads * 1.5)
            )  # More threads for stress
            test_case["loops"] = max(1, int(base_loops * 1.2))
            test_case["ramp_up"] = max(
                1, int(test_case["duration"] * 0.15)
            )  # 15% ramp-up

        # Apply optimization to spike test cases
        for test_case in product_listing.get("spike_test_cases", []):
            test_case["duration"] = int(
                time_per_test * 0.6
            )  # 60% of time per test (shorter phases)
            test_case["baseline"]["threads"] = max(1, int(base_threads * 0.5))
            test_case["spike"]["threads"] = max(
                1, int(base_threads * 2.0)
            )  # Double threads for spike
            test_case["recovery"]["threads"] = max(1, int(base_threads * 0.5))
            test_case["baseline"]["duration"] = int(test_case["duration"] * 0.3)
            test_case["spike"]["duration"] = int(test_case["duration"] * 0.4)
            test_case["recovery"]["duration"] = int(test_case["duration"] * 0.3)

        # Save updated configuration
        return self._save_config(self.config)

    def estimate_execution_time(self) -> Dict[str, Any]:
        """Estimate total execution time based on current configuration"""
        product_listing = self.config.get("test_scenarios", {}).get(
            "product_listing", {}
        )
        if not product_listing:
            return {"error": "Product listing configuration not found"}

        total_time = 0
        test_details = []

        # Calculate time for load tests
        for test_case in product_listing.get("load_test_cases", []):
            if test_case.get("enabled", False):
                duration = test_case.get("duration", 0)
                total_time += duration
                test_details.append(
                    {
                        "name": test_case.get("name", "Unknown"),
                        "type": "Load",
                        "duration": duration,
                        "threads": test_case.get("threads", 0),
                        "loops": test_case.get("loops", 0),
                    }
                )

        # Calculate time for stress tests
        for test_case in product_listing.get("stress_test_cases", []):
            if test_case.get("enabled", False):
                duration = test_case.get("duration", 0)
                total_time += duration
                test_details.append(
                    {
                        "name": test_case.get("name", "Unknown"),
                        "type": "Stress",
                        "duration": duration,
                        "threads": test_case.get("threads", 0),
                        "loops": test_case.get("loops", 0),
                    }
                )

        # Calculate time for spike tests
        for test_case in product_listing.get("spike_test_cases", []):
            if test_case.get("enabled", False):
                baseline = test_case.get("baseline", {})
                spike = test_case.get("spike", {})
                recovery = test_case.get("recovery", {})
                duration = (
                    baseline.get("duration", 0)
                    + spike.get("duration", 0)
                    + recovery.get("duration", 0)
                )
                total_time += duration
                test_details.append(
                    {
                        "name": test_case.get("name", "Unknown"),
                        "type": "Spike",
                        "duration": duration,
                        "baseline_threads": baseline.get("threads", 0),
                        "spike_threads": spike.get("threads", 0),
                        "recovery_threads": recovery.get("threads", 0),
                    }
                )

        return {
            "total_time_seconds": total_time,
            "total_time_minutes": round(total_time / 60, 2),
            "total_time_hours": round(total_time / 3600, 2),
            "test_details": test_details,
        }

    def print_duration_profiles(self):
        """Print available duration profiles"""
        print("\n📊 Available Duration Profiles:")
        print("=" * 60)

        for name, profile in self.duration_profiles.items():
            print(f"🔹 {name.upper()}: {profile.name}")
            print(f"   Description: {profile.description}")
            print(f"   Total Duration: {profile.total_duration_minutes} minutes")
            print(f"   Load Test Duration: {profile.load_test_duration}s")
            print(f"   Stress Test Duration: {profile.stress_test_duration}s")
            print(f"   Spike Test Duration: {profile.spike_test_duration}s")
            print(f"   Threads Multiplier: {profile.threads_multiplier}x")
            print(f"   Loops Multiplier: {profile.loops_multiplier}x")
            print()

    def print_current_estimate(self):
        """Print current execution time estimate"""
        estimate = self.estimate_execution_time()

        if "error" in estimate:
            print(f"❌ {estimate['error']}")
            return

        print("\n⏱️  Current Execution Time Estimate:")
        print("=" * 50)
        print(f"📊 Total Time: {estimate['total_time_seconds']} seconds")
        print(f"📊 Total Time: {estimate['total_time_minutes']} minutes")
        print(f"📊 Total Time: {estimate['total_time_hours']} hours")

        print("\n📋 Test Details:")
        for test in estimate["test_details"]:
            print(f"   🔹 {test['name']} ({test['type']}): {test['duration']}s")
            if test["type"] == "Spike":
                print(f"      Baseline: {test['baseline_threads']} threads")
                print(f"      Spike: {test['spike_threads']} threads")
                print(f"      Recovery: {test['recovery_threads']} threads")
            else:
                print(f"      Threads: {test['threads']}, Loops: {test['loops']}")


def main():
    """Main function for testing the optimizer"""
    optimizer = TestDurationOptimizer()

    print("🎯 Test Duration Optimizer")
    print("=" * 50)

    # Show available profiles
    optimizer.print_duration_profiles()

    # Show current estimate
    optimizer.print_current_estimate()

    # Example: Apply quick profile
    print("\n🚀 Applying Quick Profile...")
    if optimizer.apply_duration_profile("quick"):
        print("✅ Quick profile applied successfully")
        optimizer.print_current_estimate()
    else:
        print("❌ Failed to apply quick profile")


if __name__ == "__main__":
    main()
