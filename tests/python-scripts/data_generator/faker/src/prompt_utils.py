"""
Interactive Prompt Utility for Faker Data Generator

This module provides interactive user prompts for optional features
like SQL script generation.

@author Software Testing Team
@version 1.0.0
"""

import sys
from typing import Dict, List, Optional, Tuple, Union


def ask_yes_no(question: str, default: str = "n") -> bool:
    """
    Ask user a yes/no question.

    Args:
        question: The question to ask
        default: Default answer ('y' or 'n')

    Returns:
        True for yes, False for no
    """
    default_hint = "[Y/n]" if default.lower() == "y" else "[y/N]"

    try:
        answer = input(f"{question} {default_hint}: ").strip().lower()

        if answer == "":
            return default.lower() == "y"

        return answer in ("y", "yes")
    except (KeyboardInterrupt, EOFError):
        print("\\n⚠️  Operation cancelled by user")
        return False


def ask_multiple_choice(
    question: str, options: List[str], default_index: int = 0
) -> Tuple[int, str]:
    """
    Ask user to select from multiple options.

    Args:
        question: The question to ask
        options: List of available options
        default_index: Index of default option

    Returns:
        Tuple of (selected_index, selected_value)
    """
    print(f"\\n{question}")

    for i, option in enumerate(options):
        marker = "→" if i == default_index else " "
        print(f"{marker} {i + 1}. {option}")

    try:
        answer = input(
            f"\\nEnter your choice (1-{len(options)}) [{default_index + 1}]: "
        )

        if answer.strip() == "":
            choice = default_index + 1
        else:
            choice = int(answer.strip())

        # Clamp to valid range
        selected_index = max(0, min(len(options) - 1, choice - 1))
        return selected_index, options[selected_index]

    except (ValueError, KeyboardInterrupt, EOFError):
        print("\\n⚠️  Using default option")
        return default_index, options[default_index]


def ask_text(question: str, default_value: str = "") -> str:
    """
    Ask user for text input.

    Args:
        question: The question to ask
        default_value: Default value if no input provided

    Returns:
        User input or default value
    """
    default_hint = f" [{default_value}]" if default_value else ""

    try:
        answer = input(f"{question}{default_hint}: ").strip()
        return answer if answer else default_value
    except (KeyboardInterrupt, EOFError):
        print("\\n⚠️  Using default value")
        return default_value


def display_message(message_type: str, message: str) -> None:
    """
    Display a formatted message with emojis.

    Args:
        message_type: Type of message (info, success, warning, error, question)
        message: The message to display
    """
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "question": "❓",
    }

    icon = icons.get(message_type, "📝")
    print(f"{icon} {message}")


def prompt_for_sql_generation() -> Optional[Dict[str, Union[str, bool, int]]]:
    """
    Interactive workflow for SQL generation options.

    Returns:
        Dictionary with SQL generation options, or None if cancelled
    """
    try:
        print("\\n" + "=" * 50)
        print("🔧 OPTIONAL: SQL INSERT Script Generation")
        print("=" * 50)

        generate_sql = ask_yes_no(
            "Would you like to generate SQL INSERT script for database import?", "n"
        )

        if not generate_sql:
            display_message("info", "Skipping SQL script generation")
            return None

        # Ask for database type
        db_options = ["MySQL", "PostgreSQL", "SQLite"]
        db_index, db_choice = ask_multiple_choice(
            "Select your database type:", db_options, 0
        )

        # Ask for additional options
        include_transactions = ask_yes_no(
            "Include transaction wrapper (START TRANSACTION/COMMIT)?", "y"
        )

        on_duplicate_update = ask_yes_no(
            "Include ON DUPLICATE KEY UPDATE clause (MySQL only)?", "n"
        )

        batch_size_text = ask_text("Batch size for INSERT statements", "100")

        try:
            batch_size = int(batch_size_text)
            if batch_size < 1 or batch_size > 1000:
                print("⚠️  Batch size must be between 1 and 1000, using default (100)")
                batch_size = 100
        except ValueError:
            print("⚠️  Invalid batch size, using default (100)")
            batch_size = 100

        return {
            "db_type": db_choice.lower(),
            "include_transactions": include_transactions,
            "on_duplicate_update": on_duplicate_update,
            "batch_size": batch_size,
            "include_comments": True,
        }

    except Exception as e:
        print(f"❌ Error in SQL generation prompt: {e}")
        return None


def confirm_file_operation(operation: str, file_path: str) -> bool:
    """
    Confirmation prompt for file operations.

    Args:
        operation: Description of the operation
        file_path: Path to the file

    Returns:
        True if confirmed, False otherwise
    """
    return ask_yes_no(f"Confirm {operation} to: {file_path}?", "y")


def display_completion_summary(results: Dict[str, Union[str, int]]) -> None:
    """
    Display completion summary with file paths and statistics.

    Args:
        results: Dictionary containing result information
    """
    print("\\n" + "=" * 50)
    print("🎉 GENERATION COMPLETE")
    print("=" * 50)

    if "csv_files" in results:
        print("📄 CSV files generated:")
        for csv_file in results["csv_files"]:
            print(f"   • {csv_file}")

    if "sql_files" in results:
        print("💽 SQL files generated:")
        for sql_file in results["sql_files"]:
            print(f"   • {sql_file}")

    if "duration" in results:
        print(f"⏱️ Total time: {results['duration']}")

    if "total_records" in results:
        print(f"📊 Total records: {results['total_records']}")

    print("=" * 50)


def show_progress(message: str) -> None:
    """Show progress indicator."""
    print(f"⏳ {message}...", end="", flush=True)


def clear_progress() -> None:
    """Clear progress indicator."""
    print("\\r", end="", flush=True)


def handle_keyboard_interrupt() -> None:
    """Handle Ctrl+C gracefully."""
    print("\\n\\n⚠️  Operation cancelled by user")
    print("💡 You can restart the generator anytime")
    sys.exit(0)
