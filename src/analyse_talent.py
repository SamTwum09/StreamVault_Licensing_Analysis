
from pathlib import Path
import pandas as pd
import time

start_time = time.time()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Load the three datasets
films = pd.read_csv(DATA_DIR / "films.csv")
directors = pd.read_csv(DATA_DIR / "directors.csv")
actors = pd.read_csv(DATA_DIR / "lead_actors.csv")

# Prepare financial indicators at film level
films["budget"] = pd.to_numeric(films["budget"], errors="coerce")
films["revenue"] = pd.to_numeric(films["revenue"], errors="coerce")
films["release_year"] = pd.to_numeric(
    films["release_year"], errors="coerce"
)

films["revenue_budget_multiple"] = (
    films["revenue"] / films["budget"]
)

# Focus on films from 2000 onward
recent_films = films[films["release_year"] >= 2000].copy()

# Create a unique film-level financial lookup
film_metrics = recent_films[
    [
        "movie_id",
        "title",
        "budget",
        "revenue",
        "revenue_budget_multiple",
    ]
].copy()

# --------------------------------------------------
# DIRECTOR ANALYSIS
# --------------------------------------------------

# Join directors to film-level financial indicators
director_data = directors.merge(
    film_metrics,
    on="movie_id",
    how="inner",
    validate="many_to_one",
)

director_summary = (
    director_data
    .groupby(["director_id", "director_name"], as_index=False)
    .agg(
        film_count=("movie_id", "nunique"),
        median_revenue=("revenue", "median"),
        median_revenue_budget_multiple=(
            "revenue_budget_multiple", "median"
        ),
        total_revenue=("revenue", "sum"),
    )
)

# Require at least two candidate films for a more meaningful pattern
director_summary = director_summary[
    director_summary["film_count"] >= 2
].copy()

director_summary = director_summary.sort_values(
    ["median_revenue_budget_multiple", "median_revenue"],
    ascending=False,
)

# --------------------------------------------------
# LEAD ACTOR ANALYSIS
# --------------------------------------------------

# Join actors to film-level financial indicators
actor_data = actors.merge(
    film_metrics,
    on="movie_id",
    how="inner",
    validate="many_to_one",
)

actor_summary = (
    actor_data
    .groupby(["actor_id", "actor_name"], as_index=False)
    .agg(
        film_count=("movie_id", "nunique"),
        median_revenue=("revenue", "median"),
        median_revenue_budget_multiple=(
            "revenue_budget_multiple", "median"
        ),
        total_revenue=("revenue", "sum"),
    )
)

# Require at least two candidate films
actor_summary = actor_summary[
    actor_summary["film_count"] >= 2
].copy()

actor_summary = actor_summary.sort_values(
    ["median_revenue_budget_multiple", "median_revenue"],
    ascending=False,
)

# Save complete results
director_summary.to_csv(
    DATA_DIR / "director_performance.csv",
    index=False,
)

actor_summary.to_csv(
    DATA_DIR / "actor_performance.csv",
    index=False,
)

# Display the top ten
print("\nTOP DIRECTORS (AT LEAST 2 FILMS)")
print(director_summary.head(10).to_string(index=False))

print("\nTOP LEAD ACTORS (AT LEAST 2 FILMS)")
print(actor_summary.head(10).to_string(index=False))


# --------------------------------------------------
#  JOIN VALIDATION
# --------------------------------------------------

# Identify the films included in the 2000-onward analysis
recent_ids = set(film_metrics["movie_id"])

# Filter credit tables to the same date window
recent_directors = directors[
    directors["movie_id"].isin(recent_ids)
].copy()

recent_actors = actors[
    actors["movie_id"].isin(recent_ids)
].copy()

# Check whether every recent credit record finds a film record
director_check = recent_directors.merge(
    film_metrics[["movie_id"]],
    on="movie_id",
    how="left",
    validate="many_to_one",
    indicator=True,
)

actor_check = recent_actors.merge(
    film_metrics[["movie_id"]],
    on="movie_id",
    how="left",
    validate="many_to_one",
    indicator=True,
)

# Count records without a matching film
unmatched_directors = (director_check["_merge"] == "left_only").sum()
unmatched_actors = (actor_check["_merge"] == "left_only").sum()

print("\nJOIN VALIDATION")
print("Recent unique films:", len(recent_ids))
print("Recent director-credit records:", len(recent_directors))
print("Director records joined:", len(director_data))
print("Unmatched director records:", unmatched_directors)

print("\nRecent actor-credit records:", len(recent_actors))
print("Actor records joined:", len(actor_data))
print("Unmatched actor records:", unmatched_actors)

print("\nOLDER CREDIT RECORDS EXCLUDED BY DATE FILTER")
print("Older director records:", len(directors) - len(recent_directors))
print("Older actor records:", len(actors) - len(recent_actors))

# Check whether credit records are duplicated
print("\nDUPLICATE CREDIT CHECK")
print(
    "Duplicate director-film records:",
    recent_directors.duplicated(
        subset=["movie_id", "director_id"]
    ).sum()
)
print(
    "Duplicate actor-film records:",
    recent_actors.duplicated(
        subset=["movie_id", "actor_id"]
    ).sum()
)
