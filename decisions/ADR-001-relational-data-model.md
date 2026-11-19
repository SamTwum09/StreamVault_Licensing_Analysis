# ADR-001: Normalize TMDb JSON into Three Relational Tables

- **Status:** Accepted
- **Date:** 2026-10-31
- **Decision owner:** Samuel Twum

## Context

The raw TMDb API responses return deeply nested JSON structures containing film metadata alongside hundreds of crew and cast members. If stored as a single denormalized table or analyzed directly as nested structures, titles featuring multiple directors or ensemble casts duplicate box office revenue and budget figures across multiple rows. This would distort portfolio aggregations, inflate talent box office totals, and create severe join anomalies during licensing analysis.

## Decision

I normalize raw TMDb JSON payloads into three discrete tabular entities (`films`, `directors`, and `lead_actors`) linked strictly by `movie_id`.

## Alternatives considered

### Alternative A: Single Denormalized Flat Table

- **How it would work:** Explode all directors and cast members into a single wide tabular dataset where film metrics repeat on every row.
- **Why it is attractive:** Allows querying a single CSV file without performing relational joins in Pandas.
- **Why rejected:** Causes severe Cartesian product inflation; calculating `revenue.sum()` across directors or actors duplicates box office numbers by 3x–6x, corrupting financial evaluations.

### Alternative B: Direct Querying of Raw Nested JSON Objects

- **How it would work:** Retain raw JSON files on disk and traverse nested dictionaries and arrays on the fly during each analytical step.
- **Why it is attractive:** Eliminates an intermediate transformation script and schema definition.
- **Why rejected:** Dramatically slows execution time, prevents vectorized Pandas computations, and exposes analytical routines to structural schema errors.

## Consequences

- **What this buys:** Clean $1:1$ financial cardinality for films, eliminating double-counting of revenues and budgets. Enables fast vectorized grouping and robust referential integrity checking.
- **What this costs:** Requires maintaining an explicit schema transformation script (`src/transform_tmdb.py`) and managing foreign key relationships.
- **What it costs the client if I am wrong:** If duplicate records slip through unnormalized tables, StreamVault would overstate talent box office totals and risk overpaying studios for talent packages by millions of dollars.
- **What would make me revisit this:** If StreamVault migrates to an enterprise graph or document database where native nested document aggregation is managed transparently at the database engine level.

## What this survives

Scales linearly to 500+ titles with zero risk of metric inflation; fully compatible with relational database loaders and standard SQL engines.
