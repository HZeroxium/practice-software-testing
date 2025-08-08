# API Testing Framework - The Toolshop

## 🎯 Overview

This project contains a comprehensive API testing framework for **The Toolshop** application, focusing on three key APIs:

- **GET /brands** - Brand management API
- **GET /products** - Product catalog API
- **GET /categories** - Category management API

The framework is **fully functional** and automatically generates comprehensive reports, bug reports, and Excel files for submission.

## ✨ Key Features

- 🚀 **Data-Driven Testing** - CSV-based test scenarios with 36+ test cases
- 📊 **Automated Reporting** - Excel files, CSV reports, and markdown documentation
- 🐛 **Bug Detection** - Automatic bug report generation with priority classification
- 🔄 **Multiple Testing Modes** - Standard, data-driven, and combined testing
- 🏗️ **CI/CD Integration** - GitHub Actions workflow for automated testing
- 📱 **Cross-Platform** - Works on Windows, Linux, and macOS
- 🎯 **Easy Extension** - Add new test cases by updating CSV files

## 📁 Project Structure

```
tests/api-testing/
├── README.md                           # This comprehensive guide
├── StudentID_APITesting.md             # Assessment report (auto-generated)
├── docs/                               # Additional documentation
│   ├── CI-CD-Guide.md                  # CI/CD integration guide
│   ├── Data-Driven-Testing-Guide.md    # Data-driven testing guide
│   └── Troubleshooting-Guide.md        # Troubleshooting guide
├── test-cases/                         # Generated test cases
│   ├── brands-test-cases.csv          # 10 test cases
│   ├── products-test-cases.csv        # 14 test cases
│   └── categories-test-cases.csv      # 12 test cases
├── postman-collections/                # Postman collections
│   ├── data-driven-collection.json    # Main collection for data-driven testing
│   ├── brands-collection.json         # Standard brands collection
│   ├── products-collection.json       # Standard products collection
│   └── categories-collection.json     # Standard categories collection
├── data/                              # Test data files
│   ├── brands-test-data.csv          # 10 GET test scenarios for brands
│   ├── brands-post-test-data.json    # 10 POST test scenarios for brands
│   ├── products-test-data.csv        # 14 GET test scenarios for products
│   └── categories-test-data.csv      # 12 GET test scenarios for categories
├── scripts/                           # Test execution scripts
│   ├── run-api-tests.py              # Main test orchestrator
│   ├── data_driven_testing.py        # Data-driven testing classes
│   ├── report_generator.py           # Report generation module
│   ├── test-demo.py                  # Demo script
│   └── run-tests.bat                 # Windows batch file
├── reports/                           # Generated reports
│   ├── test-results/                 # Test execution results
│   └── bug-reports/                  # Bug reports
├── requirements.txt                   # Python dependencies
└── StudentID_*.xlsx                  # Generated Excel files
```

## Project Structure

```bash
api-testing/
├── README.md                           # This file
├── test-cases/                         # Test case definitions
│   ├── brands-test-cases.csv          # 15 test cases
│   ├── products-test-cases.csv        # 20 test cases
│   └── categories-test-cases.csv      # 12 test cases
├── postman-collections/                # Postman collections for Newman
│   ├── brands-collection.json
│   ├── products-collection.json
│   ├── categories-collection.json
│   ├── data-driven-collection.json    # Data-driven testing collection
│   ├── bug-test-collection.json       # Demo collection for bug reporting
│   └── test-collection.json           # Demo collection for testing
├── data/                              # Test data files
│   ├── brands-test-data.json         # JSON test data (legacy)
│   ├── products-test-data.json       # JSON test data (legacy)
│   ├── categories-test-data.json     # JSON test data (legacy)
│   ├── brands-test-data.csv          # CSV test data for data-driven testing
│   ├── products-test-data.csv        # CSV test data for data-driven testing
│   └── categories-test-data.csv      # CSV test data for data-driven testing
├── scripts/                           # Test execution scripts
│   ├── run-api-tests.py              # Main test runner
│   ├── data_driven_testing.py        # Data-driven testing classes
│   ├── report_generator.py           # Report generation module
│   ├── test-demo.py                  # Demo script for testing
│   ├── test-bug-report.py            # Bug report generation demo
│   └── run-tests.bat                 # Windows batch file
├── reports/                           # Generated test reports
│   ├── test-results/                 # Test execution results
│   └── bug-reports/                  # Bug reports
└── requirements.txt                   # Python dependencies
```

## 🛠️ Prerequisites

