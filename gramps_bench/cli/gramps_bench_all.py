#!/usr/bin/env python3
"""
Gramps Benchmark All Script

This script runs performance benchmarks across multiple Gramps versions and generates
comparative charts. It can be called from the command line with various options.

Usage:
    python gramps_bench_all.py <gramps_file> <gramps_source_dir> [options]
    python gramps_bench_all.py --help
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Import the gramps_bench functions
from gramps_bench import main as run_benchmark, gramps_benchmark


def run_git_checkout(gramps_source_dir, version):
    """Run git checkout for a specific version."""
    try:
        result = subprocess.run(
            ["git", "checkout", "-f", version],
            cwd=gramps_source_dir,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Checked out version {version}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to checkout version {version}: {e}")
        print(f"Git output: {e.stderr}")
        return False


def run_benchmarks_for_version(gramps_file, output_dir, version=None):
    """Run benchmarks for a specific version."""
    print(f"\n🚀 Running benchmarks for version: {version or 'current'}")
    print("=" * 60)
    
    # Set up arguments for the benchmark function
    sys.argv = [
        'gramps_bench',
        gramps_file,
        '--output', output_dir
    ]
    
    if version:
        sys.argv.extend(['--version', version])
    
    try:
        # Run the benchmark
        run_benchmark()
        return True
    except Exception as e:
        print(f"❌ Benchmark failed for version {version}: {e}")
        return False


def generate_final_charts(output_dir):
    """Generate final comparative charts."""
    print(f"\n📊 Generating final comparative charts...")
    print("=" * 60)
    
    try:
        success = gramps_benchmark(output_dir=output_dir)
        if success:
            print("✅ Chart generation completed successfully!")
            return True
        else:
            print("❌ Chart generation failed")
            return False
    except Exception as e:
        print(f"❌ Error generating charts: {e}")
        return False


def open_pdfs(output_dir):
    """Open generated PDF files with the default PDF viewer."""
    try:
        pdf_files = list(Path(output_dir).glob("*.pdf"))
        if pdf_files:
            print(f"\n📄 Opening {len(pdf_files)} PDF file(s)...")
            for pdf_file in pdf_files:
                subprocess.Popen(["evince", str(pdf_file)])
            return True
        else:
            print("No PDF files found to open")
            return False
    except Exception as e:
        print(f"❌ Error opening PDF files: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Run Gramps performance benchmarks across multiple versions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python gramps_bench_all.py /path/to/gramps_file.gramps /path/to/gramps/source
  python gramps_bench_all.py data.gramps /home/user/gramps --versions v5.1.6 v5.2.4
  python gramps_bench_all.py data.gramps /home/user/gramps --output /tmp/results --open
        """
    )
    
    parser.add_argument(
        "gramps_file",
        help="Path to the Gramps database file to test"
    )
    
    parser.add_argument(
        "gramps_source_dir",
        help="Path to the Gramps source directory (for git checkout)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default=os.getcwd(),
        help="Output directory for benchmark results (default: current directory)"
    )
    
    parser.add_argument(
        "--versions",
        nargs="+",
        default=["v5.1.6", "v5.2.4", "v6.0.4"],
        help="List of Git versions to test (default: v5.1.6 v5.2.4 v6.0.4)"
    )
    
    parser.add_argument(
        "--open",
        action="store_true",
        help="Automatically open PDF files after generation"
    )
    
    parser.add_argument(
        "--skip-charts",
        action="store_true",
        help="Skip generating final comparative charts"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.gramps_file):
        print(f"❌ Error: Gramps file not found: {args.gramps_file}")
        sys.exit(1)
    
    if not os.path.exists(args.gramps_source_dir):
        print(f"❌ Error: Gramps source directory not found: {args.gramps_source_dir}")
        sys.exit(1)
    
    # Check if it's a git repository
    git_dir = os.path.join(args.gramps_source_dir, ".git")
    if not os.path.exists(git_dir):
        print(f"❌ Error: {args.gramps_source_dir} is not a git repository")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Clean up previous benchmark results
    benchmark_dir = os.path.join(args.output, ".benchmarks")
    if os.path.exists(benchmark_dir):
        print(f"🧹 Cleaning up previous benchmark results...")
        import shutil
        shutil.rmtree(benchmark_dir)
    
    print(f"🎯 Starting Gramps performance benchmarks")
    print(f"📁 Gramps file: {args.gramps_file}")
    print(f"📁 Source directory: {args.gramps_source_dir}")
    print(f"📁 Output directory: {args.output}")
    print(f"🔢 Versions to test: {', '.join(args.versions)}")
    print("=" * 60)
    
    # Store original working directory
    original_cwd = os.getcwd()
    
    try:
        # Change to gramps source directory
        os.chdir(args.gramps_source_dir)
        
        # Run benchmarks for each version
        for version in args.versions:
            print(f"\n🔄 Processing version: {version}")
            
            # Checkout the version
            if not run_git_checkout(args.gramps_source_dir, version):
                print(f"⚠️  Skipping version {version} due to checkout failure")
                continue
            
            # Run benchmarks for this version
            if not run_benchmarks_for_version(args.gramps_file, args.output, version):
                print(f"⚠️  Skipping version {version} due to benchmark failure")
                continue
        
        # Run final benchmark without version override (current version)
        print(f"\n🔄 Processing current version")
        if not run_benchmarks_for_version(args.gramps_file, args.output):
            print("⚠️  Final benchmark failed")
        
        # Generate comparative charts
        if not args.skip_charts:
            if not generate_final_charts(args.output):
                print("⚠️  Chart generation failed")
        
        # Open PDF files
        if args.open:
            open_pdfs(args.output)
        
        print(f"\n✅ All benchmarks completed successfully!")
        print(f"📁 Results saved in: {args.output}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Benchmarks interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during benchmarks: {e}")
        sys.exit(1)
    finally:
        # Restore original working directory
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()
