#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List
import pandas as pd
from tkinter import Tk, filedialog
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet


def sanitize_sheet_name(name: str) -> str:
    """
    Sanitize a string to be a valid Excel sheet name:
      - Maximum 31 characters
      - Invalid chars []:*?/\\ replaced with underscore
    """
    invalid_chars = ["\\", "/", "*", "[", "]", ":", "?"]
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name[:31]


def auto_adjust_column_width(
    worksheet: Worksheet, df: pd.DataFrame, margin: int = 2
) -> None:
    """
    Auto-adjust column widths in the worksheet based on the DataFrame contents.

    Args:
        worksheet: The xlsxwriter Worksheet object.
        df: The DataFrame whose columns will be written.
        margin: Extra space to add to each column width.
    """
    for idx, col in enumerate(df.columns):
        # Determine max width between header and data values
        max_data_width = df[col].astype(str).map(len).max()
        header_width = len(str(col))
        adjusted_width = max(header_width, max_data_width) + margin
        worksheet.set_column(idx, idx, adjusted_width)


def csvs_to_excel() -> None:
    """
    Prompt the user to select multiple CSV files and merge them into a single
    Excel workbook. Each CSV becomes its own sheet, with styled headers and
    auto‑sized columns.
    """
    # Hide the root Tk window
    root = Tk()
    root.withdraw()

    # 1) Select CSV files
    csv_paths: List[str] = filedialog.askopenfilenames(
        title="Select CSV files to combine",
        filetypes=[("CSV files", "*.csv")],
    )
    if not csv_paths:
        print("No CSV files selected. Exiting.")
        return

    # 2) Ask where to save the Excel workbook
    save_path: str = filedialog.asksaveasfilename(
        title="Save combined Excel file as",
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
    )
    root.destroy()
    if not save_path:
        print("No save location provided. Exiting.")
        return

    # 3) Create the Excel writer with xlsxwriter engine
    with pd.ExcelWriter(save_path, engine="xlsxwriter") as writer:
        workbook: Workbook = writer.book

        # Define a header format: bold, wrapped, centered, light-green background, border
        header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
                "border": 1,
            }
        )

        for csv_file in csv_paths:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file)

            # Derive and sanitize sheet name from filename
            raw_name = os.path.splitext(os.path.basename(csv_file))[0]
            sheet_name = sanitize_sheet_name(raw_name)

            # Write DataFrame to its sheet (including the header row)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Access the worksheet object
            worksheet: Worksheet = writer.sheets[sheet_name]

            # Apply header format to the first row (row index 0)
            worksheet.set_row(0, None, header_format)

            # Freeze the header row
            worksheet.freeze_panes(1, 0)

            # Auto-adjust column widths
            auto_adjust_column_width(worksheet, df)

    print(f"✅ Successfully created Excel file:\n{save_path}")


if __name__ == "__main__":
    csvs_to_excel()
