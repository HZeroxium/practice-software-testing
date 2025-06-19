// tests/utils/registration-test-config.ts

import { RegistrationTestConfig } from "../types/registration-test-data.types";
import {
  RUN_ALL_REGISTRATION_TESTS,
  REGISTER_TEST_CASES,
  REGISTRATION_TEST_DATA_FILE,
  EXCLUDE_TEST_CASES,
  EXCLUDE_BY_PREFIX,
  EXCLUDE_BY_SUFFIX,
} from "../config/registration-test-config";

export class TestConfigManager {
  private static config: RegistrationTestConfig = {
    runAll: RUN_ALL_REGISTRATION_TESTS,
    testCaseIds: REGISTER_TEST_CASES,
    testDataFile: REGISTRATION_TEST_DATA_FILE,
    excludeTestCases: EXCLUDE_TEST_CASES,
    excludeByPrefix: EXCLUDE_BY_PREFIX,
    excludeBySuffix: EXCLUDE_BY_SUFFIX,
  };

  /**
   * Sets the test configuration
   * @param config - Test configuration object
   */
  static setConfig(config: Partial<RegistrationTestConfig>): void {
    this.config = { ...this.config, ...config };
  }

  /**
   * Gets the current test configuration
   * @returns Current test configuration
   */
  static getConfig(): RegistrationTestConfig {
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
   * Sets exclude patterns for when running all tests
   * @param excludeConfig - Exclude configuration
   */
  static setExcludePatterns(excludeConfig: {
    testCases?: string[];
    prefixes?: string[];
    suffixes?: string[];
  }): void {
    if (excludeConfig.testCases) {
      this.config.excludeTestCases = excludeConfig.testCases;
    }
    if (excludeConfig.prefixes) {
      this.config.excludeByPrefix = excludeConfig.prefixes;
    }
    if (excludeConfig.suffixes) {
      this.config.excludeBySuffix = excludeConfig.suffixes;
    }
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
      excludeTestCases: EXCLUDE_TEST_CASES,
      excludeByPrefix: EXCLUDE_BY_PREFIX,
      excludeBySuffix: EXCLUDE_BY_SUFFIX,
    };

    // Allow environment variable override for CI/CD systems
    const envTestCases = process.env.REGISTER_TEST_CASES;
    const envRunAll = process.env.RUN_ALL_REGISTRATION_TESTS;
    const envDataFile = process.env.REGISTRATION_TEST_DATA_FILE;
    const envExcludeCases = process.env.EXCLUDE_REGISTER_TEST_CASES;
    const envExcludePrefix = process.env.EXCLUDE_REGISTER_BY_PREFIX;
    const envExcludeSuffix = process.env.EXCLUDE_REGISTER_BY_SUFFIX;

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

    // Handle exclude environment variables
    if (envExcludeCases) {
      this.config.excludeTestCases = envExcludeCases
        .split(",")
        .map((id) => id.trim());
      console.log("🔧 Overriding exclude test cases from environment variable");
    }

    if (envExcludePrefix) {
      this.config.excludeByPrefix = envExcludePrefix
        .split(",")
        .map((prefix) => prefix.trim());
      console.log("🔧 Overriding exclude prefixes from environment variable");
    }

    if (envExcludeSuffix) {
      this.config.excludeBySuffix = envExcludeSuffix
        .split(",")
        .map((suffix) => suffix.trim());
      console.log("🔧 Overriding exclude suffixes from environment variable");
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

    // Show exclude configuration when running all tests
    if (this.config.runAll) {
      const hasExcludes =
        (this.config.excludeTestCases?.length || 0) > 0 ||
        (this.config.excludeByPrefix?.length || 0) > 0 ||
        (this.config.excludeBySuffix?.length || 0) > 0;

      if (hasExcludes) {
        console.log("║ Exclude Configuration:");

        if (this.config.excludeTestCases?.length) {
          console.log(
            `║   🚫 Test Cases (${this.config.excludeTestCases.length}):`
          );
          this.config.excludeTestCases.forEach((id, index) => {
            const isLast = index === this.config.excludeTestCases!.length - 1;
            console.log(`║      ${isLast ? "└─" : "├─"} ${id}`);
          });
        }

        if (this.config.excludeByPrefix?.length) {
          console.log(
            `║   🚫 By Prefix: ${this.config.excludeByPrefix.join(", ")}`
          );
        }

        if (this.config.excludeBySuffix?.length) {
          console.log(
            `║   🚫 By Suffix: ${this.config.excludeBySuffix.join(", ")}`
          );
        }
      } else {
        console.log("║ No exclusions configured");
      }
    }

    console.log("╚══════════════════════════════════════╝");
  }
}
