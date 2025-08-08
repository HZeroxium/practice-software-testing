// tests/utils/registration-form-helpers.ts

import { Page } from "@playwright/test";
import { RegistrationTestData } from "../types/registration-test-data.types";

export interface RegistrationSubmissionResult {
  isSuccess: boolean;
  hasValidationErrors: boolean;
  hasServerError: boolean;
  validationErrors: Record<string, string[]>;
  serverError?: string;
  currentUrl: string;
  redirected: boolean;
}

export class RegistrationFormHelpers {
  constructor(private page: Page) {}

  /**
   * Fills the registration form with provided data
   * @param data - Registration test data
   */
  async fillRegistrationForm(data: RegistrationTestData): Promise<void> {
    // Fill First Name
    if (data.FirstName !== undefined) {
      await this.page.fill('[data-test="first-name"]', data.FirstName);
    }

    // Fill Last Name
    if (data.LastName !== undefined) {
      await this.page.fill('[data-test="last-name"]', data.LastName);
    }

    // Fill Date of Birth
    if (data.DOB !== undefined && data.DOB !== "") {
      const formattedDOB = this.formatDateForInput(data.DOB);
      await this.page.fill('[data-test="dob"]', formattedDOB);
    }

    // Fill Address
    if (data.Street !== undefined) {
      await this.page.fill('[data-test="address"]', data.Street);
    }

    // Fill Postal Code
    if (data.PostalCode !== undefined) {
      await this.page.fill('[data-test="postcode"]', data.PostalCode);
    }

    // Fill City
    if (data.City !== undefined) {
      await this.page.fill('[data-test="city"]', data.City);
    }

    // Fill State
    if (data.State !== undefined) {
      await this.page.fill('[data-test="state"]', data.State);
    }

    // Select Country
    if (data.Country !== undefined && data.Country !== "") {
      await this.page.selectOption('[data-test="country"]', data.Country);
    }

    // Fill Phone
    if (data.Phone !== undefined) {
      await this.page.fill('[data-test="phone"]', data.Phone);
    }

    // Fill Email
    if (data.Email !== undefined) {
      await this.page.fill('[data-test="email"]', data.Email);
    }

    // Fill Password
    if (data.Password !== undefined) {
      await this.page.fill(
        'app-password-input input[type="password"], app-password-input input[type="text"]',
        data.Password
      );
    }
  }

  /**
   * Submits the form and waits for initial response
   */
  async submitFormAndWait(): Promise<void> {
    console.log("📝 Submitting registration form...");

    // Get initial URL for comparison
    const initialUrl = this.page.url();

    // Submit the form
    await this.page.click('[data-test="register-submit"]');

    // Wait for form submission to be processed
    // This gives the server time to process the request
    await this.page.waitForTimeout(1000); // Initial wait for form submission

      try {
        // Wait for one of several possible outcomes
        await Promise.race([
          // Success: Redirect to login page
          this.page.waitForURL(/login/, { timeout: 8000 }),
          // Error: Server error message appears
          this.page.waitForSelector('[data-test="register-error"]', {
            timeout: 8000,
          }),
          // Validation: Field-level errors appear
          this.page.waitForSelector('[class*="error"], [data-test*="-error"]', {
            timeout: 8000,
          }),
          // Network: Wait for network to be idle
          this.page.waitForLoadState("networkidle", { timeout: 8000 }),
        ]);
      } catch (timeoutError) {
        console.log(
          "⏱️ Submission wait timed out - continuing with current state"
        );
      }

    // Additional wait to ensure UI has updated
    await this.page.waitForTimeout(1500);

    const currentUrl = this.page.url();
    console.log(`🌐 URL changed from ${initialUrl} to ${currentUrl}`);
  }

