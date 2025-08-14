#!/usr/bin/env python3
"""
Test program for gramps-bench package

This script tests:
1. All package imports
2. Command-line program availability
3. Basic functionality of main modules
4. Package metadata and version information
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"🧪 {title}")
    print("=" * 60)

def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")

def print_info(message):
    """Print an info message."""
    print(f"ℹ️  {message}")

def test_package_imports():
    """Test all package imports."""
    print_header("Testing Package Imports")
    
    # Test main package import
    try:
        import gramps_bench
        print_success("Main package 'gramps_bench' imported successfully")
        print_info(f"Version: {gramps_bench.__version__}")
        print_info(f"Author: {gramps_bench.__author__}")
    except ImportError as e:
        print_error(f"Failed to import main package: {e}")
        return False
    
    # Test CLI module imports
    try:
        from gramps_bench.cli import gramps_bench
        print_success("CLI module imported successfully")
    except ImportError as e:
        print_error(f"Failed to import CLI module: {e}")
        return False
    
    # Test performance tests module
    try:
        from gramps_bench import performance_tests
        print_success("Performance tests module imported successfully")
    except ImportError as e:
        print_error(f"Failed to import performance tests module: {e}")
        return False
    
    # Test benchmark charts module
    try:
        from gramps_bench import benchmark_charts
        print_success("Benchmark charts module imported successfully")
    except ImportError as e:
        print_error(f"Failed to import benchmark charts module: {e}")
        return False
    
    # Test all exports from __init__.py
    try:
        from gramps_bench import main, gramps_benchmark, generate_charts
        print_success("All package exports imported successfully")
    except ImportError as e:
        print_error(f"Failed to import package exports: {e}")
        return False
    
    return True

def test_command_line_programs():
    """Test command-line program availability."""
    print_header("Testing Command-Line Programs")
    
    # Test if gramps-bench command is available
    try:
        result = subprocess.run(
            ["gramps-bench", "--help"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            print_success("'gramps-bench' command is available and working")
            print_info("Help output:")
            for line in result.stdout.split('\n')[:5]:  # Show first 5 lines
                if line.strip():
                    print(f"   {line}")
        else:
            print_error(f"'gramps-bench' command failed with return code: {result.returncode}")
            if result.stderr:
                print_error(f"Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print_error("'gramps-bench' command not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print_error("'gramps-bench' command timed out")
        return False
    except Exception as e:
        print_error(f"Error running 'gramps-bench' command: {e}")
        return False
    
    # Test if gramps-bench-all command is available
    try:
        result = subprocess.run(
            ["gramps-bench-all", "--help"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            print_success("'gramps-bench-all' command is available and working")
            print_info("Help output:")
            for line in result.stdout.split('\n')[:5]:  # Show first 5 lines
                if line.strip():
                    print(f"   {line}")
        else:
            print_error(f"'gramps-bench-all' command failed with return code: {result.returncode}")
            if result.stderr:
                print_error(f"Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print_error("'gramps-bench-all' command not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print_error("'gramps-bench-all' command timed out")
        return False
    except Exception as e:
        print_error(f"Error running 'gramps-bench-all' command: {e}")
        return False
    
    return True

def test_package_metadata():
    """Test package metadata and configuration."""
    print_header("Testing Package Metadata")
    
    # Test pyproject.toml parsing
    try:
        import tomllib
        with open("pyproject.toml", "rb") as f:
            config = tomllib.load(f)
        
        project = config.get("project", {})
        name = project.get("name", "unknown")
        version = project.get("version", "unknown")
        description = project.get("description", "unknown")
        
        print_success(f"Package name: {name}")
        print_success(f"Package version: {version}")
        print_success(f"Package description: {description}")
        
        # Check dependencies
        dependencies = project.get("dependencies", [])
        print_info(f"Number of dependencies: {len(dependencies)}")
        for dep in dependencies:
            print_info(f"  - {dep}")
        
        # Check scripts
        scripts = project.get("scripts", {})
        if "gramps-bench" in scripts:
            print_success("Command-line script 'gramps-bench' is configured")
        else:
            print_error("Command-line script 'gramps-bench' not found in configuration")
            return False
            
        if "gramps-bench-all" in scripts:
            print_success("Command-line script 'gramps-bench-all' is configured")
        else:
            print_error("Command-line script 'gramps-bench-all' not found in configuration")
            return False
            
    except Exception as e:
        print_error(f"Failed to read package metadata: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of main modules."""
    print_header("Testing Basic Functionality")
    
    # Test main function availability
    try:
        from gramps_bench import main
        print_success("Main function is callable")
        
        # Test that main function exists and is callable
        if callable(main):
            print_success("Main function is callable")
        else:
            print_error("Main function is not callable")
            return False
    except Exception as e:
        print_error(f"Failed to test main function: {e}")
        return False
    
    # Test benchmark chart generation function
    try:
        from gramps_bench import generate_charts
        if callable(generate_charts):
            print_success("Generate charts function is callable")
        else:
            print_error("Generate charts function is not callable")
            return False
    except Exception as e:
        print_error(f"Failed to test generate charts function: {e}")
        return False
    
    # Test performance benchmark function
    try:
        from gramps_bench import gramps_benchmark
        if callable(gramps_benchmark):
            print_success("Performance benchmark function is callable")
        else:
            print_error("Performance benchmark function is not callable")
            return False
    except Exception as e:
        print_error(f"Failed to test performance benchmark function: {e}")
        return False
    
    return True

def test_gramps_integration():
    """Test Gramps integration (if available)."""
    print_header("Testing Gramps Integration")
    
    try:
        import gramps
        print_success("Gramps package is available")
        
        # Test Gramps version
        from gramps.version import VERSION
        print_success(f"Gramps version: {VERSION}")
        
        # Test some basic Gramps imports that the benchmark uses
        try:
            from gramps.gen.db.utils import import_as_dict, make_database
            print_success("Gramps database utilities imported successfully")
        except ImportError as e:
            print_error(f"Failed to import Gramps database utilities: {e}")
            return False
        
        try:
            from gramps.gen.user import User
            print_success("Gramps User class imported successfully")
        except ImportError as e:
            print_error(f"Failed to import Gramps User class: {e}")
            return False
        
        try:
            from gramps.gen.config import config
            print_success("Gramps config imported successfully")
        except ImportError as e:
            print_error(f"Failed to import Gramps config: {e}")
            return False
            
    except ImportError:
        print_info("Gramps package not available - this is expected if not installed")
        print_info("Benchmark functionality will be limited without Gramps")
        return True  # Not a failure, just informational
    
    return True

def test_dependencies():
    """Test that all required dependencies are available."""
    print_header("Testing Dependencies")
    
    required_deps = [
        "pytest",
        "pytest_benchmark",
        "matplotlib",
        "numpy"
    ]
    
    all_available = True
    
    for dep in required_deps:
        try:
            importlib.import_module(dep.replace("-", "_"))
            print_success(f"'{dep}' is available")
        except ImportError:
            print_error(f"'{dep}' is not available")
            all_available = False
    
    return all_available

def main():
    """Run all tests."""
    print("🚀 Starting gramps-bench package tests...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    tests = [
        ("Package Metadata", test_package_metadata),
        ("Dependencies", test_dependencies),
        ("Package Imports", test_package_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Command-Line Programs", test_command_line_programs),
        ("Gramps Integration", test_gramps_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    if passed == total:
        print_success("All tests passed! The gramps-bench package is working correctly.")
        return 0
    else:
        print_error(f"{total - passed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 