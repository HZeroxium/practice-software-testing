/**
 * Categories Data Generator
 *
 * This module handles the generation of realistic categories data
 * with proper hierarchical relationships and data integrity.
 *
 * @author Software Testing Team
 * @version 1.0.0
 */

const CONFIG = require("../config");
const categoryData = require("../data/categories");
const MockarooService = require("../services/mockaroo");
const {
  generateSimpleULID,
  generateUniqueSlug,
  generateRandomTimestamp,
  logWithTimestamp,
} = require("../utils");

class CategoriesGenerator {
  constructor() {
    this.mockarooService = new MockarooService();
    this.generatedCategories = [];
    this.usedSlugs = new Set();
  }

  /**
   * Initialize the generator
   */
  async initialize() {
    this.mockarooService.initialize();

    // Test API connectivity
    await this.mockarooService.testConnection();

    logWithTimestamp(
      "info",
      "🏗️",
      "Categories generator initialized successfully"
    );
  }

  /**
   * Generate categories with proper hierarchy
   */
  async generateCategories(count = CONFIG.RECORDS_COUNT) {
    logWithTimestamp(
      "info",
      "🎯",
      `Starting generation of ${count} categories...`
    );

    try {
      // Step 1: Generate structured hierarchy locally first
      const structuredCategories = await this.generateHierarchicalCategories(
        count
      );

      // Step 2: Use Mockaroo for additional realistic data (timestamps, etc.)
      const mockarooData = await this.mockarooService.generateCategories(
        count,
        categoryData
      );

      // Step 3: Merge structured data with Mockaroo enhancements
      const finalCategories = this.mergeDataSources(
        structuredCategories,
        mockarooData
      );

      logWithTimestamp(
        "info",
        "✅",
        `Successfully generated ${finalCategories.length} categories`
      );

      return finalCategories;
    } catch (error) {
      logWithTimestamp(
        "error",
        "❌",
        `Error generating categories: ${error.message}`
      );
      throw error;
    }
  }

  /**
   * Generate hierarchical categories with proper parent-child relationships
   */
  async generateHierarchicalCategories(count) {
    const categories = [];
    const rootCategories = [];

    logWithTimestamp(
      "info",
      "🌳",
      "Generating hierarchical category structure..."
    );

    // Calculate how many root vs sub categories
    const rootCount = Math.ceil(count * CONFIG.ROOT_CATEGORY_RATIO);
    const subCount = count - rootCount;

    logWithTimestamp(
      "info",
      "📊",
      `Planning: ${rootCount} root categories, ${subCount} subcategories`
    );

    // Phase 1: Generate root categories
    const rootCategoryNames = categoryData.getCategoryNames();

    for (let i = 0; i < rootCount && i < rootCategoryNames.length; i++) {
      const categoryName = rootCategoryNames[i];
      const category = this.createCategory(categoryName, null);

      categories.push(category);
      rootCategories.push(category);
    }

    logWithTimestamp(
      "info",
      "🔄",
      `Generated ${rootCategories.length} root categories`
    );

    // Phase 2: Generate subcategories
    let subcategoryCount = 0;

    for (const rootCategory of rootCategories) {
      if (subcategoryCount >= subCount) break;

      const subcategoriesForRoot = categoryData.getSubcategoriesFor(
        rootCategory.name
      );
      const subcategoriesNeeded = Math.min(
        subCount - subcategoryCount,
        subcategoriesForRoot.length,
        Math.ceil(subCount / rootCategories.length)
      );

      for (let i = 0; i < subcategoriesNeeded; i++) {
        if (i < subcategoriesForRoot.length) {
          const subcategoryName = subcategoriesForRoot[i];
          const subcategory = this.createCategory(
            subcategoryName,
            rootCategory.id
          );
          categories.push(subcategory);
          subcategoryCount++;
        }
      }
    }

    // Phase 3: If we need more subcategories, create tools as categories
    while (subcategoryCount < subCount) {
      const randomRootCategory =
        rootCategories[Math.floor(Math.random() * rootCategories.length)];
      const subcategoriesForRoot = categoryData.getSubcategoriesFor(
        randomRootCategory.name
      );

      if (subcategoriesForRoot.length > 0) {
        const randomSubcategory =
          subcategoriesForRoot[
            Math.floor(Math.random() * subcategoriesForRoot.length)
          ];
        const tools = categoryData.getToolsFor(
          randomRootCategory.name,
          randomSubcategory
        );

        if (tools.length > 0) {
          const randomTool = tools[Math.floor(Math.random() * tools.length)];
          const toolCategory = this.createCategory(
            randomTool,
            randomRootCategory.id
          );
          categories.push(toolCategory);
          subcategoryCount++;
        } else {
          break; // No more tools available
        }
      } else {
        break; // No more subcategories available
      }
    }

    logWithTimestamp(
      "info",
      "✅",
      `Generated ${subcategoryCount} subcategories`
    );
    logWithTimestamp(
      "info",
      "📈",
      `Total categories generated: ${categories.length}`
    );

    return categories;
  }

