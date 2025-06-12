# Admin Add Product Feature - Data-Driven Automation Testing

This test suite provides comprehensive data-driven automation testing for the Admin Add Product Feature using Playwright and TypeScript.

## Features

- **Admin Authentication**: Automatic login with admin credentials
- **Data-Driven Testing**: Uses CSV file for product test data management
- **Flexible Test Selection**: Run all tests or specific test cases
- **Comprehensive Form Testing**: Tests all product form fields and validations
- **Error Handling**: Captures validation errors and screenshots
- **Special Value Processing**: Handles nominal values, empty values, repeated characters
- **Browser Compatibility**: Works across Chrome, Firefox, and Safari

## Test Data Format

The CSV file should have the following columns:

- `TestCaseID`: Unique identifier for the test case
- `Name`: Product name value
- `Description`: Product description
- `Price`: Product price
- `Brand`: Brand ID (1, 2, 3, etc.)
- `Category`: Category ID (1, 2, 3, etc.)
- `ProductImage`: Product image ID (1, 2, 3, etc.)
- `Stock`: Stock quantity
- `LocationOffer`: 'on' or 'off' for location offer checkbox
- `Rental`: 'on' or 'off' for rental checkbox

### Special Values in Test Data

- `nominal`: Represents standard valid values (replaced with predefined values)
- `(empty)` or `""`: Represents empty/blank values
- `"""value"""`: Represents quoted values
- `A×256`: Represents repeated characters (256 'A' characters)

## Usage

### Run All Admin Product Tests

```bash
npm run test:admin-product
```

### Run Specific Test Cases

#### Using Environment Variables

```bash
# Run specific test cases
PRODUCT_TEST_CASES="EP-AP-01,EP-AP-02,BVA-AP-01" npm run test:admin-product

# Run all tests explicitly
RUN_ALL_TESTS=true npm run test:admin-product

# Use custom admin credentials
ADMIN_EMAIL="admin@test.com" ADMIN_PASSWORD="password123" npm run test:admin-product

# Use custom data file
PRODUCT_TEST_DATA_FILE="tests/data/input/custom_product_data.csv" npm run test:admin-product
```

#### Using Configuration in Code

```typescript
import { AdminTestConfigManager } from "./utils/admin-test-config";

// Before running tests, set configuration
AdminTestConfigManager.setTestCases(["EP-AP-01", "EP-AP-02"]);
// or
AdminTestConfigManager.runAllTests();
```

### Admin Credentials

Default admin credentials:

- **Email**: admin@practicesoftwaretesting.com
- **Password**: welcome01

You can override these using environment variables:

```bash
ADMIN_EMAIL="your-admin@email.com" ADMIN_PASSWORD="your-password" npm run test:admin-product
```

## Test Results

### Screenshots

Screenshots are automatically captured:

- Before form submission: `before-submit-{TestCaseID}.png`
- After form submission: `after-submit-{TestCaseID}.png`
- On test failure: `failure-{TestCaseID}.png`
- After each test: `admin-product-{timestamp}.png`

### Console Output

Each test provides detailed console output including:

- Test case ID and processed data
- Current form values before submission
- Validation errors (if any)
- Success messages (if any)
- Submission results
- Execution time

### Expected Behaviors

The tests check for:

- Successful form submission (success message or redirect)
- Validation errors displayed on the form
- Form field interactions and data entry
- Admin authentication and navigation

## Configuration Options

### AdminTestConfigManager Methods

- `setTestCases(ids: string[])`: Set specific test cases to run
- `runAllTests()`: Run all available test cases
- `setConfig(config: Partial<AdminTestConfig>)`: Set custom configuration
- `loadConfigFromEnvironment()`: Load config from environment variables

### Environment Variables

- `PRODUCT_TEST_CASES`: Comma-separated list of test case IDs
- `RUN_ALL_TESTS`: Set to 'true' to run all tests
- `PRODUCT_TEST_DATA_FILE`: Path to custom test data file
- `ADMIN_EMAIL`: Admin email address
- `ADMIN_PASSWORD`: Admin password

## Test Types

The test suite includes various test case types:

### Equivalence Partitioning (EP)

- EP-AP-01 to EP-AP-18: Test different equivalence classes

### Boundary Value Analysis (BVA)

- BVA-AP-01 to BVA-AP-24: Test boundary conditions

## Troubleshooting

### Common Issues

1. **Admin authentication fails**

   - Verify admin credentials are correct
   - Check if admin account exists and is enabled
   - Ensure application is running and accessible

2. **Form elements not found**

   - Verify data-test attributes in the HTML
   - Check if admin navigation is working correctly
   - Ensure page has fully loaded

3. **Test data file not found**
   - Ensure the CSV file exists at the specified path
   - Check file permissions and format

### Debug Mode

Run tests in debug mode:

```bash
npm run test:admin-product:debug
```

### Headed Mode

Run tests with visible browser:

```bash
npm run test:admin-product:headed
```

## Best Practices

1. **Test Data Management**: Keep product test data organized and meaningful
2. **Admin Access**: Ensure admin credentials are secure and valid
3. **Error Handling**: Always handle potential errors gracefully
4. **Screenshots**: Use screenshots for visual verification
5. **Configuration**: Use environment variables for CI/CD integration
6. **Cleanup**: Tests automatically handle form cleanup between runs

## Contributing

When adding new test cases:

1. Add data to the CSV file following the format
2. Use meaningful test case IDs (EP-AP-XX, BVA-AP-XX)
3. Follow the special value conventions
4. Update documentation if needed
5. Test with both individual and batch runs
