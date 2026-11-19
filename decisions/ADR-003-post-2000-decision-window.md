# ADR-003: Adopt 2000-Onward Time Horizon for Core Licensing Decisions

- **Status:** Accepted
- **Date:** 2026-10-31
- **Decision owner:** Samuel Twum

## Context

Finance (Yaw) expressed skepticism regarding historical box office metrics, arguing that pre-2000 box office reporting suffered from unadjusted inflation, exchange rate volatility, and incomplete international box office tracking. We need an analytical framework that addresses Finance's concerns without discarding the entire candidate dataset.

## Decision

I establish films released from 2000 onward as the primary analytical baseline for commercial recommendations while maintaining full-history reporting as an audit benchmark.

## Alternatives considered

### Alternative A: All-Years Unfiltered Window Exclusively

- **How it would work:** Pool all candidate films across all release decades (1970s–2020s) into a single KPI calculation.
- **Why it is attractive:** Maximizes sample size (112 titles vs. 71 titles).
- **Why rejected:** Leaves Kwame vulnerable to Finance rejecting the entire analysis during board review due to unadjusted inflation distortions on older titles.

### Alternative B: Dynamic 10-Year Rolling Window (2014–2024)

- **How it would work:** Filter exclusively for films released in the last 10 years.
- **Why it is attractive:** Reflects modern theatrical and streaming audience habits most closely.
- **Why rejected:** Shrinks the candidate sample too drastically, omitting proven evergreen franchise anchors (such as *The Lord of the Rings* and early *Harry Potter* titles) that drive stable catalog streaming.

## Consequences

- **What this buys:** Directly neutralizes Finance’s skepticism and proves that the franchise advantage remains decisive (+31% multiple advantage in post-2000 vs +46% across all years).
- **What this costs:** Filters out 41 older candidate titles from primary consideration in the final shortlist.
- **What it costs the client if I am wrong:** StreamVault might overlook low-cost back-catalog classics from the 1980s and 1990s that could have been licensed at deep discounts.
- **What would make me revisit this:** If studios present vintage catalog bundles at nominal bulk fees (e.g., under $200k/film), prompting an evaluation of older back-catalog economics.

## What this survives

Survives rigorous corporate finance and board audit, ensuring the commercial acquisition case remains methodologically unassailable.
