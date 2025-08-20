# Gramps Performance Tests

This directory contains performance tests for Gramps using pytest-benchmark.

## Results

* [Markdown](https://github.com/dsblank/gramps-bench/blob/main/benchmarks/Linux-CPython-3.12-64bit.md)
* [PDF](https://github.com/dsblank/gramps-bench/blob/main/benchmarks/Linux-CPython-3.12-64bit.pdf)

## Installation

### Install from PyPI
```bash
pip install gramps-bench
```

### Install from source
```bash
# Clone the repository
git clone https://github.com/gramps-project/gramps-benchmarks.git
cd gramps-benchmarks

# Install in development mode
pip install -e .
```

## Quick Start

### Run Performance Tests
```bash
# 🚀 Run performance tests and automatically save results
gramps-bench example/gramps/example.gramps

# 🚀 Run with custom version override
gramps-bench example/gramps/example.gramps --version 6.0.4-b1

# 🚀 Run with custom output directory
gramps-bench example/gramps/example.gramps --output /path/to/results
```

### Run Multi-Version Performance Tests
```bash
# 🔄 Run benchmarks across multiple Gramps versions
gramps-bench-all /path/to/gramps_file.gramps /path/to/gramps/source

# 🔄 Run with specific versions
gramps-bench-all data.gramps /home/user/gramps --versions v5.1.6 v5.2.4 v6.0.4

# 🔄 Run with custom output and auto-open results
gramps-bench-all data.gramps /home/user/gramps --output /tmp/results --open
```

### Generate Charts from Existing Results
```bash
# 📊 Generate charts from existing benchmark files
gramps-bench

# 📊 Generate charts from specific directory
gramps-bench --output /path/to/benchmarks
```

### Output Formats

Gramps-bench supports two output formats for charts:

#### PDF Format (Default)
```bash
# Generate PDF charts (default)
gramps-bench --format pdf

# Generate PDF charts with multi-version comparison
gramps-bench-all data.gramps /home/user/gramps --format pdf --open
```

#### HTML Format
```bash
# Generate HTML webpages with interactive charts
gramps-bench --format html

# Generate HTML webpages with multi-version comparison
gramps-bench-all data.gramps /home/user/gramps --format html --open
```

**HTML Output Features:**
- **Interactive Webpages**: View results in any web browser
- **Embedded Charts**: PNG images embedded in the HTML
- **Detailed Tables**: Comprehensive performance data tables
- **Responsive Design**: Works on desktop and mobile devices
- **Easy Sharing**: HTML files can be easily shared and viewed without special software

#### Markdown Format (GitHub Compatible)
```bash
# Generate Markdown pages (GitHub compatible)
gramps-bench --format markdown

# Generate Markdown pages with multi-version comparison
gramps-bench-all data.gramps /home/user/gramps --format markdown --open
```

**Markdown Output Features:**
- **GitHub Compatible**: Renders perfectly on GitHub and other Git platforms
- **No Security Restrictions**: No issues with special characters in filenames
- **Easy Version Control**: Markdown files work seamlessly with Git
- **Universal Support**: Viewable on any platform that supports Markdown
- **Embedded Charts**: PNG images embedded in the Markdown
- **Detailed Tables**: Comprehensive performance data in Markdown tables

**PDF Output Features:**
- **Print-Friendly**: Optimized for printing and documentation
- **Compact**: Single file contains all charts and data
- **Professional**: Suitable for reports and presentations

## Advanced Usage

### Direct pytest Usage
```bash
# Set environment variable and run (results automatically saved)
GRAMPS_FILE=example/gramps/example.gramps python -m pytest gramps_bench/performance_tests.py --benchmark-save=6.0.4

# Run with version override
GRAMPS_FILE=example/gramps/example.gramps GRAMPS_VERSION=6.0.4-b1 python -m pytest gramps_bench/performance_tests.py --benchmark-save=6.0.4-b1
```

### Python Module Usage
```python
from gramps_bench import gramps_benchmark, generate_charts

# Run benchmarks programmatically
success = gramps_benchmark(gramps_file="example.gramps", output_dir="./results")

# Generate charts programmatically
generate_charts(output_dir="./results")
```

### Version Override

You can override the Gramps version used in performance tests and result naming:

```bash
# Using the command-line script
gramps-bench example.gramps --version 6.0.4-b1

# Using environment variable with pytest directly
GRAMPS_VERSION=6.0.4-b1 python -m pytest gramps_bench/performance_tests.py
```

This is useful when:
- Testing pre-release versions
- Comparing performance across different versions
- Creating custom version labels for your test results

## Multi-Version Benchmarking with gramps-bench-all

The `gramps-bench-all` command allows you to run performance benchmarks across multiple Gramps versions and generate comparative charts. This is particularly useful for:

- **Version Comparison**: Compare performance between different Gramps releases
- **Regression Testing**: Identify performance regressions between versions
- **Release Planning**: Assess performance impact of new features

### Prerequisites

Before using `gramps-bench-all`, ensure you have:

1. **Gramps Source Repository**: A local clone of the Gramps git repository
2. **Test Data**: A Gramps database file to use for benchmarking
3. **Git Access**: The ability to checkout different versions in the Gramps repository

### Basic Usage

```bash
# Run benchmarks across default versions (v5.1.6, v5.2.4, v6.0.4)
gramps-bench-all /path/to/gramps_file.gramps /path/to/gramps/source

# Run with specific versions
gramps-bench-all data.gramps /home/user/gramps --versions v5.1.6 v5.2.4

# Run with custom output directory
gramps-bench-all data.gramps /home/user/gramps --output /tmp/benchmark_results
```

### Advanced Options

```bash
# Run with auto-opening results
gramps-bench-all data.gramps /home/user/gramps --open

# Skip chart generation (only run benchmarks)
gramps-bench-all data.gramps /home/user/gramps --skip-charts

# Combine multiple options
gramps-bench-all data.gramps /home/user/gramps \
    --versions v5.1.6 v5.2.4 v6.0.4 \
    --output /tmp/results \
    --open
```

### What gramps-bench-all Does

1. **Git Checkout**: Automatically checks out each specified version in the Gramps source repository
2. **Benchmark Execution**: Runs the full benchmark suite for each version
3. **Result Collection**: Saves benchmark results with version-specific naming
4. **Chart Generation**: Creates comparative charts showing performance across versions (PDF or HTML)
5. **Result Opening**: Optionally opens the generated charts with the default viewer (PDF viewer or web browser)

### Output Structure

When using `gramps-bench-all`, the output directory will contain:

```
output_directory/
├── .benchmarks/
│   └── Linux-CPython-3.12-64bit/
│       ├── 0001_v5.1.6.json
│       ├── 0002_v5.2.4.json
│       ├── 0003_v6.0.4.json
│       └── 0004_current.json
├── benchmark_charts.pdf (or .html)
└── performance_comparison.pdf (or .html)
```

## What the Tests Measure

The performance tests benchmark various Gramps operations:

- **Database Loading**: Time to load a Gramps database file
- **Person Queries**: Retrieving person records from the database
- **Family Queries**: Retrieving family records
- **Source Queries**: Retrieving source records
- **Filter Operations**: Applying filters to person data
- **Transaction Operations**: Adding new records to the database
- **Scalability Tests**: Performance with different data sizes (10, 50, 100 records)

## Output

- **Console**: Real-time benchmark results with statistics
- **Charts**: PDF or HTML files with performance visualizations (when generating charts)
- **Benchmark Files**: Automatically saved in `.benchmarks/` directory with gramps version as default name

## Results Naming

When you run the tests with a gramps file, results are automatically saved with the naming convention:
- **Default**: `{version}` (e.g., `6.0.4`)
- **With Override**: `{override_version}` (e.g., `6.0.4-b1`)
- **Location**: `.benchmarks/Linux-CPython-3.12-64bit/0001_{version}.json`

## Requirements

- pytest
- pytest-benchmark
- matplotlib
- numpy
- gramps (the main application)

## Development

### Building the Package
```bash
# Build source distribution
python -m build

# Build wheel
python -m build --wheel
```

### Running Tests
```bash
# Run the benchmark tests
python -m pytest gramps_bench/performance_tests.py

# Run with coverage
python -m pytest gramps_bench/ --cov=gramps_bench
```