- **Python 3.8+** (3.9 or 3.11 recommended)
- **Node.js 18+** (for Newman CLI)
- **Newman CLI** (Postman's command-line tool)
- **The Toolshop API Server** (running on localhost:8091)

## ⚡ Quick Start

### 1. Install Dependencies

```bash
# Navigate to the api-testing directory
cd tests/api-testing

# Install Python dependencies
pip install -r requirements.txt

# Install Newman CLI
npm install -g newman
```

### 2. Verify Installation

```bash
# Check all dependencies
python scripts/run-api-tests.py --check-deps
```

**Expected Output:**

```
✓ Newman version (via PowerShell): 6.2.1
✓ API is accessible at http://localhost:8091
✓ Python dependencies installed
```

### 3. Run Tests

```bash
# Run all tests (data-driven mode)
python scripts/run-api-tests.py

# Or run with specific mode
python scripts/run-api-tests.py --mode data-driven
```

## 🚀 How to Use

### Single Command Execution (Recommended)

```bash
# Navigate to the api-testing directory
cd tests/api-testing

# Run all tests and generate all artifacts
python scripts/run-api-tests.py
```

**This single command will:**

- ✅ Execute all test collections (brands, products, categories)
- ✅ Generate comprehensive test reports
- ✅ Create Excel files for test cases and bug reports
- ✅ Clean up old reports automatically
- ✅ Update documentation with latest results

### Endpoint Configuration

You can specify which endpoints to test or exclude:

```bash
# Test only specific endpoints
python scripts/run-api-tests.py --endpoints brands products

# Exclude specific endpoints
python scripts/run-api-tests.py --exclude-endpoints categories

# Test only POST endpoints
python scripts/run-api-tests.py --endpoints brands --mode data-driven
```

## 🚀 How to Use

### Single Command Execution (Recommended)

```bash
# Navigate to the api-testing directory
cd tests/api-testing

# Run all tests and generate all artifacts
python scripts/run-api-tests.py
```

## 🔄 Testing Modes

The framework supports multiple testing modes to suit different needs:

### 1. Data-Driven Mode (Default) 🎯

```bash
python scripts/run-api-tests.py --mode data-driven
```

**Features:**

- Runs 36+ test scenarios from CSV files
- Dynamic environment variable injection
- Comprehensive coverage of edge cases
- Automatic test case generation
- Detailed bug reporting

### 2. Standard Mode 📋

```bash
python scripts/run-api-tests.py --mode standard
```

**Features:**

- Traditional Postman collection testing
- Predefined test scenarios
- Basic functionality testing
- Suitable for quick validation

### 3. Combined Mode 🔄

```bash
python scripts/run-api-tests.py --mode both
```

**Features:**

- Runs both standard and data-driven tests
- Maximum test coverage
- Comprehensive validation
- Complete testing suite

## 📊 Data-Driven Testing

The framework uses **CSV-based data-driven testing** for maximum flexibility:

### Test Data Files

| File                            | Test Cases   | Coverage                                |
| ------------------------------- | ------------ | --------------------------------------- |
| `data/brands-test-data.csv`     | 10 scenarios | Pagination, validation, edge cases      |
| `data/products-test-data.csv`   | 14 scenarios | Filtering, sorting, search, validation  |
| `data/categories-test-data.csv` | 12 scenarios | Basic retrieval, validation, edge cases |

### CSV Format

```csv
test_case_id,title,preconditions,inputs,test_steps,expected_result,actual_result,result
BR-001,Get Brands with Pagination,API server is running,page=1&limit=10,1. Send GET request to /brands,Status: 200 with brands data,,
```

### Key Benefits

- 🎯 **Scalable**: Easy to add new test scenarios without code changes
- 📊 **Maintainable**: Test data separated from test logic
- 🔄 **Reusable**: Same collection with different data sets
- 📈 **Comprehensive**: Covers various scenarios (pagination, filtering, sorting, etc.)

## 📁 Generated Artifacts

Running the tests automatically generates comprehensive artifacts:

### 1. Test Cases (CSV Format)

- `test-cases/brands-test-cases.csv` - 10 test cases with actual results
- `test-cases/products-test-cases.csv` - 14 test cases with actual results
- `test-cases/categories-test-cases.csv` - 12 test cases with actual results

### 2. Excel Reports

- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### 3. Bug Reports (CSV Format)

- Standard bug reports for collection failures
- Data-driven bug reports for individual test case failures
- Priority classification (High/Medium/Low)
- Detailed reproduction steps

### 4. Documentation Updates

- Updated `README.md` with latest test results
- Updated `StudentID_APITesting.md` with comprehensive results
- Automatic cleanup of old reports (keeps 5 most recent)

  - `brands-test-data.csv` - 10 test scenarios for brands endpoint
  - `products-test-data.csv` - 14 test scenarios for products endpoint
  - `categories-test-data.csv` - 12 test scenarios for categories endpoint

- **Single Collection**: Uses `data-driven-collection.json` with 3 endpoints
- **Dynamic Parameters**: Query parameters, expected results, and test data are passed via CSV
- **Easy Extension**: Add new test cases by simply updating CSV files

**Benefits of Data-Driven Testing:**

- 🎯 **Scalable**: Easy to add new test scenarios without code changes
- 📊 **Maintainable**: Test data separated from test logic
- 🔄 **Reusable**: Same collection with different data sets
- 📈 **Comprehensive**: Covers various scenarios (pagination, filtering, sorting, etc.)
- ✅ Generate test cases in CSV format
- ✅ Create bug reports (if any failures)
- ✅ Convert all reports to Excel format
- ✅ Generate comprehensive markdown reports
- ✅ Clean up old reports (keep only 5 most recent)
- ✅ Display execution summary

## ⚙️ Advanced Options

### Custom Configuration

```bash
# Run with custom base URL
python scripts/run-api-tests.py --base-url http://localhost:8091

# Run in CI/CD mode
python scripts/run-api-tests.py --ci

# Check dependencies only
python scripts/run-api-tests.py --check-deps

# Run with verbose output
python scripts/run-api-tests.py --verbose
```

### Windows Users

```bash
# Navigate to the api-testing directory
cd tests/api-testing

# Run tests using batch file
scripts/run-tests.bat
```

## 🏗️ CI/CD Integration

The framework includes a comprehensive GitHub Actions workflow for automated testing:

### Workflow Features

- **Automatic Triggers**: Runs on push/PR to main/develop branches
- **Matrix Testing**: Tests on multiple Node.js and Python versions
- **Artifact Generation**: Uploads test results and reports
- **Manual Execution**: Supports manual workflow dispatch with custom parameters

### Local CI Testing

```bash
# Test CI pipeline locally
python scripts/run-api-tests.py --ci --mode data-driven
```

### GitHub Actions

The workflow automatically:

- ✅ Installs dependencies (Node.js, Python, Newman)
- ✅ Runs tests in parallel across different environments
- ✅ Generates and uploads artifacts
- ✅ Creates comprehensive test summaries

For detailed CI/CD documentation, see: [`docs/CI-CD-Guide.md`](docs/CI-CD-Guide.md)

## Usage

### Quick Start (Demo)

To test the framework with a public API:

```bash
# Run from tests/api-testing directory
python scripts/test-demo.py
```

This will run a simple test against http://httpbin.org/json to verify the setup.

### Testing Bug Report Generation

To test the bug report generation system:

```bash
# Run from tests/api-testing directory
python scripts/test-bug-report.py
```

This will run tests that intentionally fail to demonstrate the bug reporting system.

### Running Tests Against The Toolshop API

#### Prerequisites

1. **Start The Toolshop API server** (sprint5)
2. **Ensure the API is running** on the expected port (default: 8091)
3. **Verify endpoints are accessible**: `/brands`, `/products`, `/categories`

#### Execute Tests

**From the `tests/api-testing` directory:**

```bash
# Run all tests with default settings
python scripts/run-api-tests.py

# Run tests with custom API URL
python scripts/run-api-tests.py --base-url http://localhost:8091

# Run tests in CI/CD mode
python scripts/run-api-tests.py --ci

# Check dependencies only
python scripts/run-api-tests.py --check-deps
```

#### Windows Users

Use the provided batch file for easy execution:

```bash
# From tests/api-testing directory
scripts/run-tests.bat
```

### Manual Test Execution

Run individual collections using Newman directly:

```bash
# Run specific collection
newman run postman-collections/brands-collection.json -e postman-collections/environment.json

# Run all collections
newman run postman-collections/ -e postman-collections/environment.json
```

## Test Coverage

- **GET /brands**: 5 test cases covering basic functionality, performance, and validation
- **GET /products**: 7 test cases covering pagination, filtering, sorting, and validation
- **GET /categories**: 5 test cases covering basic functionality and error handling
- **Bug Test Collection**: 6 test cases including intentionally failing tests for bug reporting

## Report Generation

The test runner automatically generates:

- **Test execution reports** (JSON/HTML format)
- **Bug reports** (CSV format)
- **Performance metrics**
- **Coverage reports**

### Generated Files

After running tests, check the `reports/` directory:

```
reports/
├── test-results/
│   ├── overall-results.json          # Complete test results
│   ├── test-summary-YYYYMMDD-HHMMSS.txt  # Human-readable summary
│   ├── brands-results.json           # Individual collection results
│   ├── products-results.json
│   ├── categories-results.json
│   └── bug-test-results.json
└── bug-reports/
    └── bug-report-YYYYMMDD-HHMMSS.csv    # Bug reports
```

### Converting to Excel

Generate Excel files for submission:

```bash
python scripts/convert-to-excel.py
```

This creates:

- `StudentID_TestCases.xlsx` (combined test cases)
- `StudentID_BugReport.xlsx` (bug reports)

## CI/CD Integration

The project includes GitHub Actions workflow for automated testing:

- Runs on push to main branch
- Generates reports automatically
- Stores artifacts for review

### Local CI/CD Testing

Test the CI/CD pipeline locally:

```bash
python scripts/run-api-tests.py --ci
```

## 🔧 Troubleshooting

### Quick Diagnosis

```bash
# Check dependencies
python scripts/run-api-tests.py --check-deps

# Verify API accessibility
curl http://localhost:8091/brands
```

### Common Issues

1. **Newman Installation Issues**

   ```bash
   # Install Newman globally
   npm install -g newman

   # For Windows PowerShell issues
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
   ```

2. **API Server Not Accessible**

   ```bash
   # Check if server is running
   netstat -an | findstr :8091  # Windows
   netstat -an | grep :8091     # Linux/macOS

   # Start the API server
   cd ../sprint5
   python app.py  # or your server start command
   ```

3. **Python Dependencies**

   ```bash
   # Install requirements
   pip install -r requirements.txt

   # Upgrade pip first
   python -m pip install --upgrade pip
   ```

4. **File Path Issues**

   ```bash
   # Ensure you're in the correct directory
   cd tests/api-testing

   # Check if files exist
   ls data/
   ls postman-collections/
   ```

### Debug Mode

```bash
# Run with verbose output
python scripts/run-api-tests.py --verbose

# Check specific components
python scripts/run-api-tests.py --check-deps --verbose
```

For comprehensive troubleshooting, see: [`docs/Troubleshooting-Guide.md`](docs/Troubleshooting-Guide.md)

## API Endpoints Tested

### GET /brands

- Basic functionality
- Response time validation
- Error handling
- Performance testing

### POST /brands

- Brand creation with valid data
- Validation (missing name, empty name, duplicate name)
- Error handling (long names, special characters)
- Request body validation

### GET /products

- Pagination (page, limit)
- Filtering (category, brand, price)
- Sorting (asc/desc)
- Search functionality
- Input validation

### GET /categories

- Basic retrieval
- Hierarchical structure
- Performance benchmarks
- Error handling

## Data-Driven Testing

All tests use data-driven approach with CSV and JSON test data files:

### GET Endpoints (CSV format)

- `data/brands-test-data.csv`
- `data/products-test-data.csv`
- `data/categories-test-data.csv`

### POST Endpoints (JSON format)

- `data/brands-post-test-data.json` - POST /brands test scenarios

## Performance Thresholds

- **Response Time**: < 2 seconds for basic operations
- **Large Dataset**: < 5 seconds for 1000+ records
- **Concurrent Requests**: 10 simultaneous requests
- **Memory Usage**: < 1MB response size

## Security Testing

- CORS headers validation
- Input sanitization
- Rate limiting (if implemented)
- Authentication (if required)

## Bug Report System

The framework automatically generates bug reports when tests fail:

- **Location**: `reports/bug-reports/`
- **Format**: CSV with proper structure
- **Content**: Bug ID, Summary, Steps, Expected vs Actual, Priority, etc.

### Bug Report Format

| Field              | Description       | Example                            |
| ------------------ | ----------------- | ---------------------------------- |
| BugID              | Unique identifier | BUG-001                            |
| Summary            | Brief description | GET /brands returns 500 error      |
| Steps To Reproduce | Detailed steps    | 1. Clear database; 2. Send request |
| Actual vs Expected | Comparison        | Expected: 200, Actual: 500         |
| Screenshot         | Visual evidence   | Not applicable for API tests       |
| Priority           | Bug severity      | High/Medium/Low                    |
| Affected Feature   | Impact scope      | brands API / sprint5               |

## Contributing

1. Add new test cases to the appropriate CSV file
2. Update test data in JSON files
3. Create new Postman collections as needed
4. Update this README with new features

## Support

For issues or questions:

1. Check the troubleshooting section
2. Verify all prerequisites are installed
3. Ensure you're running from the correct directory
4. Check the generated reports for detailed error information

## 📚 Documentation

### Main Documentation

- **README.md** (this file) - Comprehensive guide and quick reference
- **StudentID_APITesting.md** - Assessment report with detailed results

### Additional Guides

- **[CI/CD Guide](docs/CI-CD-Guide.md)** - GitHub Actions integration and automation
- **[Data-Driven Testing Guide](docs/Data-Driven-Testing-Guide.md)** - CSV-based testing approach
- **[Troubleshooting Guide](docs/Troubleshooting-Guide.md)** - Common issues and solutions

### API Documentation

- **Endpoints**: `/brands`, `/products`, `/categories`
- **Base URL**: `http://localhost:8091`
- **Methods**: GET requests with query parameters
- **Response Format**: JSON

## 🎯 Framework Status

✅ **FULLY FUNCTIONAL & PRODUCTION READY**

### ✅ Completed Features

- 🚀 **Data-Driven Testing**: 36+ test scenarios with CSV-based approach
- 📊 **Automated Reporting**: Excel files, CSV reports, markdown documentation
- 🐛 **Bug Detection**: Automatic bug report generation with priority classification
- 🔄 **Multiple Testing Modes**: Standard, data-driven, and combined testing
- 🏗️ **CI/CD Integration**: GitHub Actions workflow for automated testing
- 📱 **Cross-Platform**: Works on Windows, Linux, and macOS
- 🎯 **Easy Extension**: Add new test cases by updating CSV files
- 📈 **Comprehensive Coverage**: Pagination, filtering, sorting, validation, edge cases

### 🔧 Technical Features

- **Modular Architecture**: Separated concerns with specialized classes
- **Error Handling**: Robust error detection and reporting
- **Performance Optimization**: Efficient test execution and resource management
- **Report Cleanup**: Automatic cleanup of old reports (keeps 5 most recent)
- **Environment Management**: Dynamic environment variable injection
- **Validation**: Comprehensive input validation and error checking

## 📈 Recent Updates

### Latest Enhancements

- ✅ **Enhanced Report Generator**: Comprehensive data-driven reporting with Excel conversion
- ✅ **Improved CI/CD Workflow**: Updated GitHub Actions for better automation
- ✅ **Comprehensive Documentation**: Complete guides for all aspects of the framework
- ✅ **Bug Report Integration**: Seamless integration of data-driven bug reporting
- ✅ **Cross-Platform Compatibility**: Enhanced Windows PowerShell support
- ✅ **Performance Optimization**: Improved test execution and resource management

### Previous Milestones

- ✅ **Data-Driven API Testing**: CSV-based approach with 36 test scenarios
- ✅ **Testing Modes**: Standard, data-driven, and combined testing
- ✅ **Specialized Classes**: DataDrivenTestRunner, CSVDataLoader, PostmanEnvironmentBuilder
- ✅ **Collection Structure**: Single data-driven collection with dynamic variables
- ✅ **Excel Integration**: Automatic CSV to Excel conversion
- ✅ **Report Generation**: Comprehensive markdown reports with cleanup
- ✅ **Bug Detection**: Robust bug reporting system
- ✅ **Error Handling**: Better dependency checking and cross-platform support

## API Testing Results

# API Testing Report - The Toolshop Application

**Generated:** 2025-08-08 22:40:15  
**Base URL:** http://localhost:8091  
**Platform:** Windows

## 📊 Test Execution Summary

### Overall Results
- **Total Collections:** 0
- **Passed Collections:** 0
- **Failed Collections:** 0
- **Total Tests:** 0
- **Passed Tests:** 0
- **Failed Tests:** 0

### Collection Results

## 📝 Test Cases Summary

### BRANDS API
- **Total Test Cases:** 20
- **Passed:** 16
- **Failed:** 4
- **Success Rate:** 80.0%

### PRODUCTS API
- **Total Test Cases:** 14
- **Passed:** 13
- **Failed:** 1
- **Success Rate:** 92.9%

### CATEGORIES API
- **Total Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

## 🐛 Bug Report Summary

- **Data-Driven Bugs Found:** 14
- **Data-Driven Bug Report File:** data-driven-bug-report-20250808_224015.csv

### Data-Driven Bug Details

#### DD-BUG-001
- **Summary:** Data-driven test failed: Get Categories with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Categories API / v1.0

#### DD-BUG-002
- **Summary:** Data-driven test failed: Get Brands with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-003
- **Summary:** Data-driven test failed: Get Brands with Invalid Sort Field
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-004
- **Summary:** Data-driven test failed: Create Brand - Valid Data
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-005
- **Summary:** Data-driven test failed: Create Brand - Missing Name
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

## 🐛 Bug Report Summary

- **Total Bugs Found:** 14

## 🚀 Data-Driven Testing Results

### Executive Summary
- **Total Endpoints Tested:** 3
- **Total Test Cases:** 46
- **Passed Tests:** 32
- **Failed Tests:** 14
- **Success Rate:** 69.6%
- **Bugs Found:** 14

### CATEGORIES Endpoint
- **Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

### BRANDS Endpoint
- **Test Cases:** 20
- **Passed:** 8
- **Failed:** 12
- **Success Rate:** 40.0%

### PRODUCTS Endpoint
- **Test Cases:** 14
- **Passed:** 13
- **Failed:** 1
- **Success Rate:** 92.9%

### Data-Driven Bugs Found (14)

#### Bug #1
- **Test Case:** CA-010
- **Title:** Get Categories with Invalid Page
- **Endpoint:** categories
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #2
- **Test Case:** BR-003
- **Title:** Get Brands with Invalid Page
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #3
- **Test Case:** BR-009
- **Title:** Get Brands with Invalid Sort Field
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #4
- **Test Case:** BR-POST-001
- **Title:** Create Brand - Valid Data
- **Endpoint:** brands
- **Expected:** Status: 201; JSON response with created brand
- **Actual:** Failed with exit code 1

#### Bug #5
- **Test Case:** BR-POST-002
- **Title:** Create Brand - Missing Name
- **Endpoint:** brands
- **Expected:** Status: 422 or 400; validation error
- **Actual:** Failed with exit code 1

## 📁 Generated Files

### Excel Files
- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### CSV Files
- `brands-test-cases.csv` - Brands test cases
- `products-test-cases.csv` - Products test cases
- `categories-test-cases.csv` - Categories test cases
- `data-driven-bug-report-20250808_224015.csv` - Data-driven bug report

## 📊 Test Execution Summary

### Overall Results
- **Total Collections:** 0
- **Passed Collections:** 0
- **Failed Collections:** 0
- **Total Tests:** 0
- **Passed Tests:** 0
- **Failed Tests:** 0

### Collection Results

## 📝 Test Cases Summary

### BRANDS API
- **Total Test Cases:** 20
- **Passed:** 16
- **Failed:** 4
- **Success Rate:** 80.0%

### PRODUCTS API
- **Total Test Cases:** 14
- **Passed:** 13
- **Failed:** 1
- **Success Rate:** 92.9%

### CATEGORIES API
- **Total Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

## 🐛 Bug Report Summary

- **Data-Driven Bugs Found:** 14
- **Data-Driven Bug Report File:** data-driven-bug-report-20250808_184313.csv

### Data-Driven Bug Details

#### DD-BUG-001
- **Summary:** Data-driven test failed: Get Categories with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Categories API / v1.0

#### DD-BUG-002
- **Summary:** Data-driven test failed: Get Brands with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-003
- **Summary:** Data-driven test failed: Get Brands with Invalid Sort Field
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-004
- **Summary:** Data-driven test failed: Create Brand - Valid Data
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-005
- **Summary:** Data-driven test failed: Create Brand - Missing Name
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

## 🐛 Bug Report Summary

- **Total Bugs Found:** 14

## 🚀 Data-Driven Testing Results

### Executive Summary
- **Total Endpoints Tested:** 3
- **Total Test Cases:** 46
- **Passed Tests:** 32
- **Failed Tests:** 14
- **Success Rate:** 69.6%
- **Bugs Found:** 14

### CATEGORIES Endpoint
- **Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

### BRANDS Endpoint
- **Test Cases:** 20
- **Passed:** 8
- **Failed:** 12
- **Success Rate:** 40.0%

### PRODUCTS Endpoint
- **Test Cases:** 14
- **Passed:** 13
- **Failed:** 1
- **Success Rate:** 92.9%

### Data-Driven Bugs Found (14)

#### Bug #1
- **Test Case:** CA-010
- **Title:** Get Categories with Invalid Page
- **Endpoint:** categories
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #2
- **Test Case:** BR-003
- **Title:** Get Brands with Invalid Page
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #3
- **Test Case:** BR-009
- **Title:** Get Brands with Invalid Sort Field
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #4
- **Test Case:** BR-POST-001
- **Title:** Create Brand - Valid Data
- **Endpoint:** brands
- **Expected:** Status: 201; JSON response with created brand
- **Actual:** Failed with exit code 1

#### Bug #5
- **Test Case:** BR-POST-002
- **Title:** Create Brand - Missing Name
- **Endpoint:** brands
- **Expected:** Status: 422 or 400; validation error
- **Actual:** Failed with exit code 1

## 📁 Generated Files

### Excel Files
- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### CSV Files
- `brands-test-cases.csv` - Brands test cases
- `products-test-cases.csv` - Products test cases
- `categories-test-cases.csv` - Categories test cases
- `data-driven-bug-report-20250808_184313.csv` - Data-driven bug report

## 📊 Test Execution Summary

### Overall Results
- **Total Collections:** 0
- **Passed Collections:** 0
- **Failed Collections:** 0
- **Total Tests:** 0
- **Passed Tests:** 0
- **Failed Tests:** 0

### Collection Results

## 📝 Test Cases Summary

### BRANDS API
- **Total Test Cases:** 20
- **Passed:** 16
- **Failed:** 4
- **Success Rate:** 80.0%

### PRODUCTS API
- **Total Test Cases:** 0
- **Passed:** 0
- **Failed:** 0
- **Success Rate:** 0.0%

### CATEGORIES API
- **Total Test Cases:** 0
- **Passed:** 0
- **Failed:** 0
- **Success Rate:** 0.0%

## 🐛 Bug Report Summary

- **Data-Driven Bugs Found:** 12
- **Data-Driven Bug Report File:** data-driven-bug-report-20250808_182521.csv

### Data-Driven Bug Details

#### DD-BUG-001
- **Summary:** Data-driven test failed: Get Brands with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-002
- **Summary:** Data-driven test failed: Get Brands with Invalid Sort Field
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-003
- **Summary:** Data-driven test failed: Create Brand - Valid Data
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-004
- **Summary:** Data-driven test failed: Create Brand - Missing Name
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-005
- **Summary:** Data-driven test failed: Create Brand - Empty Name
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

## 🐛 Bug Report Summary

- **Total Bugs Found:** 12

## 🚀 Data-Driven Testing Results

### Executive Summary
- **Total Endpoints Tested:** 1
- **Total Test Cases:** 20
- **Passed Tests:** 8
- **Failed Tests:** 12
- **Success Rate:** 40.0%
- **Bugs Found:** 12

### BRANDS Endpoint
- **Test Cases:** 20
- **Passed:** 8
- **Failed:** 12
- **Success Rate:** 40.0%

### Data-Driven Bugs Found (12)

#### Bug #1
- **Test Case:** BR-003
- **Title:** Get Brands with Invalid Page
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #2
- **Test Case:** BR-009
- **Title:** Get Brands with Invalid Sort Field
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #3
- **Test Case:** BR-POST-001
- **Title:** Create Brand - Valid Data
- **Endpoint:** brands
- **Expected:** Status: 201; JSON response with created brand
- **Actual:** Failed with exit code 1

#### Bug #4
- **Test Case:** BR-POST-002
- **Title:** Create Brand - Missing Name
- **Endpoint:** brands
- **Expected:** Status: 422 or 400; validation error
- **Actual:** Failed with exit code 1

#### Bug #5
- **Test Case:** BR-POST-003
- **Title:** Create Brand - Empty Name
- **Endpoint:** brands
- **Expected:** Status: 422 or 400; validation error
- **Actual:** Failed with exit code 1

## 📁 Generated Files

### Excel Files
- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### CSV Files
- `brands-test-cases.csv` - Brands test cases
- `products-test-cases.csv` - Products test cases
- `categories-test-cases.csv` - Categories test cases
- `data-driven-bug-report-20250808_182521.csv` - Data-driven bug report

## 📊 Test Execution Summary

### Overall Results
- **Total Collections:** 0
- **Passed Collections:** 0
- **Failed Collections:** 0
- **Total Tests:** 0
- **Passed Tests:** 0
- **Failed Tests:** 0

### Collection Results

## 📝 Test Cases Summary

### BRANDS API
- **Total Test Cases:** 20
- **Passed:** 16
- **Failed:** 4
- **Success Rate:** 80.0%

### PRODUCTS API
- **Total Test Cases:** 14
- **Passed:** 13
- **Failed:** 1
- **Success Rate:** 92.9%

### CATEGORIES API
- **Total Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

## 🐛 Bug Report Summary

- **Data-Driven Bugs Found:** 14
- **Data-Driven Bug Report File:** data-driven-bug-report-20250808_171822.csv

### Data-Driven Bug Details

#### DD-BUG-001
- **Summary:** Data-driven test failed: Get Brands with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-002
- **Summary:** Data-driven test failed: Get Brands with Invalid Sort Field
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-003
- **Summary:** Data-driven test failed: Create Brand - Valid Data
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-004
- **Summary:** Data-driven test failed: Create Brand - Missing Name
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-005
- **Summary:** Data-driven test failed: Create Brand - Empty Name
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

## 🐛 Bug Report Summary

- **Total Bugs Found:** 14

## 🚀 Data-Driven Testing Results

### Executive Summary
- **Total Endpoints Tested:** 3
- **Total Test Cases:** 46
- **Passed Tests:** 32
- **Failed Tests:** 14
- **Success Rate:** 69.6%
- **Bugs Found:** 14

### BRANDS Endpoint
- **Test Cases:** 20
- **Passed:** 8
- **Failed:** 12
- **Success Rate:** 40.0%

### CATEGORIES Endpoint
- **Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

### PRODUCTS Endpoint
- **Test Cases:** 14
- **Passed:** 13
- **Failed:** 1
- **Success Rate:** 92.9%

### Data-Driven Bugs Found (14)

#### Bug #1
- **Test Case:** BR-003
- **Title:** Get Brands with Invalid Page
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #2
- **Test Case:** BR-009
- **Title:** Get Brands with Invalid Sort Field
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #3
- **Test Case:** BR-POST-001
- **Title:** Create Brand - Valid Data
- **Endpoint:** brands
- **Expected:** Status: 201; JSON response with created brand
- **Actual:** Failed with exit code 1

#### Bug #4
- **Test Case:** BR-POST-002
- **Title:** Create Brand - Missing Name
- **Endpoint:** brands
- **Expected:** Status: 422 or 400; validation error
- **Actual:** Failed with exit code 1

#### Bug #5
- **Test Case:** BR-POST-003
- **Title:** Create Brand - Empty Name
- **Endpoint:** brands
- **Expected:** Status: 422 or 400; validation error
- **Actual:** Failed with exit code 1

## 📁 Generated Files

### Excel Files
- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### CSV Files
- `brands-test-cases.csv` - Brands test cases
- `products-test-cases.csv` - Products test cases
- `categories-test-cases.csv` - Categories test cases
- `data-driven-bug-report-20250808_171822.csv` - Data-driven bug report

## 📊 Test Execution Summary

### Overall Results

- **Total Collections:** 0
- **Passed Collections:** 0
- **Failed Collections:** 0
- **Total Tests:** 0
- **Passed Tests:** 0
- **Failed Tests:** 0

### Collection Results

## 📝 Test Cases Summary

### BRANDS API

- **Total Test Cases:** 0
- **Passed:** 0
- **Failed:** 0
- **Success Rate:** 0.0%

### PRODUCTS API

- **Total Test Cases:** 0
- **Passed:** 0
- **Failed:** 0
- **Success Rate:** 0.0%

### CATEGORIES API

- **Total Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

## 🐛 Bug Report Summary

- **Data-Driven Bugs Found:** 1
- **Data-Driven Bug Report File:** data-driven-bug-report-20250808_160528.csv

### Data-Driven Bug Details

#### DD-BUG-001

- **Summary:** Data-driven test failed: Get Categories with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Categories API / v1.0

## 🐛 Bug Report Summary

- **Total Bugs Found:** 1

## 🚀 Data-Driven Testing Results

### Executive Summary

- **Total Endpoints Tested:** 1
- **Total Test Cases:** 12
- **Passed Tests:** 11
- **Failed Tests:** 1
- **Success Rate:** 91.7%
- **Bugs Found:** 1

### CATEGORIES Endpoint

- **Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

### Data-Driven Bugs Found (1)

#### Bug #1

- **Test Case:** CA-010
- **Title:** Get Categories with Invalid Page
- **Endpoint:** categories
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

## 📁 Generated Files

### Excel Files

- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### CSV Files

- `brands-test-cases.csv` - Brands test cases
- `products-test-cases.csv` - Products test cases
- `categories-test-cases.csv` - Categories test cases
- `data-driven-bug-report-20250808_160528.csv` - Data-driven bug report

## 📊 Test Execution Summary

### Overall Results

- **Total Collections:** 0
- **Passed Collections:** 0
- **Failed Collections:** 0
- **Total Tests:** 0
- **Passed Tests:** 0
- **Failed Tests:** 0

### Collection Results

## 📝 Test Cases Summary

### BRANDS API

- **Total Test Cases:** 20
- **Passed:** 16
- **Failed:** 4
- **Success Rate:** 80.0%

### PRODUCTS API

- **Total Test Cases:** 14
- **Passed:** 12
- **Failed:** 2
- **Success Rate:** 85.7%

### CATEGORIES API

- **Total Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

## 🐛 Bug Report Summary

- **Data-Driven Bugs Found:** 15
- **Data-Driven Bug Report File:** data-driven-bug-report-20250808_155857.csv

### Data-Driven Bug Details

#### DD-BUG-001

- **Summary:** Data-driven test failed: Get Categories with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Categories API / v1.0

#### DD-BUG-002

- **Summary:** Data-driven test failed: Get Brands with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-003

- **Summary:** Data-driven test failed: Get Brands with Invalid Sort Field
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-004

- **Summary:** Data-driven test failed: Create Brand - Valid Data
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-005

- **Summary:** Data-driven test failed: Create Brand - Missing Name
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

## 🐛 Bug Report Summary

- **Total Bugs Found:** 15

## 🚀 Data-Driven Testing Results

### Executive Summary

- **Total Endpoints Tested:** 3
- **Total Test Cases:** 46
- **Passed Tests:** 31
- **Failed Tests:** 15
- **Success Rate:** 67.4%
- **Bugs Found:** 15

### CATEGORIES Endpoint

- **Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

### BRANDS Endpoint

- **Test Cases:** 20
- **Passed:** 8
- **Failed:** 12
- **Success Rate:** 40.0%

### PRODUCTS Endpoint

- **Test Cases:** 14
- **Passed:** 12
- **Failed:** 2
- **Success Rate:** 85.7%

### Data-Driven Bugs Found (15)

#### Bug #1

- **Test Case:** CA-010
- **Title:** Get Categories with Invalid Page
- **Endpoint:** categories
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #2

- **Test Case:** BR-003
- **Title:** Get Brands with Invalid Page
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #3

- **Test Case:** BR-009
- **Title:** Get Brands with Invalid Sort Field
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #4

- **Test Case:** BR-POST-001
- **Title:** Create Brand - Valid Data
- **Endpoint:** brands
- **Expected:** Status: 201; JSON response with created brand
- **Actual:** Failed with exit code 1

#### Bug #5

- **Test Case:** BR-POST-002
- **Title:** Create Brand - Missing Name
- **Endpoint:** brands
- **Expected:** Status: 422 or 400; validation error
- **Actual:** Failed with exit code 1

## 📁 Generated Files

### Excel Files

- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### CSV Files

- `brands-test-cases.csv` - Brands test cases
- `products-test-cases.csv` - Products test cases
- `categories-test-cases.csv` - Categories test cases
- `data-driven-bug-report-20250808_155857.csv` - Data-driven bug report

## 📊 Test Execution Summary

### Overall Results

- **Total Collections:** 0
- **Passed Collections:** 0
- **Failed Collections:** 0
- **Total Tests:** 0
- **Passed Tests:** 0
- **Failed Tests:** 0

### Collection Results

## 📝 Test Cases Summary

### BRANDS API

- **Total Test Cases:** 10
- **Passed:** 8
- **Failed:** 2
- **Success Rate:** 80.0%

### PRODUCTS API

- **Total Test Cases:** 14
- **Passed:** 12
- **Failed:** 2
- **Success Rate:** 85.7%

### CATEGORIES API

- **Total Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

## 🐛 Bug Report Summary

- **Data-Driven Bugs Found:** 5
- **Data-Driven Bug Report File:** data-driven-bug-report-20250808_133054.csv

### Data-Driven Bug Details

#### DD-BUG-001

- **Summary:** Data-driven test failed: Get Brands with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-002

- **Summary:** Data-driven test failed: Get Brands with Invalid Sort Field
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-003

- **Summary:** Data-driven test failed: Get Categories with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Categories API / v1.0

#### DD-BUG-004

- **Summary:** Data-driven test failed: Get Products with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Products API / v1.0

#### DD-BUG-005

- **Summary:** Data-driven test failed: Get Products with Special Characters
- **Priority:** Medium
- **Affected Feature:** Products API / v1.0

## 🐛 Bug Report Summary

- **Total Bugs Found:** 5

## 🚀 Data-Driven Testing Results

### Executive Summary

- **Total Endpoints Tested:** 3
- **Total Test Cases:** 36
- **Passed Tests:** 31
- **Failed Tests:** 5
- **Success Rate:** 86.1%
- **Bugs Found:** 5

### BRANDS Endpoint

- **Test Cases:** 10
- **Passed:** 8
- **Failed:** 2
- **Success Rate:** 80.0%

### CATEGORIES Endpoint

- **Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

### PRODUCTS Endpoint

- **Test Cases:** 14
- **Passed:** 12
- **Failed:** 2
- **Success Rate:** 85.7%

### Data-Driven Bugs Found (5)

#### Bug #1

- **Test Case:** BR-003
- **Title:** Get Brands with Invalid Page
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #2

- **Test Case:** BR-009
- **Title:** Get Brands with Invalid Sort Field
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #3

- **Test Case:** CA-010
- **Title:** Get Categories with Invalid Page
- **Endpoint:** categories
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #4

- **Test Case:** PR-011
- **Title:** Get Products with Invalid Page
- **Endpoint:** products
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #5

- **Test Case:** PR-013
- **Title:** Get Products with Special Characters
- **Endpoint:** products
- **Expected:** Status: 200
- **Actual:** Failed with exit code 1

## 📁 Generated Files

### Excel Files

- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### CSV Files

- `brands-test-cases.csv` - Brands test cases
- `products-test-cases.csv` - Products test cases
- `categories-test-cases.csv` - Categories test cases
- `data-driven-bug-report-20250808_133054.csv` - Data-driven bug report

## 📊 Test Execution Summary

### Overall Results

- **Total Collections:** 0
- **Passed Collections:** 0
- **Failed Collections:** 0
- **Total Tests:** 0
- **Passed Tests:** 0
- **Failed Tests:** 0

### Collection Results

## 📝 Test Cases Summary

### BRANDS API

- **Total Test Cases:** 10
- **Passed:** 8
- **Failed:** 2
- **Success Rate:** 80.0%

### PRODUCTS API

- **Total Test Cases:** 14
- **Passed:** 12
- **Failed:** 2
- **Success Rate:** 85.7%

### CATEGORIES API

- **Total Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

## 🐛 Bug Report Summary

- **Data-Driven Bugs Found:** 5
- **Data-Driven Bug Report File:** data-driven-bug-report-20250808_132901.csv

### Data-Driven Bug Details

#### DD-BUG-001

- **Summary:** Data-driven test failed: Get Brands with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-002

- **Summary:** Data-driven test failed: Get Brands with Invalid Sort Field
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-003

- **Summary:** Data-driven test failed: Get Categories with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Categories API / v1.0

#### DD-BUG-004

- **Summary:** Data-driven test failed: Get Products with Multiple Filters
- **Priority:** Medium
- **Affected Feature:** Products API / v1.0

#### DD-BUG-005

- **Summary:** Data-driven test failed: Get Products with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Products API / v1.0

## 🐛 Bug Report Summary

- **Total Bugs Found:** 5

## 🚀 Data-Driven Testing Results

### Executive Summary

- **Total Endpoints Tested:** 3
- **Total Test Cases:** 36
- **Passed Tests:** 31
- **Failed Tests:** 5
- **Success Rate:** 86.1%
- **Bugs Found:** 5

### BRANDS Endpoint

- **Test Cases:** 10
- **Passed:** 8
- **Failed:** 2
- **Success Rate:** 80.0%

### CATEGORIES Endpoint

- **Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

### PRODUCTS Endpoint

- **Test Cases:** 14
- **Passed:** 12
- **Failed:** 2
- **Success Rate:** 85.7%

### Data-Driven Bugs Found (5)

#### Bug #1

- **Test Case:** BR-003
- **Title:** Get Brands with Invalid Page
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #2

- **Test Case:** BR-009
- **Title:** Get Brands with Invalid Sort Field
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #3

- **Test Case:** CA-010
- **Title:** Get Categories with Invalid Page
- **Endpoint:** categories
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #4

- **Test Case:** PR-009
- **Title:** Get Products with Multiple Filters
- **Endpoint:** products
- **Expected:** Status: 200
- **Actual:** Failed with exit code 1

#### Bug #5

- **Test Case:** PR-011
- **Title:** Get Products with Invalid Page
- **Endpoint:** products
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

## 📁 Generated Files

### Excel Files

- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### CSV Files

- `brands-test-cases.csv` - Brands test cases
- `products-test-cases.csv` - Products test cases
- `categories-test-cases.csv` - Categories test cases
- `data-driven-bug-report-20250808_132901.csv` - Data-driven bug report

## 📊 Test Execution Summary

### Overall Results

- **Total Collections:** 0
- **Passed Collections:** 0
- **Failed Collections:** 0
- **Total Tests:** 0
- **Passed Tests:** 0
- **Failed Tests:** 0

### Collection Results

## 📝 Test Cases Summary

### BRANDS API

- **Total Test Cases:** 10
- **Passed:** 8
- **Failed:** 2
- **Success Rate:** 80.0%

### PRODUCTS API

- **Total Test Cases:** 14
- **Passed:** 13
- **Failed:** 1
- **Success Rate:** 92.9%

### CATEGORIES API

- **Total Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

## 🐛 Bug Report Summary

- **Data-Driven Bugs Found:** 4
- **Data-Driven Bug Report File:** data-driven-bug-report-20250808_132653.csv

### Data-Driven Bug Details

#### DD-BUG-001

- **Summary:** Data-driven test failed: Get Brands with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-002

- **Summary:** Data-driven test failed: Get Brands with Invalid Sort Field
- **Priority:** Medium
- **Affected Feature:** Brands API / v1.0

#### DD-BUG-003

- **Summary:** Data-driven test failed: Get Categories with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Categories API / v1.0

#### DD-BUG-004

- **Summary:** Data-driven test failed: Get Products with Invalid Page
- **Priority:** Medium
- **Affected Feature:** Products API / v1.0

## 🐛 Bug Report Summary

- **Total Bugs Found:** 4

## 🚀 Data-Driven Testing Results

### Executive Summary

- **Total Endpoints Tested:** 3
- **Total Test Cases:** 36
- **Passed Tests:** 32
- **Failed Tests:** 4
- **Success Rate:** 88.9%
- **Bugs Found:** 4

### BRANDS Endpoint

- **Test Cases:** 10
- **Passed:** 8
- **Failed:** 2
- **Success Rate:** 80.0%

### CATEGORIES Endpoint

- **Test Cases:** 12
- **Passed:** 11
- **Failed:** 1
- **Success Rate:** 91.7%

### PRODUCTS Endpoint

- **Test Cases:** 14
- **Passed:** 13
- **Failed:** 1
- **Success Rate:** 92.9%

### Data-Driven Bugs Found (4)

#### Bug #1

- **Test Case:** BR-003
- **Title:** Get Brands with Invalid Page
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #2

- **Test Case:** BR-009
- **Title:** Get Brands with Invalid Sort Field
- **Endpoint:** brands
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #3

- **Test Case:** CA-010
- **Title:** Get Categories with Invalid Page
- **Endpoint:** categories
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

#### Bug #4

- **Test Case:** PR-011
- **Title:** Get Products with Invalid Page
- **Endpoint:** products
- **Expected:** Status: 422 or 400
- **Actual:** Failed with exit code 1

## 📁 Generated Files

### Excel Files

- `StudentID_TestCases.xlsx` - Combined test cases
- `StudentID_TestCases_Brands.xlsx` - Brands test cases
- `StudentID_TestCases_Products.xlsx` - Products test cases
- `StudentID_TestCases_Categories.xlsx` - Categories test cases
- `StudentID_BugReport.xlsx` - Bug reports

### CSV Files

- `brands-test-cases.csv` - Brands test cases
- `products-test-cases.csv` - Products test cases
- `categories-test-cases.csv` - Categories test cases
- `data-driven-bug-report-20250808_132653.csv` - Data-driven bug report
