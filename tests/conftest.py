"""
Pytest configuration and hooks for test_filter_rules.py
"""
import os
import json
import time
from datetime import datetime

# Import timing data from test_filter_rules module
def pytest_sessionfinish(session, exitstatus):
    """Save timing data to JSON file after all tests complete."""
    # Import here to avoid circular imports
    try:
        import test_filter_rules
        timing_data = test_filter_rules._timing_data
        
        if timing_data:
            # Create output filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"filter_rules_timing_{timestamp}.json"
            
            # Prepare the output data
            output_data = {
                "test_suite": "Filter Rules Timing",
                "timestamp": datetime.now().isoformat(),
                "total_rules_tested": len(timing_data),
                "rules": {}
            }
            
            # Add timing data for each rule
            for rule_name, timing_info in timing_data.items():
                output_data["rules"][rule_name] = timing_info
            
            # Calculate summary statistics
            if timing_data:
                times = [info["time_seconds"] for info in timing_data.values()]
                output_data["summary"] = {
                    "total_time_seconds": sum(times),
                    "average_time_seconds": sum(times) / len(times) if times else 0,
                    "min_time_seconds": min(times) if times else 0,
                    "max_time_seconds": max(times) if times else 0,
                }
            
            # Save to JSON file
            with open(output_file, "w") as f:
                json.dump(output_data, f, indent=2)
            
            print(f"\nTiming data saved to: {output_file}")
    except (ImportError, AttributeError):
        # If test_filter_rules module isn't available or doesn't have _timing_data, skip
        pass

