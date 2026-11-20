import sys
from pathlib import Path
import pandas as pd
import time

# Start measuring analysis time
start_time = time.perf_counter()

# Locate the project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))
from utils import coerce_boolean_franchise

# Load the cleaned film dataset
films = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "films.csv")

# Prepare numeric columns
films["budget"] = pd.to_numeric(films["budget"], errors="coerce")
films["revenue"] = pd.to_numeric(films["revenue"], errors="coerce")
films["release_year"] = pd.to_numeric(films["release_year"], errors="coerce")
films["is_franchise"] = coerce_boolean_franchise(films["is_franchise"])

# Calculate commercial performance indicators
films["revenue_budget_multiple"] = films["revenue"] / films["budget"]

# Focus on films released from 2000 onward
recent_films = films[films["release_year"] >= 2000].copy()

# Separate franchise and standalone films
franchises = recent_films[recent_films["is_franchise"]].copy()
standalones = recent_films[~recent_films["is_franchise"]].copy()

# Rank franchise films by commercial scale and efficiency
franchises["revenue_rank"] = franchises["revenue"].rank(
    ascending=False, method="min"
)
franchises["multiple_rank"] = franchises["revenue_budget_multiple"].rank(
    ascending=False, method="min"
)
franchises["combined_rank"] = (
    franchises["revenue_rank"] + franchises["multiple_rank"]
)

# Rank standalone films using the same method
standalones["revenue_rank"] = standalones["revenue"].rank(
    ascending=False, method="min"
)
standalones["multiple_rank"] = standalones["revenue_budget_multiple"].rank(
    ascending=False, method="min"
)
standalones["combined_rank"] = (
    standalones["revenue_rank"] + standalones["multiple_rank"]
)

# Select the top 3 franchise films and top 5 standalone films
top_franchises = franchises.sort_values(
    ["combined_rank", "revenue"], ascending=[True, False]
).head(3)

top_standalones = standalones.sort_values(
    ["combined_rank", "revenue"], ascending=[True, False]
).head(5)

# Keep the fields needed to explain the shortlist
columns = [
    "movie_id",
    "title",
    "collection_id",
    "collection_name",
    "release_year",
    "budget",
    "revenue",
    "revenue_budget_multiple",
    "revenue_rank",
    "multiple_rank",
    "combined_rank",
]

shortlist = pd.concat(
    [
        top_franchises.assign(category="Franchise"),
        top_standalones.assign(category="Standalone"),
    ]
)

shortlist = shortlist[["category"] + columns]

# Save the shortlist
output_path = PROJECT_ROOT / "data" / "processed" / "licensing_shortlist.csv"
shortlist.to_csv(output_path, index=False)

# Display results
print("\nTOP 3 FRANCHISE FILMS")
print(top_franchises[columns].to_string(index=False))

print("\nTOP 5 STANDALONE FILMS")
print(top_standalones[columns].to_string(index=False))

print(f"\nShortlist saved to: {output_path}")
print(f"Analysis time: {time.perf_counter() - start_time:.2f} seconds")
