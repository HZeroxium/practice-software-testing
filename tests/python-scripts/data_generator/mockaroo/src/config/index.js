/**
 * Configuration constants for Mockaroo Categories Data Generator
 *
 * This module centralizes all configuration values for easy maintenance
 * and environment-specific customization.
 *
 * @author Software Testing Team
 * @version 1.0.0
 */

const CONFIG = {
  // API Configuration
  API_TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 2000, // 2 seconds

  // Data Generation Settings
  RECORDS_COUNT: 10,
  ROOT_CATEGORY_RATIO: 0.3, // 30% root categories, 70% subcategories

  // Output Configuration
  OUTPUT_DIR: "output/csv",
  OUTPUT_FILE: "categories.csv",

  // ULID Configuration (simplified 16-character format for demo)
  ULID_LENGTH: 16,
  ULID_CHARSET: "0123456789ABCDEFGHJKMNPQRSTVWXYZ",

  // CSV Configuration
  CSV_DELIMITER: ",",
  CSV_QUOTE_CHAR: '"',
  CSV_ESCAPE_CHAR: '"',

  // Validation Settings
  MIN_NAME_LENGTH: 3,
  MAX_NAME_LENGTH: 50,
  MIN_SLUG_LENGTH: 3,
  MAX_SLUG_LENGTH: 60,

  // Date Range for generated timestamps
  DATE_RANGE: {
    START: "2024-01-01",
    END: "2024-12-31",
  },
};

module.exports = CONFIG;
