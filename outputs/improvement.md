# Improvement beyond the brief: $14M Capital Allocation Framework & Live Meeting Runner

## The problem it solves

The commercial licensing brief requested an evidence-based recommendation on whether to prioritise franchise bundles or standalone titles from a candidate list, but left the actual deployment of the $14.0M capital budget open-ended. In live executive reviews, presenting an unallocated recommendation invites prolonged debate over how much to bid per title, risks last-minute budget raids by competing corporate initiatives, and leaves negotiators without strict walk-away pricing ceilings. 

Furthermore, Adjoa needed the ability to rerun the quantitative pipeline dynamically during quarterly stakeholder meetings on her laptop, which frequently face spotty conference Wi-Fi, API rate limits, or unexpected live inquiries from leadership.

## What I built

1. **A Three-Tier Capital Allocation Framework:** Rather than treating $14.0M as an unallocated spending pool, I built a structured capital deployment model directly into the decision architecture:
   - **Tier 1: Franchise Anchor Commitment ($8.0M / 57%):** Cap *The Avengers Collection* (4 films) at $5.0M–$5.6M (35%–40% ceiling); allocate $3.0M ceiling to *The Lord of the Rings Collection* (3 films).
   - **Tier 2: Tactical Standalone Complements ($3.5M / 25%):** Cherry-pick elite, high-efficiency standalone targets (*Inception*, *Interstellar*, *Spirited Away*).
   - **Tier 3: Strategic Reserve & Rights Buffer ($2.5M / 18%):** Preserved for mandatory studio bundle add-ons, music rights clearances, or unexpected territory restrictions.

2. **Negative-Cached Live Meeting Runner (`run_pipeline.py`):** An automated master orchestrator with local persistent response caching and `.notfound` negative sentinel caching that executes all 7 acquisition, transformation, data validation, and analytical stages in ~16 seconds completely offline.

## What it is worth to Kwame

- **Boardroom Defense:**Provides Kwame with a structured starting point for defending the proposed allocation, linking negotiation priorities to historical performance while keeping the reserve available for rights, pricing and bundle uncertainty. It improves budget discipline, but does not prove that the proposed licensing fees will generate a financial return.
- **Negotiating Discipline:**The proposed ceilings are negotiation controls based on the available budget and prioritisation model. They are not independently calculated valuations of the licensing rights. Final commitments should be made only after confirming the full rights package, asking price, expected streaming demand and contract terms.
- **Live Meeting Agility:** Live Meeting Agility: Gives Adjoa a cached, locally repeatable pipeline that can run without relying on live API access when the required data has already been retrieved. This reduces the risk of network interruptions and rate limits affecting a meeting rerun, but does not remove the risk of incomplete caches or pipeline errors.

## What it cost

- **Development Time:** Approximately 3 hours to design the three-tier allocation math, engineer the negative-caching client, and build the master orchestrator.
- **Local Storage:** ~250 small JSON cache files (~1.2 MB total) in `data/raw/` to support instantaneous offline execution.
- **Risk Trade-off:** Bounding allocations into strict tiers requires discipline to reject studio bundles that exceed tier caps, requiring negotiators to pivot when studios refuse tier ceilings.
