import json
import os
import sys

# ── Config ────────────────────────────────────────────────────────
# How much slower is acceptable before we flag it?
# 0.10 = 10% slower than baseline triggers a failure
REGRESSION_THRESHOLD = 0.10

BASELINE_FILE = os.path.join(os.path.dirname(__file__), "..", "results", "baseline.json")
RESULTS_FILE  = os.path.join(os.path.dirname(__file__), "..", "results", "benchmark_results.json")

# ── Helpers ───────────────────────────────────────────────────────

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved: {path}")

def extract_metrics(data):
    """
    Turns the benchmark JSON into a simple dictionary:
    {
      "BM_SortAscending/1000": {"real_time": 60941, "items_per_second": 16409700},
      ...
    }
    """
    metrics = {}
    for bench in data["benchmarks"]:
        name = bench["name"]
        metrics[name] = {
            "real_time":        bench.get("real_time", 0),
            "cpu_time":         bench.get("cpu_time", 0),
            "items_per_second": bench.get("items_per_second", 0),
        }
    return metrics

# ── Core Logic ────────────────────────────────────────────────────

def save_as_baseline():
    """Save current results as the new baseline."""
    print("\n📌 No baseline found. Saving current results as baseline...")
    data = load_json(RESULTS_FILE)
    save_json(data, BASELINE_FILE)
    print("  Baseline saved. Future runs will compare against this.")

def compare_against_baseline():
    """
    Compare current results against baseline.
    Returns True if everything is fine, False if regressions found.
    """
    print("\n🔍 Comparing results against baseline...\n")

    baseline_data = load_json(BASELINE_FILE)
    current_data  = load_json(RESULTS_FILE)

    baseline = extract_metrics(baseline_data)
    current  = extract_metrics(current_data)

    regressions = []
    improvements = []

    for name, curr in current.items():
        if name not in baseline:
            print(f"  ⚪ NEW:      {name} (no baseline to compare)")
            continue

        base = baseline[name]

        # Compare real_time — higher time = slower = bad
        base_time = base["real_time"]
        curr_time = curr["real_time"]

        if base_time == 0:
            continue

        # Calculate % change
        # Positive = got slower (regression)
        # Negative = got faster (improvement)
        change = (curr_time - base_time) / base_time

        if change > REGRESSION_THRESHOLD:
            regressions.append({
                "name":      name,
                "baseline":  base_time,
                "current":   curr_time,
                "change_pct": change * 100
            })
            print(f"  ❌ REGRESS: {name}")
            print(f"             baseline={base_time:.0f}ns  current={curr_time:.0f}ns  change=+{change*100:.1f}%")

        elif change < -REGRESSION_THRESHOLD:
            improvements.append(name)
            print(f"  ✅ FASTER:  {name}  ({change*100:.1f}%)")

        else:
            print(f"  ✅ OK:      {name}  ({change*100:+.1f}%)")

    # ── Summary ───────────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print(f"  Total benchmarks checked : {len(current)}")
    print(f"  Regressions found        : {len(regressions)}")
    print(f"  Improvements found       : {len(improvements)}")
    print(f"  Threshold used           : {REGRESSION_THRESHOLD*100:.0f}%")
    print(f"{'─'*60}\n")

    if regressions:
        print("❌ REGRESSION DETECTED — pipeline should fail\n")
        for r in regressions:
            print(f"   {r['name']}: +{r['change_pct']:.1f}% slower")
        return False

    print("✅ No regressions detected — pipeline passed\n")
    return True

# ── Main ──────────────────────────────────────────────────────────

def main():
    # Check results file exists
    if not os.path.exists(RESULTS_FILE):
        print("❌ No benchmark results found. Run benchmarks first.")
        sys.exit(1)

    # First run ever — no baseline exists yet
    if not os.path.exists(BASELINE_FILE):
        save_as_baseline()
        print("✅ First run complete. Re-run to start comparing.\n")
        sys.exit(0)

    # Compare and exit with correct code
    # Exit code 0 = success (CI passes)
    # Exit code 1 = failure (CI fails)
    passed = compare_against_baseline()
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()

