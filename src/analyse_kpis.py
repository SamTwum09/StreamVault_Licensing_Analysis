import sys
from pathlib import Path
import time
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))
from utils import coerce_boolean_franchise

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "films.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

start_time = time.perf_counter()


# 2. Load the processed film table
films = pd.read_csv(INPUT_FILE)

# Ensure financial fields are numeric
films["budget"] = pd.to_numeric(films["budget"], errors="coerce")
films["revenue"] = pd.to_numeric(films["revenue"], errors="coerce")
films["release_year"] = pd.to_numeric(
    films["release_year"], errors="coerce"
)

# Ensure franchise classification is Boolean using centralized helper
films["is_franchise"] = coerce_boolean_franchise(films["is_franchise"])


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

    formatted = grouped.assign(
        period=period_name,
        category=grouped["is_franchise"].map({True: "Franchise", False: "Standalone"})
    )
    results.extend(formatted.to_dict("records"))


# 6. Create the final KPI table
kpi_table = pd.DataFrame(results)
columns_order = [
    "period",
    "category",
    "film_count",
    "median_budget",
    "median_revenue",
    "median_revenue_budget_multiple",
    "median_return_proxy_pct",
    "mean_revenue",
    "mean_return_proxy_pct"
]
kpi_table = kpi_table[columns_order]

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
