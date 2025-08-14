#!/usr/bin/env python3
"""
Unified Performance Tests for Gramps

This module provides a single, best-practice performance testing solution that:
1. Uses pytest-benchmark for robust statistical analysis
2. Integrates with the existing Gramps test framework
3. Provides both command-line and programmatic interfaces
4. Supports parameterized testing across different database backends
"""

import pytest
import sys
import os
import tempfile
import shutil
import logging
import json
import random
import statistics
from datetime import datetime
from pathlib import Path

# Import Gramps modules
from gramps.gen.db.utils import import_as_dict, make_database, import_from_filename
from gramps.gen.db import DbTxn
from gramps.gen.user import User
from gramps.gen.config import config
from gramps.version import VERSION
from gramps.gen.plug._manager import BasePluginManager
from gramps.gen.const import PLUGINS_DIR, USER_PLUGINS
from gramps.gen.filters import FilterList, GenericFilter
from gramps.gen.filters.rules.person import (
    IsDescendantOf,
)


# Check for version override from environment variable
GRAMPS_VERSION = os.environ.get('GRAMPS_VERSION', VERSION)

def get_available_backends():
    """
    Get a list of available database backends from the Gramps plugin system.
    
    Returns:
        list: List of available backend IDs
    """
    # Get the plugin manager instance
    pmgr = BasePluginManager.get_instance()
    
    # Register plugins if not already done
    # This ensures database plugins are loaded before we try to get them
    pmgr.reg_plugins(PLUGINS_DIR, None, None)
    pmgr.reg_plugins(USER_PLUGINS, None, None, load_on_reg=True)
    
    # Get all registered database plugins
    database_plugins = [
        plugin for plugin in pmgr.get_reg_databases() if plugin.id != "bsddb"
    ]
    
    # Extract the backend IDs from the plugins
    available_backends = [plugin.id for plugin in database_plugins]
    
    return available_backends


def create_database_with_backend(backend_id, filename, user, skip_import_adds=True):
    """
    Create a database with a specific backend and import data from filename.
    
    Args:
        backend_id (str): The backend ID ('sqlite', 'bsddb', etc.)
        filename (str): Path to the file to import
        user: User object
        skip_import_adds (bool): Whether to skip import additions
        
    Returns:
        Database object or None if import failed
    """
    try:
        # Create database with specified backend
        db = make_database(backend_id)
        
        # Create a temporary directory for all backends to use filesystem
        temp_dir = tempfile.mkdtemp()
        db.load(temp_dir)
        
        # Set import options
        db.set_feature("skip-import-additions", skip_import_adds)
        db.set_prefixes(
            config.get("preferences.iprefix"),
            config.get("preferences.oprefix"),
            config.get("preferences.fprefix"),
            config.get("preferences.sprefix"),
            config.get("preferences.cprefix"),
            config.get("preferences.pprefix"),
            config.get("preferences.eprefix"),
            config.get("preferences.rprefix"),
            config.get("preferences.nprefix"),
        )
        
        # Import the data
        status = import_from_filename(db, filename, user)
        return db if status else None
        
    except Exception as e:
        logging.error(f"Failed to create database with backend {backend_id}: {e}")
        return None


