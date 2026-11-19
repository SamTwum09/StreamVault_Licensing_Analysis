# ADR-005: Gate Analytical Pipeline on Automated Six-Point Integrity Audit

- **Status:** Accepted
- **Date:** 2026-10-31
- **Decision owner:** Samuel Twum

## Context

Allocating a $14.0M capital budget based on unverified, incomplete, or corrupted data poses severe legal and financial risks. Common issues such as orphan records, duplicate film entries, missing budgets, or zero-revenue values can compromise commercial rankings and damage executive credibility before the Board.

## Decision

I gate all downstream analytical stages behind a dedicated six-point automated data quality audit script (`src/quality_checks.py`) that halts execution on any integrity failure and logs findings to `outputs/quality_report.csv`.

## Alternatives considered

### Alternative A: Ad-Hoc Manual Spot Checks

- **How it would work:** Review processed CSV files manually in spreadsheets before running analytical scripts.
- **Why it is attractive:** Requires no upfront scripting or test design.
- **Why rejected:** Highly prone to human error, impossible to reproduce consistently, and completely unfeasible when Adjoa scales to 500+ titles.

### Alternative B: Non-Blocking Logging and Warnings Only

- **How it would work:** Log warnings for missing data or orphan keys while allowing downstream analytical scripts to continue executing.
- **Why it is attractive:** Ensures the pipeline always runs to completion regardless of input quality.
- **Why rejected:** Silent failures or corrupted numbers can propagate undetected into final executive memos and client shortlists.

## Consequences

- **What this buys:** Programmatic guarantee that every title in the analytical set has a unique ID, positive budget and revenue, non-null release year, and valid foreign key relationships.
- **What this costs:** Pipeline fails fast upon encountering dirty or malformed records, requiring developer triage before analytical deliverables can be updated.
- **What it costs the client if I am wrong:** If an over-strict rule halts execution during a live meeting due to a minor non-critical field, Adjoa could be blocked from presenting.
- **What would make me revisit this:** Ingesting streaming-original titles or indie acquisitions where production budgets are legitimately unreleased, requiring nullable budget allowances.

## What this survives

Scales seamlessly to 500+ candidate titles as a mandatory CI/CD quality gate before any quarterly analysis refresh.
