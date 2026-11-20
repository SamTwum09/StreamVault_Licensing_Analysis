
from pathlib import Path
import pandas as pd
import time

start_time = time.perf_counter()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

films = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "films.csv"
)

# Prepare numeric fields
films["budget"] = pd.to_numeric(films["budget"], errors="coerce")
films["revenue"] = pd.to_numeric(films["revenue"], errors="coerce")
films["release_year"] = pd.to_numeric(
    films["release_year"], errors="coerce"
)

films["revenue_budget_multiple"] = (
    films["revenue"] / films["budget"]
)

# Use films released from 2000 onward
recent_films = films[films["release_year"] >= 2000].copy()

# Keep franchise films with a recorded TMDb collection
franchise_films = recent_films[
    recent_films["is_franchise"].astype(str).str.lower().isin(
        ["true", "1"]
    )
    & recent_films["collection_id"].notna()
].copy()

# Summarise the candidate films belonging to each collection
collections = (
    franchise_films
    .groupby(["collection_id", "collection_name"], as_index=False)
    .agg(
        title_count=("movie_id", "nunique"),
        total_budget=("budget", "sum"),
        total_revenue=("revenue", "sum"),
        median_revenue_budget_multiple=(
            "revenue_budget_multiple", "median"
        ),
        median_release_year=("release_year", "median"),
    )
)

# Rank collections by commercial scale and efficiency
collections["revenue_rank"] = collections["total_revenue"].rank(
    ascending=False, method="min"
)

collections["multiple_rank"] = (
    collections["median_revenue_budget_multiple"].rank(
        ascending=False, method="min"
    )
)

collections["combined_rank"] = (
    collections["revenue_rank"] + collections["multiple_rank"]
)

# Select the three highest-ranked collections
top_collections = collections.sort_values(
    ["combined_rank", "total_revenue"],
    ascending=[True, False]
).head(3)

# Save all collection results, not only the top three
output_path = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "franchise_collection_analysis.csv"
)

collections.sort_values(
    ["combined_rank", "total_revenue"],
    ascending=[True, False]
).to_csv(output_path, index=False)

print("\nTOP 3 FRANCHISE COLLECTIONS")
print(top_collections.to_string(index=False))

print("\nNUMBER OF COLLECTIONS ANALYSED:", len(collections))
print("TOTAL FRANCHISE FILMS INCLUDED:", len(franchise_films))
print("Analysis time:", round(time.perf_counter() - start_time, 2), "seconds")
print("Full results saved to:", output_path)
