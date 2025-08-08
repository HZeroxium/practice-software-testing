#!/usr/bin/env python3
"""
Report Cleaner for Performance Testing

This script manages test results and reports, keeping only the most recent ones
to prevent disk space issues and maintain clean organization.

Author: Performance Testing Automation
Date: 2024
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ReportCleaner:
    """Clean and manage test reports and results"""

    def __init__(self, results_dir: str = "results", keep_recent: int = 1):
        self.results_dir = Path(results_dir)
        self.keep_recent = keep_recent

    def get_test_result_files(self) -> Dict[str, List[Path]]:
        """Get all test result files grouped by test type"""
        test_files = {}

        if not self.results_dir.exists():
            return test_files

        # Group files by test type
        for file_path in self.results_dir.rglob("*"):
            if file_path.is_file():
                # Extract test type from filename
                filename = file_path.name
                if any(
                    test_type in filename for test_type in ["load", "stress", "spike"]
                ):
                    # Determine test type
                    if "load" in filename:
                        test_type = "load"
                    elif "stress" in filename:
                        test_type = "stress"
                    elif "spike" in filename:
                        test_type = "spike"
                    else:
                        continue

                    if test_type not in test_files:
                        test_files[test_type] = []
                    test_files[test_type].append(file_path)

        return test_files

    def get_file_creation_time(self, file_path: Path) -> datetime:
        """Get file creation time"""
        try:
            # Try to get creation time, fallback to modification time
            stat = file_path.stat()
            return datetime.fromtimestamp(stat.st_ctime)
        except Exception:
            return datetime.fromtimestamp(stat.st_mtime)

    def clean_old_results(self) -> Dict[str, int]:
        """Clean old test results, keeping only the most recent ones"""
        cleaned_counts = {}
        test_files = self.get_test_result_files()

        for test_type, files in test_files.items():
            # Sort files by creation time (newest first)
            files.sort(key=lambda x: self.get_file_creation_time(x), reverse=True)

            # Keep only the most recent files
            files_to_keep = files[: self.keep_recent]
            files_to_delete = files[self.keep_recent :]

            # Delete old files
            deleted_count = 0
            for file_path in files_to_delete:
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        deleted_count += 1
                        logger.info(f"Deleted old result file: {file_path}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        deleted_count += 1
                        logger.info(f"Deleted old result directory: {file_path}")
                except Exception as e:
                    logger.error(f"Error deleting {file_path}: {e}")

            cleaned_counts[test_type] = deleted_count
            logger.info(f"Cleaned {deleted_count} old {test_type} test result files")

        return cleaned_counts

    def clean_results_folders(self) -> Dict[str, int]:
        """Clean old result folders, keeping only the most recent ones"""
        cleaned_counts = {}

        if not self.results_dir.exists():
            return cleaned_counts

        # Get all result folders (directories ending with _report or containing .jtl files)
        result_folders = []
        for item in self.results_dir.iterdir():
            if item.is_dir():
                # Check if it's a result folder (contains .jtl files or ends with _report)
                if (
                    item.name.endswith("_report")
                    or any(item.glob("*.jtl"))
                    or any(item.glob("*.log"))
                ):
                    result_folders.append(item)

        if not result_folders:
            return cleaned_counts

        # Sort folders by creation time (newest first)
        result_folders.sort(key=lambda x: self.get_file_creation_time(x), reverse=True)

        # Keep only the most recent folders
        folders_to_keep = result_folders[: self.keep_recent]
        folders_to_delete = result_folders[self.keep_recent :]

        # Delete old folders
        deleted_count = 0
        for folder_path in folders_to_delete:
            try:
                shutil.rmtree(folder_path)
                deleted_count += 1
                logger.info(f"Deleted old result folder: {folder_path}")
            except Exception as e:
                logger.error(f"Error deleting folder {folder_path}: {e}")

        cleaned_counts["folders"] = deleted_count
        logger.info(f"Cleaned {deleted_count} old result folders")

        return cleaned_counts

    def get_results_summary(self) -> Dict[str, Dict]:
        """Get summary of current test results"""
        summary = {}
        test_files = self.get_test_result_files()

        for test_type, files in test_files.items():
            # Sort files by creation time (newest first)
            files.sort(key=lambda x: self.get_file_creation_time(x), reverse=True)

            summary[test_type] = {
                "total_files": len(files),
                "recent_files": [],
                "oldest_file": None,
                "newest_file": None,
            }

            if files:
                summary[test_type]["newest_file"] = {
                    "name": files[0].name,
                    "created": self.get_file_creation_time(files[0]).isoformat(),
                    "size": files[0].stat().st_size,
                }

                summary[test_type]["oldest_file"] = {
                    "name": files[-1].name,
                    "created": self.get_file_creation_time(files[-1]).isoformat(),
                    "size": files[-1].stat().st_size,
                }

                # List recent files
                for file_path in files[: self.keep_recent]:
                    summary[test_type]["recent_files"].append(
                        {
                            "name": file_path.name,
                            "created": self.get_file_creation_time(
                                file_path
                            ).isoformat(),
                            "size": file_path.stat().st_size,
                            "type": "file" if file_path.is_file() else "directory",
                        }
                    )

        return summary

    def cleanup_temp_files(self) -> int:
        """Clean up temporary files and directories"""
        temp_dirs = ["temp", "tmp", "__pycache__"]
        deleted_count = 0

        for temp_dir in temp_dirs:
            temp_path = self.results_dir / temp_dir
            if temp_path.exists():
                try:
                    shutil.rmtree(temp_path)
                    deleted_count += 1
                    logger.info(f"Deleted temporary directory: {temp_path}")
                except Exception as e:
                    logger.error(f"Error deleting temporary directory {temp_path}: {e}")

        return deleted_count

    def get_disk_usage(self) -> Dict[str, int]:
        """Get disk usage information"""
        usage = {"total_size": 0, "file_count": 0, "directory_count": 0}

        if not self.results_dir.exists():
            return usage

        for root, dirs, files in os.walk(self.results_dir):
            usage["directory_count"] += len(dirs)
            for file in files:
                file_path = Path(root) / file
                try:
                    usage["total_size"] += file_path.stat().st_size
                    usage["file_count"] += 1
                except Exception:
                    pass

        return usage

    def create_cleanup_report(self) -> str:
        """Create a cleanup report"""
        summary = self.get_results_summary()
        disk_usage = self.get_disk_usage()

        report = f"""
