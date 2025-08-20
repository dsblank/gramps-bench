#!/usr/bin/env python3
"""
Benchmark Charts Generator for Gramps

This script reads pytest-benchmark JSON files and generates simple charts
showing individual benchmark results with each result in its own color.
No baseline comparisons, min/max/avg charts, or other complex visualizations.
"""

import argparse
import json
import os
from datetime import datetime

# Import matplotlib for chart generation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Import Gramps version
from gramps.version import VERSION
from matplotlib.backends.backend_pdf import PdfPages

# Set matplotlib backend
matplotlib.use("Agg")  # Use non-interactive backend

# Check for version override from environment variable
GRAMPS_VERSION = os.environ.get("GRAMPS_VERSION", VERSION)


def load_benchmark_file(filepath):
    """Load a pytest-benchmark JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def find_benchmark_files(directory=".benchmarks"):
    """Find all benchmark JSON files in the .benchmarks directory, grouped by folder."""
    benchmark_files_by_folder = {}

    if not os.path.exists(directory):
        print(f"Benchmark directory {directory} not found")
        return benchmark_files_by_folder

    # Look for JSON files in subdirectories
    for root, dirs, files in os.walk(directory):
        json_files = []
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                json_files.append(filepath)

        if json_files:
            # Get the relative folder name from the benchmark directory
            folder_name = os.path.relpath(root, directory)
            if folder_name == ".":
                folder_name = "root"
            benchmark_files_by_folder[folder_name] = sorted(json_files)

    return benchmark_files_by_folder


def find_benchmark_files_flat(directory=".benchmarks"):
    """Find all benchmark JSON files in the .benchmarks directory (flat list for backward compatibility)."""
    benchmark_files = []

    if not os.path.exists(directory):
        print(f"Benchmark directory {directory} not found")
        return benchmark_files

    # Look for JSON files in subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                benchmark_files.append(filepath)

    return sorted(benchmark_files)


def extract_benchmark_data(benchmark_data):
    """Extract test results from pytest-benchmark JSON data."""
    results = {}

    # Extract machine info
    machine_info = benchmark_data.get("machine_info", {})

    # Extract benchmark results
    benchmarks = benchmark_data.get("benchmarks", [])

    for benchmark in benchmarks:
        test_name = benchmark.get("name", "Unknown")
        stats = benchmark.get("stats", {})

        # Data is already in seconds, no conversion needed
        mean_time = stats.get("mean", 0)

        results[test_name] = {
            "mean": mean_time,
            "rounds": stats.get("rounds", 0),
            "min": stats.get("min", 0),
            "max": stats.get("max", 0),
            "stddev": stats.get("stddev", 0),
        }

    return results, machine_info


def generate_html_chart(test_name, run_data, output_file):
    """Generate an HTML chart for a specific test."""
    # Sort run data alphabetically by run name
    run_data.sort(key=lambda x: x[0])

    # Extract sorted data
    run_names = [data[0] for data in run_data]
    run_times = [data[1] for data in run_data]

    if not run_names:
        return ""

    # Create the chart using matplotlib and save as PNG
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))

    # Create color palette for runs
    colors = plt.cm.Set3(np.linspace(0, 1, len(run_names)))

    # Create the bar chart
    ax.bar(run_names, run_times, color=colors, alpha=0.8)

    ax.set_xlabel("Benchmark Runs")
    ax.set_ylabel("Execution Time (seconds)")
    ax.set_title(f"Benchmark: {test_name}", fontsize=12, fontweight="bold")
    ax.set_xticks(range(len(run_names)))
    ax.set_xticklabels(run_names, rotation=45, ha="right")
    ax.grid(True, alpha=0.3)

    # Value labels removed as requested

    # Adjust layout to prevent warnings
    plt.tight_layout(pad=1.5, h_pad=1.0, w_pad=1.0)

    # Save the chart as PNG
    chart_filename = f"{test_name.replace(' ', '_').replace('/', '_')}.png"
    chart_path = os.path.join(os.path.dirname(output_file), chart_filename)
    plt.savefig(chart_path, dpi=150)
    plt.close()

    return chart_filename


def generate_html_page(folder_name, all_results, benchmark_files, output_file):
    """Generate an HTML webpage for benchmark results."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gramps Performance Benchmarks - {folder_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .summary h2 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        .file-list {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .file-list h3 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        .file-list ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        .file-list li {{
            padding: 5px 0;
            border-bottom: 1px solid #dee2e6;
        }}
        .file-list li:last-child {{
            border-bottom: none;
        }}
        .chart-section {{
            margin-bottom: 40px;
        }}
        .chart-section h2 {{
            color: #2c3e50;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        .chart-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        .data-table th, .data-table td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        .data-table th {{
            background-color: #3498db;
            color: white;
        }}
        .data-table tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Gramps Performance Benchmarks (v{GRAMPS_VERSION})</h1>
        <h2 style="text-align: center; color: #2c3e50;">{folder_name}</h2>

        <div class="summary">
            <h2>Summary</h2>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Number of benchmark runs:</strong> {len(all_results)}</p>
            <p><strong>Total benchmark files:</strong> {len(benchmark_files)}</p>
        </div>

        <div class="file-list">
            <h3>Benchmark Files</h3>
            <ul>
