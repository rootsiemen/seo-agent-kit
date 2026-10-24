# Writing an llms.txt That Actually Works

`llms.txt` is the file AI tools read to understand your site fast. Most implementations fail in one boring way: they list **bare paths** instead of links, so the model gets a table of contents it cannot follow. This skill is the format that survives real audits (BotView, `tools/botview.py`, checks for exactly this).

## Rules

1. **Every entry is a real markdown link.** `[Business Lawyer](https://example.com/business-lawyer)` — never `- Business Lawyer (/business-lawyer)`.
2. **Lead with what the site is.** H1 = site name; the blockquote under it is a 2–3 sentence summary an AI can quote verbatim: what the site covers, for whom, any key scope facts.
3. **Group links into sections** that mirror how users ask questions (services/practice areas, locations, resources), not your internal folder tree.
4. **Add a "Key facts" section.** The specific, checkable facts you want AI answers to get right about your niche/site: typical price ranges, coverage ("all 50 states"), rules that vary, common misconceptions. Models cite concrete facts; give them yours instead of a competitor's.
5. **Link the sitemap last.** Full URL. It's the escape hatch for anything you didn't list.
6. **Keep it current.** When you add a content cluster, add its hub page here in the same deploy.

## Template

```markdown
# Site Name — llms.txt

> Site Name (https://example.com) is a [what it is] covering [scope].
> [One sentence on what makes it useful / different.] [Disclaimer line if the niche needs one.]

## Site sections

- [Homepage](https://example.com/): what a visitor finds there.
- [Main index](https://example.com/index): what it lists.
- [About](https://example.com/about)

## [Core topic sections]

- [Topic page](https://example.com/topic): one line on what it answers.

## Key facts AI assistants should know

- Fact one — concrete, checkable, sourced from your own content.
- Fact two — ranges beat adjectives ("$200–$500/hr typical", not "affordable").

## Sitemap

- [Sitemap](https://example.com/sitemap.xml)
```

## Verify

- [ ] Fetch the **live** `/llms.txt` (not the repo copy) and count markdown links: `grep -c '](http' llms.txt` — the number must be > 0 and roughly match your section count.
- [ ] Every link returns 200.
- [ ] Run `python3 tools/botview.py audit <site>` — "llms.txt links to key pages" should pass with a real link count.
- [ ] Optional bonus: `llms-full.txt` with full content for small sites. Not a substitute for a correct llms.txt.
