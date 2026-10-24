# GSC Buyer-Intent Regex

Your Search Console query list is mostly noise. This filter isolates the queries from people with a wallet out — the ones worth building content for. Used in production on frinjo.me and usaattorneys.company.

## The regex

In Google Search Console → Performance → Search results → click the filter on the **Queries** table → choose **Custom (regex)** → "Matches regex":

```
\b(buy|shop|order|pricing|price|cost|hire|book|schedule|reserve|near me|in stock|available|same day|best|vs|review|reviews|alternative|alternatives|deal|discount)\b
```

(The word boundaries matter — without them, "vs" and "cost" match inside unrelated words and half your list is garbage.)

## How to run it

1. Set the date range to **Last 3 months** — shorter windows hide the pattern on low-traffic sites.
2. Apply the regex on Queries. Screenshot or export both the filtered table AND the unfiltered totals (context matters).
3. Sort by **impressions**. Clicks will be near zero on a young site; impressions are the signal.

## How to read the output

- **Cluster the results by intent theme**, not by literal string. On the attorney directory, 19 filtered queries collapsed into two clusters — business-lawyer cost (~40 impressions) and divorce-lawyer cost (~24) — which became the top two content priorities (see the [content-clusters skill](../content-clusters/SKILL.md)).
- **Hunt near-page-1 stragglers**: a filtered query sitting at position 8–25 is a quick win — one expanded page can move it into click range. (Real examples: "which health insurance is best in pakistan" at 8.0, a comparison query at 10.0, on an otherwise quiet site.)
- **Average position 60+ with steady impressions = latent demand**, not failure. Google is testing you on the topic; build the definitive page.
- Compare filtered vs. unfiltered totals to state the opportunity honestly: e.g. "19 of 114 queries carry buyer intent; they hold 67 of 314 impressions and 0 clicks — that's the gap to close."

## Traps

- Don't judge by clicks on a small site — positions 50–90 generate impressions, not clicks, and the regex view will look empty if you sort by clicks.
- Long-tail cost/price queries are often served by your *guide* pages, not your homepage. Check the Pages tab with the same regex mindset before concluding a page "isn't working."
