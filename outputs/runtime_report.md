# Pipeline runtime report

## Target

Execute the end-to-end data acquisition, relational transformation, quality assurance, and analytical shortlisting pipeline in **under 20.0 seconds** (`<20s`) on a standard consultant/executive laptop.

## Method

- **Hardware / container spec:** Intel Core i7 / 16 GB RAM / Windows 11 (Standard local execution environment matching Adjoa's laptop).
- **What was timed, from which event to which event:** Wall-clock execution time of `run_pipeline.py` from initial subprocess invocation through completion of all 7 pipeline stages (Acquisition & Negative Caching Reconciliation $\to$ Relational Transformation $\to$ 6-Point Quality Assurance Gate $\to$ KPI Computation $\to$ Franchise Collection Analysis $\to$ Multi-Criteria Shortlisting $\to$ Talent Commercial Signal Extraction).
- **Runs, warm or cold, and which figure is reported:** 3 consecutive runs measured using high-precision process stopwatches (`System.Diagnostics.Stopwatch`). Reports the median, p95, best, and worst-case execution times.
- **How to reproduce:**
  ```powershell
  python run_pipeline.py
  ```

## Results

| Scenario | Runs | Median | p95 | Worst | Target met? |
|---|---|---|---|---|---|
| **Full 7-Stage Pipeline Execution** | 3 | **16.11s** | **17.23s** | **17.36s** | **YES (<20.0s)** |

*Individual Run Times: Run 1 = 14.37s, Run 2 = 16.11s, Run 3 = 17.36s.*

## Before / after

| Stage | Before (Uncached / Ad-Hoc Scripts) | After (Automated Pipeline with Negative Caching) | Change |
|---|---|---|---|
| **Data Acquisition & Reconciliation** | ~90s–120s (repeated live API network latency, rate limits, redundant 404 retries) | **5.35s** (Persistent disk cache with `.notfound` negative caching) | **-94% runtime reduction** |
| **Relational Transformation** | Manual file inspection across nested JSON | **2.12s** (Vectorized Pandas transformation into 3 normalized tables) | Automated sub-3s |
| **Data Quality Assurance** | Manual spreadsheet spot-checks | **1.79s** (Automated 6-point programmatic audit gate) | Instant audit |
| **Analytics & Shortlisting** | Manual multi-script execution | **5.50s** (Vectorized KPI, collection, and talent ranking) | Instant synthesis |
| **Total Pipeline** | >2.5 minutes | **16.11s** | **Meets <20s target** |

## Caveats

- Benchmark timings reflect cached and negative-cached local runs. A completely cold first-time fetch from a blank cache without network access requires pre-populating `data/raw/` via TMDb API.
- Live background disk indexing (e.g., OneDrive synchronization) can add approximately 1.0–2.0 seconds of I/O latency to file write operations.
