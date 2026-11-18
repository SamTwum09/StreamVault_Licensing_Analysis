
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Load processed datasets
films = pd.read_csv(DATA_DIR / "films.csv")
directors = pd.read_csv(DATA_DIR / "directors.csv")
actors = pd.read_csv(DATA_DIR / "lead_actors.csv")

checks = []

def record_check(name, passed, details):
    checks.append({
        "check": name,
        "result": "PASS" if passed else "FAIL",
        "details": details
    })

# 1. Check film uniqueness
record_check(
    "Unique film IDs",
    films["movie_id"].is_unique,
    f"Film rows: {len(films)}"
)

# 2. Check required film fields
required_fields = [
    "movie_id",
    "title",
    "release_date",
    "budget",
    "revenue",
]

missing = films[required_fields].isnull().sum().sum()

record_check(
    "Required film fields populated",
    missing == 0,
    f"Missing values: {missing}"
)

# 3. Check financial values
valid_financials = (
    (films["budget"] > 0)
    & (films["revenue"] > 0)
).all()

record_check(
    "Positive budget and revenue",
    valid_financials,
    f"Films checked: {len(films)}"
)

# 4. Check director relationships
director_duplicates = directors.duplicated(
    subset=["movie_id", "director_id"]
).sum()

director_orphans = (
    ~directors["movie_id"].isin(films["movie_id"])
).sum()

record_check(
    "Director relationships valid",
    director_duplicates == 0 and director_orphans == 0,
    f"Duplicates: {director_duplicates}; unmatched films: {director_orphans}"
)

# 5. Check actor relationships
actor_duplicates = actors.duplicated(
    subset=["movie_id", "actor_id"]
).sum()

actor_orphans = (
    ~actors["movie_id"].isin(films["movie_id"])
).sum()

record_check(
    "Actor relationships valid",
    actor_duplicates == 0 and actor_orphans == 0,
    f"Duplicates: {actor_duplicates}; unmatched films: {actor_orphans}"
)

# 6. Check release years
valid_years = films["release_year"].notna().all()

record_check(
    "Release years populated",
    valid_years,
    f"Films checked: {len(films)}"
)

# Build quality report
report = pd.DataFrame(checks)

OUTPUT_DIR.mkdir(exist_ok=True)

report_path = OUTPUT_DIR / "quality_report.csv"
report.to_csv(report_path, index=False)

print("\nDATA QUALITY REPORT")
print(report.to_string(index=False))

if (report["result"] == "FAIL").any():
    print("\nQUALITY CHECKS FAILED. Review the report before analysis.")
    raise SystemExit(1)

print("\nALL QUALITY CHECKS PASSED.")
print("Report saved to:", report_path)