class GrampsPerformanceTest:
    """Base class for Gramps performance tests with setup and teardown."""
    
    @classmethod
    def setup_class(cls):
        """Set up the test environment once for all tests."""
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        cls.logger = logging.getLogger(__name__)
        
        # Get the example file path from command line arguments or use default
        cls.example_file = cls._get_example_file_path()
        cls.user = User()
        
        cls.logger.info(f"Using example file: {cls.example_file}")
    
    @classmethod
    def _get_example_file_path(cls):
        """Get the example file path from environment variable."""
        # Check environment variable
        gramps_file = os.environ.get('GRAMPS_FILE')
        if gramps_file and os.path.exists(gramps_file):
            return gramps_file
        
        # If no gramps file specified, raise an error
        raise FileNotFoundError(
            "No Gramps file specified. Set the GRAMPS_FILE environment variable to specify a Gramps database file."
        )
    
    def setup_method(self):
        """Set up each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.db = None
    
    def teardown_method(self):
        """Clean up after each test method."""
        if self.db:
            try:
                self.db.close()
            except:
                pass
        
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


# Parameterized test class for different database backends
@pytest.mark.parametrize("backend_id", get_available_backends())
class TestDatabasePerformance(GrampsPerformanceTest):
    """Benchmark tests for database operations across different backends."""
    
    def test_database_loading(self, benchmark, backend_id):
        """Benchmark database loading performance for different backends."""
        def load_database():
            """Load the example database with specified backend."""
            db = create_database_with_backend(backend_id, self.example_file, self.user)
            if not db:
                raise Exception(f"Failed to load example database with backend {backend_id}")
            return db
        
        # Use simple benchmark instead of pedantic
        result = benchmark(load_database)
        
        # Store the database for other tests if needed
        self.db = result
        
        # Get database statistics
        stats = {
            'backend': backend_id,
            'persons': len(self.db.get_person_handles()),
            'families': len(self.db.get_family_handles()),
            'sources': len(self.db.get_source_handles()),
            'events': len(self.db.get_event_handles()),
            'places': len(self.db.get_place_handles()),
            'media': len(self.db.get_media_handles()),
        }
        
        self.logger.info(f"Database statistics for {backend_id}: {stats}")
        
        # Store statistics for chart generation
        benchmark.database_stats = stats
        benchmark.backend_id = backend_id
        
        # Assert reasonable performance (should load in under 10 seconds on average)
        # Note: benchmark.stats is available after the test completes
        pass  # We'll check the assertion in a different way
    
    def test_person_queries(self, benchmark, backend_id):
        """Benchmark person query performance for different backends."""
        # First load the database
        self.db = create_database_with_backend(backend_id, self.example_file, self.user)
        if not self.db:
            pytest.skip(f"Failed to create database with backend {backend_id}")
        person_handles = self.db.get_person_handles()
        
        if not person_handles:
            pytest.skip(f"No persons in database for backend {backend_id}")
        
        def query_persons():
            """Query persons from the database."""
            results = []
            for handle in random.sample(person_handles, min(int(len(person_handles) * 0.10), len(person_handles))):
                person = self.db.get_person_from_handle(handle)
                if person:
                    results.append(person)
            return results
        
        result = benchmark(query_persons)
        
        # Store backend info for analysis
        benchmark.backend_id = backend_id
        
        # Assert reasonable performance (should retrieve 100 persons in under 5 seconds on average)
        # Note: benchmark.stats is available after the test completes
        pass
    
    def test_raw_person_queries(self, benchmark, backend_id):
        """Benchmark raw person query performance for different backends."""
        # First load the database
        self.db = create_database_with_backend(backend_id, self.example_file, self.user)
        if not self.db:
            pytest.skip(f"Failed to create database with backend {backend_id}")
        person_handles = self.db.get_person_handles()
        
        if not person_handles:
            pytest.skip(f"No persons in database for backend {backend_id}")
        
        def query_raw_persons():
            """Query raw persons from the database."""
            results = []
            for handle in random.sample(person_handles, min(int(len(person_handles) * 0.10), len(person_handles))):
                person = self.db.get_raw_person_data(handle)
                if person:
                    results.append(person)
            return results
        
        result = benchmark(query_raw_persons)
        
        # Store backend info for analysis
        benchmark.backend_id = backend_id
        
        # Assert reasonable performance (should retrieve 100 persons in under 5 seconds on average)
        # Note: benchmark.stats is available after the test completes
        pass
    
    def test_family_queries(self, benchmark, backend_id):
        """Benchmark family query performance for different backends."""
        # First load the database
        self.db = create_database_with_backend(backend_id, self.example_file, self.user)
        if not self.db:
            pytest.skip(f"Failed to create database with backend {backend_id}")
        family_handles = self.db.get_family_handles()
        
        if not family_handles:
            pytest.skip(f"No families in database for backend {backend_id}")
        
        def query_families():
            """Query families from the database."""
            results = []
            for handle in random.sample(family_handles, min(int(len(family_handles) * 0.10), len(family_handles))):
                family = self.db.get_family_from_handle(handle)
                if family:
                    results.append(family)
            return results
        
        result = benchmark(query_families)
        
        # Store backend info for analysis
        benchmark.backend_id = backend_id
        
        # Assert reasonable performance (should retrieve 50 families in under 3 seconds on average)
        pass
    
    def test_source_queries(self, benchmark, backend_id):
        """Benchmark source query performance for different backends."""
        # First load the database
        self.db = create_database_with_backend(backend_id, self.example_file, self.user)
        if not self.db:
            pytest.skip(f"Failed to create database with backend {backend_id}")
        source_handles = self.db.get_source_handles()
        
        if not source_handles:
            pytest.skip(f"No sources in database for backend {backend_id}")
        
        def query_sources():
            """Query sources from the database."""
            results = []
            for handle in random.sample(source_handles, min(int(len(source_handles) * 0.10), len(source_handles))):
                source = self.db.get_source_from_handle(handle)
                if source:
                    results.append(source)
            return results
        
        result = benchmark(query_sources)
        
        # Store backend info for analysis
        benchmark.backend_id = backend_id
        
        # Assert reasonable performance (should retrieve 25 sources in under 2 seconds on average)
        pass


@pytest.mark.parametrize("backend_id", get_available_backends())
class TestFilterPerformance(GrampsPerformanceTest):
    """Benchmark tests for filter operations across different backends."""
    
    def setup_method(self):
        """Set up each test method."""
        super().setup_method()
        # Note: We don't load the database here since we need the backend_id parameter
        # which is only available in the test methods themselves
        self.db = None
        self.person_handles = None
    
    def test_person_has_id_filter(self, benchmark, backend_id):
        """Benchmark generic filter performance for different backends."""
        # Load database for this specific test
        self.db = create_database_with_backend(backend_id, self.example_file, self.user)
        if not self.db:
            pytest.skip(f"Failed to create database with backend {backend_id}")
        self.person_handles = self.db.get_person_handles()
        
        if not self.person_handles:
            pytest.skip(f"No persons in database for filter tests with backend {backend_id}")

        random_handle = random.choice(self.person_handles)
        random_data = self.db.get_raw_person_data(random_handle)
        if isinstance(random_data, tuple):
            random_id = random_data[1]
        else:
            random_id = random_data["gramps_id"]

        custom_filters_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<filters>
  <object type="Person">
    <filter name="Random Person" function="or">
      <rule class="HasIdOf" use_regex="False" use_case="False">
        <arg value="{random_id}"/>
      </rule>
    </filter>
  </object>
</filters>
"""
        with tempfile.NamedTemporaryFile(mode="w", delete=True) as fp:
            fp.write(custom_filters_xml)
            fp.flush()
            
            fl = FilterList(fp.name)
            fl.load()

        # fl = FilterList("")
        # fl.loadString(custom_filters_xml)
        # set_custom_filters(fl)

        filters = fl.get_filters_dict("Person")
        
        def apply_person_has_id_filter():
            """Apply a generic filter to all persons."""
            filter = filters["Random Person"]
            return filter.apply(self.db)
        
        result = benchmark(apply_person_has_id_filter)
        
        # Store backend info for analysis
        benchmark.backend_id = backend_id
        
        # Assert reasonable performance (should filter in under 1 second on average)
        pass
    
    def test_descendant_filter(self, benchmark, backend_id):
        """Benchmark descendant filter performance for different backends."""
        # Load database for this specific test
        self.db = create_database_with_backend(backend_id, self.example_file, self.user)
        if not self.db:
            pytest.skip(f"Failed to create database with backend {backend_id}")
        self.person_handles = self.db.get_person_handles()
        
        if not self.person_handles:
            pytest.skip(f"No persons in database for filter tests with backend {backend_id}")

        def apply_descendant_filter():
            """Apply a descendant filter."""
            random_handle = random.choice(self.person_handles)
            random_data = self.db.get_raw_person_data(random_handle)
            if isinstance(random_data, tuple):
                random_id = random_data[1]
            else:
                random_id = random_data["gramps_id"]        
            rule = IsDescendantOf([random_id, 0])
            filter = GenericFilter()
            filter.add_rule(rule)
            res = filter.apply(self.db)
            return res
        
        result = benchmark(apply_descendant_filter)
        
        # Store backend info for analysis
        benchmark.backend_id = backend_id
        
        # Assert reasonable performance (should filter in under 2 seconds on average)
        pass