"""

    for file in benchmark_files:
        html_content += f"                <li>{os.path.basename(file)}</li>\n"

    html_content += """            </ul>
        </div>
"""

    # Get all unique test names across all files in this folder
    all_test_names = set()
    for results in all_results.values():
        all_test_names.update(results.keys())

    test_names = sorted(list(all_test_names))

    # Generate charts and HTML for each test
    for test_name in test_names:
        # Collect data for this test from all runs
        run_data = []

        for run_name, results in all_results.items():
            if test_name in results:
                run_data.append((run_name, results[test_name]["mean"]))

        if not run_data:
            continue

        # Generate the chart image
        chart_filename = generate_html_chart(test_name, run_data, output_file)

        if chart_filename:
            html_content += f"""
        <div class="chart-section">
            <h2>Benchmark: {test_name}</h2>
            <div class="chart-container">
                <img src="{chart_filename}" alt="Chart for {test_name}">
            </div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Run</th>
                        <th>Mean Time (seconds)</th>
                        <th>Min Time (seconds)</th>
                        <th>Max Time (seconds)</th>
                        <th>Standard Deviation</th>
                        <th>Rounds</th>
                    </tr>
                </thead>
                <tbody>
"""

            # Sort run data for consistent display
            run_data.sort(key=lambda x: x[0])

            for run_name, mean_time in run_data:
                result = all_results[run_name][test_name]
                html_content += f"""
                    <tr>
                        <td>{run_name}</td>
                        <td>{result['mean']:.6f}</td>
                        <td>{result['min']:.6f}</td>
                        <td>{result['max']:.6f}</td>
                        <td>{result['stddev']:.6f}</td>
                        <td>{result['rounds']}</td>
                    </tr>
"""

            html_content += """
                </tbody>
            </table>
        </div>
"""

    html_content += f"""
        <div class="footer">
            <p>Generated by Gramps Benchmark Tool on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""

    # Write the HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)


