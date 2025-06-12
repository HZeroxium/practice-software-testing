/**
 * Registration Test Configuration
 * Modify these arrays to control which test cases run
 */

// Set to true to run all test cases, false to run only specified cases
export const RUN_ALL_REGISTRATION_TESTS = true;

// Specify which test cases to run when RUN_ALL_REGISTRATION_TESTS is false
// Add or remove test case IDs from this array
export const REGISTER_TEST_CASES: string[] = [
  "REG-EP-02",
  "REG-EP-03",
  // "TC_REG_001",
  // "TC_REG_002",
  // "TC_REG_003",
  // Add your specific test case IDs here
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

// Negative test configuration - run only error validation tests
// export const RUN_ALL_REGISTRATION_TESTS = false;
// export const REGISTER_TEST_CASES = ["TC_REG_INVALID_EMAIL", "TC_REG_WEAK_PASSWORD"];

// Boundary test configuration - run edge case tests
// export const RUN_ALL_REGISTRATION_TESTS = false;
// export const REGISTER_TEST_CASES = ["TC_REG_MIN_LENGTH", "TC_REG_MAX_LENGTH"];
