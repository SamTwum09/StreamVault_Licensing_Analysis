# StreamVault Licensing Analysis – Data Diagnosis

## 1. Purpose

The purpose of this diagnosis is to assess the quality, completeness and reliability of StreamVault's original candidate movie list before using it to support the $14 million licensing decision.

The candidate list was assembled from multiple sources over approximately four years and had not undergone a formal review or reconciliation process.

I inspected the original candidate IDs, retrieved movie and credits data, reconciled the original source rows, transformed the retrieved records and performed automated quality checks.

The diagnosis identifies the problems discovered, how they were detected, their potential effect on the recommendation and the limitations Kwame should understand before making a commercial commitment.

## 2. Candidate List Inspection

The original `id_list.csv` contained 127 source rows.

Inspection identified duplicate values, invalid identifiers and a blank row.

### Candidate list summary

| Finding | Count | Explanation |
|---|---:|---|
| Original source rows | 127 | All rows supplied in the candidate list |
| Blank ID rows | 1 | One row contained no movie ID |
| Non-blank ID values | 126 | Rows containing an ID value |
| Unique non-blank values | 120 | Distinct values before ID validation |
| Duplicate ID groups | 6 | Six IDs appeared more than once |
| Rows involved in duplicates | 12 | Two rows in each duplicate group |
| Unique valid numeric IDs | 117 | Distinct positive numeric IDs suitable for retrieval |

### Duplicate IDs identified

| TMDb ID | Original source rows |
|---|---|
| 155 | 2, 91 |
| 1891 | 55, 90 |
| 278 | 27, 60 |
| 550 | 80, 94 |
| 603 | 40, 43 |
| 680 | 8, 102 |

**How the problem was detected:** I inspected the original ID column and counted repeated values before making API requests.

**Why it matters:** If duplicate entries were treated as separate films, they could inflate candidate counts and distort financial totals, rankings and group comparisons.

**Decision:** I retained the original source rows for reconciliation but retrieved each unique valid ID only once. This preserved the original evidence without counting the same film multiple times.

## 3. Acquisition Reconciliation

I used TMDb to retrieve two records for each unique valid movie ID:

- Movie details: `/movie/{id}`
- Movie credits: `/movie/{id}/credits`

The acquisition process produced the following reconciliation.

### Original source-row outcomes

| Acquisition outcome | Source rows |
|---|---:|
| Successfully retrieved | 118 |
| Not found or partial | 5 |
| Invalid ID | 3 |
| Blank ID | 1 |
| **Total** | **127** |

The 118 successfully retrieved source rows represent 112 distinct films. The additional six successful rows are duplicate occurrences of IDs already retrieved.

### Candidate journey

| Stage | Count |
|---|---:|
| Original source rows | 127 |
| Unique non-blank values | 120 |
| Unique valid numeric IDs attempted | 117 |
| Unique films successfully retrieved | 112 |
| Valid numeric IDs not retrieved | 5 |
| Invalid ID rows | 3 |
| Blank ID rows | 1 |

This means the final analysis uses 112 distinct films, rather than treating all 127 original rows as separate titles.

### Invalid IDs

Three source rows contained values that could not be used as valid positive numeric TMDb IDs.

| Source row | Original value | Diagnosis |
|---|---|---|
| 30 | -1 | Invalid non-positive ID |
| 95 | tt0468569 | IMDb-style identifier rather than a TMDb numeric ID |
| 111 | N/A | Placeholder value, not a valid movie ID |

**How the problem was detected:** I checked the ID values for missing entries, positive numeric format and suitability for the requested TMDb endpoints.

**Decision:** I did not automatically convert or replace these values. Without confirming the intended film, replacing them could introduce incorrect records.

### Unsuccessful API retrievals

Five valid numeric IDs returned HTTP 404 responses from both the movie details and credits endpoints.

| Source row | Movie ID | Movie endpoint | Credits endpoint |
|---|---|---|---|
| 18 | 8471293 | 404 | 404 |
| 35 | 9412887 | 404 | 404 |
| 73 | 8471294 | 404 | 404 |
| 93 | 9412888 | 404 | 404 |
| 99 | 7733901 | 404 | 404 |

**How the problem was detected:** I recorded the HTTP response status for both endpoints during acquisition and included the failed records in the reconciliation output.

A 404 response means the requested resource was not found at that endpoint. It does not independently prove that the film does not exist.

**Decision:** These five records were excluded because the required movie and credits information could not be retrieved. They remain documented in `outputs/reconciliation/acquisition_reconciliation.csv`.

### Acquisition conclusion

The reconciliation accounts for all 127 original source rows.

- 117 unique valid numeric IDs were attempted.
- 112 unique films were fully retrieved.
- Five valid numeric IDs could not be retrieved.
- Three invalid ID rows and one blank row were excluded from analysis.
- Six duplicate groups were controlled so that the same film was not analysed more than once.

