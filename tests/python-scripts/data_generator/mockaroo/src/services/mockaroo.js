/**
 * Mockaroo API Service
 *
 * This module handles all interactions with the Mockaroo API,
 * including client initialization, request configuration,
 * and error handling with retry logic.
 *
 * @author Software Testing Team
 * @version 1.0.0
 */

const Mockaroo = require("mockaroo");
const CONFIG = require("../config");
const { sleep, logWithTimestamp } = require("../utils");

class MockarooService {
  constructor() {
    this.client = null;
    this.initialized = false;
  }

  /**
   * Initialize Mockaroo client
   */
  initialize() {
    const apiKey = process.env.MOCKAROO_API_KEY;

    if (!apiKey) {
      throw new Error(
        "MOCKAROO_API_KEY environment variable is required. Please check your .env file."
      );
    }

    logWithTimestamp("info", "🔑", "Initializing Mockaroo client...");

    this.client = new Mockaroo.Client({
      apiKey,
      timeout: CONFIG.API_TIMEOUT,
    });

    this.initialized = true;
    logWithTimestamp("info", "✅", "Mockaroo client initialized successfully");

    return this.client;
  }

  /**
   * Validate client is initialized
   */
  validateClient() {
    if (!this.initialized || !this.client) {
      throw new Error(
        "Mockaroo client not initialized. Call initialize() first."
      );
    }
  }

  /**
   * Generate data with retry mechanism
   */
  async generateWithRetry(requestConfig, maxRetries = CONFIG.RETRY_ATTEMPTS) {
    this.validateClient();

    let lastError;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        logWithTimestamp("info", "🔄", `Attempt ${attempt}/${maxRetries}`);

        const data = await this.client.generate(requestConfig);

        logWithTimestamp(
          "info",
          "✅",
          "Data generation completed successfully"
        );
        return data;
      } catch (error) {
        lastError = error;

        // Handle specific Mockaroo errors
        if (error instanceof Mockaroo.errors.UsageLimitExceededError) {
          logWithTimestamp(
            "error",
            "❌",
            "Daily usage limit exceeded. Please upgrade your Mockaroo plan or try again tomorrow."
          );
          throw error;
        }

        if (error instanceof Mockaroo.errors.InvalidApiKeyError) {
          logWithTimestamp(
            "error",
            "❌",
            "Invalid API key. Please check your MOCKAROO_API_KEY in .env file."
          );
          throw error;
        }

        if (error instanceof Mockaroo.errors.QuotaExceededError) {
          logWithTimestamp(
            "error",
            "❌",
            "API quota exceeded. Please wait or upgrade your plan."
          );
          throw error;
        }

        // Log the error and retry if attempts remain
        logWithTimestamp(
          "warn",
          "⚠️",
          `Attempt ${attempt} failed: ${error.message}`
        );

        if (attempt < maxRetries) {
          const delaySeconds = CONFIG.RETRY_DELAY / 1000;
          logWithTimestamp(
            "info",
            "⏳",
            `Retrying in ${delaySeconds} seconds...`
          );
          await sleep(CONFIG.RETRY_DELAY);
        }
      }
    }

    // All retries failed
    logWithTimestamp(
      "error",
      "❌",
      `All ${maxRetries} attempts failed. Last error: ${lastError.message}`
    );
    throw lastError;
  }

  /**
   * Build Mockaroo field configuration for categories
   */
  buildCategoryFields(categoryData) {
    const { CATEGORY_NAMES, SUBCATEGORY_NAMES, getAllCategorySlugs } =
      categoryData;

    return [
      {
        name: "id",
        type: "Character Sequence",
        format: "################", // 16 character sequence for ULID-like IDs
      },
      {
        name: "name",
        type: "Custom List",
        values: [...CATEGORY_NAMES, ...SUBCATEGORY_NAMES],
        selectionStyle: "random",
      },
      {
        name: "slug",
        type: "Custom List",
        values: getAllCategorySlugs(),
        selectionStyle: "random",
      },
      {
        name: "parent_id",
        type: "Custom List",
        values: [
          "",
          "",
          "",
          "",
          "",
          "", // 60% null (root categories)
          "{{id}}",
          "{{id}}", // 40% references to other IDs in dataset
        ],
        selectionStyle: "random",
      },
      {
        name: "created_at",
        type: "Datetime",
        min: CONFIG.DATE_RANGE.START,
        max: CONFIG.DATE_RANGE.END,
        format: "%Y-%m-%d %H:%M:%S",
      },
      {
        name: "updated_at",
        type: "Datetime",
        min: CONFIG.DATE_RANGE.START,
        max: CONFIG.DATE_RANGE.END,
        format: "%Y-%m-%d %H:%M:%S",
      },
    ];
  }

  /**
   * Generate categories data
   */
  async generateCategories(count = CONFIG.RECORDS_COUNT, categoryData) {
    logWithTimestamp("info", "🎯", `Generating ${count} category records...`);

    const fields = this.buildCategoryFields(categoryData);

    const requestConfig = {
      count: count,
      format: "csv",
      header: true,
      fields: fields,
    };

    return await this.generateWithRetry(requestConfig);
  }

  /**
   * Test API connectivity
   */
  async testConnection() {
    this.validateClient();

    logWithTimestamp("info", "🔍", "Testing API connectivity...");

    try {
      const testData = await this.client.generate({
        count: 1,
        fields: [
          {
            name: "test_id",
            type: "Row Number",
          },
          {
            name: "test_name",
            type: "Custom List",
            values: ["Test Category"],
          },
        ],
      });

      logWithTimestamp("info", "✅", "API connectivity test successful");
      return true;
    } catch (error) {
      logWithTimestamp(
        "error",
        "❌",
        `API connectivity test failed: ${error.message}`
      );
      throw error;
    }
  }

  /**
   * Get client instance
   */
  getClient() {
    this.validateClient();
    return this.client;
  }
}

module.exports = MockarooService;
