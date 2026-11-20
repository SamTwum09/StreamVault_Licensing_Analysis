import pandas as pd
from pathlib import Path

# Locate acquisition report

from pathlib import Path
import pandas as pd

PROJECT_PROJECT_ROOT = Path(__file__).resolve().parent.parent
report_path = PROJECT_PROJECT_ROOT / "outputs" / "reconciliation" / "acquisition_reconciliation.csv"

report = pd.read_csv(
    report_path,
    dtype="string",
    keep_default_na=False
)

# 1. Display all invalid IDs
print("\n--- INVALID ID RECORDS ---")

invalid = report[
    report["final_status"] == "invalid_id"
]

if invalid.empty:
    print("No invalid IDs found.")
else:
    print(
        invalid[
            ["source_row", "original_id", "normalized_id"]
        ].to_string(index=False)
    )

# 2. Investigate unsuccessful or partial retrievals
print("\n--- UNSUCCESSFUL OR PARTIAL RETRIEVALS ---")

problems = report[
    report["final_status"] == "not_found_or_partial"
]

if problems.empty:
    print("No unsuccessful or partial records.")
else:
    print(
        problems[
            [
                "source_row",
                "normalized_id",
                "movie_status",
                "credits_status"
            ]
        ].to_string(index=False)
    )

# 3. Check whether problem IDs are repeated
print("\n--- DISTINCT PROBLEM IDs ---")

if not problems.empty:
    print(
        problems.groupby("normalized_id").agg(
            source_rows=("source_row", list),
            movie_status=("movie_status", "first"),
            credits_status=("credits_status", "first")
        ).to_string()
    )

# 4. Count saved raw JSON files
movie_dir = PROJECT_PROJECT_ROOT / "data" / "raw" / "movies"
credits_dir = PROJECT_PROJECT_ROOT / "data" / "raw" / "credits"

movie_files = list(movie_dir.glob("*.json"))
credits_files = list(credits_dir.glob("*.json"))

print("\n--- RAW FILE COUNTS ---")
print("Movie JSON files:", len(movie_files))
print("Credits JSON files:", len(credits_files))

# 5. Verify source-row reconciliation
print("\n--- RECONCILIATION CHECK ---")
print("Total source rows:", len(report))
print("\nStatus totals:")
print(report["final_status"].value_counts().to_string())

print(
    "\nReconciliation balances:",
    len(report) == 127
)