The final processed film dataset therefore contains 112 distinct films.

## 4. Processed Data Quality Findings

After acquisition, I transformed the nested movie and credits records into three separate datasets:

- `films.csv` – one row per film.
- `directors.csv` – director-to-film relationships.
- `lead_actors.csv` – lead-actor-to-film relationships.

### Processed dataset counts

| Dataset | Records |
|---|---:|
| Films | 112 |
| Director records | 122 |
| Lead actor records | 336 |

The 122 director records reflect films with multiple credited directors. The 336 actor records represent the top three billed cast members for each retrieved film.

Keeping directors and actors in separate relationship tables avoids multiplying film-level financial figures when analysing talent.

### Automated quality checks

I implemented six automated checks on the processed data.

| Check | Result | Finding |
|---|---|---|
| Unique film IDs | PASS | 112 film rows, no duplicate IDs |
| Required fields populated | PASS | No missing required values |
| Positive budget and revenue | PASS | All 112 films had positive values |
| Director relationships valid | PASS | No duplicate or unmatched relationships |
| Actor relationships valid | PASS | No duplicate or unmatched relationships |
| Release years populated | PASS | All 112 films had release years |

All six checks passed. Results are saved in `outputs/quality_report.csv`.

**How the problems were detected:** The checks tested uniqueness, required-field completeness, positive financial values, relationship validity and release-year completeness.

**Important limitation:** Passing structural checks does not independently establish that TMDb's financial figures are historically accurate. A value can be present and positive but still be incorrect.

## 5. Financial Data and Historical Limitations

All 112 retrieved films had positive budget and revenue values. However, the presence of values does not establish their accuracy or comparability.

### Financial figures are not independently verified

The analysis uses budget and revenue figures supplied by TMDb. I did not obtain independent studio financial statements or box-office records to verify them.

**Detection:** I reviewed the available financial fields and identified that no independent financial source had been supplied or used for validation.

**Potential effect:** Incorrect figures could change film rankings, collection rankings and the comparison between franchise and standalone titles.

### No inflation adjustment

The retrieved films span release years 1966 to 2019. Historical financial values were not adjusted for inflation.

**Detection:** I examined the release-year range and confirmed that no inflation adjustment was applied during analysis.

**Potential effect:** Financial comparisons across different release periods may be misleading because the purchasing power of money changes over time.

### Currency and reporting basis not independently verified

The analysis does not independently establish that all historical financial figures use a consistent currency and accounting basis.

This does not prove that the records use inconsistent currencies. It means consistency has not been independently established.

**Potential effect:** Differences in reporting could affect comparisons, particularly for older films.

### Box-office performance is not licensing performance

The analysis uses historical theatrical revenue and production budget as indicators of commercial performance.

It does not measure:

- Streaming subscriptions or subscriber retention.
- Expected viewing hours or audience demand on StreamVault.
- Licensing fees or contract costs.
- Territory-specific demand.
- Exclusivity, rights availability or contract duration.

**Potential effect:** A film with strong historical box-office performance may not generate a strong return for StreamVault. Using theatrical performance alone to justify a licensing price could lead to an expensive deal with insufficient streaming value.

## 6. Franchise Classification Limitations

I classified a film as a franchise title when TMDb supplied a `belongs_to_collection` value.

This produced:

| Classification | Films |
|---|---:|
| Franchise | 96 |
| Standalone | 16 |
| **Total** | **112** |

**How the problem was detected:** I inspected the collection ID and collection name fields in the processed film data. Sixteen films had no collection entry.

This is a consistent classification rule, but it depends on TMDb's collection metadata. A film without a collection entry may still have commercial franchise potential or belong to a series not represented in that metadata.

**Potential effect:** Some films could be classified as standalone even when they have wider franchise relationships. This could affect the franchise-versus-standalone comparison and the bundle shortlist.

**Decision:** I used the available collection field consistently and documented the limitation rather than manually assigning franchise relationships without supporting evidence.

## 7. Risk Ranking and Effect on the Recommendation

The following risks are ranked according to their potential impact on the $14 million licensing decision.

| Priority | Issue | Why it matters to the decision |
|---|---|---|
| Critical | Box-office performance used as a licensing indicator | Strong historical theatrical performance does not prove streaming demand or justify a licensing price |
| High | Unverified financial figures | Incorrect values could change film and collection rankings |
| High | No inflation adjustment | Comparisons across different release periods may be misleading |
| High | Five unretrieved candidate IDs | Missing films could change the shortlist or group comparisons |
| High | Franchise classification depends on collection metadata | Some franchise titles may be classified as standalone |
| Medium | Currency and reporting basis not independently verified | Historical financial comparisons may not be consistent |
| Medium | Non-random candidate list | Findings may not represent the wider film market |
| Low after correction | Duplicate source IDs | Could distort totals, but duplicates were controlled before analysis |
| Medium | Invalid and blank identifiers | Intended candidates may be omitted until their identities are confirmed |

