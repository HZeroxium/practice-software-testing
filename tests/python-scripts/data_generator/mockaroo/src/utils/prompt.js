/**
 * Interactive Prompt Utility
 *
 * This module provides interactive user prompts for optional features
 * like SQL script generation, using Node.js readline interface.
 *
 * @author Software Testing Team
 * @version 1.0.0
 */

const readline = require("readline");
const { logWithTimestamp } = require("./index");

/**
 * Create readline interface
 */
function createReadlineInterface() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
}

/**
 * Ask user a yes/no question
 */
function askYesNo(question, defaultAnswer = "n") {
  return new Promise((resolve) => {
    const rl = createReadlineInterface();
    const defaultHint = defaultAnswer.toLowerCase() === "y" ? "[Y/n]" : "[y/N]";

    rl.question(`${question} ${defaultHint}: `, (answer) => {
      rl.close();

      const normalizedAnswer = answer.toLowerCase().trim();

      if (normalizedAnswer === "") {
        resolve(defaultAnswer.toLowerCase() === "y");
      } else {
        resolve(normalizedAnswer === "y" || normalizedAnswer === "yes");
      }
    });
  });
}

/**
 * Ask user to select from multiple options
 */
function askMultipleChoice(question, options, defaultIndex = 0) {
  return new Promise((resolve) => {
    const rl = createReadlineInterface();

    console.log(`\n${question}`);
    options.forEach((option, index) => {
      const marker = index === defaultIndex ? "→" : " ";
      console.log(`${marker} ${index + 1}. ${option}`);
    });

    rl.question(
      `\nEnter your choice (1-${options.length}) [${defaultIndex + 1}]: `,
      (answer) => {
        rl.close();

        const choice = parseInt(answer.trim()) || defaultIndex + 1;
        const selectedIndex = Math.max(1, Math.min(options.length, choice)) - 1;

        resolve({
          index: selectedIndex,
          value: options[selectedIndex],
        });
      }
    );
  });
}

/**
 * Ask user for text input
 */
function askText(question, defaultValue = "") {
  return new Promise((resolve) => {
    const rl = createReadlineInterface();
    const defaultHint = defaultValue ? ` [${defaultValue}]` : "";

    rl.question(`${question}${defaultHint}: `, (answer) => {
      rl.close();
      resolve(answer.trim() || defaultValue);
    });
  });
}

/**
 * Display a formatted message with emojis
 */
function displayMessage(type, message) {
  const icons = {
    info: "ℹ️",
    success: "✅",
    warning: "⚠️",
    error: "❌",
    question: "❓",
  };

  const icon = icons[type] || "📝";
  console.log(`${icon} ${message}`);
}

/**
 * Show progress indicator
 */
function showProgress(message) {
  process.stdout.write(`⏳ ${message}...`);
}

/**
 * Clear progress indicator
 */
function clearProgress() {
  process.stdout.write("\r");
}

/**
 * Interactive SQL generation workflow
 */
async function promptForSQLGeneration() {
  try {
    console.log("\n" + "=".repeat(50));
    console.log("🔧 OPTIONAL: SQL INSERT Script Generation");
    console.log("=".repeat(50));

    const generateSQL = await askYesNo(
      "Would you like to generate SQL INSERT script for database import?",
      "n"
    );

    if (!generateSQL) {
      displayMessage("info", "Skipping SQL script generation");
      return null;
    }

    // Ask for database type
    const dbOptions = ["MySQL", "PostgreSQL", "SQLite"];
    const dbChoice = await askMultipleChoice(
      "Select your database type:",
      dbOptions,
      0
    );

    // Ask for additional options
    const includeTransactions = await askYesNo(
      "Include transaction wrapper (START TRANSACTION/COMMIT)?",
      "y"
    );

    const onDuplicateUpdate = await askYesNo(
      "Include ON DUPLICATE KEY UPDATE clause (MySQL only)?",
      "n"
    );

    const batchSizeText = await askText(
      "Batch size for INSERT statements",
      "100"
    );

    const batchSize = parseInt(batchSizeText) || 100;

    return {
      dbType: dbChoice.value.toLowerCase(),
      includeTransactions,
      onDuplicateUpdate,
      batchSize,
      includeComments: true,
    };
  } catch (error) {
    logWithTimestamp(
      "error",
      "❌",
      `Error in SQL generation prompt: ${error.message}`
    );
    return null;
  }
}

/**
 * Confirmation prompt for file operations
 */
async function confirmFileOperation(operation, filePath) {
  const confirm = await askYesNo(`Confirm ${operation} to: ${filePath}?`, "y");

  return confirm;
}

/**
 * Display completion summary
 */
function displayCompletionSummary(results) {
  console.log("\n" + "=".repeat(50));
  console.log("🎉 GENERATION COMPLETE");
  console.log("=".repeat(50));

  if (results.csvFile) {
    console.log(`📄 CSV file: ${results.csvFile}`);
  }

  if (results.sqlFile) {
    console.log(`💽 SQL file: ${results.sqlFile}`);
  }

  console.log(`⏱️ Total time: ${results.duration || "N/A"}`);
  console.log("=".repeat(50));
}

module.exports = {
  askYesNo,
  askMultipleChoice,
  askText,
  displayMessage,
  showProgress,
  clearProgress,
  promptForSQLGeneration,
  confirmFileOperation,
  displayCompletionSummary,
};
