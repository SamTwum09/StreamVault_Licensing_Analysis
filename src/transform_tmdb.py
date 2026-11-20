import json
import time
from pathlib import Path

import pandas as pd


# 1. Locate project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]

MOVIE_DIR = PROJECT_ROOT / "data" / "raw" / "movies"
CREDITS_DIR = PROJECT_ROOT / "data" / "raw" / "credits"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# 2. Start measuring transformation time
start_time = time.perf_counter()

film_records = []
director_records = []
actor_records = []


# 3. Process each successfully acquired movie
movie_files = sorted(MOVIE_DIR.glob("*.json"))

for movie_file in movie_files:

    movie_id = int(movie_file.stem)

    with open(movie_file, "r", encoding="utf-8") as file:
        movie = json.load(file)

    # Extract collection information safely
    collection = movie.get("belongs_to_collection") or {}

    # Extract genres
    genres = movie.get("genres") or []
    genre_names = [
        genre.get("name")
        for genre in genres
        if genre.get("name")
    ]

    # Extract production companies
    companies = movie.get("production_companies") or []
    company_names = [
        company.get("name")
        for company in companies
        if company.get("name")
    ]

    # Build one record per film
    film_records.append({
        "movie_id": movie_id,
        "title": movie.get("title"),
        "release_date": movie.get("release_date"),
        "budget": movie.get("budget"),
        "revenue": movie.get("revenue"),
        "runtime": movie.get("runtime"),
        "collection_id": collection.get("id"),
        "collection_name": collection.get("name"),
        "is_franchise": bool(collection.get("id")),
        "genres": ", ".join(genre_names),
        "production_companies": ", ".join(company_names),
        "vote_average": movie.get("vote_average"),
        "vote_count": movie.get("vote_count"),
        "popularity": movie.get("popularity"),
    })

    # 4. Find the matching credits file
    credits_file = CREDITS_DIR / f"{movie_id}.json"

    if not credits_file.exists():
        print(f"WARNING: Credits missing for movie {movie_id}")
        continue

    with open(credits_file, "r", encoding="utf-8") as file:
        credits = json.load(file)

    # 5. Extract directors using the exact job title
    crew = credits.get("crew") or []

    for person in crew:
        if person.get("job") == "Director":
            director_records.append({
                "movie_id": movie_id,
                "director_id": person.get("id"),
                "director_name": person.get("name"),
            })

    # 6. Extract the top three billed cast members
    cast = credits.get("cast") or []

    top_cast = sorted(
        cast,
        key=lambda person: person.get("order", 999999)
    )[:3]

    for person in top_cast:
        actor_records.append({
            "movie_id": movie_id,
            "actor_id": person.get("id"),
            "actor_name": person.get("name"),
            "cast_order": person.get("order"),
            "character": person.get("character"),
        })


# 7. Convert extracted records into DataFrames
films = pd.DataFrame(film_records)
directors = pd.DataFrame(director_records)
lead_actors = pd.DataFrame(actor_records)


# 8. Create a release year column
films["release_date"] = pd.to_datetime(
    films["release_date"],
    errors="coerce"
)

films["release_year"] = films["release_date"].dt.year


# 9. Save the processed tables
films.to_csv(OUTPUT_DIR / "films.csv", index=False)
directors.to_csv(OUTPUT_DIR / "directors.csv", index=False)
lead_actors.to_csv(OUTPUT_DIR / "lead_actors.csv", index=False)


# 10. Validate the results
elapsed_time = time.perf_counter() - start_time

print("\n========== TRANSFORMATION SUMMARY ==========")

print("Movie JSON files processed:", len(movie_files))
print("Film table rows:", len(films))
print("Director records:", len(directors))
print("Lead actor records:", len(lead_actors))

print("\nDuplicate movie IDs in films table:",
      films["movie_id"].duplicated().sum())

print("Films with missing release years:",
      films["release_year"].isna().sum())

print("Films with no collection:",
      (~films["is_franchise"]).sum())

print("Films with collection:",
      films["is_franchise"].sum())

print("\nOutput files saved in:", OUTPUT_DIR)
print("Transformation time:", round(elapsed_time, 3), "seconds")

assert films["movie_id"].is_unique, (
    "ERROR: Film table contains duplicate movie IDs"
)

assert len(films) == len(movie_files), (
    "ERROR: Some movie files were not represented in the film table"
)

print("\nTransformation and validation completed successfully.")
