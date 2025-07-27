"""
SQL Generator Utility for Faker Data Generator

This module generates SQL INSERT statements from CSV data,
providing database-ready scripts for data import.

Features:
- Generates proper SQL INSERT statements
- Handles NULL values correctly
- Escapes special characters
- Supports MySQL/PostgreSQL/SQLite syntax
- Validates data types
- Includes transaction wrapping
- Batch processing for large datasets

@author Software Testing Team
@version 1.0.0
"""

import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


class SQLGenerator:
    """Generates SQL INSERT scripts from CSV data."""

    # Database-specific configurations
    DB_CONFIGS = {
        "mysql": {
            "quote": "`",
            "string_quote": "'",
            "null_value": "NULL",
            "date_format": "%Y-%m-%d %H:%M:%S",
            "batch_size": 100,
            "supports_on_duplicate": True,
        },
        "postgresql": {
            "quote": '"',
            "string_quote": "'",
            "null_value": "NULL",
            "date_format": "%Y-%m-%d %H:%M:%S",
            "batch_size": 100,
            "supports_on_duplicate": False,
        },
        "sqlite": {
            "quote": "`",
            "string_quote": "'",
            "null_value": "NULL",
            "date_format": "%Y-%m-%d %H:%M:%S",
            "batch_size": 100,
            "supports_on_duplicate": False,
        },
    }

    # SQL data type mappings
    SQL_TYPES = {
        "id": "VARCHAR",
        "name": "VARCHAR",
        "slug": "VARCHAR",
        "parent_id": "VARCHAR",
        "created_at": "TIMESTAMP",
        "updated_at": "TIMESTAMP",
        "price": "DECIMAL",
        "quantity": "INT",
        "enabled": "BOOLEAN",
        "email": "VARCHAR",
        # Add more mappings as needed
    }

    def __init__(self, db_type: str = "mysql"):
        """Initialize SQL generator with database type."""
        if db_type not in self.DB_CONFIGS:
            raise ValueError(f"Unsupported database type: {db_type}")

        self.db_type = db_type
        self.config = self.DB_CONFIGS[db_type]

    def generate_insert_script(
        self,
        data: List[Dict[str, Any]],
        table_name: str,
        *,
        batch_size: Optional[int] = None,
        include_transactions: bool = True,
        include_comments: bool = True,
        on_duplicate_update: bool = False,
    ) -> str:
        """
        Generate SQL INSERT script from data.

        Args:
            data: List of dictionaries containing row data
            table_name: Target table name
            batch_size: Number of rows per INSERT statement
            include_transactions: Whether to wrap in transaction
            include_comments: Whether to include descriptive comments
            on_duplicate_update: Whether to include ON DUPLICATE KEY UPDATE

        Returns:
            Complete SQL INSERT script as string
        """
        if not data:
            raise ValueError("Data must be a non-empty list")

        batch_size = batch_size or self.config["batch_size"]
        headers = list(data[0].keys())

        script_parts = []

        # Add header comment
        if include_comments:
            script_parts.append(self._generate_header_comment(table_name, len(data)))

        # Add transaction start
        if include_transactions:
            script_parts.append("START TRANSACTION;\n")

        # Generate batched INSERT statements
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            insert_stmt = self._generate_batch_insert(
                batch, table_name, headers, on_duplicate_update
            )
            script_parts.append(insert_stmt)

        # Add transaction commit
        if include_transactions:
            script_parts.append("COMMIT;\n")

        # Add footer comment
        if include_comments:
            script_parts.append(self._generate_footer_comment(len(data)))

        return "\n".join(script_parts)

    def generate_from_csv(
        self,
        csv_file_path: Union[str, Path],
        table_name: str,
        **kwargs,
    ) -> str:
        """
        Generate SQL script from CSV file.

        Args:
            csv_file_path: Path to CSV file
            table_name: Target table name
            **kwargs: Additional options for generate_insert_script

        Returns:
            Complete SQL INSERT script as string
        """
        csv_path = Path(csv_file_path)

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        # Read CSV data
        data = []
        with open(csv_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Clean up the row data
                cleaned_row = {}
                for key, value in row.items():
                    # Remove any quotes from headers
                    clean_key = key.strip().strip('"')
                    # Clean up values
                    clean_value = value.strip().strip('"') if value else ""
                    cleaned_row[clean_key] = clean_value
                data.append(cleaned_row)

        if not data:
            raise ValueError("CSV file contains no data rows")

        return self.generate_insert_script(data, table_name, **kwargs)

    def write_sql_file(
        self,
        sql_script: str,
        output_path: Union[str, Path],
    ) -> Path:
        """
        Write SQL script to file.

        Args:
            sql_script: The SQL script content
            output_path: Output file path

        Returns:
            Path to the written file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(sql_script)

        # Log file statistics
        file_size = output_file.stat().st_size
        line_count = sql_script.count("\n") + 1

        print(f"💾 SQL script saved to: {output_file}")
        print(f"📊 File size: {file_size / 1024:.2f} KB")
        print(f"📋 Lines: {line_count}")

        return output_file

    def _generate_header_comment(self, table_name: str, record_count: int) -> str:
        """Generate script header with metadata."""
        timestamp = datetime.now().isoformat()

        return f"""-- ============================================================
-- SQL INSERT Script for {table_name} table
-- ============================================================
-- Generated: {timestamp}
-- Database: {self.db_type.upper()}
-- Records: {record_count}
-- Generator: Faker Data Generator v2.0
-- ============================================================
"""

    def _generate_footer_comment(self, record_count: int) -> str:
        """Generate script footer."""
        return f"""-- ============================================================
-- Script completed successfully
-- Total records inserted: {record_count}
-- ============================================================"""

    def _generate_batch_insert(
        self,
        batch: List[Dict[str, Any]],
        table_name: str,
        headers: List[str],
        on_duplicate_update: bool,
    ) -> str:
        """Generate batched INSERT statement."""
        quote = self.config["quote"]

        # Quote table and column names
        quoted_table = f"{quote}{table_name}{quote}"
        quoted_headers = [f"{quote}{header}{quote}" for header in headers]

        sql_parts = [
            f"INSERT INTO {quoted_table} ({', '.join(quoted_headers)})",
            "VALUES",
        ]

        # Generate values for each row
        value_rows = []
        for row in batch:
            values = [
                self._format_value(row.get(header, ""), header) for header in headers
            ]
            value_rows.append(f"  ({', '.join(values)})")

        sql_parts.append(",\n".join(value_rows))

        # Add ON DUPLICATE KEY UPDATE for MySQL if requested
        if (
            on_duplicate_update
            and self.config["supports_on_duplicate"]
            and self.db_type == "mysql"
        ):
            sql_parts.append(self._generate_on_duplicate_update(headers))

        sql_parts.append(";\n")

        return "\n".join(sql_parts)

    def _format_value(self, value: Any, column_name: str) -> str:
        """Format value according to SQL type and database requirements."""
        string_quote = self.config["string_quote"]
        null_value = self.config["null_value"]

        # Handle null/empty values
        if value is None or value == "":
            return null_value

        # Convert to string for processing
        str_value = str(value).strip()

        if str_value == "":
            return null_value

        # Handle different data types based on column name
        if self._is_timestamp_column(column_name):
            return self._format_timestamp(str_value)
        elif self._is_numeric_column(column_name):
            try:
                return self._format_numeric(str_value)
            except ValueError as e:
                # Fallback to string if numeric parsing fails
                # This can happen if column detection is incorrect
                print(
                    f"Warning: Column '{column_name}' detected as numeric but contains non-numeric value '{str_value}'. Treating as string."
                )
                return self._format_string(str_value)
        elif self._is_boolean_column(column_name):
            return self._format_boolean(str_value)
        else:
            return self._format_string(str_value)

    def _is_timestamp_column(self, column_name: str) -> bool:
        """Check if column is a timestamp type."""
        return "_at" in column_name or "date" in column_name or column_name == "dob"

    def _is_numeric_column(self, column_name: str) -> bool:
        """Check if column is numeric type."""
        # Define explicit numeric columns to avoid false positives
        numeric_columns = {
            "price",
            "quantity",
            "stock",
            "failed_login_attempts",
            "amount",
            "total",
            "count",
            "number",
            "value",
            "weight",
            "size",
        }

        # Check exact matches first
        if column_name.lower() in numeric_columns:
            return True

        # Check for numeric suffixes/prefixes but exclude obvious string fields
        excluded_patterns = {
            "id",
            "code",
            "slug",
            "name",
            "title",
            "description",
            "email",
            "phone",
            "address",
            "street",
            "city",
            "state",
            "country",
            "postal_code",
            "provider",
            "uid",
            "secret",
            "file_name",
            "by_name",
            "by_url",
            "source_name",
            "source_url",
        }

        # If it's in excluded patterns, it's definitely not numeric
        if any(pattern in column_name.lower() for pattern in excluded_patterns):
            return False

        # Check for numeric patterns in column name
        return (
            "count" in column_name.lower()
            or "amount" in column_name.lower()
            or "total" in column_name.lower()
            or "price" in column_name.lower()
            or "quantity" in column_name.lower()
        )

    def _is_boolean_column(self, column_name: str) -> bool:
        """Check if column is boolean type."""
        boolean_columns = {
            "enabled",
            "is_rental",
            "is_location_offer",
            "totp_enabled",
            "totp_verified",
            "in_stock",
        }
        return (
            column_name in boolean_columns
            or column_name.startswith("is_")
            or column_name.startswith("has_")
            or column_name.endswith("_enabled")
            or column_name.endswith("_verified")
        )

    def _format_timestamp(self, value: str) -> str:
        """Format timestamp value."""
        # Handle empty/null timestamp values
        if not value or value.strip() == "":
            return self.config["null_value"]

        try:
            # Try to parse the timestamp
            if "T" in value:
                # ISO format
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            elif "+" in value and ":" in value.split("+")[-1]:
                # Format like: 2025-07-20 08:02:14.961422+00:00
                # Remove timezone part and microseconds for simpler SQL
                clean_value = value.split("+")[0].split(".")[0]
                dt = datetime.strptime(clean_value, "%Y-%m-%d %H:%M:%S")
            else:
                # Try various common formats
                for fmt in [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d",
                    "%Y-%m-%d %H:%M:%S.%f",
                ]:
                    try:
                        dt = datetime.strptime(value, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError(f"No matching format found for: {value}")

            formatted_date = dt.strftime(self.config["date_format"])
            return f"{self.config['string_quote']}{formatted_date}{self.config['string_quote']}"
        except ValueError as e:
            raise ValueError(f"Invalid timestamp format: {value} - {e}")

    def _format_numeric(self, value: str) -> str:
        """Format numeric value."""
        try:
            # Try to parse as float first
            num_value = float(value)
            # If it's a whole number, format as int
            if num_value.is_integer():
                return str(int(num_value))
            else:
                return str(num_value)
        except ValueError:
            # This should not happen if column detection is working properly
            raise ValueError(
                f"Invalid numeric value: {value} (expected number, got string). "
                f"This suggests a column type detection error."
            )

    def _format_boolean(self, value: str) -> str:
        """Format boolean value."""
        lower_value = value.lower()
        if lower_value in ("true", "1", "yes", "on"):
            return "TRUE" if self.db_type == "postgresql" else "1"
        elif lower_value in ("false", "0", "no", "off"):
            return "FALSE" if self.db_type == "postgresql" else "0"
        else:
            raise ValueError(f"Invalid boolean value: {value}")

    def _format_string(self, value: str) -> str:
        """Format string value with proper escaping."""
        # Escape single quotes by doubling them
        escaped_value = value.replace("'", "''")
        return (
            f"{self.config['string_quote']}{escaped_value}{self.config['string_quote']}"
        )

    def _generate_on_duplicate_update(self, headers: List[str]) -> str:
        """Generate ON DUPLICATE KEY UPDATE clause for MySQL."""
        quote = self.config["quote"]

        # Exclude id and created_at from updates
        update_columns = [
            header for header in headers if header not in ("id", "created_at")
        ]

        if not update_columns:
            return ""

        update_clauses = [
            f"{quote}{col}{quote} = VALUES({quote}{col}{quote})"
            for col in update_columns
        ]

        return f"ON DUPLICATE KEY UPDATE\n  {',\n  '.join(update_clauses)}"


def create_sql_generator(db_type: str = "mysql") -> SQLGenerator:
    """Factory function to create SQL generator instance."""
    return SQLGenerator(db_type)
