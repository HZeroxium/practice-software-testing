import { Page, Locator } from "@playwright/test";
import { RegistrationTestData } from "../types/test-data.types";

export class FormHelpers {
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
   * Submits the registration form
   */
  async submitForm(): Promise<void> {
    await this.page.click('[data-test="register-submit"]');
  }

  /**
   * Waits for form submission to complete
   * @param timeout - Maximum wait time in milliseconds
   */
  async waitForSubmissionResult(timeout: number = 10000): Promise<void> {
    try {
      // Wait for either success redirect or error message
      await Promise.race([
        this.page.waitForURL(/login/, { timeout }),
        this.page.waitForSelector('[data-test="register-error"]', { timeout }),
        this.page.waitForLoadState("networkidle", { timeout }),
      ]);
    } catch (error) {
      console.log("Form submission completed or timed out");
    }
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
   * Clears all form fields
   */
  async clearForm(): Promise<void> {
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
      await this.page.fill(field, "");
    }
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
