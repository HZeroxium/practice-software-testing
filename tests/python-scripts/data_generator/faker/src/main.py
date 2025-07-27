"""
Main entry point for the data generator application.
Provides CLI interface and configuration options.
"""

import argparse
import sys
from pathlib import Path
from typing import List

from .config import GenerationConfig
from .orchestrator import DataGenerationOrchestrator
from .sql_generator import create_sql_generator
from .file_organizer import FileOrganizer
from .prompt_utils import (
    prompt_for_sql_generation,
    display_completion_summary,
    handle_keyboard_interrupt,
    display_message,
)


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate realistic mock data for practice-software-testing e-commerce platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main                                 # Generate with default settings
  python -m src.main --users 100 --products 300     # Custom counts
  python -m src.main --output custom_output         # Custom output directory
  python -m src.main --seed 123                     # Custom random seed
  python -m src.main --pixabay-api-key YOUR_KEY     # Use real Pixabay images
  export PIXABAY_API_KEY=YOUR_KEY && python -m src.main  # API key via environment
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
        default=100,
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
        default=500,
        help="Number of products to generate (default: 500)",
    )
    parser.add_argument(
        "--favorites",
        type=int,
        default=200,
        help="Number of favorites to generate (default: 200)",
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

    # External API options
    # parser.add_argument(
    #     "--pixabay-api-key",
    #     type=str,
    #     default=None,
    #     help="Pixabay API key for realistic product images (or set PIXABAY_API_KEY env var)",
    # )
    parser.add_argument(
        "--disable-pixabay",
        action="store_true",
        help="Disable Pixabay integration even if API key is provided",
    )

    # Backup management options
    parser.add_argument(
        "--clean-backups",
        action="store_true",
        help="Clean old backup files before generation",
    )
    parser.add_argument(
        "--backup-report",
        action="store_true",
        help="Show backup files report and exit",
    )
    parser.add_argument(
        "--max-backups",
        type=int,
        default=0,
        help="Maximum number of backup files to keep per file type (default: 5)",
    )
    parser.add_argument(
        "--max-backup-age",
        type=int,
        default=7,
        help="Maximum age of backup files in days (default: 7)",
    )

    return parser


def create_config_from_args(args: argparse.Namespace) -> GenerationConfig:
    """Create a GenerationConfig from command line arguments."""
    # Get Pixabay API key from args or environment
    import os

    pixabay_api_key = os.getenv("PIXABAY_API_KEY")

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
        pixabay_api_key="51403672-ec695c0d56213e6a47f6db68a",
        # enable_pixabay_integration=not args.disable_pixabay
        # and pixabay_api_key is not None,
        pixabay_cache_enabled=True,
    )


def generate_sql_scripts(
    config: GenerationConfig, file_organizer: FileOrganizer
) -> List[Path]:
    """Generate SQL scripts for all CSV files."""
    sql_options = prompt_for_sql_generation()

    if not sql_options:
        return []

    sql_generator = create_sql_generator(sql_options["db_type"])
    generated_sql_files = []

    try:
        # Get CSV directory from file organizer
        csv_dir = file_organizer.get_csv_directory()
        sql_dir = file_organizer.get_sql_directory()

        # Define table mappings for CSV files
        table_mappings = {
            "users.csv": "users",
            "categories.csv": "categories",
            "brands.csv": "brands",
            "product_images.csv": "product_images",
            "products.csv": "products",
            "favorites.csv": "favorites",
            "invoices.csv": "invoices",
            "invoice_items.csv": "invoice_items",
            "payments.csv": "payments",
        }

        display_message("info", "Generating SQL INSERT scripts...")

        for csv_filename, table_name in table_mappings.items():
            csv_file = csv_dir / csv_filename

            if csv_file.exists():
                try:
                    # Filter out db_type since it's already set in the generator
                    generation_options = {
                        k: v for k, v in sql_options.items() if k != "db_type"
                    }

                    # Generate SQL script
                    sql_script = sql_generator.generate_from_csv(
                        csv_file, table_name, **generation_options
                    )

                    # Write SQL file to organized SQL directory
                    sql_filename = f"{table_name}_{sql_options['db_type']}.sql"
                    sql_file = sql_dir / sql_filename
                    sql_generator.write_sql_file(sql_script, sql_file)
                    generated_sql_files.append(sql_file)

                except Exception as e:
                    display_message(
                        "warning", f"Failed to generate SQL for {csv_filename}: {e}"
                    )

        if generated_sql_files:
            display_message(
                "success", f"Generated {len(generated_sql_files)} SQL scripts"
            )

    except Exception as e:
        display_message("error", f"SQL generation failed: {e}")

    return generated_sql_files


def generate_report(config: GenerationConfig, output_dir: Path) -> None:
    """Generate a detailed report of the data generation process."""
    from .report_generator import ReportGenerator

    report_generator = ReportGenerator(config, output_dir)
    report_generator.generate_report()


def main() -> None:
    """Main entry point for the CLI application."""
    try:
        parser = create_argument_parser()
        args = parser.parse_args()

        # Handle backup management commands
        if args.backup_report:
            from .file_organizer import FileOrganizer

            output_path = Path(args.output)
            file_organizer = FileOrganizer(output_path)
            file_organizer.print_backup_report()
            return

        # Create configuration from arguments
        config = create_config_from_args(args)

        # Handle backup cleaning if requested
        if args.clean_backups:
            from .file_organizer import FileOrganizer

            output_path = Path(config.output_directory)
            file_organizer = FileOrganizer(output_path)
            file_organizer.clean_old_backups(
                max_backups_per_file=args.max_backups, max_age_days=args.max_backup_age
            )
            print("✅ Backup cleanup completed!")
            if not any(
                [args.users, args.categories, args.products]
            ):  # If only cleanup requested
                return

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
        output_path = Path(config.output_directory)

        # Get the file organizer from orchestrator
        file_organizer = orchestrator.file_organizer

        # Generate report if requested
        if args.generate_report:
            generate_report(config, output_path)

        if not args.quiet:
            print("\n✅ CSV data generation completed successfully!")

        # Optional SQL generation step
        sql_files = []
        if not args.quiet:  # Only prompt in interactive mode
            try:
                sql_files = generate_sql_scripts(config, file_organizer)
            except KeyboardInterrupt:
                handle_keyboard_interrupt()

        # Display final completion summary
        if not args.quiet:
            csv_files = list(file_organizer.get_csv_directory().glob("*.csv"))
            sql_files_list = list(file_organizer.get_sql_directory().glob("*.sql"))

            summary_data = {
                "csv_files": [str(f.relative_to(output_path)) for f in csv_files],
                "sql_files": [str(f.relative_to(output_path)) for f in sql_files_list],
                "total_records": sum(
                    getattr(config, f"num_{table}", 0)
                    for table in [
                        "users",
                        "categories",
                        "brands",
                        "product_images",
                        "products",
                        "favorites",
                        "invoices",
                        "invoice_items",
                        "payments",
                    ]
                ),
            }

            display_completion_summary(summary_data)

    except KeyboardInterrupt:
        handle_keyboard_interrupt()
    except Exception as e:
        print(f"\n❌ Error during data generation: {e}")
        if not args.quiet:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