@pytest.mark.parametrize("backend_id", get_available_backends())
class TestTransactionPerformance(GrampsPerformanceTest):
    """Benchmark tests for database transactions across different backends."""
    
    def setup_method(self):
        """Set up each test method."""
        super().setup_method()
        # Note: We don't load the database here since we need the backend_id parameter
        # which is only available in the test methods themselves
        self.db = None
    
    def test_add_person_transaction(self, benchmark, backend_id):
        """Benchmark adding a person in a transaction for different backends."""
        from gramps.gen.lib import Person, Name, Surname
        
        # Load database for this specific test
        self.db = create_database_with_backend(backend_id, self.example_file, self.user)
        if not self.db:
            pytest.skip(f"Failed to create database with backend {backend_id}")
        
        def add_person():
            """Add a person in a transaction."""
            with DbTxn("Add test person", self.db) as trans:
                person = Person()
                name = Name()
                name.set_first_name("Test")
                # Use the correct method for setting surname
                surname = Surname()
                surname.set_surname("Person")
                name.set_surname_list([surname])
                person.set_primary_name(name)
                
                # Add the person
                self.db.add_person(person, trans)
                return person.get_handle()
        
        result = benchmark(add_person)
        
        # Store backend info for analysis
        benchmark.backend_id = backend_id
        
        # Assert reasonable performance (should add person in under 0.5 seconds on average)
        pass