  /**
   * Gets comprehensive submission result information
   */
  async getSubmissionResult(): Promise<RegistrationSubmissionResult> {
    const currentUrl = this.page.url();
    const initialUrl = "register"; // Expected to contain this initially
    const redirected = !currentUrl.includes(initialUrl);

    // Check for success (redirect to login)
    const isSuccess = currentUrl.includes("login");

    // Get validation errors
    const validationErrors = await this.getValidationErrors();
    const hasValidationErrors = Object.keys(validationErrors).length > 0;

    // Check for server errors
    let serverError: string | undefined;
    let hasServerError = false;

    try {
      const serverErrorElement = await this.page
        .locator('[data-test="register-error"]')
        .first();
      if (await serverErrorElement.isVisible({ timeout: 1000 })) {
        serverError = (await serverErrorElement.textContent()) || undefined;
        hasServerError = !!serverError;
      }
    } catch (error) {
      // No server error element found
    }

    // Also check for any visible error messages in the page
    if (!hasServerError) {
      try {
        const errorElements = await this.page
          .locator('.alert-danger, .error-message, [class*="error"]')
          .all();
        for (const element of errorElements) {
          if (await element.isVisible()) {
            const errorText = await element.textContent();
            if (errorText && errorText.trim()) {
              serverError = errorText.trim();
              hasServerError = true;
              break;
            }
          }
        }
      } catch (error) {
        // No additional error elements found
      }
    }

    return {
      isSuccess,
      hasValidationErrors,
      hasServerError,
      validationErrors,
      serverError,
      currentUrl,
      redirected,
    };
  }

  /**
   * Checks if there are validation errors on the form
   * @returns Object containing error information
   */
  async getValidationErrors(): Promise<Record<string, string[]>> {
    const errors: Record<string, string[]> = {};

    const errorSelectors = [
      { field: "firstName", selector: '[data-test="first-name-error"]' },
      { field: "lastName", selector: '[data-test="last-name-error"]' },
      { field: "dob", selector: '[data-test="dob-error"]' },
      { field: "address", selector: '[data-test="address-error"]' },
      { field: "postcode", selector: '[data-test="postcode-error"]' },
      { field: "city", selector: '[data-test="city-error"]' },
      { field: "state", selector: '[data-test="state-error"]' },
      { field: "country", selector: '[data-test="country-error"]' },
      { field: "phone", selector: '[data-test="phone-error"]' },
      { field: "email", selector: '[data-test="email-error"]' },
      { field: "password", selector: '[data-test="password-error"]' },
      { field: "general", selector: '[data-test="register-error"]' },
    ];

    for (const { field, selector } of errorSelectors) {
      const errorElements = await this.page.locator(selector).all();
      if (errorElements.length > 0) {
        errors[field] = [];
        for (const element of errorElements) {
          const text = await element.textContent();
          if (text && text.trim()) {
            errors[field].push(text.trim());
          }
        }
      }
    }

    return errors;
  }

  /**
   * Clears all form fields with better error handling
   */
  async clearForm(): Promise<void> {
    console.log("🧹 Clearing registration form...");

    const fields = [
      '[data-test="first-name"]',
      '[data-test="last-name"]',
      '[data-test="dob"]',
      '[data-test="address"]',
      '[data-test="postcode"]',
      '[data-test="city"]',
      '[data-test="state"]',
      '[data-test="phone"]',
      '[data-test="email"]',
      "app-password-input input",
    ];

    for (const field of fields) {
      try {
        await this.page.fill(field, "");
      } catch (error) {
        // Continue clearing other fields even if one fails
        console.log(`⚠️ Could not clear field ${field}: ${error}`);
      }
    }

    // Reset country dropdown to default
    try {
      await this.page.selectOption('[data-test="country"]', "");
    } catch (error) {
      console.log("⚠️ Could not reset country dropdown");
    }

    console.log("✅ Form cleared");
  }

  /**
   * Formats date string for HTML date input
   * @param dateStr - Date string from test data
   * @returns Formatted date string (YYYY-MM-DD)
   */
  private formatDateForInput(dateStr: string): string {
    if (!dateStr || dateStr === "(empty)") return "";

    // Handle different date formats
    let date: Date;

    // Try parsing MM/DD/YYYY format
    if (dateStr.includes("/")) {
      const parts = dateStr.split("/");
      if (parts.length === 3) {
        const month = parseInt(parts[0]) - 1; // Month is 0-indexed in Date constructor
        const day = parseInt(parts[1]);
        const year = parseInt(parts[2]);
        date = new Date(year, month, day);
      } else {
        return dateStr; // Return as-is if format is unexpected
      }
    } else {
      date = new Date(dateStr);
    }

    // Check if date is valid
    if (isNaN(date.getTime())) {
      return dateStr; // Return original string if invalid
    }

    // Format as YYYY-MM-DD
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  }
}
