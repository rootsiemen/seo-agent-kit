# Contributing

Thanks for helping make this kit better. The bar here is simple: **everything in this repo must come from work that was actually done on a real site.**

## What to contribute

- **Skill fixes** — a step in a `SKILL.md` that is wrong, stale, or fails on a real site. Include the site type and what actually happened.
- **New skills** — a workflow you run repeatedly for SEO work with AI agents. Follow the existing format: short intro, prerequisites, numbered steps, a "traps" section if you have scars.
- **BotView improvements** — bug fixes and new checks. BotView is zero-dependency Python (standard library only); keep it that way.

## How

1. Fork the repo and create a branch.
2. Make the change. For skills, keep them blunt and concrete — steps an agent can execute, not essays.
3. If you changed `tools/botview.py`, run it against at least two live sites and paste the before/after output in your PR.
4. Open a pull request describing what you changed and the real-world case behind it.

## Ground rules

- No invented metrics, case studies, or results. If a number is in this repo, it came from a real run and says when.
- No affiliate links, no tool promotions.
- Be respectful — see the [Code of Conduct](CODE_OF_CONDUCT.md).

Questions? Open an issue.
