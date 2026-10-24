# SEO Agent Kit

**Open-source SEO skills + tools for AI agents — built from real production workflows, not theory.**

Most SEO checklists are written by people who sell checklists. This kit is different: every skill here is a workflow that runs in production on real sites — a portfolio site, a government-services guides site, and a 760+ listing US attorney directory. The included tool ([BotView](tools/)) is the same auditor used to prepare client reports for those sites.

No hype. No "guaranteed #1 ranking" nonsense. Just the work, in a form your agent can execute.

## What's inside

### Skills (`skills/`)

Each folder holds a `SKILL.md` — a concrete, step-by-step workflow an AI agent (Claude Code, or any agent that reads markdown instructions) can follow end-to-end.

| Skill | What it does |
|---|---|
| [technical-audit](skills/technical-audit/SKILL.md) | Crawl health: status codes, titles/meta/canonical, sitemap, robots, HTTPS, redirect chains |
| [ai-visibility](skills/ai-visibility/SKILL.md) | GEO/AEO audit — can ChatGPT, Claude and Perplexity actually read and cite your site? |
| [llms-txt](skills/llms-txt/SKILL.md) | Write an `llms.txt` AI tools will actually use — real links, key facts, no bare paths |
| [schema-gaps](skills/schema-gaps/SKILL.md) | Find missing JSON-LD by site type and validate what you ship |
| [local-seo](skills/local-seo/SKILL.md) | Google Business Profile + citation consistency checklist (legal-directory edition included) |
| [content-clusters](skills/content-clusters/SKILL.md) | Validate a topic cluster from your own Search Console data before writing a word |
| [gsc-regex](skills/gsc-regex/SKILL.md) | Filter GSC Performance to buyer-intent queries with one regex |
| [brand-mentions](skills/brand-mentions/SKILL.md) | Build the third-party footprint AI answers are assembled from |

### Tools (`tools/`)

- **[BotView](tools/botview.py)** — zero-dependency Python auditor for AI visibility. Scores any site out of 100: llms.txt presence and link quality, AI-crawler access in robots.txt, structured data, readable-text ratio. Also `view` (see a page the way an LLM reads it) and `generate` (draft an llms.txt from a sitemap).

```bash
python3 tools/botview.py audit https://example.com
```

## Scores from real sites

BotView audits run 2026-10-24 on sites maintained with these workflows:

| Site | AI Visibility Score |
|---|---|
| frinjo.me (portfolio / web-dev studio) | **90/100** |
| igaf.me (Roman-Urdu government guides) | **90/100** |
| usaattorneys.company (US attorney directory) | **78/100** |

The 78 is honest, and the repo tells you why: a Cloudflare managed robots block was overriding the site's own crawler rules (see the [ai-visibility skill](skills/ai-visibility/SKILL.md) — that trap is documented because it cost real time to find).

## Usage

```bash
git clone https://github.com/rootsiemen/seo-agent-kit
```

Point your agent at the skill you need ("follow `skills/technical-audit/SKILL.md` for this domain") or run BotView directly. Skills are plain markdown — no framework lock-in.

## Contributing

Issues and pull requests welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). If you run a skill on a real site and find a step that doesn't survive contact with reality, that's the most valuable issue you can file.

## License

MIT — see [LICENSE](LICENSE). Built by [Muhamad Raza Haider](https://github.com/rootsiemen) ([portfolio](https://rootsiemen.github.io/Portfolio/)).
