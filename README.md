# StreamVault Content Licensing Analysis ($14M Decision Review)

An evidence-based commercial licensing analysis evaluating candidate film titles from the public TMDb API to support StreamVault's $14.0M content acquisition review on October 31.

The workflow provides a modular analytical pipeline that acquires, reconciles, validates and analyzes movie and credit data across two time horizons (all years versus 2000 onward). Cached runs are designed for rapid quarterly reruns; runtime depends on cache state, network access and local machine performance.
---

## 1. Quick Start (Reproducible in <20s)

```bash
# 1. Clone the repository
git clone https://github.com/SamTwum09/StreamVault_Licensing_Analysis.git
cd StreamVault_Licensing_Analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your TMDb API key in .env
echo "TMDB_API_KEY=your_tmdb_api_key_here" > .env

# 4. Run the full automated pipeline
python run_pipeline.py
```

---

## 2. Core Deliverables & Rubric Map

Each deliverable is aligned directly with the evaluation rubric:

| Deliverable / Rubric Area | Location | Core Focus & Client Value |
| :--- | :--- | :--- |
| **Client Memo (20%)** | [`outputs/client_memo.md`](outputs/client_memo.md) | **1-page business executive memo:** Strategic recommendation, two-window comparison, 3 franchise & 5 standalone shortlists with per-title rationales, talent signals, deal note, and capital framework. |
| **Data Diagnosis (20%)** | [`outputs/data_diagnosis.md`](outputs/data_diagnosis.md) | **Full candidate audit:** 127-row reconciliation, risk rankings, and quantified financial exposure of the 5 missing titles. |
| **Decision Notes (20%)** | [`outputs/decision_notes.md`](outputs/decision_notes.md) | **Methodology & defense:** Assumptions, cost if wrong, 500-title scalability analysis, and exact outcomes under real rejected alternatives. |
| **Working Pipeline (20%)** | [`run_pipeline.py`](run_pipeline.py) | **One-command orchestrator:** Executes acquisition, relational transformation, quality checks, and analytics with sub-20s measured runtime. |
| **Data Quality Suite (20%)** | [`outputs/quality_report.csv`](outputs/quality_report.csv) | Automated 6-point integrity audit validating uniqueness, positive financials, and relationship integrity. |
| **Architecture Decision Records** | [`decisions/`](decisions/) | 6 formal ADRs documenting relational normalization, negative caching, 2000-onward window, ranking model, quality gates, and pipeline orchestration. |
| **Measurement Report (<20s Target)** | [`outputs/runtime_report.md`](outputs/runtime_report.md) | High-precision timing benchmark (16.11s median runtime, p95 17.23s) confirming <20s execution target. |
| **Improvement Beyond Brief** | [`outputs/improvement.md`](outputs/improvement.md) | **$14M Capital Allocation Framework & Meeting Runner:** Structured deployment model and offline meeting runner. |

---

## 3. Executive Findings Summary

### Franchise vs. Standalone Performance Across Windows
Franchises demonstrated higher historical capital efficiency and audience reach across both analytical windows:

| Comparison Period | Franchise Median Multiple | Standalone Median Multiple | Premium | Recommendation Consistency |
| :--- | :---: | :---: | :---: | :---: |
| **All Years (112 titles)** | **5.62x** | **3.84x** | +46% | Prioritise Franchise Bundles |
| **2000 Onward (71 titles)** | **5.05x** | **3.84x** | +31% | Prioritise Franchise Bundles |

*Addressing Finance (Yaw):* Restricting the window to post-2000 titles eliminates pre-2000 reporting anomalies. The franchise advantage remains decisive (+31%), confirming the recommendation is robust across both windows.

### Recommended Acquisition Targets
* **Top Franchise Collection:** *The Avengers Collection* (4 candidate titles | $7.92B box office | 6.87x multiple). Bidding ceiling capped at **35%–40% of budget ($5.0M–$5.6M)**.
* **Complementary Franchise Targets:** *The Lord of the Rings Collection* (11.73x multiple) and *Harry Potter Collection* (6.17x multiple).
* **Tactical Standalone Shortlist:** *Inception* (5.24x), *Interstellar* (4.52x), *Spirited Away* (14.47x), *WALL·E* (2.90x), and *The Departed* (3.24x).

### Negotiating Levers (Talent Signals)
* **Directors:** Anthony & Joe Russo (7.55x multiple, $5.0B revenue) and Peter Jackson (6.73x multiple, $5.85B revenue across 6 films).
* **Marquee Actors:** Chris Evans & Mark Ruffalo (6.90x multiple, $5.8B–$6.5B) for action ensembles; Elijah Wood & Viggo Mortensen (11.73x multiple) for evergreen titles.

---

## 4. Repository Structure

```text
StreamVault_Licensing_Analysis/
├── run_pipeline.py            # Master one-command pipeline runner
├── requirements.txt           # Python package dependencies
├── README.md                  # Executive overview and navigation
├── decisions/                 # 6 Architecture Decision Records (ADR-001 to ADR-006)
├── data/
│   ├── id_list.csv            # Original 127 candidate IDs
│   ├── raw/                   # Cached TMDb JSON responses (movies & credits)
│   └── processed/             # 3 normalized relational tables (films, directors, actors)
├── outputs/
│   ├── client_memo.md         # 1-page executive decision memo
│   ├── decision_notes.md      # Analytical reasoning and rejected alternatives
│   ├── data_diagnosis.md      # Quality and candidate reconciliation diagnosis
│   ├── improvement.md         # Improvement beyond the brief deliverable
│   ├── runtime_report.md      # Measurement report on <20s target
│   ├── quality_report.csv     # Automated data integrity test results
│   └── reconciliation/        # Full row-by-row candidate acquisition audit
├── scripts/                   # Development and inspection utilities
└── src/                       # Modular pipeline stages
    ├── fetch_tmdb.py          # API acquisition with retries and negative caching
    ├── transform_tmdb.py      # Relational schema transformation
    ├── quality_checks.py      # 6 automated data integrity checks
    ├── analyse_kpis.py        # Franchise vs standalone financial metrics
    ├── analyse_collections.py # Franchise bundle aggregation and ranking
    ├── shortlist.py           # Multi-criteria balanced shortlisting
    └── analyse_talent.py      # Director and lead actor commercial signals
```

---

## 5. Technical Highlights & Scalability to 500 Titles

1. **Relational Data Architecture:** Normalizes nested JSON into 3 separate tables (`films`, `directors`, `lead_actors`) with `many_to_one` join validation to prevent double-counting financial metrics.
2. **Vectorized Computation:** Uses Pandas vectorization and grouping operations without row iteration.
3. **Negative Caching:** Retains missing/404 statuses locally so repeat runs avoid redundant network calls and run completely offline in seconds.
4. **Automated Quality Gate:** Enforces 6 structural validation tests before analytical outputs are generated.
