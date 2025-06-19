// tests/config/registration-test-config.ts

/**
 * Registration Test Configuration
 * Modify these arrays to control which test cases run
 */

// Set to true to run all test cases, false to run only specified cases
export const RUN_ALL_REGISTRATION_TESTS = true;

// Specify which test cases to run when RUN_ALL_REGISTRATION_TESTS is false
// Add or remove test case IDs from this array
export const REGISTER_TEST_CASES: string[] = [
  "REG-EP-01",
  // "REG-EP-02",
  // "REG-EP-03",
  // "TC_REG_001",
  // "TC_REG_002",
  // "TC_REG_003",
  // Add your specific test case IDs here
];

// Exclude configuration when RUN_ALL_REGISTRATION_TESTS is true
// These settings only apply when running all tests
export const EXCLUDE_TEST_CASES: string[] = [
  // "REG-EP-01",  // Exclude specific test case
  // "REG-BVA-25", // Exclude another specific test case
];

export const EXCLUDE_BY_PREFIX: string[] = [
  "DUP-REG-", // Exclude duplicate registration tests
  // "REG-BVA-",   // Exclude all boundary value analysis tests
  // "REG-PERF-",  // Exclude performance tests
];

export const EXCLUDE_BY_SUFFIX: string[] = [
  // "-SLOW",      // Exclude slow running tests
  // "-FLAKY",     // Exclude flaky tests
];

// Test data file path (relative to project root)
export const REGISTRATION_TEST_DATA_FILE =
  "tests/data/input/register_test_data.csv";

/**
 * Quick configuration presets
 * Uncomment one of these blocks to use predefined configurations
 */

// Smoke test configuration - run only critical happy path tests
// export const RUN_ALL_REGISTRATION_TESTS = false;
// export const REGISTER_TEST_CASES = ["TC_REG_001", "TC_REG_HAPPY_PATH"];

// Fast test configuration - exclude slow tests when running all
// export const RUN_ALL_REGISTRATION_TESTS = true;
// export const EXCLUDE_BY_SUFFIX = ["-SLOW", "-PERF"];

// Stable test configuration - exclude flaky tests
// export const RUN_ALL_REGISTRATION_TESTS = true;
// export const EXCLUDE_TEST_CASES = ["REG-EP-15", "REG-BVA-26"];
// export const EXCLUDE_BY_SUFFIX = ["-FLAKY"];
