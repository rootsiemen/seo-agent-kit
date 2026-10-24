#!/usr/bin/env python3
"""
BotView — see your website the way AI sees it.

Audits any website for AI visibility: llms.txt, AI-crawler rules in
robots.txt, structured data, and the basics an LLM needs to understand
and cite your site. Zero dependencies — Python standard library only.

Usage:
    python3 botview.py audit    https://example.com   # score + report
    python3 botview.py view     https://example.com   # the page as plain text (what an LLM reads)
    python3 botview.py generate https://example.com   # build an llms.txt from the sitemap
    python3 botview.py audit    https://example.com --json
"""

import json
import re
import ssl
import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

VERSION = "0.1.0"
UA = "BotView/0.1 (+https://github.com/rootsiemen/botview)"

AI_BOTS = ["GPTBot", "ChatGPT-User", "ClaudeBot", "Claude-Web",
           "PerplexityBot", "Google-Extended", "CCBot", "Bytespider"]


def _fetch_curl(url, timeout):
    """Fetcher via the curl binary (HTTP/2, proxy-friendly).

    Primary path: urllib is HTTP/1.1-only and several hosts (Vercel /
    Cloudflare) close the connection early for it, returning 0 bytes —
    which used to make healthy pages look like they had no title/H1.
    """
    import subprocess
    try:
        out = subprocess.run(
            ["curl", "-s", "-L", "--http2", "--max-time", str(timeout),
             "-A", UA, "-w", "\n%{http_code}", url],
            capture_output=True, timeout=timeout + 5)
        body, _, code = out.stdout.decode("utf-8", "replace").rpartition("\n")
        return int(code) if code.isdigit() else None, body
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def fetch(url, timeout=30):
    """Return (status, text) or (None, error)."""
    status, body = _fetch_curl(url, timeout)
    if status is not None and body:
        return status, body
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            raw = r.read(2_000_000)
            return r.status, raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:  # noqa: BLE001
        return status, body


