"""
StreamVault Licensing Analysis — Master Pipeline Runner
======================================================
Executes the full analytics pipeline from clean state to final outputs.
Designed for Adjoa to rerun quarterly on her laptop during live meetings.
"""

import sys
import time
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

PIPELINE_STEPS = [
    ("Acquire TMDb Data & Reconcile", PROJECT_ROOT / "src" / "fetch_tmdb.py"),
    ("Transform Raw JSON into Normalized Tables", PROJECT_ROOT / "src" / "transform_tmdb.py"),
    ("Execute Automated Quality Checks", PROJECT_ROOT / "src" / "quality_checks.py"),
    ("Compute Franchise vs Standalone KPIs", PROJECT_ROOT / "src" / "analyse_kpis.py"),
    ("Analyze Franchise Collections", PROJECT_ROOT / "src" / "analyse_collections.py"),
    ("Generate Film & Bundle Shortlists", PROJECT_ROOT / "src" / "shortlist.py"),
    ("Analyze Director & Actor Commercial Signals", PROJECT_ROOT / "src" / "analyse_talent.py"),
]


def run_pipeline():
    print("=" * 70)
    print("STREAMVAULT LICENSING ANALYSIS — AUTOMATED PIPELINE")
    print("=" * 70)
    print(f"Working Directory: {PROJECT_ROOT}")
    print(f"Python Executable: {sys.executable}")
    print("-" * 70)

    total_start = time.perf_counter()

    for step_num, (step_name, script_path) in enumerate(PIPELINE_STEPS, start=1):
        if not script_path.exists():
            print(f"\n[ERROR] Step {step_num} script not found: {script_path}")
            sys.exit(1)

        print(f"\n>>> [{step_num}/{len(PIPELINE_STEPS)}] Running: {step_name}...")
        step_start = time.perf_counter()

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True
        )

        step_elapsed = time.perf_counter() - step_start

        if result.returncode != 0:
            print(f"[FAILED] Step {step_num} failed with exit code {result.returncode}")
            print("\n--- STDOUT ---")
            print(result.stdout)
            print("\n--- STDERR ---")
            print(result.stderr)
            sys.exit(result.returncode)

        print(f"[COMPLETED] {step_name} ({step_elapsed:.2f}s)")
        # Show key summary lines from step stdout if concise
        lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        for line in lines[-3:]:
            print(f"    | {line}")

    total_elapsed = time.perf_counter() - total_start

    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION SUMMARY")
    print("=" * 70)
    print(f"All 7 pipeline stages executed successfully.")
    print(f"Total Pipeline Runtime: {total_elapsed:.2f} seconds")
    print("Processed datasets available in: data/processed/")
    print("Reconciliation reports available in: outputs/reconciliation/")
    print("Decision deliverables refreshed in: outputs/")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
