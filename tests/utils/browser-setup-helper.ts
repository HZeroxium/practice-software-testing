import { execSync } from "child_process";

export class BrowserSetupHelper {
  /**
   * Verifies that Playwright browsers are properly installed
   * @returns Promise<boolean> - True if browsers are available
   */
  static async verifyBrowsersInstalled(): Promise<boolean> {
    try {
      // Check if playwright command is available
      execSync("npx playwright --version", { stdio: "pipe" });

      // Try to get browser executable paths
      const result = execSync("npx playwright install --dry-run", {
        stdio: "pipe",
        encoding: "utf8",
      });

      // If dry-run shows no downloads needed, browsers are installed
      return !result.includes("to download");
    } catch (error) {
      console.error("Browser verification failed:", error);
      return false;
    }
  }

  /**
   * Installs Playwright browsers if they're missing
   */
  static async ensureBrowsersInstalled(): Promise<void> {
    const browsersInstalled = await this.verifyBrowsersInstalled();

    if (!browsersInstalled) {
      console.log("🌐 Installing missing Playwright browsers...");
      try {
        execSync("npx playwright install", { stdio: "inherit" });
        console.log("✅ Browsers installed successfully!");
      } catch (error) {
        throw new Error(`Failed to install browsers: ${error}`);
      }
    }
  }

  /**
   * Gets information about installed browsers
   */
  static async getBrowserInfo(): Promise<Record<string, string>> {
    try {
      const info = execSync("npx playwright --version", {
        encoding: "utf8",
        stdio: "pipe",
      });

      return {
        version: info.trim(),
        chromium: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH || "default",
        firefox: process.env.PLAYWRIGHT_FIREFOX_EXECUTABLE_PATH || "default",
        webkit: process.env.PLAYWRIGHT_WEBKIT_EXECUTABLE_PATH || "default",
      };
    } catch (error) {
      return {
        error: "Could not get browser information",
      };
    }
  }
}
