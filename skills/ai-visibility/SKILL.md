# AI Visibility Audit (GEO/AEO)

Can ChatGPT, Claude, Perplexity and Google's AI actually **read** your site and **cite** it? This is the audit BotView (`tools/botview.py`) automates. This skill explains the method so an agent can run it — with the tool, or by hand.

```bash
python3 tools/botview.py audit https://example.com
```

## What gets checked (score /100)

1. **Homepage reachable + basics** — 200 status, `<title>`, meta description, canonical. If a human crawler can't read it, an AI can't either.
2. **Exactly one H1** — heading structure is how models chunk your page into answerable sections.
3. **Structured data (JSON-LD)** — presence and types. Models lean on schema to attribute facts (prices, services, locations) to you instead of to whoever else states them.
4. **Readable-text ratio** — how much of the page weight is real text an LLM can ingest vs. script/markup bloat.
5. **llms.txt present and valid** — and critically: **does it contain real markdown links?** An llms.txt full of bare paths (`/about`) instead of `[About](https://…/about)` gives AI tools nothing clickable to follow. This exact bug shipped on a production directory site and scored a silent fail until audited — see the [llms-txt skill](../llms-txt/SKILL.md).
6. **AI crawlers not blocked** — parse robots.txt for the major agents: `GPTBot`, `ChatGPT-User`, `ClaudeBot`, `Claude-Web`, `PerplexityBot`, `Google-Extended`, `CCBot`, `Bytespider`.
7. **Sitemap present** — with a sane URL count.

## The Cloudflare trap (learned the hard way)

**Always read the LIVE robots.txt top to bottom — never trust the site's source code.**

On usaattorneys.company, the site's own robots config explicitly *allowed* every AI crawler. The live file told a different story: Cloudflare's "managed content" block sat on top of it, with `Disallow: /` for GPTBot, ClaudeBot, ChatGPT-User, Claude-Web, Google-Extended, CCBot and Bytespider. In robots.txt semantics the specific user-agent group wins — so the site was invisible to most AI crawlers while its code said the opposite. The fix was not in the repo; it was a Cloudflare dashboard setting (AI Crawl Control / managed robots).

Symptoms to suspect this trap: audit says crawlers blocked, but the codebase allows them. Cure: fetch the live file, look for a managed-content header, fix it at the CDN layer.

## Reading the score

- **85+** — citable. Remaining work is content and brand mentions, not plumbing.
- **60–84** — fix the specific failed checks; they're usually one-file changes (llms.txt links, a robots rule, missing schema).
- **<60** — the site is effectively invisible to AI search. Fix plumbing before spending anything on content.

Re-audit after every fix and record score + date. Verified reference points (2026-10-24): frinjo.me 90, igaf.me 90, usaattorneys.company 78.