  /**
   * Create a single category object
   */
  createCategory(name, parentId = null) {
    const id = generateSimpleULID();
    const slug = generateUniqueSlug(name, this.usedSlugs);
    const timestamp = generateRandomTimestamp();

    return {
      id,
      name,
      slug,
      parent_id: parentId || "",
      created_at: timestamp,
      updated_at: timestamp,
    };
  }

  /**
   * Merge structured categories with Mockaroo-generated data
   */
  mergeDataSources(structuredCategories, mockarooCSV) {
    logWithTimestamp(
      "info",
      "🔄",
      "Merging structured data with Mockaroo enhancements..."
    );

    // Parse CSV data from Mockaroo (it comes as a string)
    const csvLines = mockarooCSV.trim().split("\n");
    const headers = csvLines[0].split(",");

    // Use our structured data but enhance with any missing pieces from Mockaroo
    const finalCategories = structuredCategories.map((category, index) => {
      // If we have fewer structured categories than requested,
      // we can use Mockaroo data for additional entries
      if (index < csvLines.length - 1) {
        const csvRow = csvLines[index + 1].split(",");

        // Keep our structure but potentially use Mockaroo timestamps if needed
        return {
          ...category,
          // We could enhance here with Mockaroo data if needed
          // For now, keep our structured approach
        };
      }

      return category;
    });

    logWithTimestamp("info", "✅", "Data sources merged successfully");
    return finalCategories;
  }

  /**
   * Convert categories to CSV format
   */
  categoriesToCSV(categories) {
    const headers = [
      "id",
      "name",
      "slug",
      "parent_id",
      "created_at",
      "updated_at",
    ];

    let csv = headers.join(",") + "\n";

    categories.forEach((category) => {
      const row = headers.map((header) => {
        const value = category[header] || "";
        // Escape commas and quotes in CSV
        if (
          typeof value === "string" &&
          (value.includes(",") || value.includes('"'))
        ) {
          return `"${value.replace(/"/g, '""')}"`;
        }
        return value;
      });
      csv += row.join(",") + "\n";
    });

    return csv;
  }

  /**
   * Validate generated categories
   */
  validateCategories(categories) {
    logWithTimestamp("info", "🔍", "Validating generated categories...");

    const errors = [];
    const ids = new Set();
    const slugs = new Set();

    categories.forEach((category, index) => {
      // Check required fields
      if (!category.id) errors.push(`Row ${index + 1}: Missing ID`);
      if (!category.name) errors.push(`Row ${index + 1}: Missing name`);
      if (!category.slug) errors.push(`Row ${index + 1}: Missing slug`);

      // Check for duplicates
      if (category.id) {
        if (ids.has(category.id)) {
          errors.push(`Row ${index + 1}: Duplicate ID ${category.id}`);
        }
        ids.add(category.id);
      }

      if (category.slug) {
        if (slugs.has(category.slug)) {
          errors.push(`Row ${index + 1}: Duplicate slug ${category.slug}`);
        }
        slugs.add(category.slug);
      }

      // Check parent_id validity (if not empty, should reference existing ID)
      if (category.parent_id && category.parent_id !== "") {
        const parentExists = categories.some(
          (cat) => cat.id === category.parent_id
        );
        if (!parentExists) {
          errors.push(
            `Row ${index + 1}: Invalid parent_id ${category.parent_id}`
          );
        }
      }
    });

    if (errors.length > 0) {
      logWithTimestamp(
        "error",
        "❌",
        `Validation failed with ${errors.length} errors:`
      );
      errors.forEach((error) => console.error(`  • ${error}`));
      throw new Error(`Validation failed with ${errors.length} errors`);
    }

    logWithTimestamp("info", "✅", "Category validation passed");

    // Log statistics
    const rootCategories = categories.filter(
      (cat) => !cat.parent_id || cat.parent_id === ""
    );
    const subCategories = categories.filter(
      (cat) => cat.parent_id && cat.parent_id !== ""
    );

    logWithTimestamp(
      "info",
      "📊",
      `Statistics: ${rootCategories.length} root categories, ${subCategories.length} subcategories`
    );

    return true;
  }
}

module.exports = CategoriesGenerator;
