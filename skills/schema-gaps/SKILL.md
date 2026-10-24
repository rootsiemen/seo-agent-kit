# Schema Gap Analysis

Structured data is how you hand search engines and AI models your facts in a form they can attribute to you. This skill: find what's missing by site type, add only what the page can honestly support, validate before you ship.

## Step 1 — Inventory what exists

Fetch the live homepage and key templates (use `curl --http2`, see the [technical-audit skill](../technical-audit/SKILL.md)) and extract JSON-LD blocks:

```bash
curl -s --http2 https://example.com/ | grep -o '"@type": *"[^"]*"' | sort | uniq -c
```

Do the same for a detail page and an article page — schema is usually present on the homepage and missing exactly where it matters.

## Step 2 — Compare against the type table

| Site type | Homepage | Detail/listing page | Article/guide page |
|---|---|---|---|
| Any site | `WebSite` (+ `SearchAction` if site search exists), `Organization` | — | `Article`/`BlogPosting` |
| Local service business | `LocalBusiness` (or subtype) with NAP, hours, geo | `LocalBusiness` per location | `FAQPage` where real FAQs exist |
| Attorney / law firm | `Attorney` (a `LocalBusiness` subtype) with `practiceArea`-style services | Attorney profile: `Person`/`Attorney` + `PostalAddress` | `FAQPage` for cost/process guides |
| Directory / listings | `WebSite` + `ItemList` on index pages | The listing's own type (`Attorney`, `LocalBusiness`, `Product`…) | `Article` + `BreadcrumbList` |
| E-commerce | `Organization` + `WebSite` | `Product` with `offers` (price, currency, availability) | `Article`; `Review`/`AggregateRating` only with real reviews |
| Content/blog | `WebSite` | — | `Article` + `BreadcrumbList`; `FAQPage` if the page has a genuine Q&A section |

**Gap = a cell the page should fill but doesn't.** The most common real-world gaps: directories whose 700+ listing pages carry only a bare `WebSite` block, and FAQ content rendered as plain headings with no `FAQPage` schema behind it.

## Step 3 — Honesty rules

- Never mark up content that isn't visible on the page.
- No `AggregateRating` without real, on-site reviews. No fake prices in `offers`.
- Fee ranges in guides are editorial content, not `Product` offers — don't dress them up as such.

## Step 4 — Validate

- [ ] JSON parses (paste into any JSON validator or `python3 -m json.tool`).
- [ ] Google Rich Results Test on one URL per template.
- [ ] Re-fetch the live page after deploy — confirm the new block is actually served, not just committed.
- [ ] Note the change + date; schema regressions are silent, so the next [ai-visibility audit](../ai-visibility/SKILL.md) should show the new types.
