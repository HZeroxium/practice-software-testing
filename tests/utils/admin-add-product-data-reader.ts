// tests/utils/admin-add-product-data-reader.ts

import { parse } from "csv-parse/sync";
import * as fs from "fs";
import * as path from "path";
import {
  AddProductTestData,
  AdminTestConfig,
  NominalValues,
} from "../types/admin-test-data.types";

export class AdminAddProductDataReader {
  private static readonly DEFAULT_DATA_FILE =
    "tests/data/input/add_product_test_data.csv";

  // Define nominal values for product testing
  private static readonly NOMINAL_VALUES: NominalValues = {
    name: "Test Product",
    description:
      "This is a test product description for automation testing purposes.",
    price: "29.99",
    brand: "1", // First brand ID
    category: "1", // First category ID
    productImage: "1", // First image ID
    stock: "50",
  };

  /**
   * Reads and parses CSV test data file for admin product testing
   * @param filePath - Path to the CSV file
   * @returns Array of AddProductTestData objects
   */
  static readProductTestData(filePath?: string): AddProductTestData[] {
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
      Name: this.processSpecialValues(record.Name),
      Description: this.processSpecialValues(record.Description),
      Price: this.processSpecialValues(record.Price),
      Brand: this.processSpecialValues(record.Brand),
      Category: this.processSpecialValues(record.Category),
      ProductImage: this.processSpecialValues(record.ProductImage),
      Stock: this.processSpecialValues(record.Stock),
      LocationOffer: this.processSpecialValues(record.LocationOffer),
      Rental: this.processSpecialValues(record.Rental),
    }));
  }

  /**
   * Filters test data based on configuration with exclude support
   * @param testData - Array of test data
   * @param config - Test configuration
   * @returns Filtered test data
   */
  static filterTestData(
    testData: AddProductTestData[],
    config: AdminTestConfig
  ): AddProductTestData[] {
    if (config.runAll) {
      // When running all tests, apply exclude filters
      return this.applyExcludeFilters(testData, config);
    }

    if (!config.testCaseIds || config.testCaseIds.length === 0) {
      return testData;
    }

    // When running specific tests, only include the specified ones
    return testData.filter((data) =>
      config.testCaseIds!.includes(data.TestCaseID)
    );
  }

  /**
   * Applies exclude filters to test data
   * @param testData - Array of test data
   * @param config - Test configuration with exclude options
   * @returns Filtered test data with exclusions applied
   */
  private static applyExcludeFilters(
    testData: AddProductTestData[],
    config: AdminTestConfig
  ): AddProductTestData[] {
    return testData.filter((data) => {
      const testCaseId = data.TestCaseID;

      // Exclude specific test cases
      if (config.excludeTestCases?.includes(testCaseId)) {
        return false;
      }

      // Exclude by prefix
      if (
        config.excludeByPrefix?.some((prefix) => testCaseId.startsWith(prefix))
      ) {
        return false;
      }

      // Exclude by suffix
      if (
        config.excludeBySuffix?.some((suffix) => testCaseId.endsWith(suffix))
      ) {
        return false;
      }

      return true;
    });
  }

  /**
   * Processes special values in CSV data and replaces nominal values
   * @param value - Raw value from CSV
   * @returns Processed value
   */
  private static processSpecialValues(value: string): string {
    if (!value) return "";

    // Handle empty values
    if (value === "(empty)" || value === '""' || value === '""""') {
      return "";
    }

    // Handle none values
    if (value === "(none)") {
      return "";
    }

    // Handle nominal values replacement
    if (value === "nominal") {
      return this.getNominalValue();
    }

    // Handle repeated characters (e.g., "A×256", "D×1001")
    const repeatMatch = value.match(/^([A-Z])×(\d+)$/);
    if (repeatMatch) {
      const char = repeatMatch[1];
      const count = parseInt(repeatMatch[2]);
      return char.repeat(count);
    }

    // Handle quoted values with specific content
    if (value.startsWith('"""') && value.endsWith('"""')) {
      return value.slice(3, -3);
    }

    // Handle special characters and text
    return value;
  }

  /**
   * Gets nominal value based on context (this is a simplified version)
   * In a real implementation, you might want to track which field this is for
   * @returns A default nominal value
   */
  private static getNominalValue(): string {
    return "nominal_placeholder";
  }

  /**
   * Replaces nominal placeholders with actual nominal values
   * @param data - Test data with potential nominal placeholders
   * @returns Test data with nominal values replaced
   */
  static replaceNominalValues(data: AddProductTestData): AddProductTestData {
    return {
      ...data,
      Name:
        data.Name === "nominal_placeholder"
          ? this.NOMINAL_VALUES.name
          : data.Name,
      Description:
        data.Description === "nominal_placeholder"
          ? this.NOMINAL_VALUES.description
          : data.Description,
      Price:
        data.Price === "nominal_placeholder"
          ? this.NOMINAL_VALUES.price
          : data.Price,
      Brand:
        data.Brand === "nominal_placeholder"
          ? this.NOMINAL_VALUES.brand
          : data.Brand,
      Category:
        data.Category === "nominal_placeholder"
          ? this.NOMINAL_VALUES.category
          : data.Category,
      ProductImage:
        data.ProductImage === "nominal_placeholder"
          ? this.NOMINAL_VALUES.productImage
          : data.ProductImage,
      Stock:
        data.Stock === "nominal_placeholder"
          ? this.NOMINAL_VALUES.stock
          : data.Stock,
    };
  }

  /**
   * Gets available test case IDs from the data file
   * @param filePath - Path to the CSV file
   * @returns Array of test case IDs
   */
  static getAvailableTestCaseIds(filePath?: string): string[] {
    const testData = this.readProductTestData(filePath);
    return testData.map((data) => data.TestCaseID);
  }
}
