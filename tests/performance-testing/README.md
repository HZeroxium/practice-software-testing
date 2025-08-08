# Performance Testing Automation System

## Overview

This comprehensive performance testing automation system is designed for "The Toolshop" application (`sprint5-with-bugs` version). It provides automated JMeter test execution, dynamic configuration management, intelligent duration optimization, and comprehensive reporting capabilities.

## 🎯 Key Features

- ✅ **Intelligent Duration Optimization**: 5 predefined profiles (quick, short, medium, long, extended)
- ✅ **Real-time Execution Monitoring**: Actual vs estimated time tracking
- ✅ **Automated Cleanup**: Smart folder and file management
- ✅ **Dynamic Configuration**: Hot-reload config changes
- ✅ **Comprehensive Reporting**: Excel, HTML, and Markdown formats
- ✅ **AI-Enhanced Testing**: Optimized test design and analysis

## 🎯 Objectives

Based on **HW06-PerformanceTesting.md** requirements, this system delivers:

- ✅ **Test Cases** in CSV format with actual results
- ✅ **JMeter Scripts** (.jmx) for Load, Stress, and Spike testing
- ✅ **Data Files** for parameterized testing
- ✅ **Bug Reports** automatically generated from performance issues
- ✅ **Performance Testing Report** with comprehensive analysis
- ✅ **Automated Execution** with dynamic configuration
- ✅ **Report Management** with cleanup capabilities

## 📁 Directory Structure

```
performance-testing/
├── README.md                           # This file - Main documentation
├── docs/                               # Detailed documentation
│   └── StudentID_PerformanceTesting.md # Main performance testing report
├── config/                             # Configuration files
│   └── test_config.json               # Central configuration with duration profiles
├── data/                               # Test data and reports
│   ├── StudentID_TestCases.xlsx       # Test cases with results (Excel format)
│   ├── StudentID_BugReport.xlsx       # Generated bug reports (Excel format)
│   ├── StudentID_TestCases.csv        # Test cases source (CSV with tab delimiter)
│   ├── StudentID_BugReport.csv        # Bug reports source (CSV with tab delimiter)
│   ├── product_ids.csv                # Product IDs for stress testing
│   └── contact_form_data.csv          # Contact form data for spike testing
├── scripts/                            # JMeter test scripts (auto-generated)
│   ├── load_test_product_listing_normal.jmx
│   ├── load_test_product_listing_high.jmx
│   ├── stress_test_product_listing_moderate.jmx
│   ├── stress_test_product_listing_extreme.jmx
│   ├── spike_test_product_listing_short.jmx
│   └── spike_test_product_listing_long.jmx
├── results/                            # Test execution results
│   ├── *.jtl                          # JMeter raw results
│   ├── *.log                          # Execution logs
│   ├── *_report/                      # JMeter HTML reports
│   ├── test_execution_summary.json    # Execution summary
│   └── cleanup_report.md              # Cleanup operation reports
├── logs/                               # System logs
├── temp/                               # Temporary files
├── submission/                         # Final submission files
└── report/                             # Generated reports
    └── StudentID_PerformanceTesting.md # Main performance testing report
```

## 🚀 Quick Start

### Prerequisites

1. **JMeter 5.6.3+** installed and accessible
2. **Python 3.8+** with required packages
3. **The Toolshop Application** running:
   - Frontend: `http://localhost:4200`
   - API: `http://localhost:8091`

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify JMeter installation
python jmeter_runner.py --check-jmeter
```

### Quick Test with Profile Selection

```bash
# Run with default profile (medium)
python quick_test.py

# Edit profile in quick_test.py line 47:
profile_name = "quick"    # 15 seconds
profile_name = "short"    # 5 minutes
profile_name = "medium"   # 15 minutes
profile_name = "long"     # 30 minutes
profile_name = "extended" # 60 minutes
```

### Interactive Duration Management

```bash
# Interactive duration manager
python duration_manager.py

