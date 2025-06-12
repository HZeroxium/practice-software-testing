import { parse } from "csv-parse/sync";
import * as fs from "fs";
import * as path from "path";
import { RegistrationTestData, TestConfig } from "../types/test-data.types";

export class DataReader {
  private static readonly DEFAULT_DATA_FILE =
    "tests/data/input/register_test_data.csv";

  /**
   * Reads and parses CSV test data file
   * @param filePath - Path to the CSV file
   * @returns Array of RegistrationTestData objects
   */
  static readTestData(filePath?: string): RegistrationTestData[] {
    const csvFilePath = filePath || this.DEFAULT_DATA_FILE;
    const fullPath = path.resolve(csvFilePath);

    if (!fs.existsSync(fullPath)) {
      throw new Error(`Test data file not found: ${fullPath}`);
    }

    const fileContent = fs.readFileSync(fullPath, "utf-8");
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true,
      trim: true,
    });

    return records.map((record: any) => ({
      TestCaseID: record.TestCaseID,
      FirstName: this.processSpecialValues(record.FirstName),
      LastName: this.processSpecialValues(record.LastName),
      DOB: this.processSpecialValues(record.DOB),
      Street: this.processSpecialValues(record.Street),
      City: this.processSpecialValues(record.City),
      State: this.processSpecialValues(record.State),
      Country: this.processSpecialValues(record.Country),
      PostalCode: this.processSpecialValues(record.PostalCode),
      Phone: this.processSpecialValues(record.Phone),
      Email: this.processSpecialValues(record.Email),
      Password: this.processSpecialValues(record.Password),
    }));
  }

  /**
   * Filters test data based on configuration
   * @param testData - Array of test data
   * @param config - Test configuration
   * @returns Filtered test data
   */
  static filterTestData(
    testData: RegistrationTestData[],
    config: TestConfig
  ): RegistrationTestData[] {
    if (
      config.runAll ||
      !config.testCaseIds ||
      config.testCaseIds.length === 0
    ) {
      return testData;
    }

    return testData.filter((data) =>
      config.testCaseIds!.includes(data.TestCaseID)
    );
  }

  /**
   * Processes special values in CSV data
   * @param value - Raw value from CSV
   * @returns Processed value
   */
  private static processSpecialValues(value: string): string {
    if (!value) return "";

    // Handle empty values
    if (value === "(empty)" || value === '""') {
      return "";
    }

    // Handle none values
    if (value === "(none)") {
      return "";
    }

    // Handle repeated characters (e.g., "256×'A'", "254×'A'")
    const repeatMatch = value.match(/^(\d+)×['"](.)['"]/);
    if (repeatMatch) {
      const count = parseInt(repeatMatch[1]);
      const char = repeatMatch[2];
      return char.repeat(count);
    }

    // Handle quoted values
    if (value.startsWith('"""') && value.endsWith('"""')) {
      return value.slice(3, -3);
    }

    return value;
  }

  /**
   * Gets available test case IDs from the data file
   * @param filePath - Path to the CSV file
   * @returns Array of test case IDs
   */
  static getAvailableTestCaseIds(filePath?: string): string[] {
    const testData = this.readTestData(filePath);
    return testData.map((data) => data.TestCaseID);
  }
}
