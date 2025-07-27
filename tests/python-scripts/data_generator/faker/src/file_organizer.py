"""
File Organization Utility for Data Generator

This module handles the organization of output files into structured directories:
- CSV files go to output/csv/
- SQL files go to output/sql/
- Reports go to output/reports/

Features:
- Automatic directory creation
- File moving and copying
- Clean directory structure
- Backup functionality
- Error handling

@author Software Testing Team
@version 1.0.0
"""

import shutil
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class FileOrganizer:
    """Organizes output files into structured directories."""

    def __init__(self, base_output_dir: Path):
        """Initialize the file organizer."""
        self.base_output_dir = Path(base_output_dir)
        self.csv_dir = self.base_output_dir / "csv"
        self.sql_dir = self.base_output_dir / "sql"
        self.reports_dir = self.base_output_dir / "reports"

        # Create directories
        self._create_directories()

    def _create_directories(self) -> None:
        """Create the organized directory structure."""
        directories = [
            self.base_output_dir,
            self.csv_dir,
            self.sql_dir,
            self.reports_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def organize_csv_files(self, source_dir: Path = None) -> List[Path]:
        """
        Move CSV files from source directory to organized CSV directory.

        Args:
            source_dir: Source directory (defaults to base_output_dir)

        Returns:
            List of moved file paths
        """
        if source_dir is None:
            source_dir = self.base_output_dir

        source_dir = Path(source_dir)
        moved_files = []

        # Find all CSV files in source directory (not in subdirectories)
        csv_files = [f for f in source_dir.glob("*.csv") if f.is_file()]

        if not csv_files:
            return moved_files

        print(f"📁 Organizing {len(csv_files)} CSV files...")

        for csv_file in csv_files:
            destination = self.csv_dir / csv_file.name

            try:
                # Move file to CSV directory
                if destination.exists():
                    # Create backup if file exists
                    backup_name = f"{csv_file.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    backup_path = self.csv_dir / backup_name
                    shutil.move(str(destination), str(backup_path))
                    print(f"  📦 Created backup: {backup_name}")

                shutil.move(str(csv_file), str(destination))
                moved_files.append(destination)
                print(f"  ✅ Moved: {csv_file.name} → csv/{csv_file.name}")

            except Exception as e:
                print(f"  ❌ Failed to move {csv_file.name}: {str(e)}")

        return moved_files

    def organize_sql_files(self, source_dir: Path = None) -> List[Path]:
        """
        Move SQL files from source directory to organized SQL directory.

        Args:
            source_dir: Source directory (defaults to base_output_dir)

        Returns:
            List of moved file paths
        """
        if source_dir is None:
            source_dir = self.base_output_dir

        source_dir = Path(source_dir)
        moved_files = []

        # Find all SQL files in source directory (not in subdirectories)
        sql_files = [f for f in source_dir.glob("*.sql") if f.is_file()]

        if not sql_files:
            return moved_files

        print(f"🗂️  Organizing {len(sql_files)} SQL files...")

        for sql_file in sql_files:
            destination = self.sql_dir / sql_file.name

            try:
                # Move file to SQL directory
                if destination.exists():
                    # Create backup if file exists
                    backup_name = f"{sql_file.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
                    backup_path = self.sql_dir / backup_name
                    shutil.move(str(destination), str(backup_path))
                    print(f"  📦 Created backup: {backup_name}")

                shutil.move(str(sql_file), str(destination))
                moved_files.append(destination)
                print(f"  ✅ Moved: {sql_file.name} → sql/{sql_file.name}")

            except Exception as e:
                print(f"  ❌ Failed to move {sql_file.name}: {str(e)}")

        return moved_files

    def organize_report_files(self, source_dir: Path = None) -> List[Path]:
        """
        Move report files (.md, .txt, .html) to organized reports directory.

        Args:
            source_dir: Source directory (defaults to base_output_dir)

        Returns:
            List of moved file paths
        """
        if source_dir is None:
            source_dir = self.base_output_dir

        source_dir = Path(source_dir)
        moved_files = []

        # Find all report files in source directory
        report_extensions = ["*.md", "*.txt", "*.html", "*.json"]
        report_files = []
        for pattern in report_extensions:
            report_files.extend([f for f in source_dir.glob(pattern) if f.is_file()])

        if not report_files:
            return moved_files

        print(f"📊 Organizing {len(report_files)} report files...")

        for report_file in report_files:
            destination = self.reports_dir / report_file.name

            try:
                # Move file to reports directory
                if destination.exists():
                    # Create backup if file exists
                    backup_name = f"{report_file.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{report_file.suffix}"
                    backup_path = self.reports_dir / backup_name
                    shutil.move(str(destination), str(backup_path))
                    print(f"  📦 Created backup: {backup_name}")

                shutil.move(str(report_file), str(destination))
                moved_files.append(destination)
                print(f"  ✅ Moved: {report_file.name} → reports/{report_file.name}")

            except Exception as e:
                print(f"  ❌ Failed to move {report_file.name}: {str(e)}")

        return moved_files

    def organize_all_files(self, source_dir: Path = None) -> Dict[str, List[Path]]:
        """
        Organize all files into their respective directories.

        Args:
            source_dir: Source directory (defaults to base_output_dir)

        Returns:
            Dictionary with moved files by category
        """
        print("🗂️  Starting file organization...")

        result = {
            "csv": self.organize_csv_files(source_dir),
            "sql": self.organize_sql_files(source_dir),
            "reports": self.organize_report_files(source_dir),
        }

        # Print summary
        total_moved = sum(len(files) for files in result.values())
        if total_moved > 0:
            print(f"\n✅ File organization completed! Moved {total_moved} files:")
            print(f"  📄 CSV files: {len(result['csv'])}")
            print(f"  🗃️  SQL files: {len(result['sql'])}")
            print(f"  📊 Report files: {len(result['reports'])}")
        else:
            print("\n📂 No files to organize")

        return result

    def get_csv_directory(self) -> Path:
        """Get the CSV directory path."""
        return self.csv_dir

    def get_sql_directory(self) -> Path:
        """Get the SQL directory path."""
        return self.sql_dir

    def get_reports_directory(self) -> Path:
        """Get the reports directory path."""
        return self.reports_dir

    def clean_old_backups(
        self, max_backups_per_file: int = 3, max_age_days: int = 7
    ) -> None:
        """
        Clean old backup files to prevent excessive accumulation.

        Args:
            max_backups_per_file: Maximum number of backups to keep per file type
            max_age_days: Maximum age of backups in days
        """
        print(
            f"🗑️  Cleaning old backup files (keeping {max_backups_per_file} recent, max {max_age_days} days old)..."
        )

        cleaned_count = 0
        total_size_cleaned = 0

        # Define backup patterns for each directory
        directories_to_clean = [
            (self.csv_dir, "*_backup_*.csv"),
            (self.sql_dir, "*_backup_*.sql"),
            (self.reports_dir, "*_backup_*"),
        ]

        for directory, pattern in directories_to_clean:
            if not directory.exists():
                continue

            # Group backup files by their base name
            backup_groups = {}

            for backup_file in directory.glob(pattern):
                if not backup_file.is_file():
                    continue

                # Extract base name from backup filename
                # Format: {basename}_backup_{timestamp}.{ext}
                filename = backup_file.name
                if "_backup_" not in filename:
                    continue

                base_name = filename.split("_backup_")[0]
                if base_name not in backup_groups:
                    backup_groups[base_name] = []

                backup_groups[base_name].append(backup_file)

            # Clean each group of backups
            for base_name, backup_files in backup_groups.items():
                # Sort by modification time (newest first)
                backup_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

                # Remove old backups beyond the limit
                files_to_remove = backup_files[max_backups_per_file:]

                # Also remove files older than max_age_days
                cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 3600)

                for backup_file in backup_files:
                    file_age = backup_file.stat().st_mtime

                    # Remove if too old or beyond the count limit
                    if file_age < cutoff_time or backup_file in files_to_remove:
                        try:
                            file_size = backup_file.stat().st_size
                            backup_file.unlink()
                            cleaned_count += 1
                            total_size_cleaned += file_size
                            print(f"    🗑️  Removed {backup_file.name}")
                        except OSError as e:
                            print(f"    ⚠️  Failed to remove {backup_file.name}: {e}")

        if cleaned_count > 0:
            size_mb = total_size_cleaned / (1024 * 1024)
            print(f"✅ Cleaned {cleaned_count} backup files, freed {size_mb:.2f} MB")
        else:
            print("✅ No old backup files to clean")

    def get_backup_statistics(self) -> Dict[str, any]:
        """
        Get statistics about backup files in the output directories.

        Returns:
            Dictionary with backup file statistics
        """
        stats = {
            "total_backups": 0,
            "total_size_mb": 0,
            "by_directory": {},
            "oldest_backup": None,
            "newest_backup": None,
        }

        directories_to_check = [
            ("csv", self.csv_dir, "*_backup_*.csv"),
            ("sql", self.sql_dir, "*_backup_*.sql"),
            ("reports", self.reports_dir, "*_backup_*"),
        ]

        all_backup_times = []

        for dir_name, directory, pattern in directories_to_check:
            if not directory.exists():
                continue

            backup_files = list(directory.glob(pattern))
            dir_stats = {"count": len(backup_files), "size_mb": 0, "files": []}

            for backup_file in backup_files:
                if backup_file.is_file():
                    file_size = backup_file.stat().st_size
                    file_time = backup_file.stat().st_mtime

                    dir_stats["size_mb"] += file_size / (1024 * 1024)
                    dir_stats["files"].append(
                        {
                            "name": backup_file.name,
                            "size_mb": file_size / (1024 * 1024),
                            "modified": datetime.fromtimestamp(file_time).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                    )

                    all_backup_times.append(file_time)

            stats["by_directory"][dir_name] = dir_stats
            stats["total_backups"] += dir_stats["count"]
            stats["total_size_mb"] += dir_stats["size_mb"]

        # Calculate oldest and newest backup times
        if all_backup_times:
            oldest_time = min(all_backup_times)
            newest_time = max(all_backup_times)
            stats["oldest_backup"] = datetime.fromtimestamp(oldest_time).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            stats["newest_backup"] = datetime.fromtimestamp(newest_time).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        return stats

    def print_backup_report(self) -> None:
        """Print a detailed report of backup files."""
        stats = self.get_backup_statistics()

        print("\n📊 BACKUP FILES REPORT")
        print("=" * 50)
        print(f"Total backup files: {stats['total_backups']}")
        print(f"Total size: {stats['total_size_mb']:.2f} MB")

        if stats["oldest_backup"]:
            print(f"Oldest backup: {stats['oldest_backup']}")
        if stats["newest_backup"]:
            print(f"Newest backup: {stats['newest_backup']}")

        print("\nBy Directory:")
        for dir_name, dir_stats in stats["by_directory"].items():
            if dir_stats["count"] > 0:
                print(
                    f"  📁 {dir_name}/: {dir_stats['count']} files, {dir_stats['size_mb']:.2f} MB"
                )

                # Show top 5 largest files
                if dir_stats["files"]:
                    largest_files = sorted(
                        dir_stats["files"], key=lambda x: x["size_mb"], reverse=True
                    )[:5]
                    for file_info in largest_files:
                        print(
                            f"    • {file_info['name']} ({file_info['size_mb']:.2f} MB, {file_info['modified']})"
                        )

        print("=" * 50)

    def clean_empty_directories(self) -> None:
        """Remove empty subdirectories."""
        directories = [self.csv_dir, self.sql_dir, self.reports_dir]

        for directory in directories:
            if directory.exists() and not any(directory.iterdir()):
                try:
                    directory.rmdir()
                    print(f"🗑️  Removed empty directory: {directory.name}")
                except Exception as e:
                    print(f"⚠️  Could not remove directory {directory.name}: {str(e)}")

    def create_directory_structure_info(self) -> None:
        """Create a README file explaining the directory structure."""
        readme_content = """# Data Generator Output Structure

This directory contains the generated data organized into subdirectories:

## 📁 Directory Structure

```
output/
├── csv/                    # Generated CSV data files
│   ├── users.csv
│   ├── categories.csv
│   ├── brands.csv
│   ├── product_images.csv
│   ├── products.csv
│   ├── favorites.csv
│   ├── invoices.csv
│   ├── invoice_items.csv
│   └── payments.csv
├── sql/                    # Generated SQL scripts
│   ├── insert_statements.sql
│   ├── mysql_import.sql
│   └── postgresql_import.sql
└── reports/                # Generation reports and documentation
    ├── data_generation_report.md
    ├── validation_report.json
    └── field_specifications.md
```

## 📄 File Descriptions

### CSV Files
- **users.csv**: User accounts and profile information
- **categories.csv**: Product categories with hierarchical structure
- **brands.csv**: Product brands and manufacturers
- **product_images.csv**: Product image metadata and attributions
- **products.csv**: Product catalog with details and relationships
- **favorites.csv**: User favorite products (many-to-many relationship)
- **invoices.csv**: Order invoices and billing information
- **invoice_items.csv**: Line items for each invoice
- **payments.csv**: Payment transactions and status

### SQL Files
- **insert_statements.sql**: Standard SQL INSERT statements
- **mysql_import.sql**: MySQL-specific import script
- **postgresql_import.sql**: PostgreSQL-specific import script

### Report Files
- **data_generation_report.md**: Comprehensive generation report
- **validation_report.json**: Data validation results
- **field_specifications.md**: Detailed field documentation

## 🔧 Usage

### Import CSV Files
```bash
# Import into MySQL
mysql -u username -p database_name < sql/mysql_import.sql

# Import into PostgreSQL
psql -U username -d database_name -f sql/postgresql_import.sql
```

### Direct CSV Import
Each CSV file can be imported directly into database tables using your preferred method.

## 📊 Data Relationships

The generated data maintains referential integrity with proper foreign key relationships:
- Products → Categories, Brands, Product Images
- Favorites → Users, Products
- Invoices → Users
- Invoice Items → Invoices, Products
- Payments → Invoices

## 🎯 Generated by Practice Software Testing Data Generator v2.0.0
"""

        readme_path = self.base_output_dir / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        print(f"📋 Created directory structure documentation: README.md")


def organize_output_files(base_output_dir: Path) -> FileOrganizer:
    """
    Convenience function to organize output files.

    Args:
        base_output_dir: Base output directory

    Returns:
        FileOrganizer instance
    """
    organizer = FileOrganizer(base_output_dir)
    organizer.organize_all_files()
    organizer.create_directory_structure_info()
    return organizer


if __name__ == "__main__":
    # Example usage for testing
    import sys

    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1])
        organize_output_files(output_dir)
    else:
        print("Usage: python file_organizer.py <output_directory>")
        sys.exit(1)
