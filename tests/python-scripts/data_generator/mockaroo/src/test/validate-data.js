/**
 * Data Validation Test Script
 *
 * This script validates the generated categories.csv file to ensure
 * data integrity and proper parent-child relationships.
 *
 * @author Software Testing Team
 * @version 1.0.0
 */

const fs = require("fs");
const path = require("path");

/**
 * Parse CSV file and return array of objects
 */
function parseCSV(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const lines = content.trim().split("\n");
  const headers = lines[0].split(",");

  return lines.slice(1).map((line) => {
    const values = line.split(",");
    const obj = {};
    headers.forEach((header, index) => {
      obj[header] = values[index] || "";
    });
    return obj;
  });
}

/**
 * Validate categories data
 */
function validateCategories(categories) {
  const errors = [];
  const warnings = [];
  const ids = new Set();
  const slugs = new Set();

  console.log("🔍 Starting comprehensive data validation...\n");

  // Basic validation
  categories.forEach((category, index) => {
    const rowNum = index + 2; // +2 because we start from row 2 (after header)

    // Required fields
    if (!category.id) errors.push(`Row ${rowNum}: Missing ID`);
    if (!category.name) errors.push(`Row ${rowNum}: Missing name`);
    if (!category.slug) errors.push(`Row ${rowNum}: Missing slug`);

    // ID uniqueness
    if (category.id) {
      if (ids.has(category.id)) {
        errors.push(`Row ${rowNum}: Duplicate ID "${category.id}"`);
      }
      ids.add(category.id);
    }

    // Slug uniqueness
    if (category.slug) {
      if (slugs.has(category.slug)) {
        errors.push(`Row ${rowNum}: Duplicate slug "${category.slug}"`);
      }
      slugs.add(category.slug);
    }

    // Slug format validation
    if (category.slug && !/^[a-z0-9-]+$/.test(category.slug)) {
      warnings.push(
        `Row ${rowNum}: Slug "${category.slug}" contains invalid characters`
      );
    }

    // Date format validation
    const dateRegex = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;
    if (category.created_at && !dateRegex.test(category.created_at)) {
      errors.push(
        `Row ${rowNum}: Invalid created_at format "${category.created_at}"`
      );
    }
    if (category.updated_at && !dateRegex.test(category.updated_at)) {
      errors.push(
        `Row ${rowNum}: Invalid updated_at format "${category.updated_at}"`
      );
    }
  });

  // Parent-child relationship validation
  categories.forEach((category, index) => {
    const rowNum = index + 2;

    if (category.parent_id && category.parent_id !== "") {
      const parentExists = categories.some(
        (cat) => cat.id === category.parent_id
      );
      if (!parentExists) {
        errors.push(
          `Row ${rowNum}: Invalid parent_id "${category.parent_id}" - no matching category found`
        );
      }

      // Check for circular references (category cannot be parent of itself)
      if (category.parent_id === category.id) {
        errors.push(
          `Row ${rowNum}: Category "${category.id}" cannot be parent of itself`
        );
      }
    }
  });

  // Hierarchy analysis
  const rootCategories = categories.filter(
    (cat) => !cat.parent_id || cat.parent_id === ""
  );
  const childCategories = categories.filter(
    (cat) => cat.parent_id && cat.parent_id !== ""
  );

  console.log("📊 Data Statistics:");
  console.log(`   Total categories: ${categories.length}`);
  console.log(`   Root categories: ${rootCategories.length}`);
  console.log(`   Child categories: ${childCategories.length}`);
  console.log(`   Unique IDs: ${ids.size}`);
  console.log(`   Unique slugs: ${slugs.size}\n`);

  // Display hierarchy
  console.log("🌳 Category Hierarchy:");
  rootCategories.forEach((root) => {
    console.log(`   📁 ${root.name} (${root.id})`);
    const children = categories.filter((cat) => cat.parent_id === root.id);
    children.forEach((child) => {
      console.log(`      └── 📄 ${child.name} (${child.id})`);
    });
  });
  console.log();

  // Report results
  if (errors.length === 0 && warnings.length === 0) {
    console.log("✅ All validations passed! Data integrity is excellent.");
  } else {
    if (errors.length > 0) {
      console.log(`❌ Found ${errors.length} error(s):`);
      errors.forEach((error) => console.log(`   • ${error}`));
      console.log();
    }

    if (warnings.length > 0) {
      console.log(`⚠️  Found ${warnings.length} warning(s):`);
      warnings.forEach((warning) => console.log(`   • ${warning}`));
      console.log();
    }
  }

  return {
    errors,
    warnings,
    stats: {
      total: categories.length,
      roots: rootCategories.length,
      children: childCategories.length,
    },
  };
}

/**
 * Main validation function
 */
function main() {
  try {
    console.log("🧪 Categories Data Validation Test");
    console.log("=".repeat(50));

    const csvPath = path.join(__dirname, "../../output/categories.csv");

    if (!fs.existsSync(csvPath)) {
      console.error(`❌ CSV file not found: ${csvPath}`);
      console.error("Please run the generator first: npm run generate");
      process.exit(1);
    }

    console.log(`📁 Reading file: ${csvPath}\n`);

    const categories = parseCSV(csvPath);
    const results = validateCategories(categories);

    // Exit with appropriate code
    if (results.errors.length > 0) {
      console.log("🚨 Validation failed - please fix the errors above");
      process.exit(1);
    } else if (results.warnings.length > 0) {
      console.log("⚠️  Validation passed with warnings - consider reviewing");
      process.exit(0);
    } else {
      console.log("🎉 Perfect! All validations passed successfully");
      process.exit(0);
    }
  } catch (error) {
    console.error("❌ Validation script failed:", error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { validateCategories, parseCSV };
