
import time
from pathlib import Path

import pandas as pd


# 1. Locate project folders
ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "processed" / "films.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

start_time = time.perf_counter()


# 2. Load the processed film table
films = pd.read_csv(INPUT_FILE)

# Ensure financial fields are numeric
films["budget"] = pd.to_numeric(films["budget"], errors="coerce")
films["revenue"] = pd.to_numeric(films["revenue"], errors="coerce")
films["release_year"] = pd.to_numeric(
    films["release_year"], errors="coerce"
)

# Ensure franchise classification is Boolean
films["is_franchise"] = (
    films["is_franchise"]
    .astype(str)
    .str.lower()
    .map({"true": True, "false": False})
)


# 3. Calculate film-level financial indicators
films["revenue_budget_multiple"] = (
    films["revenue"] / films["budget"]
)

films["return_proxy_pct"] = (
    (films["revenue"] - films["budget"])
    / films["budget"]
) * 100


# 4. Define the two required analysis periods
periods = {
    "All years": films.copy(),
    "2000 onward": films[films["release_year"] >= 2000].copy()
}


# 5. Summarise franchise versus standalone performance
results = []

for period_name, period_data in periods.items():

    grouped = period_data.groupby("is_franchise").agg(
        film_count=("movie_id", "nunique"),
        median_budget=("budget", "median"),
        median_revenue=("revenue", "median"),
        median_revenue_budget_multiple=(
            "revenue_budget_multiple", "median"
        ),
        median_return_proxy_pct=("return_proxy_pct", "median"),
        mean_revenue=("revenue", "mean"),
        mean_return_proxy_pct=("return_proxy_pct", "mean")
    ).reset_index()

    for _, row in grouped.iterrows():
        results.append({
            "period": period_name,
            "category": (
                "Franchise" if row["is_franchise"]
                else "Standalone"
            ),
            "film_count": row["film_count"],
            "median_budget": row["median_budget"],
            "median_revenue": row["median_revenue"],
            "median_revenue_budget_multiple":
                row["median_revenue_budget_multiple"],
            "median_return_proxy_pct":
                row["median_return_proxy_pct"],
            "mean_revenue": row["mean_revenue"],
            "mean_return_proxy_pct":
                row["mean_return_proxy_pct"]
        })


# 6. Create the final KPI table
kpi_table = pd.DataFrame(results)

# Save the output
output_file = OUTPUT_DIR / "franchise_standalone_kpis.csv"
kpi_table.to_csv(output_file, index=False)


# 7. Display results
print("\n========== FRANCHISE VS STANDALONE ANALYSIS ==========")

for period_name in periods:

    print(f"\n--- {period_name.upper()} ---")

    period_results = kpi_table[
        kpi_table["period"] == period_name
    ]

    print(
        period_results[
            [
                "category",
                "film_count",
                "median_budget",
                "median_revenue",
                "median_revenue_budget_multiple",
                "median_return_proxy_pct"
            ]
        ].to_string(index=False)
    )


# 8. Validate the analysis
print("\n========== VALIDATION ==========")

print("Unique films in original dataset:", films["movie_id"].nunique())

print(
    "Films with valid financial indicators:",
    films["revenue_budget_multiple"].notna().sum()
)

print(
    "KPI groups produced:",
    len(kpi_table)
)

assert films["movie_id"].is_unique
assert films["revenue_budget_multiple"].notna().all()
assert films["return_proxy_pct"].notna().all()

elapsed = time.perf_counter() - start_time

print("\nKPI output saved to:", output_file)
print("Analysis time:", round(elapsed, 3), "seconds")
print("\nAnalysis completed successfully.")
