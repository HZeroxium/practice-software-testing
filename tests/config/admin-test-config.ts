/**
 * Admin Product Test Configuration
 * Modify these arrays to control which test cases run
 */

// Set to true to run all test cases, false to run only specified cases
export const RUN_ALL_ADMIN_TESTS = true;

// Specify which test cases to run when RUN_ALL_ADMIN_TESTS is false
// Add or remove test case IDs from this array
export const ADMIN_TEST_CASES: string[] = [
  // "TC_ADMIN_PRODUCT_001",
  // "TC_ADMIN_PRODUCT_002",
  // "TC_ADMIN_PRODUCT_003",
  // Add your specific test case IDs here
];

// Test data file path (relative to project root)
export const ADMIN_TEST_DATA_FILE =
  "tests/data/input/admin_product_test_data.csv";

// Admin credentials for authentication
export const ADMIN_CREDENTIALS = {
  email: "admin@example.com",
  password: "admin123",
  // Override these values in your local environment if needed
};

/**
 * Quick configuration presets
 * Uncomment one of these blocks to use predefined configurations
 */

// Product creation smoke tests
// export const RUN_ALL_ADMIN_TESTS = false;
// export const ADMIN_TEST_CASES = ["TC_ADMIN_PRODUCT_HAPPY", "TC_ADMIN_PRODUCT_BASIC"];

// Product validation tests
// export const RUN_ALL_ADMIN_TESTS = false;
// export const ADMIN_TEST_CASES = ["TC_ADMIN_PRODUCT_INVALID_PRICE", "TC_ADMIN_PRODUCT_EMPTY_NAME"];

// Product image upload tests
// export const RUN_ALL_ADMIN_TESTS = false;
// export const ADMIN_TEST_CASES = ["TC_ADMIN_PRODUCT_IMAGE_UPLOAD", "TC_ADMIN_PRODUCT_NO_IMAGE"];
