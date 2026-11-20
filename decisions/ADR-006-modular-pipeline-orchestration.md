# ADR-006: Orchestrate Analytical Pipeline via Modular Python Scripts

- **Status:** Accepted
- **Date:** 2026-10-31
- **Decision owner:** Samuel Twum

## Context

Adjoa needs to rerun the full licensing analysis quarterly on her laptop during live executive meetings, and the engineering team will expand the codebase to support 500+ titles next year. Relying on an interactive notebook creates hidden execution state dependencies, cell ordering bugs, and slow manual execution steps.

## Decision

I orchestrate the end-to-end analytical workflow as modular, single-responsibility Python scripts coordinated by a master pipeline runner (`run_pipeline.py`).

## Alternatives considered

### Alternative A: Monolithic Interactive Jupyter Notebook

- **How it would work:** Place all ingestion, transformation, quality validation, and KPI calculations into a single `.ipynb` notebook.
- **Why it is attractive:** Easy for ad-hoc charting and exploratory data manipulation.
- **Why rejected:** Suffers from hidden execution state, out-of-order cell runs, unrepeatable manual execution, and lack of clean CLI automation for live meetings.

### Alternative B: Enterprise Workflow Orchestrator (Airflow / Prefect / Dagster)

- **How it would work:** Define pipeline stages as DAG tasks in a heavy orchestration framework.
- **Why it is attractive:** Enterprise-grade scheduling, monitoring UI, and retry infrastructure.
- **Why rejected:** Overkill for a local laptop environment, requires running daemon processes and databases, and violates the requirement for lightweight, zero-overhead execution.

## Consequences

- **What this buys:** Clean CLI invocation (`python run_pipeline.py`), modular pipeline execution, reduced manual sequencing, and repeatable processing when the same input data, dependencies and configuration are available. Execution time depends on cache state, network availability and machine performance.
- **What this costs:** Requires running separate inspection scripts for ad-hoc data viewing rather than clicking through interactive notebook cells.
- **What it costs the client if I am wrong:** If Adjoa is unfamiliar with running Python scripts from a shell, she may find the command-line interface less visual than a spreadsheet or notebook UI.
- **What would make me revisit this:** Transitioning the quarterly pipeline to an automated cloud batch job triggered on schedule or webhook.

## What this survives

Survives developer environment handoffs, OS changes, and dataset scaling up to thousands of titles with zero dependency on interactive kernels.
