import { test as base } from "@playwright/test";
import { BrowserSetupHelper } from "./utils/browser-setup-helper";
import { TestConfigManager } from "./utils/registration-test-config";

/**
 * Extended test fixture that ensures proper browser setup and configuration loading
 */
export const test = base.extend({
  // Ensure browsers are installed and configuration is loaded before each test worker starts
  workerSetup: [
    async ({}, use, workerInfo) => {
      console.log(`🔧 Setting up test worker ${workerInfo.workerIndex}...`);

      // Load test configuration from TypeScript files
      TestConfigManager.loadConfigFromEnvironment();

      // Print configuration for visibility
      TestConfigManager.printConfig();

      // Verify browsers are installed
      await BrowserSetupHelper.ensureBrowsersInstalled();

      // Get browser info for debugging
      const browserInfo = await BrowserSetupHelper.getBrowserInfo();
      console.log("🌐 Browser info:", browserInfo);

      console.log(`✅ Worker ${workerInfo.workerIndex} setup complete`);
      await use("ready");
    },
    { scope: "worker" },
  ],
});

export { expect } from "@playwright/test";
