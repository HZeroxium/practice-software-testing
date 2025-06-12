import { AdminTestConfig } from "../types/admin-test-data.types";

export class AdminTestConfigManager {
  private static config: AdminTestConfig = {
    runAll: true,
    testCaseIds: [],
    testDataFile: "tests/data/input/add_product_test_data.csv",
    adminCredentials: {
      email: "admin@practicesoftwaretesting.com",
      password: "welcome01",
    },
  };

  /**
   * Sets the test configuration
   * @param config - Test configuration object
   */
  static setConfig(config: Partial<AdminTestConfig>): void {
    this.config = { ...this.config, ...config };
  }

  /**
   * Gets the current test configuration
   * @returns Current test configuration
   */
  static getConfig(): AdminTestConfig {
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
    const envTestCases =
      process.env.PRODUCT_TEST_CASES || process.env.TEST_CASES;
    const envRunAll = process.env.RUN_ALL_TESTS;
    const envDataFile =
      process.env.PRODUCT_TEST_DATA_FILE || process.env.TEST_DATA_FILE;
    const envAdminEmail = process.env.ADMIN_EMAIL;
    const envAdminPassword = process.env.ADMIN_PASSWORD;

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

    if (envAdminEmail && envAdminPassword) {
      this.config.adminCredentials = {
        email: envAdminEmail,
        password: envAdminPassword,
      };
    }
  }

  /**
   * Prints current configuration
   */
  static printConfig(): void {
    console.log("=== Admin Product Test Configuration ===");
    console.log(`Run All Tests: ${this.config.runAll}`);
    console.log(`Test Data File: ${this.config.testDataFile}`);
    console.log(`Admin Email: ${this.config.adminCredentials?.email}`);

    if (
      !this.config.runAll &&
      this.config.testCaseIds &&
      this.config.testCaseIds.length > 0
    ) {
      console.log(`Selected Test Cases: ${this.config.testCaseIds.join(", ")}`);
    }
    console.log("=======================================");
  }
}
