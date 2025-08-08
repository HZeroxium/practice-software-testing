#!/usr/bin/env python3
"""
Duration Manager for Performance Testing

This script provides an easy way to manage test duration profiles and optimize
test configurations for different execution times.

Author: Performance Testing Automation
Date: 2024
"""

import sys
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from test_duration_optimizer import TestDurationOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def show_menu():
    """Show the main menu"""
    print("\n" + "=" * 60)
    print("🎯 TEST DURATION MANAGER")
    print("=" * 60)
    print("1. Show available duration profiles")
    print("2. Show current execution time estimate")
    print("3. Apply quick profile (~15 seconds)")
    print("4. Apply short profile (~5 minutes)")
    print("5. Apply medium profile (~15 minutes)")
    print("6. Apply long profile (~30 minutes)")
    print("7. Apply extended profile (~60 minutes)")
    print("8. Optimize for custom duration")
    print("9. Run quick test with current configuration")
    print("0. Exit")
    print("=" * 60)


def apply_profile(
    optimizer: TestDurationOptimizer, profile_name: str, description: str
):
    """Apply a duration profile"""
    print(f"\n🚀 Applying {profile_name} profile: {description}")
    print("-" * 50)

    success = optimizer.apply_duration_profile(profile_name)

    if success:
        print(f"✅ {profile_name.title()} profile applied successfully!")
        print("\n📊 Updated execution time estimate:")
        optimizer.print_current_estimate()
    else:
        print(f"❌ Failed to apply {profile_name} profile")


def optimize_custom_duration(optimizer: TestDurationOptimizer):
    """Optimize for custom duration"""
    print("\n🎯 Custom Duration Optimization")
    print("-" * 40)

    try:
        minutes = int(input("Enter target duration in minutes: ").strip())
        if minutes <= 0:
            print("❌ Duration must be greater than 0!")
            return

        print(f"\n🚀 Optimizing for {minutes} minutes...")
        print("-" * 40)

        success = optimizer.optimize_for_duration(minutes)

        if success:
            print(f"✅ Configuration optimized for {minutes} minutes!")
            print("\n📊 Updated execution time estimate:")
            optimizer.print_current_estimate()
        else:
            print(f"❌ Failed to optimize for {minutes} minutes")

    except ValueError:
        print("❌ Invalid duration value! Please enter a number.")
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")


def run_quick_test():
    """Run test with current configuration"""
    print("\n🚀 Running Test...")
    print("-" * 30)

    try:
        from quick_test import main as run_quick_test_main

        run_quick_test_main()
    except ImportError:
        print("❌ Test module not found!")
    except Exception as e:
        print(f"❌ Error running test: {e}")


def main():
    """Main function"""
    print("🎯 Test Duration Manager")
    print("=" * 50)

    # Initialize optimizer
    optimizer = TestDurationOptimizer()

    while True:
        show_menu()

        try:
            choice = input("\nEnter your choice (0-9): ").strip()

            if choice == "1":
                optimizer.print_duration_profiles()

            elif choice == "2":
                # Reload config before showing estimate
                optimizer.config = optimizer._load_config()
                optimizer.print_current_estimate()

            elif choice == "3":
                apply_profile(optimizer, "quick", "Fast validation test (~15 seconds)")

            elif choice == "4":
                apply_profile(optimizer, "short", "Brief performance test (~5 minutes)")

            elif choice == "5":
                apply_profile(
                    optimizer, "medium", "Standard performance test (~15 minutes)"
                )

            elif choice == "6":
                apply_profile(
                    optimizer, "long", "Comprehensive performance test (~30 minutes)"
                )

            elif choice == "7":
                apply_profile(
                    optimizer, "extended", "Extended performance test (~60 minutes)"
                )

            elif choice == "8":
                optimize_custom_duration(optimizer)

            elif choice == "9":
                run_quick_test()

            elif choice == "0":
                print("\n👋 Exiting Duration Manager...")
                break

            else:
                print("❌ Invalid choice. Please try again.")

        except KeyboardInterrupt:
            print("\n\n👋 Exiting Duration Manager...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
