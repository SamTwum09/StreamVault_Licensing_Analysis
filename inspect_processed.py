
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"

films = pd.read_csv(DATA / "films.csv")
directors = pd.read_csv(DATA / "directors.csv")
actors = pd.read_csv(DATA / "lead_actors.csv")

print("\n========== DATA QUALITY AUDIT ==========")

print("\n1. TABLE SIZES")
print("Films:", len(films))
print("Director records:", len(directors))
print("Lead actor records:", len(actors))

print("\n2. MISSING VALUES IN FILMS")
print(films.isna().sum().to_string())

print("\n3. ZERO BUDGET AND REVENUE")
print("Zero budgets:", (films["budget"] == 0).sum())
print("Zero revenues:", (films["revenue"] == 0).sum())

print("\n4. FINANCIAL DATA AVAILABILITY")
print("Films with positive budget:", (films["budget"] > 0).sum())
print("Films with positive revenue:", (films["revenue"] > 0).sum())
print(
    "Films with both positive budget and revenue:",
    ((films["budget"] > 0) & (films["revenue"] > 0)).sum()
)

print("\n5. COLLECTION CLASSIFICATION")
print(films["is_franchise"].value_counts().to_string())

print("\n6. DIRECTOR DATA QUALITY")
print("Missing director names:", directors["director_name"].isna().sum())
print("Unique director IDs:", directors["director_id"].nunique())

print("\n7. LEAD ACTOR DATA QUALITY")
print("Missing actor names:", actors["actor_name"].isna().sum())
print("Unique actor IDs:", actors["actor_id"].nunique())

print("\n8. RELEASE YEAR COVERAGE")
print("Earliest year:", films["release_year"].min())
print("Latest year:", films["release_year"].max())
print("Films released before 2000:",
      (films["release_year"] < 2000).sum())
print("Films released from 2000 onward:",
      (films["release_year"] >= 2000).sum())

print("\n========== AUDIT COMPLETED ==========")
