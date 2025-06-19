// tests/utils/admin-auth-helper.ts

import { Page } from "@playwright/test";

export class AdminAuthHelper {
  private static readonly DEFAULT_ADMIN_CREDENTIALS = {
    email: "admin@practicesoftwaretesting.com",
    password: "welcome01",
  };

  constructor(private page: Page) {}

  /**
   * Performs admin login
   * @param credentials - Admin credentials (optional, uses default if not provided)
   */
  async loginAsAdmin(credentials?: {
    email: string;
    password: string;
  }): Promise<void> {
    const creds = credentials || AdminAuthHelper.DEFAULT_ADMIN_CREDENTIALS;

    // Navigate to login page
    await this.page.goto("/#/auth/login");
    await this.page.waitForLoadState("networkidle");

    // Fill login form
    await this.page.fill('[data-test="email"]', creds.email);
    await this.page.fill('[data-test="password"]', creds.password);

    // Submit login form
    await this.page.click('[data-test="login-submit"]');

    // Wait for navigation to admin dashboard
    await this.page.waitForURL(/admin\/dashboard/, { timeout: 10000 });
    await this.page.waitForLoadState("networkidle");
  }

  /**
   * Navigates to admin products add page
   */
  async navigateToAddProduct(): Promise<void> {
    // Navigate to admin products page first
    await this.page.goto("/#/admin/products");
    await this.page.waitForLoadState("networkidle");

    // Click on Add Product button
    await this.page.click('[data-test="product-add"]');
    await this.page.waitForLoadState("networkidle");

    // Verify we're on the add product page
    await this.page.waitForSelector(
      '[data-test="page-title"]:has-text("Add Product")'
    );
  }

  /**
   * Checks if user is authenticated as admin
   * @returns True if authenticated as admin
   */
  async isAuthenticatedAsAdmin(): Promise<boolean> {
    try {
      await this.page.goto("/#/admin/dashboard");
      await this.page.waitForSelector('[data-test="page-title"]', {
        timeout: 5000,
      });
      const title = await this.page.textContent('[data-test="page-title"]');
      return title?.includes("Dashboard") || false;
    } catch {
      return false;
    }
  }

  /**
   * Logs out the admin user
   */
  async logout(): Promise<void> {
    try {
      // Look for logout link or user menu
      const logoutButton = this.page
        .locator("text=Logout")
        .or(this.page.locator('[data-test="logout"]'));
      if (await logoutButton.isVisible({ timeout: 2000 })) {
        await logoutButton.click();
        await this.page.waitForURL(/auth\/login/, { timeout: 5000 });
      }
    } catch {
      // If logout fails, clear storage and navigate to login
      await this.page.evaluate(() => {
        localStorage.clear();
        sessionStorage.clear();
      });
      await this.page.goto("/#/auth/login");
    }
  }
}
