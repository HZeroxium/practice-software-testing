import { TestConfig } from "../types/test-data.types";
import {
  RUN_ALL_REGISTRATION_TESTS,
  REGISTER_TEST_CASES,
  REGISTRATION_TEST_DATA_FILE,
} from "../config/registration-test-config";

export class TestConfigManager {
  private static config: TestConfig = {
    runAll: RUN_ALL_REGISTRATION_TESTS,
    testCaseIds: REGISTER_TEST_CASES,
    testDataFile: REGISTRATION_TEST_DATA_FILE,
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
   * Loads configuration from TypeScript config file (default behavior)
   * Also supports environment variable override for CI/CD compatibility
   */
  static loadConfigFromEnvironment(): void {
    // Start with TypeScript configuration as base
    this.config = {
      runAll: RUN_ALL_REGISTRATION_TESTS,
      testCaseIds: REGISTER_TEST_CASES,
      testDataFile: REGISTRATION_TEST_DATA_FILE,
    };

    // Allow environment variable override for CI/CD systems
    const envTestCases = process.env.REGISTER_TEST_CASES;
    const envRunAll = process.env.RUN_ALL_REGISTRATION_TESTS;
    const envDataFile = process.env.REGISTRATION_TEST_DATA_FILE;

    if (envTestCases) {
      const testCaseIds = envTestCases.split(",").map((id) => id.trim());
      this.setTestCases(testCaseIds);
      console.log("🔧 Overriding test cases from environment variable");
    }

    if (envRunAll === "true") {
      this.runAllTests();
      console.log("🔧 Overriding runAll from environment variable");
    } else if (envRunAll === "false") {
      this.config.runAll = false;
    }

    if (envDataFile) {
      this.config.testDataFile = envDataFile;
      console.log("🔧 Overriding test data file from environment variable");
    }
  }

  /**
   * Quick configuration methods for common test scenarios
   */
  static configureForSmokeTests(): void {
    console.log("🔧 Configuring for smoke tests");
    this.setConfig({
      runAll: false,
      testCaseIds: ["TC_REG_001", "TC_REG_HAPPY_PATH"],
    });
  }

  static configureForRegressionTests(): void {
    console.log("🔧 Configuring for regression tests");
    this.runAllTests();
  }

  static configureForNegativeTests(): void {
    console.log("🔧 Configuring for negative tests");
    this.setConfig({
      runAll: false,
      testCaseIds: [
        "TC_REG_INVALID_EMAIL",
        "TC_REG_WEAK_PASSWORD",
        "TC_REG_DUPLICATE_EMAIL",
      ],
    });
  }

  /**
   * Prints current configuration with enhanced formatting
   */
  static printConfig(): void {
    console.log("╔══════════════════════════════════════╗");
    console.log("║        Registration Test Config      ║");
    console.log("╠══════════════════════════════════════╣");
    console.log(`║ Run All Tests: ${this.config.runAll ? "✅ YES" : "❌ NO"}`);
    console.log(`║ Test Data File: ${this.config.testDataFile}`);

    if (
      !this.config.runAll &&
      this.config.testCaseIds &&
      this.config.testCaseIds.length > 0
    ) {
      console.log(`║ Selected Test Cases (${this.config.testCaseIds.length}):`);
      this.config.testCaseIds.forEach((id, index) => {
        const isLast = index === this.config.testCaseIds!.length - 1;
        console.log(`║   ${isLast ? "└─" : "├─"} ${id}`);
      });
    } else if (!this.config.runAll) {
      console.log("║ ⚠️  No specific test cases selected");
    }
    console.log("╚══════════════════════════════════════╝");
  }
}