def generate_performance_charts(benchmark_results, output_file=None):
    """Generate simple performance charts from benchmark results showing only individual results."""

    if output_file is None:
        output_file = "performance_charts.pdf"

    with PdfPages(output_file) as pdf:
        # Extract test names and times
        test_names = []
        mean_times = []

        for test_name, result in benchmark_results.items():
            if hasattr(result, "stats"):
                test_names.append(test_name)
                mean_times.append(result.stats.mean)

        if not test_names:
            print("No benchmark results found for chart generation")
            return False

        # Create a color palette - each test gets its own distinct color
        colors = plt.cm.Set3(np.linspace(0, 1, len(test_names)))

        # Generate individual charts for each test
        for i, (test_name, result) in enumerate(benchmark_results.items()):
            if hasattr(result, "stats"):
                fig, ax = plt.subplots(1, 1, figsize=(12, 7))

                # Use the same color as in the main chart
                color = colors[i]

                # Create a simple bar chart for this individual test
                ax.bar([test_name], [result.stats.mean], color=color, alpha=0.8)

                ax.set_xlabel("Test")
                ax.set_ylabel("Execution Time (seconds)")
                ax.set_title(f"Benchmark: {test_name}", fontsize=12, fontweight="bold")
                ax.grid(True, alpha=0.3)

                # Value labels removed as requested

                # Add test info
                info_text = f"Rounds: {result.stats.rounds}\n"
                info_text += f"Iterations: {result.stats.iterations}"

                ax.text(
                    0.02,
                    0.98,
                    info_text,
                    transform=ax.transAxes,
                    ha="left",
                    va="top",
                    fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                )

                # Metadata removed as requested

                # Adjust layout to prevent warnings
                plt.tight_layout(pad=1.5, h_pad=1.0, w_pad=1.0)
                pdf.savefig(fig)
                plt.close()

    print(f"Performance charts saved to: {output_file}")
    return True


def save_benchmark_results(benchmark_results, output_file=None):
    """Save benchmark results to JSON file."""
    if output_file is None:
        output_file = f"performance_results_{GRAMPS_VERSION}.json"

    results_data = {
        "test_suite": "Gramps Performance Tests",
        "gramps_version": GRAMPS_VERSION,
        "timestamp": datetime.now().isoformat(),
        "success": True,
        "tests_run": len(benchmark_results),
        "benchmark_results": {},
    }

    for test_name, result in benchmark_results.items():
        if hasattr(result, "stats"):
            results_data["benchmark_results"][test_name] = {
                "mean": result.stats.mean,
                "median": result.stats.median,
                "stddev": result.stats.stddev,
                "min": result.stats.min,
                "max": result.stats.max,
                "rounds": result.stats.rounds,
                "iterations": result.stats.iterations,
                "database_stats": getattr(result, "database_stats", None),
            }

    with open(output_file, "w") as f:
        json.dump(results_data, f, indent=2)

    print(f"Benchmark results saved to: {output_file}")
    return output_file


def generate_single_run_charts(benchmark_file, output_file=None):
    """Generate simple charts for a single benchmark run showing only individual results."""
    print(f"Loading benchmark data from: {benchmark_file}")

    try:
        benchmark_data = load_benchmark_file(benchmark_file)
    except Exception as e:
        print(f"Error loading benchmark file: {e}")
        return False

    results, machine_info = extract_benchmark_data(benchmark_data)

    if not results:
        print("No benchmark results found")
        return False

    if output_file is None:
        basename = os.path.splitext(os.path.basename(benchmark_file))[0]
        output_file = f"{basename}.pdf"

    print(f"Generating charts for {len(results)} tests...")

    with PdfPages(output_file) as pdf:
        # Extract data for individual charts
        test_names = list(results.keys())
        [results[name]["mean"] for name in test_names]

        # Create a color palette - each test gets its own distinct color
        colors = plt.cm.Set3(np.linspace(0, 1, len(test_names)))

        # Generate individual charts for each test
        for i, (test_name, test_data) in enumerate(results.items()):
            fig, ax = plt.subplots(1, 1, figsize=(12, 7))

            # Use the same color as in the main chart
            color = colors[i]

            # Create a simple bar chart for this individual test
            ax.bar([test_name], [test_data["mean"]], color=color, alpha=0.8)

            ax.set_xlabel("Test")
            ax.set_ylabel("Execution Time (seconds)")
            ax.set_title(f"Benchmark: {test_name}", fontsize=12, fontweight="bold")
            ax.grid(True, alpha=0.3)

            # Value labels removed as requested

            # Add test info
            info_text = f"Rounds: {test_data['rounds']}\n"
            info_text += f"Iterations: {test_data['iterations']}"

            ax.text(
                0.02,
                0.98,
                info_text,
                transform=ax.transAxes,
                ha="left",
                va="top",
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
            )

            # Machine info removed as requested - this information is available on the first page

            # Metadata removed as requested

            # Adjust layout to prevent warnings
            plt.tight_layout(pad=1.5, h_pad=1.0, w_pad=1.0)
            pdf.savefig(fig)
            plt.close()

    print(f"Charts saved to: {output_file}")
    return True


