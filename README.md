# StreamVault Licensing Analysis

## 1. Project Overview

This project analyses StreamVault's candidate movie list to support a $14 million content licensing decision.

The objective is to evaluate whether StreamVault should prioritise franchise bundles or standalone films, identify promising acquisition targets, and examine whether directors and lead actors show patterns associated with stronger historical commercial performance.

Movie and credits data are acquired from the public TMDb API, transformed using Python and Pandas, and analysed using reproducible scripts.

## 2. Key Questions

The analysis addresses five questions:

1. Do franchise films demonstrate stronger historical financial performance than standalone films?
2. Does the recommendation remain consistent when considering films released from 2000 onward?
3. Which three franchise collections and five standalone films should receive acquisition attention?
4. Do directors and lead actors show patterns that may help inform acquisition priorities?
5. What data-quality limitations should StreamVault consider before committing licensing funds?

## 3. Project Structure

```text
StreamVault_Licensing_Analysis/
│
├── data/
│   ├── id_list.csv
│   ├── raw/
│   │   ├── movies/
│   │   └── credits/
│   └── processed/
│       ├── films.csv
│       ├── directors.csv
│       ├── lead_actors.csv
│       ├── franchise_standalone_kpis.csv
│       ├── licensing_shortlist.csv
│       ├── franchise_collection_analysis.csv
│       ├── director_performance.csv
│       └── actor_performance.csv
│
├── outputs/
│   ├── data_diagnosis.md
│   ├── decision_notes.md
│   ├── client_memo.md
│   ├── quality_report.csv
│   └── reconciliation/
│       └── acquisition_reconciliation.csv
│
├── src/
│   ├── fetch_tmdb.py
│   ├── transform_tmdb.py
│   ├── quality_checks.py
│   ├── analyse_kpis.py
│   ├── shortlist.py
│   ├── analyse_collections.py
│   └── analyse_talent.py
│
├── notebook/
├── .env
├── .gitignore
├── test_connection.py
├── inspect_candidates.py
├── inspect_acquisition.py
└── inspect_processed.py
```

## 4. Technologies Used

- Python – acquisition, transformation and analysis.
- Pandas – data cleaning, tabular transformations, joins and aggregation.
- NumPy – numerical analysis support.
- Requests – communication with the TMDb API.
- python-dotenv – loading API credentials securely from environment variables.
- TMDb API – movie details and credits.

## 5. Environment Setup

### Requirements

Python 3 and the following packages are required:

```bash
python -m pip install -r requirements.txt
```

### API configuration

Create a `.env` file in the project root:

```text
TMDB_API_KEY=your_tmdb_api_key
```

Replace the placeholder with your own TMDb API key.

Do not commit `.env` or expose your API key in source code or GitHub.

The `.gitignore` file should include:

```text
.env
__pycache__/
*.pyc
.ipynb_checkpoints/
.venv/
```

## 6. Execution Order

### Option A: Automated One-Command Pipeline (Recommended for Adjoa in Live Meetings)

To execute the entire acquisition, transformation, validation, and analytics pipeline end-to-end:

```bash
python run_pipeline.py
```

This runs all stages in sequence, validates data integrity, outputs timing benchmarks (executes in ~12 seconds with cache), and refreshes all processed datasets and reports.

---

### Option B: Step-by-Step Execution

Alternatively, individual modules can be executed in sequence from the project root:

### Step 1: Test API connection

```bash
python test_connection.py
```

This confirms that the API key loads and the TMDb API is reachable.

### Step 2: Inspect the original candidate list

```bash
python inspect_candidates.py
```

This identifies blank IDs, duplicate values and invalid candidate identifiers.

### Step 3: Acquire movie and credits data

```bash
python src/fetch_tmdb.py
```

This retrieves movie details and credits for unique valid numeric IDs and generates the acquisition reconciliation file.

### Step 4: Inspect acquisition results

```bash
python inspect_acquisition.py
```

This reviews invalid identifiers, unsuccessful retrievals and acquisition totals.

### Step 5: Transform the raw JSON responses

```bash
python src/transform_tmdb.py
```

This creates the film, director and lead-actor datasets.

### Step 6: Run automated quality checks

```bash
python src/quality_checks.py
```

This validates uniqueness, required fields, financial values, relationships and release years.

All six checks should pass before proceeding with the analysis.

### Step 7: Inspect processed data

```bash
python inspect_processed.py
```

This provides an additional overview of the processed datasets and their quality.

### Step 8: Analyse franchise and standalone performance

```bash
python src/analyse_kpis.py
```

This calculates financial performance indicators for all years and for films released from 2000 onward.

### Step 9: Generate film shortlists

```bash
python src/shortlist.py
```

This ranks the top three franchise films and five standalone films using the selected ranking method.

### Step 10: Analyse franchise collections

```bash
python src/analyse_collections.py
```

This aggregates candidate films into collections and identifies the leading franchise bundle opportunities.

### Step 11: Analyse director and actor patterns

```bash
python src/analyse_talent.py
```

This evaluates historical film performance associated with directors and lead actors.

## 7. Key Results

The acquisition and transformation process produced:

| Measure | Result |
|---|---:|
| Original source rows | 127 |
| Unique valid numeric IDs | 117 |
| Fully retrieved unique films | 112 |
| Unretrieved numeric IDs | 5 |
| Invalid ID rows | 3 |
| Blank ID rows | 1 |
| Duplicate ID groups | 6 |
| Processed film records | 112 |

