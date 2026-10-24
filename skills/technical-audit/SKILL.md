# Technical Audit

Crawl-health check for any live site. Run this before you touch content — a site with broken basics wastes every article written on it.

## Fetching rule (read this first)

**Use `curl --http2` to fetch pages from Cloudflare/Vercel-fronted hosts.** Plain HTTP/1.1 clients (Python `urllib`, many default libraries) get early-closed connections and 0-byte or truncated bodies from these hosts, which makes healthy pages look like they have no `<title>`, no meta, no canonical. A "site is broken" conclusion drawn from a broken fetch is the most common audit error. BotView (in `tools/`) already fetches via curl for this reason.

```bash
curl -s --http2 -L -o page.html -w "%{http_code} %{url_effective}\n" https://example.com/
```

## Checklist

### 1. Reachability & status codes
- [ ] Homepage returns **200** (not a redirect to a different domain unless intended).
- [ ] Sample every template type: a category/index page, a detail page, a blog post, a utility page (contact/about).
- [ ] No 404s reachable from internal links on sampled pages; no 5xx anywhere.
- [ ] Redirect chains: no URL should need more than **1 redirect** to reach its final page. Log chains (A→B→C) for collapsing.

### 2. On-page basics (per sampled page)
- [ ] Exactly one `<title>`, unique per page, ~50–60 chars, keyword first.
- [ ] Meta description present, unique, ~150 chars, written for humans (it's your CTR copy).
- [ ] Exactly **one `<h1>`**. (Two H1s is the single most common finding on real sites.)
- [ ] Canonical tag present and self-referencing on indexable pages.

### 3. Crawl files
- [ ] `/robots.txt` returns 200 and its rules match intent (cross-check with the [ai-visibility skill](../ai-visibility/SKILL.md) — robots is where AI crawlers get silently blocked).
- [ ] `/sitemap.xml` returns 200, lists only canonical 200 URLs, and its URL count roughly matches the real page count. A sitemap that lags a fresh publish by 15+ minutes is normal on some stacks — verify a new page by fetching its URL directly, not by waiting for the sitemap.
- [ ] Sitemap is referenced in robots.txt and submitted in Google Search Console.

### 4. HTTPS & host consistency
- [ ] HTTP → HTTPS redirect in one hop; www/non-www resolves to exactly one canonical host.
- [ ] No mixed-content warnings on sampled pages (no `http://` asset URLs in the HTML).

### 5. Output

Produce a findings table: **URL · issue · severity (blocker / fix-soon / minor) · exact fix**. Fix blockers before any content work. Re-run the audit after fixes and record the date — an audit without a date goes stale silently.
