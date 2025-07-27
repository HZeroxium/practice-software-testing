# Mockaroo Categories Data Generator

A professional-grade data generator for creating realistic categories data with proper hierarchical relationships using the Mockaroo API. This tool generates structured test data for e-commerce applications, specifically designed for hardware/tool store categories.

## 🌟 Features

- **Hierarchical Data Structure**: Generates proper parent-child relationships
- **Realistic Categories**: Based on real hardware store classifications
- **Data Integrity**: Comprehensive validation ensures referential integrity
- **Modular Architecture**: Easy to extend and maintain
- **CSV Output**: Database-ready format for easy import
- **SQL Script Generation**: Optional SQL INSERT scripts for direct database import
- **Multiple Database Support**: MySQL, PostgreSQL, SQLite SQL generation
- **Interactive Prompts**: User-friendly options for SQL generation
- **Comprehensive Logging**: Detailed progress tracking and error reporting
- **Validation Testing**: Built-in data integrity validation
- **ULID-style IDs**: Unique, sortable identifiers
- **Retry Logic**: Robust API error handling with automatic retries

## 🏗️ Architecture

The application follows a modular architecture for maintainability and extensibility:

```plaintext
src/
├── config/           # Configuration constants
├── data/             # Category definitions and structures
├── generators/       # Data generation logic
├── services/         # External API interactions
├── utils/            # Common utilities
├── test/             # Validation and testing scripts
└── main.js           # Main entry point
```

## 📋 Requirements

- Node.js 14.x or higher
- npm 6.x or higher
- Mockaroo API account (free tier available)

## Installation

1. Install dependencies:

```bash
npm install
```

2. Configure your Mockaroo API key in the `.env` file:

```bash
MOCKAROO_API_KEY=your_api_key_here
```

## Usage

### Basic Data Generation

Generate 10 categories and save to CSV:

```bash
npm run generate
```

Or run directly:

```bash
node src/main.js
```

### SQL Script Generation

After CSV generation, the tool will interactively prompt you to generate SQL INSERT scripts:

````text
🔧 OPTIONAL: SQL INSERT Script Generation
==================================================
Would you like to generate SQL INSERT script for database import? [y/N]: y

Select your database type:
→ 1. MySQL
  2. PostgreSQL
  3. SQLite

Include transaction wrapper (START TRANSACTION/COMMIT)? [Y/n]: y
Include ON DUPLICATE KEY UPDATE clause (MySQL only)? [y/N]: n
Batch size for INSERT statements [100]: 100
```### Manual SQL Generation

You can also generate SQL scripts from existing CSV files:

```bash
npm run generate-sql
````

### Validation

Validate generated data integrity:

```bash
npm run validate
```

## Output

The generator creates the following files in the `output/` directory:

### CSV Files

- `categories.csv` - Main data file with the following structure:
  - id (ULID format)
  - name (Category name)
  - slug (URL-friendly slug)
  - parent_id (ULID for parent category, NULL for top-level)
  - created_at (ISO timestamp)
  - updated_at (ISO timestamp)

### SQL Files (Optional)

- `categories.sql` - SQL INSERT script for database import
  - Includes proper transaction wrapping
  - Handles NULL values correctly
  - Supports multiple database types (MySQL, PostgreSQL, SQLite)
  - Batch processing for optimal performance

## Database Schema Compatibility

This generator creates data compatible with the following database schema:

```sql
CREATE TABLE categories (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    parent_id VARCHAR(26) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);
```

## API Usage

This project demonstrates best practices for using the Mockaroo API with Node.js:

- Error handling for API rate limits and failures
- Proper field configuration for realistic data generation
- CSV output formatting with headers
- Environment variable configuration for API keys

## Contributing

When extending this generator:

1. Add new category types to the field configuration
2. Ensure ULID format compliance for ID fields
3. Maintain parent-child relationship integrity
4. Test with small batches before scaling up

## License

ISC
