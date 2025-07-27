/**
 * SQL Generator Utility
 *
 * This module generates SQL INSERT statements from CSV data,
 * providing database-ready scripts for data import.
 *
 * Features:
 * - Generates proper SQL INSERT statements
 * - Handles NULL values correctly
 * - Escapes special characters
 * - Supports MySQL/PostgreSQL syntax
 * - Validates data types
 * - Includes transaction wrapping
 *
 * @author Software Testing Team
 * @version 1.0.0
 */

const fs = require("fs");
const path = require("path");
const { logWithTimestamp, escapeCSVField } = require("./index");

/**
 * Database-specific configurations
 */
const DB_CONFIGS = {
  mysql: {
    quote: "`",
    stringQuote: "'",
    nullValue: "NULL",
    dateFormat: "YYYY-MM-DD HH:mm:ss",
    batchSize: 100,
  },
  postgresql: {
    quote: '"',
    stringQuote: "'",
    nullValue: "NULL",
    dateFormat: "YYYY-MM-DD HH:mm:ss",
    batchSize: 100,
  },
  sqlite: {
    quote: "`",
    stringQuote: "'",
    nullValue: "NULL",
    dateFormat: "YYYY-MM-DD HH:mm:ss",
    batchSize: 100,
  },
};

/**
 * SQL data type mappings
 */
const SQL_TYPES = {
  id: "VARCHAR",
  name: "VARCHAR",
  slug: "VARCHAR",
  parent_id: "VARCHAR",
  created_at: "TIMESTAMP",
  updated_at: "TIMESTAMP",
  // Add more mappings as needed
};

/**
 * Generate SQL INSERT script from CSV data
 *
 * @param {Array} data - Array of data objects
 * @param {string} tableName - Target table name
 * @param {Object} options - Generation options
 * @returns {string} - SQL INSERT script
 */
function generateSQLInsertScript(data, tableName, options = {}) {
  const {
    dbType = "mysql",
    batchSize = 100,
    includeTransactions = true,
    includeComments = true,
    onDuplicateUpdate = false,
  } = options;

  if (!Array.isArray(data) || data.length === 0) {
    throw new Error("Data must be a non-empty array");
  }

  const dbConfig = DB_CONFIGS[dbType] || DB_CONFIGS.mysql;
  const headers = Object.keys(data[0]);

  let sqlScript = "";

  // Add header comment
  if (includeComments) {
    sqlScript += generateScriptHeader(tableName, data.length, dbType);
  }

  // Add transaction start
  if (includeTransactions) {
    sqlScript += "START TRANSACTION;\n\n";
  }

  // Generate batched INSERT statements
  for (let i = 0; i < data.length; i += batchSize) {
    const batch = data.slice(i, i + batchSize);
    sqlScript += generateBatchInsert(
      batch,
      tableName,
      headers,
      dbConfig,
      onDuplicateUpdate
    );
    sqlScript += "\n";
  }

  // Add transaction commit
  if (includeTransactions) {
    sqlScript += "COMMIT;\n\n";
  }

  // Add footer comment
  if (includeComments) {
    sqlScript += generateScriptFooter(data.length);
  }

  return sqlScript;
}

/**
 * Generate script header with metadata
 */
function generateScriptHeader(tableName, recordCount, dbType) {
  const timestamp = new Date().toISOString();

  return `-- ============================================================
-- SQL INSERT Script for ${tableName} table
-- ============================================================
-- Generated: ${timestamp}
-- Database: ${dbType.toUpperCase()}
-- Records: ${recordCount}
-- Generator: Mockaroo Categories Data Generator v2.0
-- ============================================================

`;
}

/**
 * Generate script footer
 */
function generateScriptFooter(recordCount) {
  return `-- ============================================================
-- Script completed successfully
-- Total records inserted: ${recordCount}
-- ============================================================
`;
}

/**
 * Generate batched INSERT statement
 */
function generateBatchInsert(
  batch,
  tableName,
  headers,
  dbConfig,
  onDuplicateUpdate
) {
  const { quote, stringQuote } = dbConfig;

  // Quote table and column names
  const quotedTableName = `${quote}${tableName}${quote}`;
  const quotedHeaders = headers.map((header) => `${quote}${header}${quote}`);

  let sql = `INSERT INTO ${quotedTableName} (${quotedHeaders.join(
    ", "
  )})\nVALUES\n`;

  // Generate values for each row
  const valueRows = batch.map((row) => {
    const values = headers.map((header) =>
      formatValue(row[header], header, dbConfig)
    );
    return `  (${values.join(", ")})`;
  });

  sql += valueRows.join(",\n");

  // Add ON DUPLICATE KEY UPDATE for MySQL if requested
  if (onDuplicateUpdate && dbConfig === DB_CONFIGS.mysql) {
    sql += generateOnDuplicateUpdate(headers, dbConfig);
  }

  sql += ";\n";

  return sql;
}

/**
 * Format value according to SQL type and database requirements
 */
