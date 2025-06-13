import { test, expect, Page } from "@playwright/test";
import { AdminDataReader } from "./utils/admin-add-product-data-reader";
import { AdminFormHelpers } from "./utils/admin-add-product-form-helpers";
import { AdminAuthHelper } from "./utils/admin-auth-helper";
import { AdminTestConfigManager } from "./utils/admin-add-product-test-config";
import { AdminTestResult } from "./types/admin-test-data.types";

// Load configuration from environment
AdminTestConfigManager.loadConfigFromEnvironment();

// Read and filter test data
const allTestData = AdminDataReader.readProductTestData();
const testData = AdminDataReader.filterTestData(
  allTestData,
  AdminTestConfigManager.getConfig()
);

// Print configuration
AdminTestConfigManager.printConfig();

test.describe("Admin Add Product Feature - Data Driven Tests", () => {
  let formHelpers: AdminFormHelpers;
  let authHelper: AdminAuthHelper;

  test.beforeEach(async ({ page }) => {
    formHelpers = new AdminFormHelpers(page);
    authHelper = new AdminAuthHelper(page);

    // Login as admin
    const config = AdminTestConfigManager.getConfig();
    await authHelper.loginAsAdmin(config.adminCredentials);

    // Navigate to add product page
    await authHelper.navigateToAddProduct();

    // Verify we're on the add product page
    await expect(page.locator('[data-test="page-title"]')).toContainText(
      "Add Product"
    );
  });

  // Generate a test for each data row
  for (const data of testData) {
    test(`Admin Add Product Test - ${data.TestCaseID}`, async ({ page }) => {
      const testResult: AdminTestResult = {
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

        // Replace nominal values with actual values
        const processedData = AdminDataReader.replaceNominalValues(data);
        console.log(
          "📋 Processed Test Data:",
          JSON.stringify(processedData, null, 2)
        );

        // Clear form before filling (ensure clean state)
        await formHelpers.clearForm();

        // Fill the add product form with test data
        await formHelpers.fillAddProductForm(processedData);

        // Log current form values for debugging
        const currentValues = await formHelpers.getCurrentFormValues();
        console.log("📝 Current Form Values:", currentValues);

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
        console.log("📊 Submission Result:", submissionResult);

        if (submissionResult.isSuccess) {
          console.log(
            "✅ Product creation successful - success message displayed or redirected"
          );
        } else if (submissionResult.hasValidationErrors) {
          console.log(
            "⚠️ Product creation failed with validation errors:",
            submissionResult.validationErrors
          );
        } else if (submissionResult.hasServerError) {
          console.log(
            "❌ Product creation failed with server error:",
            submissionResult.serverError
          );
        } else {
          console.log(
            "ℹ️ Product creation status unclear - requires manual verification"
          );
        }

        testResult.duration = Date.now() - startTime;
        testResult.validationErrors = submissionResult.validationErrors;
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
  test("Admin Test Configuration Summary", async ({ page }) => {
    console.log("\n╔═══════════════════════════════════════════════════════╗");
    console.log("║             Admin Test Execution Summary             ║");
    console.log("╠═══════════════════════════════════════════════════════╣");
    console.log(`║ Total test cases available: ${allTestData.length}`);
    console.log(`║ Test cases executed: ${testData.length}`);

    if (!AdminTestConfigManager.getConfig().runAll) {
      console.log(
        `║ Selected test cases: ${testData.map((d) => d.TestCaseID).join(", ")}`
      );
    }

    const config = AdminTestConfigManager.getConfig();
    console.log(`║ Admin credentials: ${config.adminCredentials?.email}`);
    console.log("║ Configuration source: TypeScript config files        ║");
    console.log("╚═══════════════════════════════════════════════════════╝\n");

    // This test always passes - it's just for informational purposes
    expect(testData.length).toBeGreaterThan(0);
  });

  // Test to verify form field existence and accessibility
  test("Admin Add Product Form Field Verification", async ({ page }) => {
    // Verify all required form fields are present
    const requiredFields = [
      '[data-test="name"]',
      '[data-test="description"]',
      '[data-test="price"]',
      '[data-test="stock"]',
      '[data-test="brand-id"]',
      '[data-test="category-id"]',
      '[data-test="product-image-id"]',
      '[data-test="location-offer"]',
      '[data-test="rental"]',
      '[data-test="product-submit"]',
    ];

    for (const field of requiredFields) {
      await expect(page.locator(field)).toBeVisible();
    }

    console.log("✅ All admin product form fields are accessible");
  });
});

// Optional: Export test data for external reporting
export { testData, allTestData };
