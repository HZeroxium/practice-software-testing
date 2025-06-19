// tests/utils/admin-add-product-form-helpers.ts

import { Page } from "@playwright/test";
import { AddProductTestData } from "../types/admin-test-data.types";

export interface AdminSubmissionResult {
  isSuccess: boolean;
  hasValidationErrors: boolean;
  hasServerError: boolean;
  validationErrors: Record<string, string[]>;
  serverError?: string;
  currentUrl: string;
  redirected: boolean;
}

export class AdminAddProductFormHelpers {
  constructor(private page: Page) {}

  /**
   * Fills the add product form with provided data
   * @param data - Product test data
   */
  async fillAddProductForm(data: AddProductTestData): Promise<void> {
    // Fill Product Name
    if (data.Name !== undefined && data.Name !== "") {
      await this.page.fill('[data-test="name"]', data.Name);
    } else if (data.Name === "") {
      await this.page.fill('[data-test="name"]', "");
    }

    // Fill Description
    if (data.Description !== undefined && data.Description !== "") {
      await this.page.fill('[data-test="description"]', data.Description);
    } else if (data.Description === "") {
      await this.page.fill('[data-test="description"]', "");
    }

    // Fill Price
    if (data.Price !== undefined && data.Price !== "") {
      await this.page.fill('[data-test="price"]', data.Price);
    } else if (data.Price === "") {
      await this.page.fill('[data-test="price"]', "");
    }

    // Fill Stock
    if (data.Stock !== undefined && data.Stock !== "") {
      await this.page.fill('[data-test="stock"]', data.Stock);
    } else if (data.Stock === "") {
      await this.page.fill('[data-test="stock"]', "");
    }

    // Set Location Offer checkbox
    await this.setCheckbox(
      '[data-test="location-offer"]',
      data.LocationOffer === "on"
    );

    // Set Rental checkbox
    await this.setCheckbox('[data-test="rental"]', data.Rental === "on");

    // Select Brand (if not empty)
    if (data.Brand !== undefined && data.Brand !== "") {
      await this.page.selectOption('[data-test="brand-id"]', data.Brand);
    }

    // Select Category (if not empty)
    if (data.Category !== undefined && data.Category !== "") {
      await this.page.selectOption('[data-test="category-id"]', data.Category);
    }

    // Select Product Image (if not empty)
    if (data.ProductImage !== undefined && data.ProductImage !== "") {
      await this.page.selectOption(
        '[data-test="product-image-id"]',
        data.ProductImage
      );
    }
  }

  /**
   * Submits the product form
   */
  async submitForm(): Promise<void> {
    await this.page.click('[data-test="product-submit"]');
  }