# Apply specific duration profiles
python config_manager.py  # Choose options 10-13
```

### Full Test Execution

```bash
# Run complete performance testing workflow
python run_performance_tests.py
```

### Real-time Execution Monitoring

The system now provides real-time execution monitoring:

```bash
# Example output with actual vs estimated time
⏱️  Estimated execution time: ~12.1 minutes
⏱️  Actual execution time: ~753.3 seconds (12.6 minutes)
```

## 🔧 Core Components

### 1. **run_performance_tests.py** - Main Orchestrator

- **Purpose**: Single entry point for all performance testing activities
- **Features**:
  - Automated workflow execution
  - Dynamic configuration management
  - Report generation and cleanup
  - Integration of all components

### 2. **config_manager.py** - Configuration Management

- **Purpose**: Interactive configuration management
- **Features**:
  - Create quick test configurations
  - Create production test configurations
  - Interactive parameter modification
  - Configuration validation

### 3. **jmeter_template_generator.py** - Dynamic JMeter Scripts

- **Purpose**: Generate JMeter test plans from configuration
- **Features**:
  - Dynamic script generation
  - Configuration-driven parameters
  - Support for all test types (Load, Stress, Spike)

### 4. **jmeter_runner.py** - JMeter Execution Engine

- **Purpose**: Execute JMeter tests and parse results
- **Features**:
  - Non-GUI JMeter execution
  - Result parsing and analysis
  - Environment validation
  - HTML report generation

### 5. **report_generator.py** - Report Generation

- **Purpose**: Generate comprehensive reports
- **Features**:
  - Bug report generation
  - Test case result updates
  - Performance issue identification
  - Execution summary creation

### 6. **report_cleaner.py** - Report Management

- **Purpose**: Manage test results and reports
- **Features**:
  - Automatic cleanup of old reports
  - Disk space management
  - Configurable retention policies

### 7. **view_reports.py** - Report Viewer

- **Purpose**: View and analyze generated reports
- **Features**:
  - HTML report navigation
  - CSV report viewing
  - Execution summary display
  - Quick access to all artifacts

### 8. **test_duration_optimizer.py** - Duration Optimization

- **Purpose**: Optimize test duration based on desired execution time
- **Features**:
  - 5 predefined duration profiles (quick, short, medium, long, extended)
  - Custom duration optimization with intelligent parameter adjustment
  - Real-time execution time estimation
  - Automatic JMeter parameter optimization
  - Profile-based configuration management

### 9. **duration_manager.py** - Duration Management

- **Purpose**: Interactive duration profile management
- **Features**:
  - Easy profile switching with real-time feedback
  - Custom duration optimization with validation
  - Quick test execution with profile selection
  - Real-time configuration updates and verification
  - Execution time comparison (estimated vs actual)

### 10. **quick_test.py** - Quick Test Runner

- **Purpose**: Fast test execution with profile selection
- **Features**:
  - Profile-based test configuration
  - Real-time execution monitoring
  - Actual vs estimated time tracking
  - Comprehensive result reporting
  - Integration with duration optimizer

## 📊 Test Scenarios

### 1. **Load Testing** - Product Listing

- **Target**: Product listing page and API
- **Objective**: Verify performance under normal load
- **Endpoints**:
  - `http://localhost:4200/` (Frontend)
  - `http://localhost:8091/products` (API)

### 2. **Stress Testing** - Product Detail

- **Target**: Product detail pages with related products
- **Objective**: Identify breaking points under high load
- **Endpoints**:
  - `http://localhost:4200/product/{id}` (Frontend)
  - `http://localhost:8091/products/{id}` (API)
  - `http://localhost:8091/products/{id}/related` (API)

### 3. **Spike Testing** - Contact Form

- **Target**: Contact form submission
- **Objective**: Test system recovery after traffic spikes
- **Endpoints**:
  - `http://localhost:8091/messages` (API POST)

## ⚙️ Configuration

### Duration Profiles

The system now supports intelligent duration optimization with predefined profiles:

#### Quick Profile (~15 seconds)

- **Purpose**: Fast validation testing
- **Use Case**: Code verification, quick checks
- **Command**: `python duration_manager.py` → Option 3

#### Short Profile (~5 minutes)

- **Purpose**: Brief performance testing
- **Use Case**: Development testing, basic validation
- **Command**: `python duration_manager.py` → Option 4

#### Medium Profile (~15 minutes)

- **Purpose**: Standard performance testing
- **Use Case**: Regular testing, moderate load validation
- **Command**: `python duration_manager.py` → Option 5

#### Long Profile (~30 minutes)

- **Purpose**: Comprehensive performance testing
- **Use Case**: Production-like testing, thorough validation
- **Command**: `python duration_manager.py` → Option 6

#### Extended Profile (~60 minutes)

- **Purpose**: Extended performance testing
- **Use Case**: Deep analysis, stress testing
- **Command**: `python duration_manager.py` → Option 7

### Custom Duration Optimization

```bash
# Optimize for specific duration (e.g., 45 minutes)
python duration_manager.py  # Option 8
# Enter: 45

# Or use config manager
python config_manager.py    # Option 12
# Enter: 45
```

### Automatic Parameter Adjustment

The system automatically adjusts:

- **Threads**: Based on duration and test type
- **Loops**: Optimized for target execution time
- **Ramp-up**: Proportional to test duration
- **Test distribution**: Balanced across load, stress, and spike tests

## 📈 Generated Artifacts

### 1. **Test Cases** (`data/StudentID_TestCases.xlsx`)

- 6 comprehensive test cases (2 Load + 2 Stress + 2 Spike)
- Actual results populated automatically with real execution data
- Pass/Fail status based on configurable thresholds
- Professional Excel formatting with color-coded results
- Auto-adjusted column widths and borders
- Real-time data from JMeter execution

### 2. **Bug Reports** (`data/StudentID_BugReport.xlsx`)

- Automatically generated from performance issues detected during execution
- Detailed reproduction steps with actual test data
- Priority classification based on impact analysis
- Screenshot references and evidence collection
- Professional Excel formatting with clean styling
- Integration with test execution results

