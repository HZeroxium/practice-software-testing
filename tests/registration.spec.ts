// tests/registration.spec.ts

import { test, expect } from "@playwright/test";
import { RegistrationDataReader } from "./utils/registration-data-reader";
import { RegistrationFormHelpers } from "./utils/registration-form-helpers";
import { TestConfigManager } from "./utils/registration-test-config";
import { RegistrationTestResult } from "./types/registration-test-data.types";

// Load configuration from TypeScript files (with optional environment override)
TestConfigManager.loadConfigFromEnvironment();

// Read and filter test data
const allTestData = RegistrationDataReader.readTestData();
const testData = RegistrationDataReader.filterTestData(
  allTestData,
  TestConfigManager.getConfig()
);

// Print configuration
TestConfigManager.printConfig();

test.describe("Registration Feature - Data Driven Tests", () => {
  let formHelpers: RegistrationFormHelpers;

  test.beforeEach(async ({ page }) => {
    formHelpers = new RegistrationFormHelpers(page);

    // Navigate to registration page
    await page.goto("/#/auth/register");
    await page.waitForLoadState("networkidle");

    // Verify we're on the registration page
    await expect(page.locator('[data-test="register-form"]')).toBeVisible();
  });

  // Generate a test for each data row
  for (const data of testData) {
    test(`Registration Test - ${data.TestCaseID}`, async ({ page }) => {
      const testResult: RegistrationTestResult = {
        testCaseId: data.TestCaseID,
        status: "passed",
      };

      const startTime = Date.now();

      try {
        console.log(
          `\n╔══════ Executing Test Case: ${data.TestCaseID} ══════╗`
        );
        console.log("║ Test Data:", JSON.stringify(data, null, 2));
        console.log(
          "╚═══════════════════════════════════════════════════════╝"
        );

        // Clear form before filling (ensure clean state)
        await formHelpers.clearForm();

        // Fill the registration form with test data
        await formHelpers.fillRegistrationForm(data);

        // Take screenshot before submission
        await page.screenshot({
          path: `test-results/screenshots/before-submit/${data.TestCaseID}.png`,
          fullPage: true,
        });

        // Submit the form and wait for initial response
        await formHelpers.submitFormAndWait();

        // Take screenshot after submission with proper wait
        await page.screenshot({
          path: `test-results/screenshots/after-submit/${data.TestCaseID}.png`,
          fullPage: true,
        });

        // Get final submission status
        const submissionResult = await formHelpers.getSubmissionResult();

        // Log the results
        console.log("Submission Result:", submissionResult);

        if (submissionResult.isSuccess) {
          console.log("✅ Registration successful - redirected to login page");
        } else if (submissionResult.hasValidationErrors) {
          console.log(
            "⚠️ Registration failed with validation errors:",
            submissionResult.validationErrors
          );
        } else if (submissionResult.hasServerError) {
          console.log(
            "❌ Registration failed with server error:",
            submissionResult.serverError
          );
        } else {
          console.log(
            "ℹ️ Registration status unclear - requires manual verification"
          );
        }

        testResult.duration = Date.now() - startTime;
        console.log(
          `✅ Test ${data.TestCaseID} completed in ${testResult.duration}ms`
        );
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
    console.log("\n╔═══════════════════════════════════════════════════════╗");
    console.log("║              Test Execution Summary                   ║");
    console.log("╠═══════════════════════════════════════════════════════╣");
    console.log(`║ Total test cases available: ${allTestData.length}`);
    console.log(`║ Test cases executed: ${testData.length}`);

    if (!TestConfigManager.getConfig().runAll) {
      console.log(
        `║ Selected test cases: ${testData.map((d) => d.TestCaseID).join(", ")}`
      );
    }

    console.log("║ Configuration source: TypeScript config files        ║");
    console.log("╚═══════════════════════════════════════════════════════╝\n");

    // This test always passes - it's just for informational purposes
    expect(testData.length).toBeGreaterThan(0);
  });
});

// Optional: Export test data for external reporting
export { testData, allTestData };