def generate_multi_run_charts(benchmark_files, output_file=None):
    """Generate charts comparing multiple benchmark runs for each test."""
    if not benchmark_files:
        print("No benchmark files provided")
        return False

    print(f"Loading {len(benchmark_files)} benchmark files...")

    # Load all benchmark data
    all_results = {}
    all_machine_info = {}

    for file in benchmark_files:
        try:
            benchmark_data = load_benchmark_file(file)
            results, machine_info = extract_benchmark_data(benchmark_data)
            # Clean up the filename: remove leading numbers and .json extension
            file_name = os.path.basename(file)
            # Remove all .json extensions (handle cases like .json.json)
            while file_name.endswith(".json"):
                file_name = file_name[:-5]  # Remove '.json'
            # Remove leading numbers (like "0001_", "0002_", etc.)
            if "_" in file_name:
                parts = file_name.split("_", 1)
                if len(parts) == 2 and parts[0].isdigit():
                    file_name = parts[1]
            all_results[file_name] = results
            all_machine_info[file_name] = machine_info
        except Exception as e:
            print(f"Error loading benchmark file {file}: {e}")
            continue

    if not all_results:
        print("No valid benchmark results found")
        return False

    if output_file is None:
        output_file = "benchmark_multi_run.pdf"

    print("Generating multi-run comparison charts...")

    with PdfPages(output_file) as pdf:
        # Get all unique test names across all files
        all_test_names = set()
        for results in all_results.values():
            all_test_names.update(results.keys())

        test_names = sorted(list(all_test_names))

        # Generate a chart for each test showing all runs
        for test_name in test_names:
            fig, ax = plt.subplots(1, 1, figsize=(12, 7))

            # Collect data for this test from all runs
            run_data = []

            # Create color palette for runs
            colors = plt.cm.Set3(np.linspace(0, 1, len(all_results)))

            for i, (run_name, results) in enumerate(all_results.items()):
                if test_name in results:
                    run_data.append((run_name, results[test_name]["mean"], colors[i]))

            # Sort run data alphabetically by run name
            run_data.sort(key=lambda x: x[0])

            # Extract sorted data
            run_names = [data[0] for data in run_data]
            run_times = [data[1] for data in run_data]
            run_colors = [data[2] for data in run_data]

            if not run_names:
                continue

                # Create the bar chart
                ax.bar(run_names, run_times, color=run_colors, alpha=0.8)

                ax.set_xlabel("Benchmark Runs")
                ax.set_ylabel("Execution Time (seconds)")
                ax.set_title(f"Benchmark: {test_name}", fontsize=12, fontweight="bold")
                ax.set_xticks(range(len(run_names)))
                ax.set_xticklabels(run_names, rotation=45, ha="right")
                ax.grid(True, alpha=0.3)

            # Value labels removed as requested

            # Metadata removed as requested

            # Adjust layout to prevent warnings
            plt.tight_layout(pad=1.5, h_pad=1.0, w_pad=1.0)
            pdf.savefig(fig)
            plt.close()

    print(f"Multi-run comparison charts saved to: {output_file}")
    return True


