#!/usr/bin/env python3
"""Builds the site: src/page.html filled from i18n/<lang>.json, one static page per language
(index.html, az/index.html), plus sitemap.xml and robots.txt.

    python3 build.py

Placeholders: {{key}} is HTML-escaped text; keys ending in ".html" and "cur.*" go in as
they are; {{json:key}} is escaped for a JSON string (the structured data block).
Every language file must have the same keys, and every placeholder must be filled.
"""
import datetime
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://manydesk.github.io"
PAGES = {"en": "index.html", "az": "az/index.html"}

template = (ROOT / "src/page.html").read_text(encoding="utf-8")
langs = {lang: json.loads((ROOT / f"i18n/{lang}.json").read_text(encoding="utf-8")) for lang in PAGES}

keys = {lang: set(d) for lang, d in langs.items()}
base = keys["en"]
for lang, k in keys.items():
    if k != base:
        sys.exit(f"i18n/{lang}.json differs from en.json: missing {sorted(base - k)}, extra {sorted(k - base)}")

used = set(m.group(2) for m in re.finditer(r"\{\{(json:)?([\w.]+)\}\}", template))
unknown = used - base
if unknown:
    sys.exit(f"placeholders with no translation: {sorted(unknown)}")


def fill(d: dict) -> str:
    def one(m: re.Match) -> str:
        key, value = m.group(2), d[m.group(2)]
        if m.group(1):
            return json.dumps(value, ensure_ascii=False)[1:-1]
        if key.endswith(".html") or key.startswith("cur."):
            return value
        return html.escape(value, quote=True)

    return re.sub(r"\{\{(json:)?([\w.]+)\}\}", one, template)


for lang, path in PAGES.items():
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(fill(langs[lang]), encoding="utf-8")
    print(f"wrote {path}")

today = datetime.date.today().isoformat()
alternates = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{langs[l]["url"]}"/>' for l in PAGES)
urls = "".join(
    f"""
  <url>
    <loc>{langs[l]["url"]}</loc>
    <lastmod>{today}</lastmod>{alternates}
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>
  </url>"""
    for l in PAGES
)
(ROOT / "sitemap.xml").write_text(
    f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}
</urlset>
""",
    encoding="utf-8",
)
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
print("wrote sitemap.xml, robots.txt")
