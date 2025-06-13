import { AdminTestConfig } from "../types/admin-test-data.types";
import {
  RUN_ALL_ADMIN_TESTS,
  ADMIN_TEST_CASES,
  ADMIN_TEST_DATA_FILE,
  ADMIN_CREDENTIALS,
  EXCLUDE_ADMIN_TEST_CASES,
  EXCLUDE_ADMIN_BY_PREFIX,
  EXCLUDE_ADMIN_BY_SUFFIX,
} from "../config/admin-add-product-test-config";

export class AdminTestConfigManager {
  private static config: AdminTestConfig = {
    runAll: RUN_ALL_ADMIN_TESTS,
    testCaseIds: ADMIN_TEST_CASES,
    testDataFile: ADMIN_TEST_DATA_FILE,
    adminCredentials: ADMIN_CREDENTIALS,
    excludeTestCases: EXCLUDE_ADMIN_TEST_CASES,
    excludeByPrefix: EXCLUDE_ADMIN_BY_PREFIX,
    excludeBySuffix: EXCLUDE_ADMIN_BY_SUFFIX,
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
   * Gets test cases from environment variables or command line
   */
  static loadConfigFromEnvironment(): void {
    // Start with TypeScript configuration as base
    this.config = {
      runAll: RUN_ALL_ADMIN_TESTS,
      testCaseIds: ADMIN_TEST_CASES,
      testDataFile: ADMIN_TEST_DATA_FILE,
      adminCredentials: ADMIN_CREDENTIALS,
      excludeTestCases: EXCLUDE_ADMIN_TEST_CASES,
      excludeByPrefix: EXCLUDE_ADMIN_BY_PREFIX,
      excludeBySuffix: EXCLUDE_ADMIN_BY_SUFFIX,
    };

    const envTestCases =
      process.env.PRODUCT_TEST_CASES || process.env.TEST_CASES;
    const envRunAll = process.env.RUN_ALL_TESTS;
    const envDataFile =
      process.env.PRODUCT_TEST_DATA_FILE || process.env.TEST_DATA_FILE;
    const envAdminEmail = process.env.ADMIN_EMAIL;
    const envAdminPassword = process.env.ADMIN_PASSWORD;
    const envExcludeCases = process.env.EXCLUDE_ADMIN_TEST_CASES;
    const envExcludePrefix = process.env.EXCLUDE_ADMIN_BY_PREFIX;
    const envExcludeSuffix = process.env.EXCLUDE_ADMIN_BY_SUFFIX;

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
   * Prints current configuration with enhanced formatting
   */
  static printConfig(): void {
    console.log("╔══════════════════════════════════════╗");
    console.log("║       Admin Product Test Config     ║");
    console.log("╠══════════════════════════════════════╣");
    console.log(`║ Run All Tests: ${this.config.runAll ? "✅ YES" : "❌ NO"}`);
    console.log(`║ Test Data File: ${this.config.testDataFile}`);
    console.log(`║ Admin Email: ${this.config.adminCredentials?.email}`);

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
