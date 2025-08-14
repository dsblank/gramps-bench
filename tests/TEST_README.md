# Gramps-Bench Test Program

This directory contains a comprehensive test program (`test_gramps_bench.py`) to verify that the gramps-bench package is working correctly.

## What the Test Program Does

The test program checks:

1. **Package Metadata** - Verifies `pyproject.toml` configuration and package information
2. **Dependencies** - Ensures all required dependencies are available
3. **Package Imports** - Tests all module imports and package exports
4. **Basic Functionality** - Verifies that main functions are callable
5. **Command-Line Programs** - Tests the `gramps-bench` and `gramps-bench-all` command-line tools
6. **Gramps Integration** - Checks Gramps package availability and integration

## Command-Line Tools

### gramps-bench
The main benchmarking tool that runs performance tests on a single Gramps database file.

### gramps-bench-all
A comprehensive tool that runs benchmarks across multiple Gramps versions by:
- Checking out different Git versions of Gramps
- Running benchmarks for each version
- Generating comparative charts
- Optionally opening PDF results

## How to Run the Tests

### Prerequisites

Make sure you have the gramps-bench package installed in development mode:

```bash
pip install -e .
```

### Running the Tests

Simply run the test program:

```bash
python test_gramps_bench.py
```

### Expected Output

If everything is working correctly, you should see output like:

```
🚀 Starting gramps-bench package tests...
Python version: 3.12.2 | packaged by conda-forge | (main, Feb 16 2024, 20:50:58) [GCC 12.3.0]
Working directory: /path/to/gramps-benchmarks

============================================================
🧪 Testing Package Metadata
============================================================
✅ Package name: gramps-bench
✅ Package version: 1.0.0
✅ Package description: Performance benchmarking tools for Gramps genealogy software
...

============================================================
🧪 Test Summary
============================================================
Tests passed: 6/6
  ✅ PASS - Package Metadata
  ✅ PASS - Dependencies
  ✅ PASS - Package Imports
  ✅ PASS - Basic Functionality
  ✅ PASS - Command-Line Programs
  ✅ PASS - Gramps Integration
✅ All tests passed! The gramps-bench package is working correctly.
```

## Troubleshooting

### Command-Line Program Not Found

If the `gramps-bench` or `gramps-bench-all` commands are not found, make sure:

1. The package is installed in development mode: `pip install -e .`
2. The entry points in `pyproject.toml` are correct:
   - `gramps-bench = "gramps_bench.cli.gramps_bench:main"`
   - `gramps-bench-all = "gramps_bench.cli.gramps_bench_all:main"`

### Import Errors

If you see import errors:

1. Check that all dependencies are installed: `pip install -r requirements.txt`
2. Verify that the package structure is correct
3. Make sure you're running from the correct directory

### Gramps Integration Issues

The test program will show warnings if Gramps is not installed, but this is expected if you're only testing the benchmark tools without Gramps itself.

## Test Program Features

- **Comprehensive Coverage**: Tests all major components of the package
- **Clear Output**: Uses emojis and formatting to make results easy to read
- **Error Handling**: Gracefully handles missing dependencies or configuration issues
- **Exit Codes**: Returns appropriate exit codes for CI/CD integration

## Using in CI/CD

The test program returns exit code 0 on success and 1 on failure, making it suitable for continuous integration:

```yaml
# Example GitHub Actions step
- name: Test gramps-bench package
  run: python test_gramps_bench.py
```

## Manual Testing

You can also test individual components manually:

```bash
# Test the command-line programs
gramps-bench --help
gramps-bench-all --help

# Test imports
python -c "import gramps_bench; print('Import successful')"

# Test specific modules
python -c "from gramps_bench.cli.gramps_bench import main; print('CLI module OK')"
python -c "from gramps_bench.cli.gramps_bench_all import main; print('CLI all module OK')"
``` 