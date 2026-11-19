
import pandas as pd
from pathlib import Path

# 1. Locate the original candidate list
file_path = Path("data/id_list.csv")

if not file_path.exists():
    raise FileNotFoundError(
        "id_list.csv was not found inside the data folder."
    )

# 2. Load IDs as text to preserve the original values
df = pd.read_csv(
    file_path,
    dtype="string",
    keep_default_na=False,
    skip_blank_lines=False
)
# 3. Identify the ID column
id_column = df.columns[0]

# 4. Preserve the original values and create a
#    separate normalized version for inspection
df["source_row"] = range(2, len(df) + 2)
df["original_id"] = df[id_column]
df["checked_id"] = df["original_id"].str.strip()

# 5. Identify blank IDs
blank_rows = df[df["checked_id"] == ""]

# 6. Identify duplicate IDs
valid_ids = df[df["checked_id"] != ""]

duplicate_rows = valid_ids[
    valid_ids.duplicated(
        subset=["checked_id"],
        keep=False
    )
]

# 7. Calculate summary statistics
print("\n--- CANDIDATE LIST INSPECTION ---")

print("Total data rows:", len(df))
print("Blank ID rows:", len(blank_rows))
print("Non-blank ID rows:", len(valid_ids))
print("Unique non-blank IDs:", valid_ids["checked_id"].nunique())
print("Rows involved in duplicates:", len(duplicate_rows))
print(
    "Number of duplicate ID groups:",
    duplicate_rows["checked_id"].nunique()
)

# 8. Display duplicate IDs
print("\n--- DUPLICATE ID GROUPS ---")

if duplicate_rows.empty:
    print("No duplicate IDs found.")
else:
    print(
        duplicate_rows.groupby("checked_id")["source_row"]
        .apply(list)
    )

# 9. Display blank rows
print("\n--- BLANK ID ROWS ---")

if blank_rows.empty:
    print("No blank IDs found.")
else:
    print(blank_rows[["source_row", "original_id"]])

# 10. Save a reconciliation working copy
output_path = Path("data/candidate_inspection.csv")

df.to_csv(output_path, index=False)

print("\nInspection saved to:", output_path)
