"""
Main entry point for the data generator application.
Provides CLI interface and configuration options.
"""

import argparse
import sys
from pathlib import Path

from .config import GenerationConfig
from .orchestrator import DataGenerationOrchestrator


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate realistic mock data for practice-software-testing e-commerce platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m data_generator                           # Generate with default settings
  python -m data_generator --users 5000 --products 2000  # Custom counts
  python -m data_generator --output custom_output   # Custom output directory
  python -m data_generator --seed 123               # Custom random seed
        """,
    )

    # Record count arguments
    parser.add_argument(
        "--users",
        type=int,
        default=1000,
        help="Number of users to generate (default: 1000)",
    )
    parser.add_argument(
        "--categories",
        type=int,
        default=1000,
        help="Number of categories to generate (default: 1000)",
    )
    parser.add_argument(
        "--brands",
        type=int,
        default=200,
        help="Number of brands to generate (default: 200)",
    )
    parser.add_argument(
        "--product-images",
        type=int,
        default=500,
        help="Number of product images to generate (default: 500)",
    )
    parser.add_argument(
        "--products",
        type=int,
        default=1000,
        help="Number of products to generate (default: 1000)",
    )
    parser.add_argument(
        "--favorites",
        type=int,
        default=2000,
        help="Number of favorites to generate (default: 2000)",
    )
    parser.add_argument(
        "--invoices",
        type=int,
        default=800,
        help="Number of invoices to generate (default: 800)",
    )
    parser.add_argument(
        "--invoice-items",
        type=int,
        default=1500,
        help="Number of invoice items to generate (default: 1500)",
    )
    parser.add_argument(
        "--payments",
        type=int,
        default=800,
        help="Number of payments to generate (default: 800)",
    )

    # Configuration arguments
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory for CSV files (default: output)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible generation (default: 42)",
    )
    parser.add_argument(
        "--enable-deep-hierarchy",
        action="store_true",
        help="Enable 3-level category hierarchy (default: disabled)",
    )

    # Price range arguments
    parser.add_argument(
        "--min-price",
        type=float,
        default=1.99,
        help="Minimum product price (default: 1.99)",
    )
    parser.add_argument(
        "--max-price",
        type=float,
        default=9999.99,
        help="Maximum product price (default: 9999.99)",
    )

    # Other options
    parser.add_argument(
        "--generate-report",
        action="store_true",
        help="Generate detailed report after data generation",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")

    return parser


def create_config_from_args(args: argparse.Namespace) -> GenerationConfig:
    """Create a GenerationConfig from command line arguments."""
    return GenerationConfig(
        num_users=args.users,
        num_categories=args.categories,
        num_brands=args.brands,
        num_product_images=args.product_images,
        num_products=args.products,
        num_favorites=args.favorites,
        num_invoices=args.invoices,
        num_invoice_items=args.invoice_items,
        num_payments=args.payments,
        output_directory=args.output,
        random_seed=args.seed,
        enable_deep_hierarchy=args.enable_deep_hierarchy,
        min_price=args.min_price,
        max_price=args.max_price,
    )


def generate_report(config: GenerationConfig, output_dir: Path) -> None:
    """Generate a detailed report of the data generation process."""
    from .report_generator import ReportGenerator

    report_generator = ReportGenerator(config, output_dir)
    report_generator.generate_report()


def main() -> None:
    """Main entry point for the CLI application."""
    parser = create_argument_parser()
    args = parser.parse_args()

    try:
        # Create configuration from arguments
        config = create_config_from_args(args)

        # Validate configuration
        if config.num_products > config.num_categories * config.num_brands:
            print(
                "⚠️  Warning: More products than category-brand combinations available"
            )

        # Run data generation
        orchestrator = DataGenerationOrchestrator(config)

        if not args.quiet:
            print(f"🎯 Starting data generation with seed {config.random_seed}")
            print(f"📁 Output directory: {config.output_directory}")

        generated_data = orchestrator.generate_all_data()

        # Generate report if requested
        if args.generate_report:
            output_path = Path(config.output_directory)
            generate_report(config, output_path)

        if not args.quiet:
            print("\n🎉 Data generation completed successfully!")

    except KeyboardInterrupt:
        print("\n⚠️  Data generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during data generation: {e}")
        if not args.quiet:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