### 3. **JMeter HTML Reports** (`results/*_report/`)

- Interactive dashboards with real-time data
- Performance graphs and charts with actual metrics
- Detailed request/response analysis
- Error analysis with root cause identification
- APDEX (Application Performance Index) calculations
- Response time distribution analysis

### 4. **Main Report** (`docs/StudentID_PerformanceTesting.md`)

- Comprehensive analysis with actual execution data
- Performance findings with real metrics
- Recommendations based on actual bottlenecks
- Self-assessment with detailed justification
- AI tools usage documentation
- YouTube video integration

### 5. **Execution Summary** (`results/test_execution_summary.json`)

- Real-time execution statistics
- Test pass/fail rates
- Performance metrics aggregation
- Bug count and classification
- Duration profile effectiveness analysis

### 6. **Cleanup Reports** (`results/cleanup_report.md`)

- Automated cleanup operation logs
- Disk space savings analysis
- File retention policy enforcement
- System maintenance tracking

## 🛠️ Usage Examples

### Interactive Configuration

```bash
# Configure test parameters interactively
python config_manager.py

# Create quick test configuration
python config_manager.py --quick

# Create production configuration
python config_manager.py --production
```

### Custom Test Execution

```bash
# Run with custom configuration
python run_performance_tests.py --config custom_config.json

# Run specific test scenarios
python run_performance_tests.py --scenarios load,stress

# Skip report cleanup
python run_performance_tests.py --no-cleanup
```

### Report Management

```bash
# View all reports
python view_reports.py

# Clean old reports manually
python report_cleaner.py --keep-recent 2

# Generate cleanup report
python report_cleaner.py --report-only
```

## 📋 Assessment Criteria Compliance

This system fully satisfies the **HW06-PerformanceTesting.md** requirements:

### ✅ **Test Cases (Excel Format)**

- **Format**: Test Case ID, Title, Preconditions, Inputs, Test Steps, Expected Result, Actual Result, Result
- **Content**: 6 comprehensive test cases covering Load, Stress, and Spike testing
- **Automation**: Actual results and pass/fail status populated automatically
- **Professional Formatting**: Excel (.xlsx) with color-coded results and styling
- **CSV Source**: Tab-delimited CSV to avoid comma conflicts in data

### ✅ **JMeter Scripts (.jmx)**

- **Load Test**: Product listing page and API
- **Stress Test**: Product detail pages with related products
- **Spike Test**: Contact form submission
- **Dynamic**: Generated from configuration files

### ✅ **Data Files**

- **product_ids.csv**: Product IDs for stress testing
- **contact_form_data.csv**: Contact form data for spike testing
- **Headers**: Properly formatted for JMeter CSV Data Set

### ✅ **Bug Report (Excel Format)**

- **Format**: BugID, Summary, Steps To Reproduce, Actual vs Expected Result, Screenshot, Priority, Affected Feature / Version
- **Generation**: Automatically created from performance issues
- **Content**: Detailed bug descriptions with reproduction steps
- **Professional Formatting**: Excel (.xlsx) with clean styling and borders
- **CSV Source**: Tab-delimited CSV to avoid comma conflicts in data

### ✅ **Performance Testing Report**

- **Format**: Markdown with comprehensive analysis
- **Content**: Test execution results, bug findings, recommendations
- **Structure**: Follows assignment requirements

### ✅ **Automation Features**

- **Single Command Execution**: `python run_performance_tests.py`
- **Dynamic Configuration**: Easy parameter modification
- **Report Management**: Automatic cleanup and organization
- **Comprehensive Logging**: Detailed execution traces

## 🔍 Troubleshooting

### Common Issues

1. **JMeter Not Found**

   ```bash
   # Check JMeter installation
   python jmeter_runner.py --check-jmeter
   ```

2. **Application Not Accessible**

   ```bash
   # Verify application URLs
   curl http://localhost:4200
   curl http://localhost:8091/products
   ```

3. **CSV Data File Errors**

   ```bash
   # Regenerate JMeter templates
   python jmeter_template_generator.py
   ```

4. **Report Cleanup Issues**

   ```bash
   # Manual cleanup
   python report_cleaner.py --force
   ```

## 📚 Additional Documentation

- **[Quick Test Guide](docs/quick-test-guide.md)**: How to run quick validation tests
- **[Production Test Guide](docs/production-test-guide.md)**: How to configure and run production tests
- **[Troubleshooting Guide](docs/troubleshooting.md)**: Common issues and solutions
- **[Main Performance Report](docs/StudentID_PerformanceTesting.md)**: Comprehensive analysis and findings

## 🤝 Contributing

This system is designed for educational purposes and follows best practices for:

- **Modular Design**: Each component has a specific responsibility
- **Configuration Management**: Centralized and dynamic configuration
- **Error Handling**: Comprehensive error handling and logging
- **Documentation**: Detailed documentation and usage examples

## 📄 License

This project is created for educational purposes as part of the Software Testing course requirements.
