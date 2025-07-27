"""
Data Validation System for E-commerce Data Generator

This module provides comprehensive validation for generated CSV data,
ensuring foreign key consistency and data integrity across all tables.

Features:
- Foreign key constraint validation
- Data type consistency checks
- Business logic validation
- ULID format validation
- Email format validation
- Price and quantity range validation
- Duplicate detection
- Comprehensive error reporting

@author Software Testing Team
@version 1.0.0
"""

import csv
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from decimal import Decimal, InvalidOperation
from datetime import datetime


class ValidationError:
    """Represents a validation error with context."""

    def __init__(
        self,
        error_type: str,
        table: str,
        row_id: str,
        field: str,
        message: str,
        row_number: int = None,
    ):
        self.error_type = error_type
        self.table = table
        self.row_id = row_id
        self.field = field
        self.message = message
        self.row_number = row_number

    def __str__(self) -> str:
        row_info = f" (row {self.row_number})" if self.row_number else ""
        return f"[{self.error_type}] {self.table}.{self.field}: {self.message} (ID: {self.row_id}){row_info}"


class DataValidator:
    """Comprehensive data validator for e-commerce CSV data."""

    # ULID format regex
    ULID_PATTERN = re.compile(r"^[0-9A-HJKMNP-TV-Z]{26}$")

    # Email format regex (basic)
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    # Foreign key relationships
    FOREIGN_KEY_CONSTRAINTS = {
        "products": {
            "category_id": "categories",
            "brand_id": "brands",
            "product_image_id": "product_images",
        },
        "favorites": {"user_id": "users", "product_id": "products"},
        "invoices": {"user_id": "users"},
        "invoice_items": {"invoice_id": "invoices", "product_id": "products"},
        "payments": {"invoice_id": "invoices"},
        "categories": {"parent_id": "categories"},  # Self-referencing
    }

    # Required fields for each table
    REQUIRED_FIELDS = {
        "users": [
            "id",
            "first_name",
            "last_name",
            "email",
            "role",
            "created_at",
            "updated_at",
        ],
        "categories": ["id", "name", "slug", "created_at", "updated_at"],
        "brands": ["id", "name", "slug", "created_at", "updated_at"],
        "product_images": [
            "id",
            "by_name",
            "by_url",
            "source_name",
            "source_url",
            "file_name",
            "title",
            "created_at",
            "updated_at",
        ],
        "products": [
            "id",
            "name",
            "description",
            "price",
            "category_id",
            "brand_id",
            "product_image_id",
            "created_at",
            "updated_at",
        ],
        "favorites": ["id", "user_id", "product_id", "created_at", "updated_at"],
        "invoices": [
            "id",
            "invoice_number",
            "invoice_date",
            "billing_address",
            "billing_city",
            "billing_country",
            "user_id",
            "total",
            "created_at",
            "updated_at",
        ],
        "invoice_items": [
            "id",
            "invoice_id",
            "product_id",
            "quantity",
            "unit_price",
            "created_at",
            "updated_at",
        ],
        "payments": [
            "id",
            "invoice_id",
            "method",
            "status",
            "created_at",
            "updated_at",
        ],
    }

    # Valid enum values
    VALID_ENUMS = {
        "user_role": ["customer", "admin", "manager", "sales_rep", "warehouse_staff"],
        "payment_method": [
            "CREDIT_CARD",
            "BANK_TRANSFER",
            "CASH_ON_DELIVERY",
            "BUY_NOW_PAY_LATER",
        ],
        "payment_status": ["PENDING", "SUCCESS", "FAILED"],
    }

    def __init__(self, csv_directory: Path):
        """Initialize validator with CSV directory path."""
        self.csv_directory = Path(csv_directory)
        self.data_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.id_sets: Dict[str, Set[str]] = {}
        self.errors: List[ValidationError] = []

    def validate_all_data(self) -> Tuple[bool, List[ValidationError]]:
        """
        Validate all CSV data for consistency and integrity.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        print("🔍 Starting comprehensive data validation...")

        # Clear previous validation results
        self.errors.clear()
        self.data_cache.clear()
        self.id_sets.clear()

        # Load all CSV data
        self._load_all_csv_data()

        # Perform validations
        self._validate_file_existence()
        self._validate_data_structure()
        self._validate_required_fields()
        self._validate_data_types()
        self._validate_foreign_keys()
        self._validate_business_logic()
        self._validate_duplicates()

        # Report results
        is_valid = len(self.errors) == 0
        self._print_validation_summary(is_valid)

        return is_valid, self.errors

    def _load_all_csv_data(self) -> None:
        """Load all CSV files into memory for validation."""
        print("  📁 Loading CSV files...")

        expected_files = [
            "users.csv",
            "categories.csv",
            "brands.csv",
            "product_images.csv",
            "products.csv",
            "favorites.csv",
            "invoices.csv",
            "invoice_items.csv",
            "payments.csv",
        ]

        for filename in expected_files:
            table_name = filename.replace(".csv", "")
            filepath = self.csv_directory / filename

            if filepath.exists():
                try:
                    self.data_cache[table_name] = self._load_csv_file(filepath)
                    self.id_sets[table_name] = {
                        row["id"] for row in self.data_cache[table_name]
                    }
                    print(
                        f"    ✅ Loaded {table_name}: {len(self.data_cache[table_name])} records"
                    )
                except Exception as e:
                    self._add_error(
                        "FILE_ERROR",
                        table_name,
                        "N/A",
                        "file",
                        f"Failed to load CSV: {str(e)}",
                    )
            else:
                self._add_error(
                    "MISSING_FILE",
                    table_name,
                    "N/A",
                    "file",
                    f"Required file not found: {filename}",
                )

    def _load_csv_file(self, filepath: Path) -> List[Dict[str, Any]]:
        """Load a single CSV file and return list of dictionaries."""
        data = []
        with open(filepath, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(
                reader, start=2
            ):  # Start from 2 (header is row 1)
                # Store row number for error reporting
                row["_row_number"] = row_num
                data.append(row)
        return data

    def _validate_file_existence(self) -> None:
        """Validate that all required CSV files exist."""
        print("  🗂️  Validating file existence...")

        required_files = [
            "users.csv",
            "categories.csv",
            "brands.csv",
            "product_images.csv",
            "products.csv",
            "favorites.csv",
            "invoices.csv",
            "invoice_items.csv",
            "payments.csv",
        ]

        for filename in required_files:
            table_name = filename.replace(".csv", "")
            if table_name not in self.data_cache:
                self._add_error(
                    "MISSING_FILE",
                    table_name,
                    "N/A",
                    "file",
                    f"Required CSV file missing: {filename}",
                )

    def _validate_data_structure(self) -> None:
        """Validate basic data structure and format."""
        print("  🏗️  Validating data structure...")

        for table_name, data in self.data_cache.items():
            if not data:
                self._add_error(
                    "EMPTY_TABLE", table_name, "N/A", "data", "Table contains no data"
                )
                continue

            # Check if all rows have consistent columns
            expected_columns = set(data[0].keys()) - {"_row_number"}
            for row in data:
                actual_columns = set(row.keys()) - {"_row_number"}
                if actual_columns != expected_columns:
                    self._add_error(
                        "INCONSISTENT_COLUMNS",
                        table_name,
                        row.get("id", "N/A"),
                        "structure",
                        f"Row has different columns than expected",
                        row.get("_row_number"),
                    )

    def _validate_required_fields(self) -> None:
        """Validate that all required fields are present and not empty."""
        print("  📋 Validating required fields...")

        for table_name, data in self.data_cache.items():
            if table_name not in self.REQUIRED_FIELDS:
                continue

            required_fields = self.REQUIRED_FIELDS[table_name]

            for row in data:
                row_id = row.get("id", "N/A")
                row_number = row.get("_row_number")

                for field in required_fields:
                    if (
                        field not in row
                        or not row[field]
                        or str(row[field]).strip() == ""
                    ):
                        self._add_error(
                            "MISSING_REQUIRED_FIELD",
                            table_name,
                            row_id,
                            field,
                            f"Required field is empty or missing",
                            row_number,
                        )

    def _validate_data_types(self) -> None:
        """Validate data types and formats."""
        print("  🔢 Validating data types and formats...")

        for table_name, data in self.data_cache.items():
            for row in data:
                row_id = row.get("id", "N/A")
                row_number = row.get("_row_number")

                # Validate ULID format for ID fields
                self._validate_ulid_field(table_name, row, "id", row_number)

                # Validate specific field types based on table
                if table_name == "users":
                    self._validate_email_field(table_name, row, "email", row_number)
                    self._validate_enum_field(
                        table_name, row, "role", "user_role", row_number
                    )

                elif table_name == "products":
                    self._validate_price_field(table_name, row, "price", row_number)
                    self._validate_boolean_field(
                        table_name, row, "in_stock", row_number
                    )
                    self._validate_boolean_field(
                        table_name, row, "is_location_offer", row_number
                    )
                    self._validate_boolean_field(
                        table_name, row, "is_rental", row_number
                    )
                    self._validate_integer_field(table_name, row, "stock", row_number)

                elif table_name == "invoice_items":
                    self._validate_integer_field(
                        table_name, row, "quantity", row_number
                    )
                    self._validate_price_field(
                        table_name, row, "unit_price", row_number
                    )

                elif table_name == "invoices":
                    self._validate_price_field(table_name, row, "total", row_number)

                elif table_name == "payments":
                    self._validate_enum_field(
                        table_name, row, "method", "payment_method", row_number
                    )
                    self._validate_enum_field(
                        table_name, row, "status", "payment_status", row_number
                    )

    def _validate_foreign_keys(self) -> None:
        """Validate foreign key constraints."""
        print("  🔗 Validating foreign key constraints...")

        for table_name, constraints in self.FOREIGN_KEY_CONSTRAINTS.items():
            if table_name not in self.data_cache:
                continue

            for row in self.data_cache[table_name]:
                row_id = row.get("id", "N/A")
                row_number = row.get("_row_number")

                for fk_field, referenced_table in constraints.items():
                    fk_value = row.get(fk_field)

                    # Skip validation for optional foreign keys (NULL values)
                    if not fk_value or str(fk_value).strip() == "":
                        # Check if this field allows NULL
                        if table_name == "categories" and fk_field == "parent_id":
                            continue  # parent_id can be NULL for root categories
                        elif table_name == "users" and fk_field in ["uid", "provider"]:
                            continue  # These can be NULL
                        else:
                            self._add_error(
                                "NULL_FOREIGN_KEY",
                                table_name,
                                row_id,
                                fk_field,
                                f"Foreign key cannot be NULL",
                                row_number,
                            )
                        continue

                    # Check if referenced ID exists
                    if referenced_table not in self.id_sets:
                        self._add_error(
                            "MISSING_REFERENCE_TABLE",
                            table_name,
                            row_id,
                            fk_field,
                            f"Referenced table '{referenced_table}' not found",
                            row_number,
                        )
                        continue

                    if fk_value not in self.id_sets[referenced_table]:
                        self._add_error(
                            "BROKEN_FOREIGN_KEY",
                            table_name,
                            row_id,
                            fk_field,
                            f"Referenced ID '{fk_value}' not found in table '{referenced_table}'",
                            row_number,
                        )

    def _validate_business_logic(self) -> None:
        """Validate business logic rules."""
        print("  💼 Validating business logic...")

        # Validate invoice totals match sum of invoice items
        self._validate_invoice_totals()

        # Validate unique constraints
        self._validate_unique_constraints()

        # Validate category hierarchy
        self._validate_category_hierarchy()

    def _validate_invoice_totals(self) -> None:
        """Validate that invoice totals match the sum of their items."""
        if "invoices" not in self.data_cache or "invoice_items" not in self.data_cache:
            return

        # Calculate totals for each invoice from items
        calculated_totals = {}
        for item in self.data_cache["invoice_items"]:
            invoice_id = item.get("invoice_id")
            quantity = int(item.get("quantity", 0))
            unit_price = Decimal(str(item.get("unit_price", "0")))
            item_total = quantity * unit_price

            if invoice_id not in calculated_totals:
                calculated_totals[invoice_id] = Decimal("0")
            calculated_totals[invoice_id] += item_total

        # Compare with recorded totals
        for invoice in self.data_cache["invoices"]:
            invoice_id = invoice.get("id")
            recorded_total = Decimal(str(invoice.get("total", "0")))
            calculated_total = calculated_totals.get(invoice_id, Decimal("0"))

            if abs(recorded_total - calculated_total) > Decimal(
                "0.01"
            ):  # Allow small rounding differences
                self._add_error(
                    "INVOICE_TOTAL_MISMATCH",
                    "invoices",
                    invoice_id,
                    "total",
                    f"Recorded total {recorded_total} doesn't match calculated total {calculated_total}",
                    invoice.get("_row_number"),
                )

    def _validate_unique_constraints(self) -> None:
        """Validate unique constraints."""
        # Email uniqueness in users
        if "users" in self.data_cache:
            emails = {}
            for user in self.data_cache["users"]:
                email = user.get("email", "").lower()
                if email in emails:
                    self._add_error(
                        "DUPLICATE_EMAIL",
                        "users",
                        user.get("id"),
                        "email",
                        f"Duplicate email: {email}",
                        user.get("_row_number"),
                    )
                else:
                    emails[email] = user.get("id")

        # Slug uniqueness in categories and brands
        for table_name in ["categories", "brands"]:
            if table_name in self.data_cache:
                slugs = {}
                for row in self.data_cache[table_name]:
                    slug = row.get("slug", "")
                    if slug in slugs:
                        self._add_error(
                            "DUPLICATE_SLUG",
                            table_name,
                            row.get("id"),
                            "slug",
                            f"Duplicate slug: {slug}",
                            row.get("_row_number"),
                        )
                    else:
                        slugs[slug] = row.get("id")

    def _validate_category_hierarchy(self) -> None:
        """Validate category hierarchy to prevent circular references."""
        if "categories" not in self.data_cache:
            return

        for category in self.data_cache["categories"]:
            cat_id = category.get("id")
            parent_id = category.get("parent_id")

            if parent_id and parent_id == cat_id:
                self._add_error(
                    "CIRCULAR_REFERENCE",
                    "categories",
                    cat_id,
                    "parent_id",
                    "Category cannot be its own parent",
                    category.get("_row_number"),
                )

    def _validate_duplicates(self) -> None:
        """Validate for duplicate IDs and other constraints."""
        print("  🔍 Checking for duplicates...")

        for table_name, data in self.data_cache.items():
            seen_ids = set()
            for row in data:
                row_id = row.get("id")
                if row_id in seen_ids:
                    self._add_error(
                        "DUPLICATE_ID",
                        table_name,
                        row_id,
                        "id",
                        f"Duplicate ID found",
                        row.get("_row_number"),
                    )
                else:
                    seen_ids.add(row_id)

    def _validate_ulid_field(
        self, table_name: str, row: Dict, field: str, row_number: int
    ) -> None:
        """Validate ULID format."""
        value = row.get(field, "")
        if value and not self.ULID_PATTERN.match(str(value)):
            self._add_error(
                "INVALID_ULID",
                table_name,
                row.get("id", "N/A"),
                field,
                f"Invalid ULID format: {value}",
                row_number,
            )

    def _validate_email_field(
        self, table_name: str, row: Dict, field: str, row_number: int
    ) -> None:
        """Validate email format."""
        value = row.get(field, "")
        if value and not self.EMAIL_PATTERN.match(str(value)):
            self._add_error(
                "INVALID_EMAIL",
                table_name,
                row.get("id", "N/A"),
                field,
                f"Invalid email format: {value}",
                row_number,
            )

    def _validate_enum_field(
        self, table_name: str, row: Dict, field: str, enum_type: str, row_number: int
    ) -> None:
        """Validate enum field values."""
        value = row.get(field, "")
        if value and str(value) not in self.VALID_ENUMS.get(enum_type, []):
            self._add_error(
                "INVALID_ENUM",
                table_name,
                row.get("id", "N/A"),
                field,
                f"Invalid {enum_type} value: {value}",
                row_number,
            )

    def _validate_price_field(
        self, table_name: str, row: Dict, field: str, row_number: int
    ) -> None:
        """Validate price field (decimal format and range)."""
        value = row.get(field, "")
        if value:
            try:
                price = Decimal(str(value))
                if price < 0:
                    self._add_error(
                        "NEGATIVE_PRICE",
                        table_name,
                        row.get("id", "N/A"),
                        field,
                        f"Price cannot be negative: {price}",
                        row_number,
                    )
                elif price > Decimal("999999.99"):
                    self._add_error(
                        "PRICE_TOO_HIGH",
                        table_name,
                        row.get("id", "N/A"),
                        field,
                        f"Price too high: {price}",
                        row_number,
                    )
            except (InvalidOperation, ValueError):
                self._add_error(
                    "INVALID_PRICE",
                    table_name,
                    row.get("id", "N/A"),
                    field,
                    f"Invalid price format: {value}",
                    row_number,
                )

    def _validate_boolean_field(
        self, table_name: str, row: Dict, field: str, row_number: int
    ) -> None:
        """Validate boolean field values."""
        value = row.get(field, "")
        if value and str(value).lower() not in ["true", "false", "1", "0"]:
            self._add_error(
                "INVALID_BOOLEAN",
                table_name,
                row.get("id", "N/A"),
                field,
                f"Invalid boolean value: {value}",
                row_number,
            )

    def _validate_integer_field(
        self, table_name: str, row: Dict, field: str, row_number: int
    ) -> None:
        """Validate integer field values."""
        value = row.get(field, "")
        if value:
            try:
                int_value = int(value)
                if int_value < 0:
                    self._add_error(
                        "NEGATIVE_INTEGER",
                        table_name,
                        row.get("id", "N/A"),
                        field,
                        f"Integer cannot be negative: {int_value}",
                        row_number,
                    )
            except (ValueError, TypeError):
                self._add_error(
                    "INVALID_INTEGER",
                    table_name,
                    row.get("id", "N/A"),
                    field,
                    f"Invalid integer format: {value}",
                    row_number,
                )

    def _add_error(
        self,
        error_type: str,
        table: str,
        row_id: str,
        field: str,
        message: str,
        row_number: int = None,
    ) -> None:
        """Add a validation error to the error list."""
        error = ValidationError(error_type, table, row_id, field, message, row_number)
        self.errors.append(error)

    def _print_validation_summary(self, is_valid: bool) -> None:
        """Print validation summary."""
        print()
        if is_valid:
            print("✅ Data validation completed successfully!")
            print("🎯 All foreign key constraints are satisfied")
            print("📊 All data integrity checks passed")
            print("🔒 No business logic violations found")
        else:
            print("❌ Data validation failed!")
            print(f"🚨 Found {len(self.errors)} validation errors:")
            print()

            # Group errors by type
            error_types = {}
            for error in self.errors:
                if error.error_type not in error_types:
                    error_types[error.error_type] = []
                error_types[error.error_type].append(error)

            for error_type, errors in error_types.items():
                print(f"  🔴 {error_type} ({len(errors)} errors):")
                for error in errors[:5]:  # Show first 5 errors of each type
                    print(f"     {error}")
                if len(errors) > 5:
                    print(f"     ... and {len(errors) - 5} more")
                print()

            print(
                "❗ Data generation pipeline will be halted due to validation failures"
            )
            print("💡 Please review the errors above and regenerate the data")


def validate_generated_data(csv_directory: Path) -> Tuple[bool, List[ValidationError]]:
    """
    Convenience function to validate generated CSV data.

    Args:
        csv_directory: Path to directory containing CSV files

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    validator = DataValidator(csv_directory)
    return validator.validate_all_data()


if __name__ == "__main__":
    # Example usage for testing
    import sys

    if len(sys.argv) > 1:
        csv_dir = Path(sys.argv[1])
        is_valid, errors = validate_generated_data(csv_dir)
        if not is_valid:
            sys.exit(1)
    else:
        print("Usage: python data_validator.py <csv_directory>")
        sys.exit(1)
