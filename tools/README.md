# Tools

## BotView — see your website the way AI sees it

`botview.py` is a zero-dependency Python 3 auditor (standard library only) for **AI visibility**: whether ChatGPT, Claude, Perplexity and other AI tools can read, understand, and cite your site.

### Usage

```bash
# Full audit with a score out of 100
python3 botview.py audit https://example.com

# Machine-readable output
python3 botview.py audit https://example.com --json

# The page as plain text — what an LLM actually reads
python3 botview.py view https://example.com

# Draft an llms.txt from the site's sitemap
python3 botview.py generate https://example.com
```

### What the audit checks

- Homepage reachable (200), `<title>`, meta description, canonical URL
- Exactly one H1
- Structured data (JSON-LD) — presence and types
- Readable-text ratio (real content vs. page weight)
- `llms.txt` present, valid, and **containing real markdown links** (bare paths fail)
- AI crawlers allowed in robots.txt — GPTBot, ChatGPT-User, ClaudeBot, Claude-Web, PerplexityBot, Google-Extended, CCBot, Bytespider
- Sitemap present, with URL count

Fetching uses `curl` (HTTP/2) under the hood: plain HTTP/1.1 clients get early-closed connections from several Cloudflare/Vercel hosts and report healthy pages as broken. See the [ai-visibility skill](../skills/ai-visibility/SKILL.md) for the full method, including the Cloudflare managed-robots trap this tool was built to catch.

### Reference scores (2026-10-24)

| Site | Score |
|---|---|
| frinjo.me | 90/100 |
| igaf.me | 90/100 |
| usaattorneys.company | 78/100 |

MIT licensed — see [../LICENSE](../LICENSE).
