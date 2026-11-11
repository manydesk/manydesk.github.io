# manydesk.github.io

The ManyDesk website: https://manydesk.github.io (English) and https://manydesk.github.io/az/ (Azerbaijani).

## Editing

The pages are generated; edit the sources, not `index.html` or `az/index.html`:

- `src/page.html` — the page template (`{{key}}` placeholders)
- `i18n/en.json`, `i18n/az.json` — the text of each language (same keys in both)

Then rebuild and commit the output:

```bash
python3 build.py
```

`build.py` checks that both languages have the same keys and that every placeholder is filled, then writes both pages, `sitemap.xml` and `robots.txt`. Download links and the current version come from the latest release of [manydesk/many-desk](https://github.com/manydesk/many-desk) at runtime, so a new release needs no change here.

## SEO and accessibility

- One static page per language with `hreflang`, canonical URLs, Open Graph / Twitter cards (`og-image.png`, 1200×630), `SoftwareApplication` structured data, sitemap and robots.txt.
- WCAG 2.1 AA: skip link, landmarks, one `h1` and an ordered heading outline, labelled navigation and language switch, decorative icons hidden from screen readers, a text description for the diagram, table headers, visible focus, live region for the release version, AA contrast in light and dark mode, reduced-motion support.
