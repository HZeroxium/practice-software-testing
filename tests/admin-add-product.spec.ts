import { test, expect, Page } from "@playwright/test";
import { AdminDataReader } from "./utils/admin-data-reader";
import { AdminFormHelpers } from "./utils/admin-form-helpers";
import { AdminAuthHelper } from "./utils/admin-auth-helper";
import { AdminTestConfigManager } from "./utils/admin-test-config";
import {
  AddProductTestData,
  AdminTestResult,
} from "./types/admin-test-data.types";

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

  test.afterEach(async ({ page }) => {
    // Take a screenshot after each test
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    await page.screenshot({
      path: `test-results/screenshots/admin-product-${timestamp}.png`,
      fullPage: true,
    });
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
          `\n=== Executing Admin Product Test Case: ${data.TestCaseID} ===`
        );

        // Replace nominal values with actual values
        const processedData = AdminDataReader.replaceNominalValues(data);
        console.log(
          "Processed Test Data:",
          JSON.stringify(processedData, null, 2)
        );

        // Clear form before filling (ensure clean state)
        await formHelpers.clearForm();

        // Fill the add product form with test data
        await formHelpers.fillAddProductForm(processedData);

        // Take screenshot before submission
        await page.screenshot({
          path: `test-results/screenshots/before-submit-${data.TestCaseID}.png`,
          fullPage: true,
        });

        // Log current form values for debugging
        const currentValues = await formHelpers.getCurrentFormValues();
        console.log("Current Form Values:", currentValues);

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

        // Get success messages (if any)
        const successMessages = await formHelpers.getSuccessMessages();

        if (Object.keys(validationErrors).length > 0) {
          console.log("Validation Errors Found:", validationErrors);
          testResult.validationErrors = validationErrors;
        }

        if (successMessages.length > 0) {
          console.log("Success Messages:", successMessages);
        }

        // Check current URL and page state to determine result
        const currentUrl = page.url();

        if (successMessages.some((msg) => msg.includes("saved"))) {
          console.log(
            "✅ Product creation appears successful - success message displayed"
          );
        } else if (Object.keys(validationErrors).length > 0) {
          console.log("⚠️ Product creation failed with validation errors");
        } else if (
          currentUrl.includes("/admin/products") &&
          !currentUrl.includes("/add")
        ) {
          console.log(
            "✅ Product creation appears successful - redirected to products list"
          );
        } else {
          console.log("ℹ️ Product form submitted - awaiting result analysis");
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

  // Test to verify admin authentication
  test("Admin Authentication Verification", async ({ page }) => {
    const isAuthenticated = await authHelper.isAuthenticatedAsAdmin();
    expect(isAuthenticated).toBe(true);

    // Verify admin can access products page
    await page.goto("/#/admin/products");
    await expect(page.locator('[data-test="page-title"]')).toContainText(
      "Products"
    );
  });

  // Summary test to display configuration
  test("Admin Test Configuration Summary", async ({ page }) => {
    console.log("\n=== Admin Product Test Execution Summary ===");
    console.log(`Total test cases available: ${allTestData.length}`);
    console.log(`Test cases executed: ${testData.length}`);

    if (!AdminTestConfigManager.getConfig().runAll) {
      console.log(
        `Selected test cases: ${testData.map((d) => d.TestCaseID).join(", ")}`
      );
    }

    const config = AdminTestConfigManager.getConfig();
    console.log(`Admin credentials: ${config.adminCredentials?.email}`);
    console.log("==========================================\n");

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
