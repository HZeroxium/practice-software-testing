"""
Main orchestrator for the data generation process.
Coordinates all generators and manages dependencies between tables.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

from faker import Faker

from .config import GenerationConfig, DEFAULT_CONFIG
from .providers import ECommerceProvider, HardwareToolProvider
from .generators import (
    UserGenerator,
    CategoryGenerator,
    BrandGenerator,
    ProductImageGenerator,
    ProductGenerator,
    FavoriteGenerator,
    InvoiceGenerator,
    InvoiceItemGenerator,
    PaymentGenerator,
)
from .data_validator import DataValidator
from .file_organizer import FileOrganizer


class DataGenerationOrchestrator:
    """Orchestrates the entire data generation process."""

    def __init__(self, config: Optional[GenerationConfig] = None):
        """Initialize the orchestrator with configuration."""
        self.config = config or DEFAULT_CONFIG
        self._setup_faker()
        self._setup_generators()
        self.generated_data: Dict[str, List[Dict[str, Any]]] = {}

        # Initialize file organizer
        self.file_organizer = FileOrganizer(Path(self.config.output_directory))

    def _setup_faker(self) -> None:
        """Setup Faker with custom providers and seed."""
        Faker.seed(self.config.random_seed)
        self.fake = Faker()
        self.fake.add_provider(ECommerceProvider)
        self.fake.add_provider(HardwareToolProvider)

    def _setup_generators(self) -> None:
        """Initialize all data generators."""
        self.generators = {
            "users": UserGenerator(self.config, self.fake),
            "categories": CategoryGenerator(self.config, self.fake),
            "brands": BrandGenerator(self.config, self.fake),
            "product_images": ProductImageGenerator(self.config, self.fake),
            "products": ProductGenerator(self.config, self.fake),
            "favorites": FavoriteGenerator(self.config, self.fake),
            "invoices": InvoiceGenerator(self.config, self.fake),
            "invoice_items": InvoiceItemGenerator(self.config, self.fake),
            "payments": PaymentGenerator(self.config, self.fake),
        }

    def generate_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate all data in the correct dependency order."""
        print(
            "🚀 Starting comprehensive data generation for practice-software-testing platform"
        )
        print("📋 Domain: Tool & Hardware E-commerce")
        print("🗃️ Target: All 9 database tables with realistic relationships")
        print(
            f"🎯 Configuration: {self.config.num_users} users, {self.config.num_products} products"
        )
        print()

        start_time = time.time()

        # Phase 1: Generate independent tables
        print("📊 Phase 1: Generating independent entities...")
        self._generate_users()
        self._generate_categories()
        self._generate_brands()
        self._generate_product_images()

        # Phase 2: Generate dependent tables
        print("\n📊 Phase 2: Generating dependent entities...")
        self._generate_products()
        self._generate_favorites()
        self._generate_invoices()

        # Phase 3: Generate invoice items and update invoice totals
        print("\n📊 Phase 3: Generating invoice items and payments...")
        self._generate_invoice_items()
        self._generate_payments()

        # Phase 4: Save all data to CSV files (temporarily to base directory)
        print("\n💾 Phase 4: Saving data to CSV files...")
        self._save_all_data()

        # Phase 5: Validate generated data
        print("\n🔍 Phase 5: Validating data integrity...")
        is_valid = self._validate_generated_data()

        if not is_valid:
            print("\n❌ Data validation failed! Stopping pipeline.")
            print("💡 Please check the validation errors above and try again.")
            sys.exit(1)

        # Phase 6: Organize files into proper directory structure
        print("\n📁 Phase 6: Organizing output files...")
        self._organize_output_files()

        end_time = time.time()

        # Generate summary report
        self._print_generation_summary(end_time - start_time)

        return self.generated_data

    def _generate_users(self) -> None:
        """Generate user data."""
        self.generated_data["users"] = self.generators["users"].generate(
            self.config.num_users
        )

    def _generate_categories(self) -> None:
        """Generate category data."""
        self.generated_data["categories"] = self.generators["categories"].generate(
            self.config.num_categories
        )

    def _generate_brands(self) -> None:
        """Generate brand data."""
        self.generated_data["brands"] = self.generators["brands"].generate(
            self.config.num_brands
        )

    def _generate_product_images(self) -> None:
        """Generate product image data."""
        self.generated_data["product_images"] = self.generators[
            "product_images"
        ].generate(
            count=self.config.num_product_images,
            categories=self.generated_data["categories"],
        )

    def _generate_products(self) -> None:
        """Generate product data."""
        self.generated_data["products"] = self.generators["products"].generate(
            count=self.config.num_products,
            categories=self.generated_data["categories"],
            brands=self.generated_data["brands"],
            images=self.generated_data["product_images"],
        )

    def _generate_favorites(self) -> None:
        """Generate favorite data."""
        self.generated_data["favorites"] = self.generators["favorites"].generate(
            count=self.config.num_favorites,
            users=self.generated_data["users"],
            products=self.generated_data["products"],
        )

    def _generate_invoices(self) -> None:
        """Generate invoice data."""
        self.generated_data["invoices"] = self.generators["invoices"].generate(
            count=self.config.num_invoices, users=self.generated_data["users"]
        )

    def _generate_invoice_items(self) -> None:
        """Generate invoice item data and update invoice totals."""
        invoice_items, invoice_totals = self.generators["invoice_items"].generate(
            count=self.config.num_invoice_items,
            invoices=self.generated_data["invoices"],
            products=self.generated_data["products"],
        )

        self.generated_data["invoice_items"] = invoice_items

        # Update invoice totals
        for invoice in self.generated_data["invoices"]:
            if invoice["id"] in invoice_totals:
                invoice["total"] = invoice_totals[invoice["id"]]

    def _generate_payments(self) -> None:
        """Generate payment data."""
        self.generated_data["payments"] = self.generators["payments"].generate(
            count=self.config.num_payments, invoices=self.generated_data["invoices"]
        )

    def _save_all_data(self) -> None:
        """Save all generated data to CSV files."""
        # Ensure output directory exists
        output_path = Path(self.config.output_directory)
        output_path.mkdir(exist_ok=True)

        # Define file mapping
        file_mapping = {
            "users": "users.csv",
            "categories": "categories.csv",
            "brands": "brands.csv",
            "product_images": "product_images.csv",
            "products": "products.csv",
            "favorites": "favorites.csv",
            "invoices": "invoices.csv",
            "invoice_items": "invoice_items.csv",
            "payments": "payments.csv",
        }

        for table_name, filename in file_mapping.items():
            if table_name in self.generated_data:
                self.generators[table_name].save_to_csv(
                    self.generated_data[table_name], filename
                )

    def _validate_generated_data(self) -> bool:
        """Validate the generated data for consistency and integrity."""
        # Use the base output directory (where CSVs are temporarily saved)
        validator = DataValidator(Path(self.config.output_directory))
        is_valid, errors = validator.validate_all_data()

        # If validation fails, save error report
        if not is_valid:
            self._save_validation_errors(errors)

        return is_valid

    def _save_validation_errors(self, errors) -> None:
        """Save validation errors to a report file."""
        output_path = Path(self.config.output_directory)
        error_report_path = output_path / "validation_errors.txt"

        with open(error_report_path, "w", encoding="utf-8") as f:
            f.write("VALIDATION ERROR REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total errors found: {len(errors)}\n\n")

            # Group errors by type
            error_types = {}
            for error in errors:
                if error.error_type not in error_types:
                    error_types[error.error_type] = []
                error_types[error.error_type].append(error)

            for error_type, type_errors in error_types.items():
                f.write(f"\n{error_type} ({len(type_errors)} errors):\n")
                f.write("-" * 40 + "\n")
                for error in type_errors:
                    f.write(f"{error}\n")

        print(f"💾 Validation errors saved to: {error_report_path}")

    def _organize_output_files(self) -> None:
        """Organize output files into structured directories and clean old backups."""
        # Clean old backups before organizing new files
        print("🧹 Cleaning old backup files...")
        self.file_organizer.clean_old_backups(max_backups_per_file=5, max_age_days=7)

        # Organize the current output files
        organized_files = self.file_organizer.organize_all_files()

        # Update our tracking of where files are located
        self.csv_files_location = self.file_organizer.get_csv_directory()
        self.sql_files_location = self.file_organizer.get_sql_directory()

        return organized_files

    def _print_generation_summary(self, duration: float) -> None:
        """Print a comprehensive summary of the generation process."""
        print("\n" + "=" * 80)
        print("📊 DATA GENERATION SUMMARY")
        print("=" * 80)

        print(f"⏱️  Total Generation Time: {duration:.2f} seconds")
        print(f"🔧 Configuration Used: {self.config.random_seed} (seed)")
        print()

        print("📋 Generated Records by Table:")
        total_records = 0
        for table_name, data in self.generated_data.items():
            count = len(data)
            total_records += count
            print(f"  📁 {table_name.replace('_', ' ').title()}: {count:,} records")

        print(f"\n🎯 Total Records Generated: {total_records:,}")
        print()

        # Data relationships summary
        print("🔗 Data Relationship Summary:")
        if "categories" in self.generated_data:
            root_cats = len(
                [c for c in self.generated_data["categories"] if c["parent_id"] is None]
            )
            sub_cats = len(
                [
                    c
                    for c in self.generated_data["categories"]
                    if c["parent_id"] is not None
                ]
            )
            print(f"  🏷️  Categories: {root_cats} root, {sub_cats} subcategories")

        if "products" in self.generated_data:
            in_stock = len(
                [p for p in self.generated_data["products"] if p["in_stock"]]
            )
            out_of_stock = len(self.generated_data["products"]) - in_stock
            print(f"  📦 Products: {in_stock} in stock, {out_of_stock} out of stock")

        if "invoices" in self.generated_data and "invoice_items" in self.generated_data:
            avg_items = len(self.generated_data["invoice_items"]) / len(
                self.generated_data["invoices"]
            )
            print(f"  🧾 Invoices: Average {avg_items:.1f} items per invoice")

        if "payments" in self.generated_data:
            successful_payments = len(
                [p for p in self.generated_data["payments"] if p["status"] == "SUCCESS"]
            )
            success_rate = (
                successful_payments / len(self.generated_data["payments"])
            ) * 100
            print(f"  💳 Payments: {success_rate:.1f}% success rate")

        print()
        print("📁 Output Files:")
        # Check organized CSV directory
        csv_dir = self.file_organizer.get_csv_directory()
        if csv_dir.exists():
            for csv_file in csv_dir.glob("*.csv"):
                file_size = csv_file.stat().st_size
                size_mb = file_size / (1024 * 1024)
                print(f"  📄 csv/{csv_file.name}: {size_mb:.2f} MB")

        # Check SQL directory if it exists
        sql_dir = self.file_organizer.get_sql_directory()
        if sql_dir.exists() and any(sql_dir.glob("*.sql")):
            for sql_file in sql_dir.glob("*.sql"):
                file_size = sql_file.stat().st_size
                size_mb = file_size / (1024 * 1024)
                print(f"  🗂️  sql/{sql_file.name}: {size_mb:.2f} MB")

        print()
        print("✅ Data generation completed successfully!")
        print("💡 Files are ready for import into practice-software-testing database")
        print("🔍 Review the generated report.md for detailed field specifications")


def main(config: Optional[GenerationConfig] = None) -> None:
    """Main entry point for data generation."""
    orchestrator = DataGenerationOrchestrator(config)
    orchestrator.generate_all_data()


if __name__ == "__main__":
    main()
