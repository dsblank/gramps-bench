#!/usr/bin/env python3
"""
Generate a Markdown report from filter rules timing JSON file.

Usage:
    python generate_timing_report.py <input_json_file> [output_md_file]
"""

import json
import sys
import os
from pathlib import Path


def generate_markdown_report(json_file, output_file=None):
    """
    Read timing JSON file and generate a Markdown table report.
    
    Args:
        json_file: Path to the input JSON file
        output_file: Path to output Markdown file (optional, defaults to input name with .md extension)
    """
    # Read JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract rules data
    rules = data.get('rules', {})
    
    if not rules:
        print("No timing data found in JSON file.")
        return
    
    # Create list of (test_name, time) tuples
    test_times = []
    for rule_name, rule_data in rules.items():
        time_seconds = rule_data.get('time_seconds', 0)
        test_times.append((rule_name, time_seconds))
    
    # Sort by time (longest first)
    test_times.sort(key=lambda x: x[1], reverse=True)
    
    # Generate Markdown table
    markdown_lines = []
    markdown_lines.append("| Test Name | Average Time (seconds) |")
    markdown_lines.append("|-----------|------------------------|")
    
    for test_name, time_seconds in test_times:
        markdown_lines.append(f"| {test_name} | {time_seconds:.6f} |")
    
    markdown_content = "\n".join(markdown_lines)
    
    # Determine output file
    if output_file is None:
        json_path = Path(json_file)
        output_file = json_path.with_suffix('.md')
    
    # Write Markdown file
    with open(output_file, 'w') as f:
        f.write(markdown_content)
    
    print(f"Markdown report generated: {output_file}")
    print(f"Total tests: {len(test_times)}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate_timing_report.py <input_json_file> [output_md_file]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if not os.path.exists(json_file):
        print(f"Error: File not found: {json_file}")
        sys.exit(1)
    
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        generate_markdown_report(json_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

