# ADR-002: Implement Negative Caching and Local File Storage for API Calls

- **Status:** Accepted
- **Date:** 2026-10-31
- **Decision owner:** Samuel Twum

## Context

Adjoa must rerun the licensing pipeline live during executive meetings on her laptop, often facing conference room Wi-Fi latency, packet drops, or strict external API rate limits. Furthermore, the candidate list contains erroneous or non-existent IDs that consistently return HTTP 404 responses. Repeatedly making live network requests on every pipeline run causes unacceptably slow execution and fragile presentations.

## Decision

I implement persistent local disk caching for all successful TMDb API responses and cache non-existent or 404 records as `.notfound` sentinel files.

## Alternatives considered

### Alternative A: Direct Live Network Requests on Every Run

- **How it would work:** Query TMDb's live REST API on every invocation of the pipeline for all 127 candidate IDs.
- **Why it is attractive:** Ensures instantaneous reflection of any upstream TMDb metadata updates.
- **Why rejected:** Highly vulnerable to network failure, hits rate limits, and takes minutes instead of seconds, making live meeting reruns risky and unreliable.

### Alternative B: In-Memory Runtime Caching Only

- **How it would work:** Cache responses in application memory during a single execution session.
- **Why it is attractive:** Avoids creating hundreds of raw JSON files on local disk.
- **Why rejected:** Memory is cleared when the process exits, meaning every rerun from the terminal starts cold and incurs full network overhead.

## Consequences

- **What this buys:** Predictable cached execution, reduced repeat API requests, and the ability to rerun the analysis offline when all required source responses are already cached. Cached execution avoids unnecessary network calls, although uncached requests remain subject to network availability, API rate limits and retries.
- **What this costs:** Consumes local disk storage (~250 files in `data/raw/`) and requires explicit manual cache invalidation if TMDb data needs a fresh sync.
- **What it costs the client if I am wrong:** If a missing ID was caused by a temporary TMDb outage rather than a permanently invalid ID, caching `.notfound` prevents retrying unless manually cleared, potentially omitting a valid candidate title.
- **What would make me revisit this:** A verified list of corrected IDs from the studios requiring complete cache invalidation.

## What this survives

Survives offline presentation environments and scales effortlessly to 500 candidate titles without exceeding TMDb API request quotas.
