const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

/**
 * Setup script for Playwright browsers and dependencies
 * This ensures all required browsers are installed before running tests
 */

console.log("🎭 Setting up Playwright browsers...");

try {
  // Check if Playwright is installed
  console.log("📋 Checking Playwright installation...");
  execSync("npx playwright --version", { stdio: "inherit" });

  // Install system dependencies (Linux/Ubuntu)
  if (process.platform === "linux") {
    console.log("🔧 Installing system dependencies...");
    try {
      execSync("npx playwright install-deps", { stdio: "inherit" });
    } catch (error) {
      console.warn(
        "⚠️ Could not install system dependencies. You may need to run with sudo."
      );
    }
  }

  // Install browsers
  console.log("🌐 Installing browsers...");
  execSync("npx playwright install", { stdio: "inherit" });

  // Verify browser installation
  console.log("✅ Verifying browser installation...");

  const browserPaths = {
    chromium: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH,
    firefox: process.env.PLAYWRIGHT_FIREFOX_EXECUTABLE_PATH,
    webkit: process.env.PLAYWRIGHT_WEBKIT_EXECUTABLE_PATH,
  };

  console.log("🎯 Playwright setup completed successfully!");
  console.log("📝 Available commands:");
  console.log("  npm run test:registration          - Run registration tests");
  console.log("  npm run test:admin-product         - Run admin product tests");
  console.log(
    "  npm run test:registration:headed   - Run with visible browser"
  );
  console.log("  npm run test:ui                    - Run with Playwright UI");
} catch (error) {
  console.error("❌ Playwright setup failed:", error.message);
  console.log("\n🔧 Troubleshooting steps:");
  console.log("1. Ensure you have a stable internet connection");
  console.log("2. Try running: npm install");
  console.log("3. Try running: npx playwright install --force");
  console.log("4. Check if you have sufficient disk space");
  console.log("5. On Windows, try running as Administrator");

  process.exit(1);
}