function formatValue(value, columnName, dbConfig) {
  const { stringQuote, nullValue } = dbConfig;

  // Handle null/empty values
  if (value === null || value === undefined || value === "") {
    return nullValue;
  }

  // Convert to string for processing
  const stringValue = String(value).trim();

  if (stringValue === "") {
    return nullValue;
  }

  // Handle different data types based on column name
  if (isTimestampColumn(columnName)) {
    return formatTimestamp(stringValue, stringQuote);
  } else if (isNumericColumn(columnName)) {
    return formatNumeric(stringValue);
  } else {
    return formatString(stringValue, stringQuote);
  }
}

/**
 * Check if column is a timestamp type
 */
function isTimestampColumn(columnName) {
  return (
    columnName.includes("_at") ||
    columnName.includes("date") ||
    columnName === "dob"
  );
}

/**
 * Check if column is numeric type
 */
function isNumericColumn(columnName) {
  return (
    columnName === "price" ||
    columnName === "quantity" ||
    columnName.includes("count") ||
    columnName.includes("amount")
  );
}

/**
 * Format timestamp value
 */
function formatTimestamp(value, stringQuote) {
  // Validate timestamp format
  const timestamp = new Date(value);
  if (isNaN(timestamp.getTime())) {
    throw new Error(`Invalid timestamp format: ${value}`);
  }

  const formattedDate = timestamp.toISOString().slice(0, 19).replace("T", " ");
  return `${stringQuote}${formattedDate}${stringQuote}`;
}

/**
 * Format numeric value
 */
function formatNumeric(value) {
  const numValue = parseFloat(value);
  if (isNaN(numValue)) {
    throw new Error(`Invalid numeric value: ${value}`);
  }
  return numValue.toString();
}

/**
 * Format string value with proper escaping
 */
function formatString(value, stringQuote) {
  // Escape single quotes by doubling them
  const escapedValue = value.replace(/'/g, "''");
  return `${stringQuote}${escapedValue}${stringQuote}`;
}

/**
 * Generate ON DUPLICATE KEY UPDATE clause for MySQL
 */
function generateOnDuplicateUpdate(headers, dbConfig) {
  const { quote } = dbConfig;
  const updateClauses = headers
    .filter((header) => header !== "id" && header !== "created_at")
    .map(
      (header) =>
        `${quote}${header}${quote} = VALUES(${quote}${header}${quote})`
    );

  if (updateClauses.length === 0) {
    return "";
  }

  return `\nON DUPLICATE KEY UPDATE\n  ${updateClauses.join(",\n  ")}`;
}

/**
 * Write SQL script to file
 */
function writeSQLFile(filePath, sqlScript) {
  try {
    fs.writeFileSync(filePath, sqlScript, "utf8");

    const stats = fs.statSync(filePath);
    const lines = sqlScript.split("\n").length;

    logWithTimestamp("info", "💾", `SQL script saved to: ${filePath}`);
    console.log(
      `📊 File size: ${Math.round((stats.size / 1024) * 100) / 100} KB`
    );
    console.log(`📋 Lines: ${lines}`);

    return filePath;
  } catch (error) {
    logWithTimestamp("error", "❌", `Error writing SQL file: ${error.message}`);
    throw error;
  }
}

/**
 * Generate SQL script from CSV file
 */
function generateSQLFromCSV(csvFilePath, tableName, options = {}) {
  try {
    // Read and parse CSV file
    const csvContent = fs.readFileSync(csvFilePath, "utf8");
    const lines = csvContent.trim().split("\n");

    if (lines.length < 2) {
      throw new Error(
        "CSV file must contain at least a header and one data row"
      );
    }

    // Parse headers
    const headers = lines[0]
      .split(",")
      .map((header) => header.trim().replace(/"/g, ""));

    // Parse data rows
    const data = lines.slice(1).map((line) => {
      const values = parseCSVLine(line);
      const row = {};
      headers.forEach((header, index) => {
        row[header] = values[index] || "";
      });
      return row;
    });

    // Generate SQL script
    return generateSQLInsertScript(data, tableName, options);
  } catch (error) {
    logWithTimestamp(
      "error",
      "❌",
      `Error generating SQL from CSV: ${error.message}`
    );
    throw error;
  }
}

/**
 * Parse CSV line with proper quote handling
 */
function parseCSVLine(line) {
  const values = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];

    if (char === '"') {
      if (inQuotes && line[i + 1] === '"') {
        // Escaped quote
        current += '"';
        i++; // Skip next quote
      } else {
        // Toggle quote state
        inQuotes = !inQuotes;
      }
    } else if (char === "," && !inQuotes) {
      // End of field
      values.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }

  // Add final field
  values.push(current.trim());

  return values;
}

/**
 * Validate SQL generation options
 */
function validateSQLOptions(options) {
  const validDbTypes = Object.keys(DB_CONFIGS);

  if (options.dbType && !validDbTypes.includes(options.dbType)) {
    throw new Error(
      `Invalid database type. Supported: ${validDbTypes.join(", ")}`
    );
  }

  if (
    options.batchSize &&
    (options.batchSize < 1 || options.batchSize > 1000)
  ) {
    throw new Error("Batch size must be between 1 and 1000");
  }

  return true;
}

module.exports = {
  generateSQLInsertScript,
  generateSQLFromCSV,
  writeSQLFile,
  validateSQLOptions,
  DB_CONFIGS,
  SQL_TYPES,
};
