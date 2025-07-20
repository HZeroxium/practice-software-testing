"""
Demo script showcasing the comprehensive data generator capabilities.
Generates sample data and demonstrates various features.
"""

import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from .config import GenerationConfig
from orchestrator import DataGenerationOrchestrator
from report_generator import ReportGenerator


def demo_small_dataset():
    """Generate a small dataset for demonstration purposes."""
    print("🎯 Demo 1: Small Dataset Generation")
    print("=" * 50)

    config = GenerationConfig(
        num_users=50,
        num_categories=100,
        num_brands=20,
        num_product_images=30,
        num_products=100,
        num_favorites=150,
        num_invoices=40,
        num_invoice_items=80,
        num_payments=40,
        output_directory="demo_output_small",
        random_seed=42,
    )

    orchestrator = DataGenerationOrchestrator(config)
    data = orchestrator.generate_all_data()

    print("\n📊 Small Dataset Summary:")
    for table_name, records in data.items():
        print(f"  • {table_name}: {len(records)} records")

    return config, data


def demo_medium_dataset():
    """Generate a medium dataset for testing purposes."""
    print("\n🎯 Demo 2: Medium Dataset Generation")
    print("=" * 50)

    config = GenerationConfig(
        num_users=1000,
        num_categories=500,
        num_brands=100,
        num_product_images=200,
        num_products=1000,
        num_favorites=2000,
        num_invoices=500,
        num_invoice_items=1200,
        num_payments=500,
        output_directory="demo_output_medium",
        random_seed=123,
    )

    orchestrator = DataGenerationOrchestrator(config)
    data = orchestrator.generate_all_data()

    print("\n📊 Medium Dataset Summary:")
    for table_name, records in data.items():
        print(f"  • {table_name}: {len(records)} records")

    return config, data


def demo_custom_configuration():
    """Demonstrate custom configuration options."""
    print("\n🎯 Demo 3: Custom Configuration")
    print("=" * 50)

    config = GenerationConfig(
        num_users=200,
        num_categories=300,
        num_brands=50,
        num_product_images=100,
        num_products=500,
        num_favorites=800,
        num_invoices=150,
        num_invoice_items=400,
        num_payments=150,
        # Custom business logic
        admin_totp_probability=0.25,  # Higher TOTP adoption for admins
        user_totp_probability=0.05,  # Higher TOTP adoption for users
        product_in_stock_probability=0.90,  # Higher stock availability
        product_location_offer_probability=0.15,  # More location offers
        product_rental_probability=0.10,  # More rental products
        # Custom price range
        min_price=5.00,
        max_price=5000.00,
        # Custom invoice settings
        min_invoice_items=1,
        max_invoice_items=15,  # Larger orders
        min_quantity_per_item=1,
        max_quantity_per_item=10,  # Higher quantities
        output_directory="demo_output_custom",
        random_seed=456,
    )

    orchestrator = DataGenerationOrchestrator(config)
    data = orchestrator.generate_all_data()

    # Analyze the generated data
    print("\n📊 Custom Dataset Analysis:")

    # User analysis
    users = data["users"]
    admin_count = len([u for u in users if u["role"] == "admin"])
    totp_enabled_users = len([u for u in users if u["totp_enabled"]])
    print(
        f"  • Admin users: {admin_count}/{len(users)} ({admin_count/len(users)*100:.1f}%)"
    )
    print(
        f"  • TOTP enabled: {totp_enabled_users}/{len(users)} ({totp_enabled_users/len(users)*100:.1f}%)"
    )

    # Product analysis
    products = data["products"]
    in_stock_count = len([p for p in products if p["in_stock"]])
    location_offers = len([p for p in products if p["is_location_offer"]])
    rental_products = len([p for p in products if p["is_rental"]])
    print(
        f"  • In stock products: {in_stock_count}/{len(products)} ({in_stock_count/len(products)*100:.1f}%)"
    )
    print(
        f"  • Location offers: {location_offers}/{len(products)} ({location_offers/len(products)*100:.1f}%)"
    )
    print(
        f"  • Rental products: {rental_products}/{len(products)} ({rental_products/len(products)*100:.1f}%)"
    )

    # Price analysis
    prices = [float(p["price"]) for p in products]
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    print(
        f"  • Price range: ${min_price:.2f} - ${max_price:.2f} (avg: ${avg_price:.2f})"
    )

    return config, data


def demo_report_generation():
    """Demonstrate report generation."""
    print("\n🎯 Demo 4: Report Generation")
    print("=" * 50)

    config = GenerationConfig(
        num_users=100,
        num_categories=200,
        num_brands=30,
        num_product_images=50,
        num_products=200,
        num_favorites=300,
        num_invoices=80,
        num_invoice_items=160,
        num_payments=80,
        output_directory="demo_output_report",
        random_seed=789,
    )

    orchestrator = DataGenerationOrchestrator(config)
    orchestrator.generate_all_data()

    # Generate comprehensive report
    output_path = Path(config.output_directory)
    report_generator = ReportGenerator(config, output_path)
    report_generator.generate_report()

    print(f"📝 Comprehensive report generated: {output_path}/data_generation_report.md")

    return config


def main():
    """Run all demonstration scenarios."""
    print("🚀 Data Generator Comprehensive Demo")
    print("=" * 80)
    print("This demo showcases the full capabilities of the refactored data generator")
    print("for the practice-software-testing e-commerce platform.")
    print()

    try:
        # Run all demos
        demo_small_dataset()
        demo_medium_dataset()
        demo_custom_configuration()
        demo_report_generation()

        print("\n" + "=" * 80)
        print("🎉 All demonstrations completed successfully!")
        print()
        print("📁 Generated Output Directories:")
        for dir_name in [
            "demo_output_small",
            "demo_output_medium",
            "demo_output_custom",
            "demo_output_report",
        ]:
            dir_path = Path(dir_name)
            if dir_path.exists():
                file_count = len(list(dir_path.glob("*.csv")))
                print(f"  • {dir_name}: {file_count} CSV files")

        print()
        print("🔍 Next Steps:")
        print("  1. Review the generated CSV files in each output directory")
        print(
            "  2. Check the comprehensive report in demo_output_report/data_generation_report.md"
        )
        print("  3. Import the data into your practice-software-testing database")
        print("  4. Run your tests with realistic, comprehensive data")
        print()
        print("💡 For production use:")
        print(
            "  python -m data_generator --users 10000 --products 5000 --generate-report"
        )

    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