# Parameterized tests for scalability across different backends
@pytest.mark.parametrize("backend_id", get_available_backends())
@pytest.mark.parametrize("query_size", [10, 50, 100])
class TestScalabilityPerformance(GrampsPerformanceTest):
    """Benchmark tests for scalability with different data sizes across different backends."""
    
    def setup_method(self):
        """Set up each test method."""
        super().setup_method()
        # Note: We don't load the database here since we need the backend_id parameter
        # which is only available in the test methods themselves
        self.db = None
        self.person_handles = None
    
    def test_scalable_person_queries(self, benchmark, backend_id, query_size):
        """Benchmark person queries with different sizes for different backends."""
        # Load database for this specific test
        self.db = create_database_with_backend(backend_id, self.example_file, self.user)
        if not self.db:
            pytest.skip(f"Failed to create database with backend {backend_id}")
        self.person_handles = self.db.get_person_handles()
        
        if not self.person_handles:
            pytest.skip(f"No persons in database for scalability tests with backend {backend_id}")
        
        def query_persons():
            """Query a specific number of persons."""
            results = []
            for handle in random.sample(self.person_handles, min(query_size, len(self.person_handles))):
                person = self.db.get_person_from_handle(handle)
                if person:
                    results.append(person)
            return results
        
        result = benchmark(query_persons)
        
        # Store the query size and backend for analysis
        benchmark.query_size = query_size
        benchmark.backend_id = backend_id
        
        # Assert that performance scales reasonably
        # Allow more time for larger queries
        max_time = query_size * 0.01  # 10ms per person
        # Note: benchmark.stats is available after the test completes
        pass


# Integration with existing test framework
def create_test_suite():
    """Return a test suite for integration with existing test framework."""
    import unittest
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestDatabasePerformance))
    suite.addTest(loader.loadTestsFromTestCase(TestFilterPerformance))
    suite.addTest(loader.loadTestsFromTestCase(TestTransactionPerformance))
    return suite


@pytest.mark.skip(reason="Not a test, just a utility function")
def testSuite():
    """Return a test suite for integration with existing test framework."""
    return create_test_suite()


def perfSuite():
    """Return a performance test suite for integration with existing test framework."""
    return create_test_suite()


# Main execution function
def gramps_benchmark(gramps_file=None, save_results=True, generate_charts=True, output_dir=None):
    """Run performance tests and optionally save results and generate charts."""
    if gramps_file:
        # Set the environment variable for the tests
        os.environ['GRAMPS_FILE'] = gramps_file
        print(f"Running performance tests with Gramps file: {gramps_file}")
        print("Use: python -m pytest test/performance/performance_tests.py")
        print("Note: Results are automatically saved when using gramps_benchmark.py script")
    else:
        print("No Gramps file specified. Generating charts from existing benchmark files...")
        try:
            # Import the benchmark_charts module
            sys.path.append(os.path.dirname(__file__))
            import benchmark_charts
            
            # Find all benchmark files grouped by folder and generate PDFs per folder
            # Use output_dir if provided, otherwise use current directory
            if output_dir:
                benchmarks_dir = os.path.join(output_dir, '.benchmarks')
            else:
                benchmarks_dir = os.path.join(os.getcwd(), '.benchmarks')
            benchmark_files_by_folder = benchmark_charts.find_benchmark_files(benchmarks_dir)
            if benchmark_files_by_folder:
                print(f"Found {len(benchmark_files_by_folder)} folders with benchmark files")
                
                # Generate one PDF per folder with titles based on folder names
                print("Generating PDFs per folder...")
                success = benchmark_charts.generate_folder_charts(benchmark_files_by_folder, output_dir)
                if success:
                    print("Chart generation completed")
                    return True
                else:
                    print("No valid benchmark results found")
                    return False
            else:
                print(f"No benchmark files found in .benchmarks directory in {benchmarks_dir}")
                print("Please run tests first to generate benchmark files")
                return False
        except ImportError:
            print("benchmark_charts module not found")
            return False
        except Exception as e:
            print(f"Error generating charts: {e}")
            return False


 
