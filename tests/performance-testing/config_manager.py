#!/usr/bin/env python3
"""
Configuration Manager for Performance Testing

This script provides an easy way to modify test configuration parameters
without editing JSON files directly.

Author: Performance Testing Automation
Date: 2024
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from test_duration_optimizer import TestDurationOptimizer

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manage performance testing configuration"""

    def __init__(self, config_file: str = "config/test_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.duration_optimizer = TestDurationOptimizer(str(self.config_file))

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

    def _save_config(self) -> bool:
        """Save configuration to JSON file"""
        try:
            self.config_file.parent.mkdir(exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False

    def update_application_urls(
        self, frontend_url: str = None, api_url: str = None
    ) -> bool:
        """Update application URLs"""
        if frontend_url:
            self.config.setdefault("application", {})["frontend_url"] = frontend_url
        if api_url:
            self.config.setdefault("application", {})["api_url"] = api_url

        return self._save_config()

    def update_load_test_config(
        self,
        threads: int = None,
        ramp_up: int = None,
        loops: int = None,
        duration: int = None,
    ) -> bool:
        """Update load test configuration"""
        scenario = self.config.setdefault("test_scenarios", {}).setdefault(
            "load_test_product_listing", {}
        )

        if threads is not None:
            scenario["threads"] = threads
        if ramp_up is not None:
            scenario["ramp_up"] = ramp_up
        if loops is not None:
            scenario["loops"] = loops
        if duration is not None:
            scenario["duration"] = duration

        return self._save_config()

    def update_stress_test_config(
        self,
        threads: int = None,
        ramp_up: int = None,
        loops: int = None,
        duration: int = None,
    ) -> bool:
        """Update stress test configuration"""
        scenario = self.config.setdefault("test_scenarios", {}).setdefault(
            "stress_test_product_detail", {}
        )

        if threads is not None:
            scenario["threads"] = threads
        if ramp_up is not None:
            scenario["ramp_up"] = ramp_up
        if loops is not None:
            scenario["loops"] = loops
        if duration is not None:
            scenario["duration"] = duration

        return self._save_config()

    def update_spike_test_config(
        self,
        baseline_threads: int = None,
        spike_threads: int = None,
        recovery_threads: int = None,
    ) -> bool:
        """Update spike test configuration"""
        scenario = self.config.setdefault("test_scenarios", {}).setdefault(
            "spike_test_contact_form", {}
        )

        if baseline_threads is not None:
            scenario.setdefault("baseline", {})["threads"] = baseline_threads
        if spike_threads is not None:
            scenario.setdefault("spike", {})["threads"] = spike_threads
        if recovery_threads is not None:
            scenario.setdefault("recovery", {})["threads"] = recovery_threads

        return self._save_config()

    def update_reporting_config(
        self, keep_recent: int = None, cleanup_old: bool = None
    ) -> bool:
        """Update reporting configuration"""
        reporting = self.config.setdefault("reporting", {})

        if keep_recent is not None:
            reporting["keep_recent_reports"] = keep_recent
        if cleanup_old is not None:
            reporting["cleanup_old_results"] = cleanup_old

        return self._save_config()

    def enable_test_scenario(self, scenario_name: str, enabled: bool = True) -> bool:
        """Enable or disable a test scenario"""
        scenarios = self.config.setdefault("test_scenarios", {})
        if scenario_name in scenarios:
            scenarios[scenario_name]["enabled"] = enabled
            return self._save_config()
        else:
            logger.error(f"Test scenario '{scenario_name}' not found")
            return False

    def get_current_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config.copy()

    def print_current_config(self) -> None:
        """Print current configuration in a readable format"""
        print("\n" + "=" * 60)
        print("CURRENT PERFORMANCE TESTING CONFIGURATION")
        print("=" * 60)

        # Application URLs
        app_config = self.config.get("application", {})
        print(f"\n📱 Application URLs:")
        print(f"   Frontend: {app_config.get('frontend_url', 'http://localhost:4200')}")
        print(f"   API: {app_config.get('api_url', 'http://localhost:8091')}")

        # Test Scenarios
        print(f"\n🧪 Test Scenarios:")
        scenarios = self.config.get("test_scenarios", {})
        for name, config in scenarios.items():
            enabled = "✅" if config.get("enabled", True) else "❌"
            print(f"   {enabled} {name}:")

            if "threads" in config:
                print(f"      Threads: {config['threads']}")
            if "ramp_up" in config:
                print(f"      Ramp-up: {config['ramp_up']}s")
            if "loops" in config:
                print(f"      Loops: {config['loops']}")
            if "duration" in config:
                print(f"      Duration: {config['duration']}s")

            # Spike test has special configuration
            if "baseline" in config:
                print(
                    f"      Baseline: {config['baseline'].get('threads', 10)} threads"
                )
                print(f"      Spike: {config['spike'].get('threads', 100)} threads")
                print(
                    f"      Recovery: {config['recovery'].get('threads', 10)} threads"
                )

        # Reporting
        reporting = self.config.get("reporting", {})
        print(f"\n📊 Reporting:")
        print(f"   Keep recent reports: {reporting.get('keep_recent_reports', 3)}")
        print(f"   Cleanup old results: {reporting.get('cleanup_old_results', True)}")

        print("\n" + "=" * 60)

    def create_quick_test_config(self) -> bool:
        """Create a quick test configuration using duration optimizer"""
        print("Creating quick test configuration...")

        # Apply quick duration profile
        success = self.duration_optimizer.apply_duration_profile("quick")

        if success:
            print("Quick test configuration created successfully!")
            return True
        else:
            print("Failed to create quick test configuration")
            return False

    def create_production_test_config(self) -> bool:
        """Create a production-like test configuration using duration optimizer"""
        print("Creating production test configuration...")

        # Apply long duration profile for production-like testing
        success = self.duration_optimizer.apply_duration_profile("long")

        if success:
            print("Production test configuration created successfully!")
            return True
        else:
            print("Failed to create production test configuration")
            return False

    def apply_duration_profile(self, profile_name: str) -> bool:
        """Apply a predefined duration profile"""
        print(f"Applying {profile_name} duration profile...")
        success = self.duration_optimizer.apply_duration_profile(profile_name)

        if success:
            print(f"{profile_name.title()} profile applied successfully!")
            return True
        else:
            print(f"Failed to apply {profile_name} profile")
            return False

    def optimize_for_duration(self, target_minutes: int) -> bool:
        """Optimize test configuration for a specific target duration"""
        print(f"Optimizing for {target_minutes} minutes...")
        success = self.duration_optimizer.optimize_for_duration(target_minutes)

        if success:
            print(f"Configuration optimized for {target_minutes} minutes!")
            return True
        else:
            print(f"Failed to optimize for {target_minutes} minutes")
            return False

    def show_duration_profiles(self) -> None:
        """Show available duration profiles"""
        self.duration_optimizer.print_duration_profiles()

    def show_execution_estimate(self) -> None:
        """Show current execution time estimate"""
        self.duration_optimizer.print_current_estimate()


def main():
    """Main execution function with interactive menu"""
    config_manager = ConfigManager()

    while True:
        print("\n" + "=" * 60)
        print("PERFORMANCE TESTING CONFIGURATION MANAGER")
        print("=" * 60)
        print("1. View current configuration")
        print("2. Update application URLs")
        print("3. Update load test configuration")
        print("4. Update stress test configuration")
        print("5. Update spike test configuration")
        print("6. Update reporting configuration")
        print("7. Enable/disable test scenarios")
        print("8. Create quick test configuration")
        print("9. Create production test configuration")
        print("10. Show duration profiles")
        print("11. Apply duration profile")
        print("12. Optimize for custom duration")
        print("13. Show execution time estimate")
        print("0. Exit")

        choice = input("\nEnter your choice (0-13): ").strip()

        if choice == "1":
            config_manager.print_current_config()

        elif choice == "2":
            frontend = input("Frontend URL (press Enter to skip): ").strip()
            api = input("API URL (press Enter to skip): ").strip()
            frontend = frontend if frontend else None
            api = api if api else None
            if config_manager.update_application_urls(frontend, api):
                print("Application URLs updated successfully!")

        elif choice == "3":
            threads = input("Number of threads (press Enter to skip): ").strip()
            ramp_up = input("Ramp-up time in seconds (press Enter to skip): ").strip()
            loops = input("Number of loops (press Enter to skip): ").strip()
            duration = input("Duration in seconds (press Enter to skip): ").strip()

            threads = int(threads) if threads.isdigit() else None
            ramp_up = int(ramp_up) if ramp_up.isdigit() else None
            loops = int(loops) if loops.isdigit() else None
            duration = int(duration) if duration.isdigit() else None

            if config_manager.update_load_test_config(
                threads, ramp_up, loops, duration
            ):
                print("Load test configuration updated successfully!")

        elif choice == "4":
            threads = input("Number of threads (press Enter to skip): ").strip()
            ramp_up = input("Ramp-up time in seconds (press Enter to skip): ").strip()
            loops = input("Number of loops (press Enter to skip): ").strip()
            duration = input("Duration in seconds (press Enter to skip): ").strip()

            threads = int(threads) if threads.isdigit() else None
            ramp_up = int(ramp_up) if ramp_up.isdigit() else None
            loops = int(loops) if loops.isdigit() else None
            duration = int(duration) if duration.isdigit() else None

            if config_manager.update_stress_test_config(
                threads, ramp_up, loops, duration
            ):
                print("Stress test configuration updated successfully!")

        elif choice == "5":
            baseline = input("Baseline threads (press Enter to skip): ").strip()
            spike = input("Spike threads (press Enter to skip): ").strip()
            recovery = input("Recovery threads (press Enter to skip): ").strip()

            baseline = int(baseline) if baseline.isdigit() else None
            spike = int(spike) if spike.isdigit() else None
            recovery = int(recovery) if recovery.isdigit() else None

            if config_manager.update_spike_test_config(baseline, spike, recovery):
                print("Spike test configuration updated successfully!")

        elif choice == "6":
            keep_recent = input("Keep recent reports (press Enter to skip): ").strip()
            cleanup = (
                input("Cleanup old results (y/n, press Enter to skip): ")
                .strip()
                .lower()
            )

            keep_recent = int(keep_recent) if keep_recent.isdigit() else None
            cleanup = cleanup == "y" if cleanup in ["y", "n"] else None

            if config_manager.update_reporting_config(keep_recent, cleanup):
                print("Reporting configuration updated successfully!")

        elif choice == "7":
            scenarios = config_manager.config.get("test_scenarios", {})
            print("\nAvailable scenarios:")
            for i, name in enumerate(scenarios.keys(), 1):
                enabled = scenarios[name].get("enabled", True)
                status = "✅ Enabled" if enabled else "❌ Disabled"
                print(f"{i}. {name} - {status}")

            scenario_choice = input(
                "Enter scenario number (press Enter to skip): "
            ).strip()
            if scenario_choice.isdigit():
                scenario_idx = int(scenario_choice) - 1
                scenario_names = list(scenarios.keys())
                if 0 <= scenario_idx < len(scenario_names):
                    scenario_name = scenario_names[scenario_idx]
                    enable = input(f"Enable {scenario_name}? (y/n): ").strip().lower()
                    if enable in ["y", "n"]:
                        enabled = enable == "y"
                        if config_manager.enable_test_scenario(scenario_name, enabled):
                            print(
                                f"Scenario {scenario_name} {'enabled' if enabled else 'disabled'} successfully!"
                            )

        elif choice == "8":
            if config_manager.create_quick_test_config():
                print("Quick test configuration created!")

        elif choice == "9":
            if config_manager.create_production_test_config():
                print("Production test configuration created!")

        elif choice == "10":
            config_manager.show_duration_profiles()

        elif choice == "11":
            print("\nAvailable profiles: quick, short, medium, long, extended")
            profile = input("Enter profile name: ").strip().lower()
            if profile in ["quick", "short", "medium", "long", "extended"]:
                config_manager.apply_duration_profile(profile)
            else:
                print("Invalid profile name!")

        elif choice == "12":
            try:
                minutes = int(input("Enter target duration in minutes: ").strip())
                if minutes > 0:
                    config_manager.optimize_for_duration(minutes)
                else:
                    print("Duration must be greater than 0!")
            except ValueError:
                print("Invalid duration value!")

        elif choice == "13":
            config_manager.show_execution_estimate()

        elif choice == "0":
            print("Exiting configuration manager...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