# Performance Testing Results Cleanup Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Results Directory:** {self.results_dir.absolute()}
**Keep Recent Files:** {self.keep_recent}

## Disk Usage Summary

- **Total Size:** {disk_usage['total_size'] / (1024*1024):.2f} MB
- **Total Files:** {disk_usage['file_count']}
- **Total Directories:** {disk_usage['directory_count']}

## Test Results Summary

"""

        for test_type, info in summary.items():
            report += f"""
### {test_type.title()} Testing

- **Total Files:** {info['total_files']}
- **Recent Files Kept:** {len(info['recent_files'])}
- **Newest File:** {info['newest_file']['name'] if info['newest_file'] else 'None'}
- **Oldest File:** {info['oldest_file']['name'] if info['oldest_file'] else 'None'}

**Recent Files:**
"""
            for file_info in info["recent_files"]:
                report += f"- {file_info['name']} ({file_info['size'] / 1024:.1f} KB, {file_info['created']})\n"

        return report

    def run_cleanup(self) -> Dict[str, any]:
        """Run complete cleanup process"""
        logger.info("Starting report cleanup process...")

        # Get initial summary
        initial_summary = self.get_results_summary()
        initial_disk_usage = self.get_disk_usage()

        # Clean old results
        cleaned_counts = self.clean_old_results()

        # Clean old result folders
        # folder_cleaned = self.clean_results_folders()

        # Clean temporary files
        temp_cleaned = self.cleanup_temp_files()

        # Get final summary
        final_summary = self.get_results_summary()
        final_disk_usage = self.get_disk_usage()

        # Create cleanup report
        cleanup_report = self.create_cleanup_report()

        # Save cleanup report
        report_file = self.results_dir / "cleanup_report.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(cleanup_report)

        # Calculate savings
        disk_saved = initial_disk_usage["total_size"] - final_disk_usage["total_size"]
        files_saved = initial_disk_usage["file_count"] - final_disk_usage["file_count"]

        result = {
            "initial_summary": initial_summary,
            "final_summary": final_summary,
            "cleaned_counts": cleaned_counts,
            # "folder_cleaned": folder_cleaned,
            "temp_cleaned": temp_cleaned,
            "disk_saved_mb": disk_saved / (1024 * 1024),
            "files_saved": files_saved,
            "cleanup_report_file": str(report_file),
        }

        logger.info(
            f"Cleanup completed. Saved {result['disk_saved_mb']:.2f} MB and {result['files_saved']} files"
        )
        return result


def main():
    """Main execution function"""
    try:
        cleaner = ReportCleaner()
        result = cleaner.run_cleanup()

        print(f"Cleanup completed successfully!")
        print(f"Disk space saved: {result['disk_saved_mb']:.2f} MB")
        print(f"Files removed: {result['files_saved']}")
        print(f"Cleanup report: {result['cleanup_report_file']}")

    except Exception as e:
        logger.error(f"Cleanup failed: {e}")


if __name__ == "__main__":
    main()
