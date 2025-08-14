#!/usr/bin/env python3
"""
Simple wrapper script for running Gramps performance tests.

Usage:
    # Run benchmarks and save results:
    python gramps_benchmark.py <gramps_file> [--output <directory>]
    # Generate charts:
    python gramps_benchmark.py [--output <directory>]
"""

import argparse
import os
import subprocess
import sys

from ..performance_tests import gramps_benchmark


def get_gramps_version(version_override=None):
    """Get the current Gramps version or use the provided override."""
    if version_override:
        return version_override
    try:
        # Import gramps version
        from gramps.version import VERSION

        return VERSION
    except ImportError:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Run Gramps performance tests")
    parser.add_argument("gramps_file", nargs="?", help="Gramps database file to test")
    parser.add_argument(
        "--output",
        "-o",
        help="Output directory for benchmark results (default: current directory)",
    )
    parser.add_argument("--version", help="Override Gramps version (e.g., '6.0.4-b1')")
    args = parser.parse_args()

    output_dir = args.output

    if args.gramps_file:
        # Run benchmarks with provided gramps file
        gramps_file = args.gramps_file

        # Resolve the path to make it absolute
        gramps_file = os.path.abspath(gramps_file)

        if not os.path.exists(gramps_file):
            print(f"❌ Error: Gramps file not found: {gramps_file}")
            sys.exit(1)

        # Get gramps version for default save name
        gramps_version = get_gramps_version(args.version)
        save_name = f"{gramps_version}"

        print(f"🚀 Running performance tests with: {gramps_file}")
        print(f"📊 Results will be saved as: {save_name}")
        if args.version:
            print(f"🔧 Using overridden version: {args.version}")
        print("=" * 60)

        # Set environment variable and run pytest
        env = os.environ.copy()
        env["GRAMPS_FILE"] = gramps_file
        if args.version:
            env["GRAMPS_VERSION"] = args.version

        # Debug: Print the environment variable being set
        print(f"🔧 Setting GRAMPS_FILE environment variable to: {gramps_file}")
        if args.version:
            print(f"🔧 Setting GRAMPS_VERSION environment variable to: {args.version}")
        working_dir = output_dir if output_dir else os.getcwd()

        # Create output directory if it doesn't exist
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"🔧 Created output directory: {output_dir}")

        print(f"🔧 Working directory: {working_dir}")

        try:
            test_file_path = os.path.join(
                os.path.dirname(__file__), "..", "performance_tests.py"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    test_file_path,
                    f"--benchmark-save={save_name}",
                ],
                env=env,
                cwd=working_dir,
            )

            if result.returncode == 0:
                print("\n✅ Performance tests completed successfully!")
                benchmark_dir = os.path.join(working_dir, ".benchmarks")
                print(f"📁 Results saved in: {benchmark_dir}")
            else:
                print(
                    f"\n❌ Performance tests failed with exit code: {result.returncode}"
                )
                sys.exit(result.returncode)

        except KeyboardInterrupt:
            print("\n⏹️  Tests interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error running tests: {e}")
            sys.exit(1)

    else:
        # Generate charts from existing benchmark files
        print("📊 Generating performance charts from existing benchmark files...")
        if output_dir:
            print(f"📁 Looking for benchmark files in: {output_dir}")
        else:
            print(f"📁 Looking for benchmark files in: {os.getcwd()}")
        print("=" * 60)

        try:
            # Import and run the chart generation
            success = gramps_benchmark(output_dir=output_dir)
            if success:
                print("\n✅ Chart generation completed successfully!")
            else:
                print("\n❌ Chart generation failed")
                sys.exit(1)

        except ImportError as e:
            print(f"❌ Error importing performance_tests: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error generating charts: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
