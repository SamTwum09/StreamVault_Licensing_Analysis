# ADR-004: Rank Candidates Using Combined Revenue and Multiple Ranks

- **Status:** Accepted
- **Date:** 2026-10-31
- **Decision owner:** Samuel Twum

## Context

Shortlisting titles based on a single financial metric creates severe commercial distortions. Sorting purely by total box office selects mega-budget studio blockbusters with high acquisition costs and mediocre margins.Sorting purely by historical box-office revenue prioritises films with larger theatrical gross, but does not account for production budget or distinguish absolute gross from performance relative to production cost. Production budget is not StreamVault's licensing cost, and theatrical gross does not establish streaming profitability.

## Decision

I rank candidate titles and franchise collections using an equally weighted sum of their Total Revenue Rank and Median Revenue Multiple Rank.

## Alternatives considered

### Alternative A: Rank Exclusively by Total Revenue

- **How it would work:** Sort candidates descending strictly by cumulative global box office gross.
- **Why it is attractive:** Intuitive and easy to explain to studio executives who trade on gross box office figures.
- **Why rejected:** Ignores capital efficiency; pushes high-cost, moderate-return tentpoles into the top slots while discarding capital-efficient titles like *Spirited Away*.

### Alternative B: Rank Exclusively by Revenue Multiple

- **How it would work:** Sort candidates descending strictly by their box-office-to-budget multiple.
- **Why it is attractive:** Maximizes theoretical capital efficiency and return per dollar spent.
- **Why rejected:** Favors niche micro-budget films with minimal absolute reach, deprioritizing major audience drivers like *The Avengers* and *Inception*.

## Consequences

- **What this buys:**A balanced ranking that combines absolute historical box-office scale with historical revenue-to-budget performance, reducing reliance on either metric alone.
- **What this costs:** Omits single-dimension outliers that score exceptionally in one dimension but poorly in the other.
- **What it costs the client if I am wrong:** If StreamVault faces an acute churn crisis where only massive global brands stop cancellations regardless of price, prioritizing multiple-weighted titles could dilute subscriber acquisition impact.
- **What would make me revisit this:** A clear strategic mandate from Kwame to prioritize either sheer subscriber acquisition volume or pure cash preservation.

## What this survives

Survives portfolio expansion to 500+ titles; easily adapts to parameterized weighting (e.g., 60/40) as corporate priorities evolve.