def generate_folder_charts(benchmark_files_by_folder, output_dir=None, format="pdf"):
    """Generate one chart file per folder with title based on folder name."""
    if not benchmark_files_by_folder:
        print("No benchmark files found")
        return False

    if output_dir is None:
        output_dir = "."

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    success_count = 0

    for folder_name, benchmark_files in benchmark_files_by_folder.items():
        print(f"\nProcessing folder: {folder_name}")
        print(f"Found {len(benchmark_files)} benchmark files")

        # Create a clean folder name for the output filename
        clean_folder_name = folder_name.replace("/", "_").replace("\\", "_")

        # Load all benchmark data for this folder
        all_results = {}
        all_machine_info = {}

        for file in benchmark_files:
            try:
                benchmark_data = load_benchmark_file(file)
                results, machine_info = extract_benchmark_data(benchmark_data)
                # Clean up the filename: remove leading numbers and .json extension
                file_name = os.path.basename(file)
                # Remove all .json extensions (handle cases like .json.json)
                while file_name.endswith(".json"):
                    file_name = file_name[:-5]  # Remove '.json'
                # Remove leading numbers (like "0001_", "0002_", etc.)
                if "_" in file_name:
                    parts = file_name.split("_", 1)
                    if len(parts) == 2 and parts[0].isdigit():
                        file_name = parts[1]
                all_results[file_name] = results
                all_machine_info[file_name] = machine_info
            except Exception as e:
                print(f"Error loading benchmark file {file}: {e}")
                continue

        if not all_results:
            print(f"No valid benchmark results found for folder {folder_name}")
            continue

        if format.lower() == "html":
            # Generate HTML webpage
            output_file = os.path.join(output_dir, f"{clean_folder_name}.html")
            print(f"Generating HTML for folder: {folder_name}")
            generate_html_page(folder_name, all_results, benchmark_files, output_file)
            print(f"HTML saved to: {output_file}")
        else:
            # Generate PDF (original functionality)
            output_file = os.path.join(output_dir, f"{clean_folder_name}.pdf")
            print(f"Generating PDF for folder: {folder_name}")

            with PdfPages(output_file) as pdf:
                # Add a title page
                fig, ax = plt.subplots(1, 1, figsize=(10, 8))
                ax.axis("off")

                # Create title
                title_text = (
                    f"Gramps Performance Benchmarks (v{GRAMPS_VERSION})\n{folder_name}"
                )
                ax.text(
                    0.5,
                    0.7,
                    title_text,
                    transform=ax.transAxes,
                    ha="center",
                    va="center",
                    fontsize=20,
                    fontweight="bold",
                )

                # Add summary information
                summary_text = (
                    f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                summary_text += f"Number of benchmark runs: {len(all_results)}\n"
                summary_text += f"Total benchmark files: {len(benchmark_files)}"

                ax.text(
                    0.5,
                    0.5,
                    summary_text,
                    transform=ax.transAxes,
                    ha="center",
                    va="center",
                    fontsize=12,
                )

                # Add file list
                file_list = "Benchmark files:\n"
                for file in benchmark_files:
                    file_list += f"• {os.path.basename(file)}\n"

                ax.text(
                    0.5,
                    0.3,
                    file_list,
                    transform=ax.transAxes,
                    ha="center",
                    va="center",
                    fontsize=10,
                    family="monospace",
                )

                pdf.savefig(fig)
                plt.close()

                # Get all unique test names across all files in this folder
                all_test_names = set()
                for results in all_results.values():
                    all_test_names.update(results.keys())

                test_names = sorted(list(all_test_names))

                # Generate a chart for each test showing all runs in this folder
                for test_name in test_names:
                    fig, ax = plt.subplots(1, 1, figsize=(12, 7))

                    # Collect data for this test from all runs
                    run_data = []

                    # Create color palette for runs
                    colors = plt.cm.Set3(np.linspace(0, 1, len(all_results)))

                    for i, (run_name, results) in enumerate(all_results.items()):
                        if test_name in results:
                            run_data.append(
                                (run_name, results[test_name]["mean"], colors[i])
                            )

                    # Sort run data alphabetically by run name
                    run_data.sort(key=lambda x: x[0])

                    # Extract sorted data
                    run_names = [data[0] for data in run_data]
                    run_times = [data[1] for data in run_data]
                    run_colors = [data[2] for data in run_data]

                    if not run_names:
                        continue

                    # Create the bar chart
                    ax.bar(run_names, run_times, color=run_colors, alpha=0.8)

                    ax.set_xlabel("Benchmark Runs")
                    ax.set_ylabel("Execution Time (seconds)")
                    ax.set_title(
                        f"Benchmark: {test_name}", fontsize=12, fontweight="bold"
                    )
                    ax.set_xticks(range(len(run_names)))
                    ax.set_xticklabels(run_names, rotation=45, ha="right")
                    ax.grid(True, alpha=0.3)

                    # Value labels removed as requested

                    # Metadata removed as requested

                    # Adjust layout to prevent warnings
                    plt.tight_layout(pad=1.5, h_pad=1.0, w_pad=1.0)
                    pdf.savefig(fig)
                    plt.close()

            print(f"PDF saved to: {output_file}")

        success_count += 1

    format_name = "HTML files" if format.lower() == "html" else "PDF files"
    print(f"\nGenerated {success_count} {format_name}")
    return success_count > 0


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Generate simple charts from pytest-benchmark JSON files"
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Single benchmark JSON file to generate charts for",
    )
    parser.add_argument(
        "--baseline", "-b", type=str, help="First benchmark file for comparison"
    )
    parser.add_argument(
        "--current", "-c", type=str, help="Second benchmark file for comparison"
    )
    parser.add_argument("--output", "-o", type=str, help="Output PDF file")
    parser.add_argument("--output-dir", type=str, help="Output directory for PDF files")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automatically find and process all benchmark files",
    )
    parser.add_argument(
        "--list", action="store_true", help="List all available benchmark files"
    )
    parser.add_argument(
        "--per-folder",
        action="store_true",
        default=True,
        help="Generate one chart file per folder (default)",
    )
    parser.add_argument(
        "--multi-run",
        action="store_true",
        help="Generate multi-run comparison charts (legacy mode)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["pdf", "html"],
        default="pdf",
        help="Output format for per-folder generation (pdf or html)",
    )

    args = parser.parse_args()

    if args.list:
        benchmark_files_by_folder = find_benchmark_files()
        if benchmark_files_by_folder:
            print("Available benchmark files by folder:")
            for folder, files in benchmark_files_by_folder.items():
                print(f"  Folder: {folder}")
                for file in files:
                    print(f"    {file}")
        else:
            print("No benchmark files found in .benchmarks directory")
        return

    if args.auto:
        if args.multi_run:
            # Legacy mode: generate multi-run comparison charts
            benchmark_files = find_benchmark_files_flat()
            if not benchmark_files:
                print("No benchmark files found in .benchmarks directory")
                return

            print(f"Found {len(benchmark_files)} benchmark files")

            # Only generate multi-run comparison charts if there are multiple files
            if len(benchmark_files) >= 2:
                print("Generating multi-run comparison charts...")
                generate_multi_run_charts(benchmark_files, args.output)
            else:
                print("Need at least 2 benchmark files to generate comparison charts")
        else:
            # New default mode: generate one PDF per folder
            benchmark_files_by_folder = find_benchmark_files()
            if not benchmark_files_by_folder:
                print("No benchmark files found in .benchmarks directory")
                return

            print(
                f"Found {len(benchmark_files_by_folder)} folders with benchmark files"
            )
            generate_folder_charts(
                benchmark_files_by_folder, args.output_dir, args.format
            )

    elif args.baseline and args.current:
        # Generate multi-run charts for the two specified files
        generate_multi_run_charts([args.baseline, args.current], args.output)

    elif args.file:
        # Generate single run charts
        generate_single_run_charts(args.file, args.output)

    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 benchmark_charts.py --list")
        print(
            "  python3 benchmark_charts.py --file .benchmarks/Linux-CPython-3.12-64bit/0001_baseline.json"
        )
        print("  python3 benchmark_charts.py --baseline run1.json --current run2.json")
        print("  python3 benchmark_charts.py --auto")
        print("  python3 benchmark_charts.py --auto --multi-run  # Legacy mode")


if __name__ == "__main__":
    main()
