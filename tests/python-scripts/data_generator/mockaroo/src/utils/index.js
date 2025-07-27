/**
 * Utility Functions
 *
 * This module provides common utility functions used throughout
 * the Mockaroo Categories Data Generator application.
 *
 * @author Software Testing Team
 * @version 1.0.0
 */

const fs = require("fs");
const path = require("path");
const CONFIG = require("../config");

/**
 * Generate a simple ULID-like identifier
 * For production use, consider using a proper ULID library
 */
function generateSimpleULID() {
  const timestamp = Date.now().toString(36).toUpperCase();
  const random = Math.random()
    .toString(36)
    .substr(2, CONFIG.ULID_LENGTH - timestamp.length)
    .toUpperCase();
  return (timestamp + random)
    .padEnd(CONFIG.ULID_LENGTH, "0")
    .substr(0, CONFIG.ULID_LENGTH);
}

/**
 * Convert a name to a URL-friendly slug
 */
function nameToSlug(name) {
  return name
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, "") // Remove special characters
    .replace(/[\s_-]+/g, "-") // Replace spaces and underscores with hyphens
    .replace(/^-+|-+$/g, ""); // Remove leading/trailing hyphens
}

/**
 * Generate unique slug from a name and existing slugs set
 */
function generateUniqueSlug(name, usedSlugs) {
  let baseSlug = nameToSlug(name);
  let slug = baseSlug;
  let counter = 1;

  while (usedSlugs.has(slug)) {
    slug = `${baseSlug}-${counter}`;
    counter++;
  }

  usedSlugs.add(slug);
  return slug;
}

/**
 * Format timestamp for database
 */
function formatTimestamp(date = new Date()) {
  return date.toISOString().slice(0, 19).replace("T", " ");
}

/**
 * Generate random timestamp within configured date range
 */
function generateRandomTimestamp() {
  const startDate = new Date(CONFIG.DATE_RANGE.START);
  const endDate = new Date(CONFIG.DATE_RANGE.END);
  const randomTime =
    startDate.getTime() +
    Math.random() * (endDate.getTime() - startDate.getTime());
  return formatTimestamp(new Date(randomTime));
}

/**
 * Ensure output directory exists
 */
function ensureOutputDirectory(outputDir) {
  const outputPath = path.resolve(outputDir);

  if (!fs.existsSync(outputPath)) {
    fs.mkdirSync(outputPath, { recursive: true });
    console.log(`📁 Created output directory: ${outputPath}`);
  }

  return outputPath;
}

/**
 * Write data to CSV file
 */
function writeCSVFile(filePath, data, headers = null) {
  try {
    let csvContent = "";

    // Add headers if provided
    if (headers && Array.isArray(headers)) {
      csvContent += headers.join(CONFIG.CSV_DELIMITER) + "\n";
    }

    // Add data rows
    if (Array.isArray(data)) {
      data.forEach((row) => {
        if (Array.isArray(row)) {
          csvContent +=
            row
              .map((field) => escapeCSVField(field))
              .join(CONFIG.CSV_DELIMITER) + "\n";
        } else if (typeof row === "object") {
          const values = headers
            ? headers.map((header) => row[header] || "")
            : Object.values(row);
          csvContent +=
            values
              .map((field) => escapeCSVField(field))
              .join(CONFIG.CSV_DELIMITER) + "\n";
        }
      });
    }

    fs.writeFileSync(filePath, csvContent, "utf8");

    // Get file stats
    const stats = fs.statSync(filePath);
    const lines = csvContent.split("\n").filter((line) => line.trim()).length;

    console.log(`💾 Data saved successfully to: ${filePath}`);
    console.log(
      `📊 File size: ${Math.round((stats.size / 1024) * 100) / 100} KB`
    );
    console.log(
      `📋 Records generated: ${lines - (headers ? 1 : 0)} (excluding header)`
    );

    return filePath;
  } catch (error) {
    console.error("❌ Error writing CSV file:", error.message);
    throw error;
  }
}

/**
 * Escape CSV field value
 */
function escapeCSVField(field) {
  if (field === null || field === undefined) {
    return "";
  }

  const stringField = String(field);

  // Check if field needs quoting
  if (
    stringField.includes(CONFIG.CSV_DELIMITER) ||
    stringField.includes(CONFIG.CSV_QUOTE_CHAR) ||
    stringField.includes("\n") ||
    stringField.includes("\r")
  ) {
    // Escape internal quotes by doubling them
    const escapedField = stringField.replace(
      new RegExp(CONFIG.CSV_QUOTE_CHAR, "g"),
      CONFIG.CSV_QUOTE_CHAR + CONFIG.CSV_QUOTE_CHAR
    );

    return CONFIG.CSV_QUOTE_CHAR + escapedField + CONFIG.CSV_QUOTE_CHAR;
  }

  return stringField;
}

/**
 * Validate CSV data structure
 */
function validateCSVData(data, expectedHeaders) {
  if (!Array.isArray(data) || data.length === 0) {
    throw new Error("Data must be a non-empty array");
  }

  if (expectedHeaders && Array.isArray(expectedHeaders)) {
    const firstRow = data[0];
    if (typeof firstRow === "object" && !Array.isArray(firstRow)) {
      const missingHeaders = expectedHeaders.filter(
        (header) => !(header in firstRow)
      );
      if (missingHeaders.length > 0) {
        throw new Error(
          `Missing expected headers: ${missingHeaders.join(", ")}`
        );
      }
    }
  }

  return true;
}

/**
 * Sleep for specified milliseconds
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Format duration in human-readable format
 */
function formatDuration(milliseconds) {
  const seconds = milliseconds / 1000;
  if (seconds < 60) {
    return `${seconds.toFixed(2)} seconds`;
  } else if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = (seconds % 60).toFixed(0);
    return `${minutes}m ${remainingSeconds}s`;
  } else {
    const hours = Math.floor(seconds / 3600);
    const remainingMinutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${remainingMinutes}m`;
  }
}

/**
 * Log with timestamp and emoji
 */
function logWithTimestamp(level, emoji, message) {
  const timestamp = new Date().toISOString();
  const levelStr = level.toUpperCase().padEnd(5);
  console.log(`[${timestamp}] ${levelStr} ${emoji} ${message}`);
}

module.exports = {
  generateSimpleULID,
  nameToSlug,
  generateUniqueSlug,
  formatTimestamp,
  generateRandomTimestamp,
  ensureOutputDirectory,
  writeCSVFile,
  escapeCSVField,
  validateCSVData,
  sleep,
  formatDuration,
  logWithTimestamp,
};