These are qualitative risk assessments based on potential decision impact, not measured probabilities of loss.

## 8. Effect on the Recommendation

The analysis compared franchise and standalone performance across two time windows.

The franchise group had a higher median revenue-to-budget multiple in both periods.

| Period | Franchise median multiple | Standalone median multiple |
|---|---:|---:|
| All years | 5.62x | 3.84x |
| 2000 onward | 5.05x | 3.84x |

The post-2000 comparison contains 63 franchise films and only eight standalone films.

The direction of the result did not change between the two periods. This supports prioritising franchise bundles while retaining selected standalone titles as complementary opportunities.

However, the result is directional evidence rather than proof of future licensing returns.

The recommendation is limited by:

- Five valid IDs that could not be retrieved.
- Three invalid IDs and one blank source row.
- Unverified financial figures.
- No inflation adjustment.
- Unverified historical currency and reporting consistency.
- Potential franchise classification gaps.
- The small post-2000 standalone sample of eight films.
- The absence of actual licensing prices and streaming-demand evidence.

The evidence supports prioritising franchise negotiations for further evaluation. It does not establish that a particular bundle is worth a particular amount.

## 9. What the Candidate Gap Costs Kwame

The final analysis contains 112 distinct films out of 117 unique valid numeric IDs attempted (and 127 total source rows).

### Breakdown of the 15-Row Gap:
1. **6 Duplicate Rows:** Fully captured and analyzed via their unique IDs; zero data loss, duplicate distortion avoided.
2. **1 Blank Row & 3 Invalid IDs (`-1`, `tt0468569`, `N/A`):** 4 source entries that could not be mapped to TMDb numeric IDs without external verification.
3. **5 Unretrieved Numeric IDs (HTTP 404):** IDs 8471293, 9412887, 8471294, 9412888, 7733901 returned 404 errors on both movie and credits endpoints.

### Quantifying the Cost of the Gap to Kwame:
The 5 unretrieved IDs represent **4.3% of the valid candidate pool (5 / 117)**. 

While the exact titles cannot be determined from TMDb alone, their financial and negotiation cost can be bounded:
* **The "Hidden Bundle Trap" Exposure:** Studios frequently package weaker or unlisted middle entries into franchise bundles ("take all six Space Raider films or none"). If 2 or 3 of these unretrieved IDs belong to studio collections under active consideration (e.g. unlisted sequels or spin-offs), StreamVault could be forced to license them as mandatory tie-ins. At an estimated average licensing cost of $300,000 to $500,000 per catalog title, an unmodeled mandatory title represents an **unexpected capital drain of $600,000 to $1.5M** against Kwame's $14M envelope (4% to 11% of total budget).
* **Opportunity Cost of Omission:** If any of the 5 missing titles is a high-performing standalone title (similar to *Spirited Away* with a 14.5x multiple), StreamVault misses the opportunity to license an efficient audience driver, potentially leaving it to competitors.
* **Negotiation Risk:** Entering a licensing review without accounting for 5 candidate IDs allows studio licensing desks or Finance (Yaw) to challenge the completeness of Kwame's model.

**Mitigation:** Kwame must instruct his acquisition team to demand complete, contractually binding title schedules and IMDb/TMDb identifier confirmation directly from the studio before finalizing the bundle deal.

## 10. What Could Not Be Verified

The following items remain unresolved:

1. Whether the five 404 IDs represent incorrect identifiers or unavailable TMDb records.
2. The intended films behind the three invalid IDs and the blank row.
3. Whether all TMDb budget and revenue figures are accurate.
4. Whether historical financial figures use a consistent currency and reporting basis.
5. Whether historical figures should be adjusted for inflation before comparison.
6. Whether TMDb collection metadata captures every relevant franchise relationship.
7. Whether the candidate list represents the wider licensing market.
8. The actual licensing fees, territories, exclusivity, duration and rights availability for shortlisted titles.
9. The expected subscriber, viewing and revenue contribution of each title or bundle.

Before signing a licensing agreement, StreamVault should verify the missing candidates, validate material financial evidence, obtain studio rights and pricing information, and assess expected streaming value.

## 11. Final Diagnosis

The original candidate list was not ready for direct commercial analysis. It contained duplicate entries, invalid identifiers, a blank row and five valid numeric IDs that could not be retrieved.

I addressed these issues through source-row inspection, unique-ID acquisition, complete reconciliation, structured transformation and automated quality checks.

The resulting dataset contains 112 distinct films and passed all six automated structural quality checks.

The franchise group had a higher median revenue-to-budget multiple in both the all-years and post-2000 comparisons. This provides a consistent directional case for prioritising franchise bundles while retaining selected standalone opportunities.

However, the analysis does not establish the financial value of a licensing agreement or justify spending a particular amount. The recommendation should guide negotiations and further due diligence, not replace commercial rights, pricing and streaming-demand validation.