class PageParser(HTMLParser):
    """Extracts what an LLM crawler cares about from a page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta_desc = ""
        self.canonical = ""
        self.h1 = []
        self.schema_types = []
        self.text_parts = []
        self._in_title = False
        self._in_h1 = False
        self._skip = 0
        self._in_ldjson = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
        elif tag in ("script", "style", "noscript"):
            self._skip += 1
            if a.get("type") == "application/ld+json":
                self._in_ldjson = True
        elif tag == "meta" and a.get("name", "").lower() == "description":
            self.meta_desc = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag in ("script", "style", "noscript"):
            self._skip = max(0, self._skip - 1)
            if tag == "script":
                self._in_ldjson = False

    def handle_data(self, data):
        if self._in_ldjson:
            for m in re.findall(r'"@type"\s*:\s*"([^"]+)"', data):
                self.schema_types.append(m)
        if self._skip:
            return
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self.title += text
        elif self._in_h1:
            self.h1.append(text)
        else:
            self.text_parts.append(text)


def parse_robots(text):
    """Return {bot: 'allowed'|'blocked'|'not mentioned'} for AI bots."""
    rules = {}
    current = []
    if not text:
        return {b: "unknown (no robots.txt)" for b in AI_BOTS}
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line or ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        if k.lower() == "user-agent":
            current.append(v)
        elif k.lower() == "disallow":
            for agent in current:
                if v == "/":
                    rules[agent.lower()] = "blocked"
    out = {}
    for bot in AI_BOTS:
        out[bot] = rules.get(bot.lower(), "allowed (not blocked)")
    return out


def audit(base):
    base = base.rstrip("/")
    if not base.startswith("http"):
        base = "https://" + base
    checks = []  # (name, ok, detail, points, max_points)

    def add(name, ok, detail, pts, maxp=None):
        if maxp is None:
            maxp = pts
        checks.append({"check": name, "ok": bool(ok), "detail": detail,
                       "points": pts if ok else 0, "max": maxp})

    status, html = fetch(base + "/")
    if status is None:
        return {"site": base, "error": f"could not fetch homepage: {html}"}
    p = PageParser()
    p.feed(html)
    visible_text = " ".join(p.text_parts)
    text_ratio = len(visible_text) / max(len(html), 1)

    add("Homepage reachable (200)", status == 200, f"HTTP {status}", 8)
    add("Title tag", bool(p.title), p.title[:70] or "missing", 8)
    add("Meta description", bool(p.meta_desc),
        (p.meta_desc[:70] + "…") if p.meta_desc else "missing", 8)
    add("Canonical URL", bool(p.canonical), p.canonical or "missing", 6)
    add("Exactly one H1", len(p.h1) == 1,
        f"{len(p.h1)} H1 found" + (f": {p.h1[0][:50]}" if p.h1 else ""), 6)
    add("Structured data (JSON-LD)", bool(p.schema_types),
        ", ".join(sorted(set(p.schema_types))) or "none found", 10)
    add("Readable text content", text_ratio > 0.05,
        f"text is {text_ratio:.0%} of page weight "
        f"({len(visible_text)} chars an LLM can read)", 8)

    # llms.txt — the new standard file for AI crawlers
    s_llms, llms = fetch(base + "/llms.txt")
    llms_ok = s_llms == 200 and llms.lstrip().startswith("#")
    add("llms.txt present & valid", llms_ok,
        "found" if s_llms == 200 else f"HTTP {s_llms}",
        16)
    if llms_ok:
        links = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", llms)
        add("llms.txt links to key pages", len(links) >= 3,
            f"{len(links)} links listed", 6)
    else:
        add("llms.txt links to key pages", False, "no llms.txt", 0, 6)
    s_full, _ = fetch(base + "/llms-full.txt")
    add("llms-full.txt (bonus)", s_full == 200,
        "found" if s_full == 200 else "not present (optional)", 4)

    # robots.txt — are AI crawlers let in?
    _, robots = fetch(base + "/robots.txt")
    bot_rules = parse_robots(robots)
    blocked = [b for b, v in bot_rules.items() if v == "blocked"]
    add("AI crawlers not blocked", not blocked,
        ("blocked: " + ", ".join(blocked)) if blocked
        else "GPTBot, ClaudeBot, PerplexityBot… all allowed", 12)

    # sitemap
    s_sm, sm = fetch(base + "/sitemap.xml")
    n_urls = len(re.findall(r"<loc>", sm)) if s_sm == 200 else 0
    add("Sitemap present", s_sm == 200 and n_urls > 0,
        f"{n_urls} URLs" if n_urls else "missing/empty", 8)

    score = sum(c["points"] for c in checks)
    max_score = sum(c["max"] for c in checks)
    return {"site": base, "score": score, "max": max_score,
            "title": p.title, "schema": sorted(set(p.schema_types)),
            "ai_bots": bot_rules, "checks": checks}


def print_report(r):
    if "error" in r:
        print(f"✗ {r['site']}: {r['error']}")
        return
    print(f"\n🔍 BotView audit — {r['site']}")
    print(f"   AI Visibility Score: {r['score']}/{r['max']}\n")
    for c in r["checks"]:
        mark = "✓" if c["ok"] else "✗"
        print(f"  {mark} {c['check']:<34} {c['detail']}")
    print("\n  AI crawlers:")
    for bot, v in r["ai_bots"].items():
        print(f"    {bot:<18} {v}")
    print()


def view(base):
    if not base.startswith("http"):
        base = "https://" + base
    status, html = fetch(base)
    if status is None:
        print(f"could not fetch: {html}")
        return
    p = PageParser()
    p.feed(html)
    print(f"# {p.title}\n")
    print("\n".join(x for x in p.text_parts if len(x) > 1)[:6000])
    print(f"\n--- {len(' '.join(p.text_parts))} chars of readable text "
          f"(this is all an AI model gets from this page)")


def generate(base):
    """Build an llms.txt draft from the site's sitemap."""
    if not base.startswith("http"):
        base = "https://" + base
    base = base.rstrip("/")
    _, sm = fetch(base + "/sitemap.xml")
    urls = re.findall(r"<loc>([^<]+)</loc>", sm)[:60]
    if not urls:
        print("No sitemap found — cannot generate. Add a sitemap first.")
        return
    _, home = fetch(base + "/")
    p = PageParser()
    p.feed(home)
    out = [f"# {p.title or urlparse(base).netloc}", ""]
    if p.meta_desc:
        out += [f"> {p.meta_desc}", ""]
    out += ["## Pages", ""]
    for u in urls:
        out.append(f"- [{u}]({u})")
    print("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("audit", "view", "generate"):
        print(__doc__)
        sys.exit(1)
    cmd, target = sys.argv[1], sys.argv[2]
    if cmd == "audit":
        r = audit(target)
        if "--json" in sys.argv:
            print(json.dumps(r, indent=2))
        else:
            print_report(r)
    elif cmd == "view":
        view(target)
    else:
        generate(target)
