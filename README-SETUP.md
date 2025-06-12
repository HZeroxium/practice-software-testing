# Playwright Test Suite Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Setup Playwright Browsers

```bash
npm run setup
```

### 3. Run Tests

```bash
# Registration tests
npm run test:registration

# Admin product tests
npm run test:admin-product
```

## Detailed Setup Instructions

### Prerequisites

- Node.js 18+
- npm or yarn
- Stable internet connection (for browser downloads)

### Installation Steps

1. **Clone and Install**

   ```bash
   git clone <repository>
   cd practice-software-testing
   npm install
   ```

2. **Setup Playwright**

   ```bash
   # Install browsers and dependencies
   npm run setup:all

   # Or step by step:
   npm run setup:deps  # Install system dependencies (Linux only)
   npm run setup       # Install browsers
   ```

3. **Verify Installation**
   ```bash
   npm run test:check
   ```

### Troubleshooting

#### Browser Installation Issues

**Error: Executable doesn't exist**

```bash
# Solution 1: Reinstall browsers
npx playwright install

# Solution 2: Force reinstall
npx playwright install --force

# Solution 3: Install specific browser
npx playwright install chromium
```

**Permission Issues (Windows)**

- Run Command Prompt as Administrator
- Or use PowerShell as Administrator

**Network Issues**

```bash
# Use corporate proxy
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080

# Then retry setup
npm run setup
```

**Disk Space Issues**

- Playwright browsers require ~1GB disk space
- Clear temporary files: `npx playwright uninstall && npm run setup`

#### Common Solutions

1. **Complete Reinstall**

   ```bash
   # Remove node_modules and reinstall
   rm -rf node_modules package-lock.json
   npm install
   npm run setup
   ```

2. **Check Browser Paths**

   ```bash
   # List installed browsers
   npx playwright install --dry-run
   ```

3. **Environment Variables**
   ```bash
   # Set custom browser paths if needed
   export PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/path/to/chrome
   export PLAYWRIGHT_FIREFOX_EXECUTABLE_PATH=/path/to/firefox
   ```

## Available Scripts

| Script                       | Description                      |
| ---------------------------- | -------------------------------- |
| `npm run setup`              | Install Playwright browsers      |
| `npm run setup:deps`         | Install system dependencies      |
| `npm run setup:all`          | Complete setup (deps + browsers) |
| `npm run test:check`         | Verify Playwright installation   |
| `npm run test:registration`  | Run registration tests           |
| `npm run test:admin-product` | Run admin product tests          |
| `npm run test:ui`            | Run tests with UI mode           |
| `npm run test:report`        | Show test report                 |

## CI/CD Setup

### GitHub Actions

```yaml
- name: Setup Playwright
  run: |
    npm ci
    npx playwright install --with-deps
```

### Docker

```dockerfile
FROM mcr.microsoft.com/playwright:v1.51.1-focal
COPY . .
RUN npm ci && npx playwright install
```

## Browser Configuration

### Default Browsers

- Chromium (default)
- Firefox
- WebKit (Safari)

### Custom Configuration

Edit `playwright.config.ts` to customize:

- Browser selection
- Test timeout
- Retry logic
- Screenshots/videos
- Base URL

## Environment Variables

| Variable             | Description                | Default                           |
| -------------------- | -------------------------- | --------------------------------- |
| `TEST_CASES`         | Specific test cases to run | All tests                         |
| `PRODUCT_TEST_CASES` | Product test cases         | All product tests                 |
| `RUN_ALL_TESTS`      | Force run all tests        | false                             |
| `ADMIN_EMAIL`        | Admin email                | admin@practicesoftwaretesting.com |
| `ADMIN_PASSWORD`     | Admin password             | welcome01                         |

## Support

For issues:

1. Check this troubleshooting guide
2. Review Playwright documentation
3. Check GitHub issues
4. Contact the development team