  /**
   * Waits for form submission to complete
   * @param timeout - Maximum wait time in milliseconds
   */
  async waitForSubmissionResult(timeout: number = 15000): Promise<void> {
    try {
      // Wait for either success message, error message, or form validation
      await Promise.race([
        this.page.waitForSelector(".alert-success", { timeout }),
        this.page.waitForSelector(".alert-danger", { timeout }),
        this.page.waitForSelector(".is-invalid", { timeout }),
        this.page.waitForLoadState("networkidle", { timeout: 5000 }),
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
      {
        field: "name",
        selector:
          '[data-test="name"] + .alert-danger, .alert-danger:has-text("Name")',
      },
      {
        field: "description",
        selector:
          '[data-test="description"] + .alert-danger, .alert-danger:has-text("Description")',
      },
      {
        field: "price",
        selector:
          '[data-test="price"] + .alert-danger, .alert-danger:has-text("Price")',
      },
      {
        field: "stock",
        selector:
          '[data-test="stock"] + .alert-danger, .alert-danger:has-text("Stock"), .alert-danger:has-text("Quantity")',
      },
      {
        field: "brand",
        selector:
          '[data-test="brand-id"] + .alert-danger, .alert-danger:has-text("Brand")',
      },
      {
        field: "category",
        selector:
          '[data-test="category-id"] + .alert-danger, .alert-danger:has-text("Category")',
      },
      {
        field: "image",
        selector:
          '[data-test="product-image-id"] + .alert-danger, .alert-danger:has-text("Image")',
      },
      { field: "general", selector: ".alert-danger" },
    ];

    for (const { field, selector } of errorSelectors) {
      try {
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
      } catch {
        // Ignore errors when checking for validation messages
      }
    }

    return errors;
  }

  /**
   * Gets success messages from the form
   * @returns Array of success messages
   */
  async getSuccessMessages(): Promise<string[]> {
    const messages: string[] = [];

    try {
      const successElements = await this.page.locator(".alert-success").all();
      for (const element of successElements) {
        const text = await element.textContent();
        if (text && text.trim()) {
          messages.push(text.trim());
        }
      }
    } catch {
      // Ignore errors when checking for success messages
    }

    return messages;
  }

  /**
   * Clears all form fields
   */
  async clearForm(): Promise<void> {
    const fields = [
      '[data-test="name"]',
      '[data-test="description"]',
      '[data-test="price"]',
      '[data-test="stock"]',
    ];

    for (const field of fields) {
      try {
        await this.page.fill(field, "");
      } catch {
        // Ignore if field doesn't exist or can't be cleared
      }
    }

    // Reset dropdowns to default
    const dropdowns = [
      '[data-test="brand-id"]',
      '[data-test="category-id"]',
      '[data-test="product-image-id"]',
    ];

    for (const dropdown of dropdowns) {
      try {
        await this.page.selectOption(dropdown, "");
      } catch {
        // Ignore if dropdown doesn't exist or can't be reset
      }
    }

    // Uncheck checkboxes
    await this.setCheckbox('[data-test="location-offer"]', false);
    await this.setCheckbox('[data-test="rental"]', false);
  }

  /**
   * Helper method to set checkbox state
   * @param selector - Checkbox selector
   * @param checked - Whether checkbox should be checked
   */
  private async setCheckbox(selector: string, checked: boolean): Promise<void> {
    try {
      const checkbox = this.page.locator(selector);
      const isChecked = await checkbox.isChecked();

      if (checked !== isChecked) {
        await checkbox.click();
      }
    } catch {
      // Ignore if checkbox doesn't exist
    }
  }

  /**
   * Gets current form values for debugging
   * @returns Object with current form values
   */
  async getCurrentFormValues(): Promise<Record<string, string>> {
    const values: Record<string, string> = {};

    try {
      values.name = (await this.page.inputValue('[data-test="name"]')) || "";
      values.description =
        (await this.page.inputValue('[data-test="description"]')) || "";
      values.price = (await this.page.inputValue('[data-test="price"]')) || "";
      values.stock = (await this.page.inputValue('[data-test="stock"]')) || "";
      values.brand =
        (await this.page.inputValue('[data-test="brand-id"]')) || "";
      values.category =
        (await this.page.inputValue('[data-test="category-id"]')) || "";
      values.productImage =
        (await this.page.inputValue('[data-test="product-image-id"]')) || "";
      values.locationOffer = (
        await this.page.isChecked('[data-test="location-offer"]')
      ).toString();
      values.rental = (
        await this.page.isChecked('[data-test="rental"]')
      ).toString();
    } catch (error) {
      console.log("Error getting form values:", error);
    }

    return values;
  }

  /**
   * Submits the form and waits for initial response
   */
  async submitFormAndWait(): Promise<void> {
    console.log("📝 Submitting admin product form...");

    // Get initial URL for comparison
    const initialUrl = this.page.url();

    // Submit the form
    await this.page.click('[data-test="product-submit"]');

    // Wait for form submission to be processed
    // This gives the server time to process the request
    await this.page.waitForTimeout(1000); // Initial wait for form submission

    try {
      // Wait for one of several possible outcomes
      await Promise.race([
        // Success: Success message appears
        this.page.waitForSelector(".alert-success", { timeout: 8000 }),
        // Error: Server error message appears
        this.page.waitForSelector(".alert-danger", { timeout: 8000 }),
        // Validation: Field-level errors appear
        this.page.waitForSelector(".is-invalid, [class*='error']", {
          timeout: 8000,
        }),
        // Redirect: URL change (to products list)
        this.page.waitForURL(/admin\/products/, { timeout: 8000 }),
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
  async getSubmissionResult(): Promise<AdminSubmissionResult> {
    const currentUrl = this.page.url();
    const initialUrlPattern = "add"; // Expected to contain this initially
    const redirected = !currentUrl.includes(initialUrlPattern);

    // Check for success (redirect to products list or success message)
    const isSuccessRedirect =
      currentUrl.includes("/admin/products") && !currentUrl.includes("/add");
    const successMessages = await this.getSuccessMessages();
    const isSuccess = isSuccessRedirect || successMessages.length > 0;

    // Get validation errors
    const validationErrors = await this.getValidationErrors();
    const hasValidationErrors = Object.keys(validationErrors).length > 0;

    // Check for server errors
    let serverError: string | undefined;
    let hasServerError = false;

    try {
      const serverErrorElements = await this.page
        .locator('.alert-danger:not([data-test*="-error"])')
        .all();

      for (const element of serverErrorElements) {
        if (await element.isVisible({ timeout: 1000 })) {
          const errorText = await element.textContent();
          if (errorText && errorText.trim()) {
            serverError = errorText.trim();
            hasServerError = true;
            break;
          }
        }
      }
    } catch (error) {
      // No server error element found
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
}
