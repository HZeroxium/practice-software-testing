import { TestConfig } from "../types/test-data.types";

export class TestConfigManager {
  private static config: TestConfig = {
    runAll: true,
    testCaseIds: [],
    testDataFile: "tests/data/input/register_test_data.csv",
  };

  /**
   * Sets the test configuration
   * @param config - Test configuration object
   */
  static setConfig(config: Partial<TestConfig>): void {
    this.config = { ...this.config, ...config };
  }

  /**
   * Gets the current test configuration
   * @returns Current test configuration
   */
  static getConfig(): TestConfig {
    return { ...this.config };
  }

  /**
   * Sets specific test cases to run
   * @param testCaseIds - Array of test case IDs
   */
  static setTestCases(testCaseIds: string[]): void {
    this.config.testCaseIds = testCaseIds;
    this.config.runAll = false;
  }

  /**
   * Sets to run all test cases
   */
  static runAllTests(): void {
    this.config.runAll = true;
    this.config.testCaseIds = [];
  }

  /**
   * Gets test cases from environment variables or command line
   */
  static loadConfigFromEnvironment(): void {
    const envTestCases = process.env.TEST_CASES;
    const envRunAll = process.env.RUN_ALL_TESTS;
    const envDataFile = process.env.TEST_DATA_FILE;

    if (envTestCases) {
      const testCaseIds = envTestCases.split(",").map((id) => id.trim());
      this.setTestCases(testCaseIds);
    }

    if (envRunAll === "true") {
      this.runAllTests();
    }

    if (envDataFile) {
      this.config.testDataFile = envDataFile;
    }
  }

  /**
   * Prints current configuration
   */
  static printConfig(): void {
    console.log("=== Test Configuration ===");
    console.log(`Run All Tests: ${this.config.runAll}`);
    console.log(`Test Data File: ${this.config.testDataFile}`);

    if (
      !this.config.runAll &&
      this.config.testCaseIds &&
      this.config.testCaseIds.length > 0
    ) {
      console.log(`Selected Test Cases: ${this.config.testCaseIds.join(", ")}`);
    }
    console.log("==========================");
  }
}
