/**
 * Mockaroo Categories Data Generator - Main Entry Point
 *
 * This script generates realistic test data for the categories table using Mockaroo API.
 * It creates hierarchical tool categories based on real hardware store classifications
 * with proper parent-child relationships and data integrity.
 *
 * Features:
 * - Generates realistic category names from hardware store taxonomy
 * - Creates proper parent-child relationships for hierarchical structure
 * - Outputs data in CSV format for database import
 * - Uses ULID-like format for primary keys
 * - Implements comprehensive error handling and logging
 * - Modular architecture for easy maintenance and extension
 *
 * @author Software Testing Team
 * @version 2.0.0
 */

require("dotenv").config();
const path = require("path");

// Import modules
const CONFIG = require("./config");
const CategoriesGenerator = require("./generators/categories");
const {
  ensureOutputDirectory,
  writeCSVFile,
  formatDuration,
  logWithTimestamp,
} = require("./utils");
const { generateSQLFromCSV, writeSQLFile } = require("./utils/sql-generator");
const {
  promptForSQLGeneration,
  displayCompletionSummary,
} = require("./utils/prompt");

/**
 * Main execution function
 */
async function main() {
  const startTime = Date.now();

  try {
    logWithTimestamp(
      "info",
      "🚀",
      "Starting Mockaroo Categories Data Generator v2.0"
    );
    console.log("=".repeat(50));

    // Initialize generator
    const generator = new CategoriesGenerator();
    await generator.initialize();

    // Ensure output directory exists
    const outputPath = ensureOutputDirectory(
      path.join(__dirname, "..", CONFIG.OUTPUT_DIR)
    );

    // Generate categories data
    const categories = await generator.generateCategories(CONFIG.RECORDS_COUNT);

    // Validate the generated data
    generator.validateCategories(categories);

    // Convert to CSV and save
    const csvData = generator.categoriesToCSV(categories);
    const filePath = writeCSVFile(
      path.join(outputPath, CONFIG.OUTPUT_FILE),
      csvData
        .split("\n")
        .slice(1)
        .filter((line) => line.trim())
        .map((line) => {
          // Parse CSV line back to object for consistency
          const values = line.split(",");
          return {
            id: values[0] || "",
            name: values[1] || "",
            slug: values[2] || "",
            parent_id: values[3] || "",
            created_at: values[4] || "",
            updated_at: values[5] || "",
          };
        }),
      ["id", "name", "slug", "parent_id", "created_at", "updated_at"]
    );

    // Display summary
    displaySummary(filePath, categories, startTime);

    // Optional SQL generation step
    const sqlOptions = await promptForSQLGeneration();
    let sqlFilePath = null;

    if (sqlOptions) {
      try {
        logWithTimestamp("info", "🔧", "Generating SQL INSERT script...");

        const sqlScript = generateSQLFromCSV(
          filePath,
          "categories",
          sqlOptions
        );
        sqlFilePath = filePath.replace(/\.csv$/i, ".sql");

        writeSQLFile(sqlFilePath, sqlScript);

        logWithTimestamp("success", "✅", "SQL script generated successfully");
      } catch (sqlError) {
        logWithTimestamp(
          "error",
          "❌",
          `SQL generation failed: ${sqlError.message}`
        );
        console.log("⚠️  Continuing without SQL script generation");
      }
    }

    // Display final completion summary
    displayCompletionSummary({
      csvFile: filePath,
      sqlFile: sqlFilePath,
      duration: formatDuration(Date.now() - startTime),
    });
  } catch (error) {
    handleError(error);
    process.exit(1);
  }
}

/**
 * Display generation summary
 */
function displaySummary(filePath, categories, startTime) {
  const endTime = Date.now();
  const duration = formatDuration(endTime - startTime);

  console.log("\n" + "=".repeat(60));
  console.log("🎉 CATEGORIES DATA GENERATION COMPLETE");
  console.log("=".repeat(60));
  console.log(`⏱️  Total time: ${duration}`);
  console.log(`📁 Output file: ${filePath}`);
  console.log(`🎯 Records requested: ${CONFIG.RECORDS_COUNT}`);
  console.log(`📋 Records generated: ${categories.length}`);
  console.log(`🔗 Database table: categories`);
  console.log(`🌐 Data source: Mockaroo API + Local Logic`);

  // Category statistics
  const rootCategories = categories.filter(
    (cat) => !cat.parent_id || cat.parent_id === ""
  );
  const subCategories = categories.filter(
    (cat) => cat.parent_id && cat.parent_id !== ""
  );

  console.log(`� Root categories: ${rootCategories.length}`);
  console.log(`📊 Subcategories: ${subCategories.length}`);
  console.log("=".repeat(60));

  console.log("\n📋 Next steps:");
  console.log("1. Review the generated CSV file for data quality");
  console.log("2. Import data into your database using:");
  console.log(
    "   mysql> LOAD DATA INFILE 'categories.csv' INTO TABLE categories"
  );
  console.log("   OR use your preferred database import tool");
  console.log("3. Verify referential integrity:");
  console.log(
    "   - Check all parent_id values reference existing category IDs"
  );
  console.log("   - Validate hierarchical relationships");
  console.log("4. Run your tests with the new realistic data");

  console.log("\n� Quality checks performed:");
  console.log("✅ ID uniqueness validation");
  console.log("✅ Slug uniqueness validation");
  console.log("✅ Parent-child relationship integrity");
  console.log("✅ Required field validation");
  console.log("✅ Hierarchical structure validation");
}

/**
 * Handle errors with appropriate logging and user guidance
 */
function handleError(error) {
  console.log("\n❌ GENERATION FAILED");
  console.log("=".repeat(50));

  if (error.message && error.message.includes("MOCKAROO_API_KEY")) {
    logWithTimestamp("error", "🔑", "API key configuration issue");
    console.error(
      "Please ensure your .env file contains a valid MOCKAROO_API_KEY"
    );
  } else if (error.message && error.message.includes("usage limit")) {
    logWithTimestamp("error", "📊", "API usage limit exceeded");
    console.error(
      "Daily API usage limit exceeded. Please upgrade your plan or try again tomorrow."
    );
  } else if (error.message && error.message.includes("quota")) {
    logWithTimestamp("error", "🚫", "API quota exceeded");
    console.error("API quota exceeded. Please wait or upgrade your plan.");
  } else if (error.message && error.message.includes("network")) {
    logWithTimestamp("error", "🌐", "Network connectivity issue");
    console.error(
      "Network issue detected. Please check your internet connection."
    );
  } else {
    logWithTimestamp("error", "❌", `Unexpected error: ${error.message}`);
  }

  console.log("\n🔧 Troubleshooting guide:");
  console.log(
    "1. Verify your .env file contains: MOCKAROO_API_KEY=your_key_here"
  );
  console.log("2. Check your internet connection");
  console.log("3. Ensure you haven't exceeded API rate limits");
  console.log("4. Try reducing the number of records in config/index.js");
  console.log(
    "5. Check Mockaroo service status at https://status.mockaroo.com/"
  );

  if (process.env.NODE_ENV === "development") {
    console.log("\n🐛 Debug information:");
    console.error(error.stack);
  }
}

// Execute if called directly
if (require.main === module) {
  main();
}

// Export for testing and programmatic use
module.exports = {
  main,
  displaySummary,
  handleError,
  CONFIG,
};