### Franchise versus standalone performance

| Comparison period | Franchise median multiple | Standalone median multiple |
|---|---:|---:|
| All years | 5.62x | 3.84x |
| 2000 onward | 5.05x | 3.84x |

The franchise group demonstrated a higher median historical revenue-to-budget multiple in both comparison periods.

The recommendation is therefore to prioritise franchise bundle negotiations while retaining selected standalone titles as complementary opportunities.

### Preferred franchise target

The Avengers Collection ranked first among the 24 collections analysed using the combined ranking of total historical revenue and median revenue-to-budget multiple.

Its four represented candidate films recorded approximately $7.92 billion in historical box-office revenue.

These results do not establish future streaming returns or a defensible licensing price.

## 8. Important Assumptions and Limitations

- TMDb is the source of the movie and credits data.
- A film is classified as a franchise title when it has a TMDb collection association.
- The top three billed cast members are used as lead actors.
- Historical production budgets and box-office revenues are used as commercial performance indicators.
- Financial values were not independently verified or adjusted for inflation and currency differences.
- Historical box-office performance is not equivalent to streaming or licensing profitability.
- The candidate list may not represent the wider film market.
- The analysis covers 112 successfully retrieved films, not every original source row.

These limitations should be considered before making a licensing commitment.

## 9. Reproducibility and Scalability

The analysis is divided into separate scripts for acquisition, transformation, validation and analysis.

This makes the process easier to maintain and rerun as the candidate list grows from 127 source rows towards the expected 500 titles.

The acquisition script retrieves unique IDs and caches successful API responses locally. The processed datasets separate films from their one-to-many director and actor relationships to reduce the risk of duplicated financial totals.

The automated quality-check script provides a repeatable validation step before analysis.

For larger future runs, the acquisition process should be reviewed for cache refresh requirements, API rate limits and additional performance testing.

## 10. Main Deliverables & Rubric Mapping

| Deliverable / Rubric Requirement | Repository Location | Description |
|---|---|---|
| **Data Diagnosis (20%)** | [`outputs/data_diagnosis.md`](file:///c:/Users/SamuelTwum/OneDrive%20-%20AmaliTech%20gGmbH/Desktop/StreamVault_Licensing_Analysis/outputs/data_diagnosis.md) | Full audit of 127 source rows, 6 duplicates, 3 invalid, 1 blank, 5 missing; risk rankings and quantified gap analysis. |
| **Data Acquisition (20%)** | [`src/fetch_tmdb.py`](file:///c:/Users/SamuelTwum/OneDrive%20-%20AmaliTech%20gGmbH/Desktop/StreamVault_Licensing_Analysis/src/fetch_tmdb.py) & [`outputs/reconciliation/acquisition_reconciliation.csv`](file:///c:/Users/SamuelTwum/OneDrive%20-%20AmaliTech%20gGmbH/Desktop/StreamVault_Licensing_Analysis/outputs/reconciliation/acquisition_reconciliation.csv) | Full API extraction with local JSON caching, backoff retries, and row-level traceability back to `id_list.csv`. |
| **Working Analysis (20%)** | [`run_pipeline.py`](file:///c:/Users/SamuelTwum/OneDrive%20-%20AmaliTech%20gGmbH/Desktop/StreamVault_Licensing_Analysis/run_pipeline.py) & `src/` | 3-table relational model (`films`, `directors`, `lead_actors`), join validation, vectorized calculations, and measured sub-minute runtime. |
| **Decision Notes & Reasoning (20%)** | [`outputs/decision_notes.md`](file:///c:/Users/SamuelTwum/OneDrive%20-%20AmaliTech%20gGmbH/Desktop/StreamVault_Licensing_Analysis/outputs/decision_notes.md) | Judgement calls, cost if wrong, 500-title scalability analysis, and exact outcomes under rejected alternatives. |
| **Client Memo (20%)** | [`outputs/client_memo.md`](file:///c:/Users/SamuelTwum/OneDrive%20-%20AmaliTech%20gGmbH/Desktop/StreamVault_Licensing_Analysis/outputs/client_memo.md) | 1-page executive memo in business language: franchise vs. standalone across both windows, shortlists with per-title rationale, talent signals, deal note, and capital framework. |
| **Improvement Beyond Brief #1 (for Kwame)** | Section 6 of `client_memo.md` & `decision_notes.md` | The **$14M Portfolio Capital Allocation Framework** ($8M franchise anchor, $3.5M standalone tactical, $2.5M reserve). |
| **Improvement Beyond Brief #2 (for Adjoa)** | [`run_pipeline.py`](file:///c:/Users/SamuelTwum/OneDrive%20-%20AmaliTech%20gGmbH/Desktop/StreamVault_Licensing_Analysis/run_pipeline.py) | **One-command master pipeline runner** with execution timing and negative caching, executing in ~12 seconds for live meeting reruns. |

## 11. Final Recommendation

StreamVault should prioritise franchise bundle negotiations, beginning with The Avengers Collection, while retaining selected standalone films as complementary opportunities.

The $14 million budget should be treated as a spending ceiling rather than a target. Final acquisition decisions should depend on verified rights, studio pricing, contract conditions and expected streaming value.