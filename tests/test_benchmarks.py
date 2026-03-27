import subprocess
import json
import os
import pytest

# Path to our compiled benchmark executable
BENCH_BINARY = os.path.join(os.path.dirname(__file__), "..", "build", "benchmarks", "bench_sort")

# Path where JSON results will be saved
JSON_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "results", "benchmark_results.json")

def run_benchmark():
    """
    Runs the C++ benchmark binary and tells it to save results as JSON.
    Google Benchmark has a built-in flag for this: --benchmark_format=json
    """
    os.makedirs(os.path.dirname(JSON_OUTPUT), exist_ok=True)

    result = subprocess.run(
        [BENCH_BINARY,
         "--benchmark_format=json",
         f"--benchmark_out={JSON_OUTPUT}"],
        capture_output=True,
        text=True
    )

    return result

def load_results():
    """Reads and parses the JSON file the benchmark produced"""
    with open(JSON_OUTPUT, "r") as f:
        return json.load(f)

# ── Tests start here ────────────────────────────────────────────

def test_benchmark_runs_successfully():
    """Test 1: Does the benchmark even run without crashing?"""
    result = run_benchmark()
    assert result.returncode == 0, f"Benchmark crashed! Error: {result.stderr}"

def test_json_output_exists():
    """Test 2: Did it actually produce a JSON file?"""
    run_benchmark()
    assert os.path.exists(JSON_OUTPUT), "JSON output file was not created"

def test_json_has_benchmarks():
    """Test 3: Does the JSON contain benchmark results?"""
    run_benchmark()
    data = load_results()
    assert "benchmarks" in data, "JSON missing 'benchmarks' key"
    assert len(data["benchmarks"]) > 0, "No benchmark entries found"

def test_sort_benchmark_present():
    """Test 4: Is our sort benchmark in the results?"""
    run_benchmark()
    data = load_results()
    names = [b["name"] for b in data["benchmarks"]]
    sort_benchmarks = [n for n in names if "SortAscending" in n]
    assert len(sort_benchmarks) > 0, "SortAscending benchmark not found in results"

def test_sum_benchmark_present():
    """Test 5: Is our sum benchmark in the results?"""
    run_benchmark()
    data = load_results()
    names = [b["name"] for b in data["benchmarks"]]
    sum_benchmarks = [n for n in names if "SumArray" in n]
    assert len(sum_benchmarks) > 0, "SumArray benchmark not found in results"

def test_latency_is_positive():
    """Test 6: Are all measured times positive numbers? (sanity check)"""
    run_benchmark()
    data = load_results()
    for bench in data["benchmarks"]:
        assert bench["real_time"] > 0, f"{bench['name']} has non-positive time"

def test_sort_throughput_reasonable():
    """
    Test 7: Is sort throughput above 1 million items/sec?
    If this fails, something is seriously wrong with the implementation.
    """
    run_benchmark()
    data = load_results()
    for bench in data["benchmarks"]:
        if "SortAscending" in bench["name"]:
            items_per_sec = bench.get("items_per_second", 0)
            assert items_per_sec > 1_000_000, \
                f"Sort throughput too low: {items_per_sec} items/sec"

