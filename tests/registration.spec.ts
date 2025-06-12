import { test, expect, Page } from "@playwright/test";
import { DataReader } from "./utils/data-reader";
import { FormHelpers } from "./utils/form-helpers";
import { TestConfigManager } from "./utils/test-config";
import { RegistrationTestData, TestResult } from "./types/test-data.types";

// Load configuration from environment
TestConfigManager.loadConfigFromEnvironment();

// Read and filter test data
const allTestData = DataReader.readTestData();
const testData = DataReader.filterTestData(
  allTestData,
  TestConfigManager.getConfig()
);

// Print configuration
TestConfigManager.printConfig();

test.describe("Registration Feature - Data Driven Tests", () => {
  let formHelpers: FormHelpers;

  test.beforeEach(async ({ page }) => {
    formHelpers = new FormHelpers(page);

    // Navigate to registration page
    await page.goto("/#/auth/register");
    await page.waitForLoadState("networkidle");

    // Verify we're on the registration page
    await expect(page.locator('[data-test="register-form"]')).toBeVisible();
  });

  // Generate a test for each data row
  for (const data of testData) {
    test(`Registration Test - ${data.TestCaseID}`, async ({ page }) => {
      const testResult: TestResult = {
        testCaseId: data.TestCaseID,
        status: "passed",
      };

      const startTime = Date.now();

      try {
        console.log(`\n=== Executing Test Case: ${data.TestCaseID} ===`);
        console.log("Test Data:", JSON.stringify(data, null, 2));

        // Clear form before filling (ensure clean state)
        await formHelpers.clearForm();

        // Fill the registration form with test data
        await formHelpers.fillRegistrationForm(data);

        // Take screenshot before submission
        await page.screenshot({
          path: `test-results/screenshots/before-submit-${data.TestCaseID}.png`,
          fullPage: true,
        });

        // Submit the form
        await formHelpers.submitForm();

        // Wait for submission result
        await formHelpers.waitForSubmissionResult();

        // Take screenshot after submission
        await page.screenshot({
          path: `test-results/screenshots/after-submit-${data.TestCaseID}.png`,
          fullPage: true,
        });

        // Get validation errors (if any)
        const validationErrors = await formHelpers.getValidationErrors();

        if (Object.keys(validationErrors).length > 0) {
          console.log("Validation Errors Found:", validationErrors);
        }

        // Check current URL to determine result
        const currentUrl = page.url();

        if (currentUrl.includes("login")) {
          console.log(
            "✅ Registration appears successful - redirected to login page"
          );
        } else if (Object.keys(validationErrors).length > 0) {
          console.log("⚠️ Registration failed with validation errors");
        } else {
          console.log("ℹ️ Registration form submitted - no immediate feedback");
        }

        testResult.duration = Date.now() - startTime;
        console.log(`Test completed in ${testResult.duration}ms`);
      } catch (error) {
        testResult.status = "failed";
        testResult.errorMessage =
          error instanceof Error ? error.message : String(error);
        testResult.duration = Date.now() - startTime;

        console.error(`❌ Test Case ${data.TestCaseID} failed:`, error);

        // Take screenshot on failure
        await page.screenshot({
          path: `test-results/screenshots/failure-${data.TestCaseID}.png`,
          fullPage: true,
        });

        throw error;
      }
    });
  }

  // Summary test to display configuration
  test("Test Configuration Summary", async ({ page }) => {
    console.log("\n=== Test Execution Summary ===");
    console.log(`Total test cases available: ${allTestData.length}`);
    console.log(`Test cases executed: ${testData.length}`);

    if (!TestConfigManager.getConfig().runAll) {
      console.log(
        `Selected test cases: ${testData.map((d) => d.TestCaseID).join(", ")}`
      );
    }

    console.log("==============================\n");

    // This test always passes - it's just for informational purposes
    expect(testData.length).toBeGreaterThan(0);
  });
});

// Optional: Export test data for external reporting
export { testData, allTestData };
