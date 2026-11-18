
import os
import json
import time
import re
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


# --------------------------------------------------
# 1. PROJECT PATHS AND CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("TMDB_API_KEY")

INPUT_FILE = PROJECT_ROOT / "data" / "id_list.csv"

MOVIE_DIR = PROJECT_ROOT / "data" / "raw" / "movies"
CREDITS_DIR = PROJECT_ROOT / "data" / "raw" / "credits"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "reconciliation"

BASE_URL = "https://api.themoviedb.org/3"

# Create output folders if they do not exist
for folder in [MOVIE_DIR, CREDITS_DIR, OUTPUT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. VALIDATE CONFIGURATION
# --------------------------------------------------

if not API_KEY:
    raise ValueError(
        "TMDB_API_KEY not found. Check your .env file."
    )

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Candidate list not found: {INPUT_FILE}"
    )


# --------------------------------------------------
# 3. LOAD THE ORIGINAL CANDIDATE LIST
# --------------------------------------------------

candidates = pd.read_csv(
    INPUT_FILE,
    dtype="string",
    keep_default_na=False,
    skip_blank_lines=False
)

id_column = candidates.columns[0]

# Preserve original row numbers and values
candidates["source_row"] = range(
    2, len(candidates) + 2
)

candidates["original_id"] = candidates[id_column]

candidates["checked_id"] = (
    candidates["original_id"].str.strip()
)

print("Source rows loaded:", len(candidates))


# --------------------------------------------------
# 4. PREPARE UNIQUE VALID MOVIE IDS
# --------------------------------------------------

valid_ids = candidates[
    candidates["checked_id"].str.fullmatch(r"\d+").fillna(False)
]

unique_ids = valid_ids["checked_id"].drop_duplicates().tolist()

print("Unique movie IDs to retrieve:", len(unique_ids))
print("Duplicate entries preserved in source list.")


# --------------------------------------------------
# 5. CREATE API SESSION
# --------------------------------------------------

session = requests.Session()


# --------------------------------------------------
# 6. FUNCTION TO FETCH AND CACHE JSON
# --------------------------------------------------

def fetch_tmdb(endpoint, output_file):

    # Reuse negative cache (known missing/404 titles)
    notfound_file = output_file.with_suffix(".notfound")
    if notfound_file.exists():
        return None, "http_404"

    # Reuse an existing successful response
    if output_file.exists():
        try:
            with open(output_file, "r", encoding="utf-8") as file:
                cached_data = json.load(file)

            if isinstance(cached_data, dict):
                if cached_data.get("success") is not False:
                    return cached_data, "cached"

        except (json.JSONDecodeError, OSError):
            print("Invalid cache; downloading again.")

    url = f"{BASE_URL}/{endpoint}"

    params = {
        "api_key": API_KEY
    }

    # Retry temporary failures
    for attempt in range(4):

        try:
            response = session.get(
                url,
                params=params,
                timeout=30
            )

            if response.status_code == 200:

                data = response.json()

                if not isinstance(data, dict):
                    return None, "invalid_response"

                if data.get("success") is False:
                    return None, "api_error"

                # Save original response
                with open(
                    output_file,
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        data,
                        file,
                        ensure_ascii=False,
                        indent=2
                    )

                time.sleep(0.25)

                return data, "downloaded"

            # These errors are not fixed by retrying
            if response.status_code in [401, 403, 404]:
                if response.status_code == 404:
                    try:
                        with open(output_file.with_suffix(".notfound"), "w", encoding="utf-8") as f:
                            f.write("404")
                    except OSError:
                        pass
                return None, f"http_{response.status_code}"

            # Retry rate limits and temporary server errors
            if response.status_code == 429 or response.status_code >= 500:

                if response.status_code == 429:
                    wait_time = int(
                        response.headers.get("Retry-After", 2)
                    )
                else:
                    wait_time = 2 ** attempt

                print(
                    f"Temporary API error {response.status_code}. "
                    f"Waiting {wait_time} seconds."
                )

                time.sleep(wait_time)
                continue

            return None, f"http_{response.status_code}"

        except requests.exceptions.RequestException:
            if attempt == 3:
                return None, "request_error"

            time.sleep(2 ** attempt)

        except ValueError:
            return None, "invalid_json"

    return None, "failed_after_retries"


# --------------------------------------------------
# 7. RETRIEVE MOVIE DETAILS AND CREDITS
# --------------------------------------------------

results = {}

for position, movie_id in enumerate(unique_ids, start=1):

    print(
        f"\nProcessing movie {position}/{len(unique_ids)}: "
        f"ID {movie_id}"
    )

    movie_file = MOVIE_DIR / f"{movie_id}.json"
    credits_file = CREDITS_DIR / f"{movie_id}.json"

    # Retrieve movie details
    movie_data, movie_status = fetch_tmdb(
        f"movie/{movie_id}",
        movie_file
    )

    # Retrieve cast and crew
    credits_data, credits_status = fetch_tmdb(
        f"movie/{movie_id}/credits",
        credits_file
    )

    results[movie_id] = {
        "movie_status": movie_status,
        "credits_status": credits_status
    }

    print("Movie details:", movie_status)
    print("Credits:", credits_status)


# --------------------------------------------------
# 8. RECONCILE EVERY ORIGINAL SOURCE ROW
# --------------------------------------------------

reconciliation = []

for _, row in candidates.iterrows():

    movie_id = row["checked_id"]

    if movie_id == "":
        movie_status = "blank_id"
        credits_status = "blank_id"
        final_status = "blank_id"

    elif not re.fullmatch(r"\d+", movie_id):
        movie_status = "invalid_id"
        credits_status = "invalid_id"
        final_status = "invalid_id"

    else:
        record = results[movie_id]

        movie_status = record["movie_status"]
        credits_status = record["credits_status"]

        if (
            movie_status in ["downloaded", "cached"]
            and credits_status in ["downloaded", "cached"]
        ):
            final_status = "retrieved"

        elif (
            movie_status.startswith("http_404")
            or credits_status.startswith("http_404")
        ):
            final_status = "not_found_or_partial"

        else:
            final_status = "retrieval_failed_or_partial"

    reconciliation.append({
        "source_row": row["source_row"],
        "original_id": row["original_id"],
        "normalized_id": movie_id,
        "movie_status": movie_status,
        "credits_status": credits_status,
        "final_status": final_status
    })


# --------------------------------------------------
# 9. SAVE RECONCILIATION REPORT
# --------------------------------------------------

report = pd.DataFrame(reconciliation)

report_path = OUTPUT_DIR / "acquisition_reconciliation.csv"

report.to_csv(report_path, index=False)


# --------------------------------------------------
# 10. PRINT FINAL SUMMARY
# --------------------------------------------------

print("\n======================================")
print("TMDB ACQUISITION SUMMARY")
print("======================================")

print("Original source rows:", len(candidates))
print("Unique valid movie IDs:", len(unique_ids))

print(
    "Fully retrieved unique IDs:",
    sum(
        1 for result in results.values()
        if result["movie_status"] in ["downloaded", "cached"]
        and result["credits_status"] in ["downloaded", "cached"]
    )
)

print("\nSource-row reconciliation:")
print(report["final_status"].value_counts(dropna=False))

print("\nReconciliation saved to:")
print(report_path)

print("\nAcquisition process completed.")
