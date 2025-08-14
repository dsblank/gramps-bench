"""
Gramps Performance Benchmarking Tools

This package provides performance testing and benchmarking tools for Gramps genealogy software.
"""

__version__ = "1.0.0"
__author__ = "Gramps Development Team"
__email__ = "gramps-devel@lists.sourceforge.net"

from .cli.gramps_bench import main
from .performance_tests import gramps_benchmark
from .benchmark_charts import main as generate_charts

__all__ = ["main", "gramps_benchmark", "generate_charts"] 
