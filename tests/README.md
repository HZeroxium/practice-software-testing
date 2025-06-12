# Registration Feature - Data-Driven Automation Testing

This test suite provides comprehensive data-driven automation testing for the Registration Feature using Playwright and TypeScript.

## Features

- **Data-Driven Testing**: Uses CSV file for test data management
- **Flexible Test Selection**: Run all tests or specific test cases
- **Comprehensive Form Testing**: Tests all registration form fields
- **Error Handling**: Captures validation errors and screenshots
- **Special Value Processing**: Handles empty values, repeated characters, etc.
- **Browser Compatibility**: Works across Chrome, Firefox, and Safari

## File Structure

```
tests/
├── data/
│   └── input/
│       └── register_test_data.csv    # Test data file
├── types/
│   └── test-data.types.ts           # TypeScript type definitions
├── utils/
│   ├── data-reader.ts               # CSV data reading utilities
│   ├── form-helpers.ts              # Form interaction helpers
│   └── test-config.ts               # Configuration management
├── registration.spec.ts             # Main test script
└── README.md                        # This documentation
```

## Usage

### Run All Tests

```bash
npx playwright test registration.spec.ts
```

### Run Specific Test Cases

#### Using Environment Variables

```bash
# Run specific test cases
TEST_CASES="REG-EP-01,REG-EP-02,REG-BVA-01" npx playwright test registration.spec.ts

# Run all tests explicitly
RUN_ALL_TESTS=true npx playwright test registration.spec.ts

# Use custom data file
TEST_DATA_FILE="tests/data/input/custom_test_data.csv" npx playwright test registration.spec.ts
```

#### Using Configuration in Code

```typescript
import { TestConfigManager } from "./utils/test-config";

// Before running tests, set configuration
TestConfigManager.setTestCases(["REG-EP-01", "REG-EP-02"]);
// or
TestConfigManager.runAllTests();
```

### Test Data Format

The CSV file should have the following columns:

- `TestCaseID`: Unique identifier for the test case
- `FirstName`: First name value
- `LastName`: Last name value
- `DOB`: Date of birth (MM/DD/YYYY format)
- `Street`: Street address
- `City`: City name
- `State`: State/Province
- `Country`: Country code
- `PostalCode`: Postal/ZIP code
- `Phone`: Phone number
- `Email`: Email address
- `Password`: Password

### Special Values in Test Data

- `(empty)` or `""`: Represents empty/blank values
- `(none)`: Represents no selection (for dropdowns)
- `256×'A'`: Represents repeated characters (256 'A' characters)
- `"""value"""`: Represents quoted values

## Test Results

### Screenshots

Screenshots are automatically captured:

- Before form submission: `before-submit-{TestCaseID}.png`
- After form submission: `after-submit-{TestCaseID}.png`
- On test failure: `failure-{TestCaseID}.png`

### Console Output

Each test provides detailed console output including:

- Test case ID and data
- Validation errors (if any)
- Submission results
- Execution time

### Expected Behaviors

The tests check for:

- Successful form submission (redirect to login page)
- Validation errors displayed on the form
- Form field interactions
- Browser compatibility

## Configuration Options

### TestConfigManager Methods

- `setTestCases(ids: string[])`: Set specific test cases to run
- `runAllTests()`: Run all available test cases
- `setConfig(config: Partial<TestConfig>)`: Set custom configuration
- `loadConfigFromEnvironment()`: Load config from environment variables

### Environment Variables

- `TEST_CASES`: Comma-separated list of test case IDs
- `RUN_ALL_TESTS`: Set to 'true' to run all tests
- `TEST_DATA_FILE`: Path to custom test data file

## Browser Support

The test suite supports all Playwright browsers:

- Chromium
- Firefox
- WebKit (Safari)

## Troubleshooting

### Common Issues

1. **Test data file not found**

   - Ensure the CSV file exists at the specified path
   - Check file permissions

2. **Form elements not found**

   - Verify data-test attributes in the HTML
   - Check if the application URL is correct

3. **Date format issues**
   - Ensure dates are in MM/DD/YYYY format in CSV
   - Check browser date input compatibility

### Debug Mode

Run tests in debug mode:

```bash
npx playwright test registration.spec.ts --debug
```

### Headed Mode

Run tests with visible browser:

```bash
npx playwright test registration.spec.ts --headed
```

## Contributing

When adding new test cases:

1. Add data to the CSV file
2. Use meaningful test case IDs
3. Follow the special value conventions
4. Update documentation if needed

## Best Practices

1. **Test Data Management**: Keep test data organized and meaningful
2. **Assertions**: Add specific assertions based on expected behaviors
3. **Error Handling**: Always handle potential errors gracefully
4. **Screenshots**: Use screenshots for visual verification
5. **Configuration**: Use environment variables for CI/CD integration
