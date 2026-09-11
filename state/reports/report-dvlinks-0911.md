# DV Link Audit 2026-09-11

Scope: all .html in ~/data-vault (210 files: root, guides/, tools/, printables/, agents/, datasets/). Covers post-catalog-launch state: nav swap, portfolio redirect, agents refresh.

## Method

Local crawl (no HTTP): href extraction, relative + absolute-internal resolution against repo layout, dup id scan, og:url vs path, sitemap URLs vs files. HTTP: 25 GETs of budget 40 (curl, 15s timeout each).

## Results

| Check | Count | Broken |
|---|---|---|
| HTML files crawled | 210 | — |
| Internal relative hrefs | all | 0 |
| Internal absolute (jayjex.github.io/data-vault/) | all | 0 |
| Cross-repo links (jayjex.github.io/matchbook-labs/*) | ~200 hrefs | 0 (spot-check: 1 probe, 200) |
| Sitemap URLs vs files | 217 | 0 |
| Duplicate element ids | — | 0 |
| og:url mismatches | 210 | 0 |
| Getly live check (5 first-card/category + 5 sample) | 10 | 0 (all 200) |
| Fourthwall live check (3 sample + 2 flagship) | 5 | 0 (all 200) |
| Other external sample | 10 | 0 dead / 2 unverified |

## Notes

- ~200 hrefs point to `jayjex.github.io/matchbook-labs/*.html` (free-printables-index.html, printable-index-roundup.html, printables/free-printables-vs-paid.html, guides/hud-income-limits.html, guides/index.html, guides/mcp-server-build-tutorial.html). Targets live in the matchbook-labs repo, not data-vault; local file check can't resolve them. Probe of `matchbook-labs/monthly-budget-planner-printable.html` 200. Live, no action.
- `portfolio.html` not in sitemap: intentional. It is a noindex meta-refresh redirect to /data-vault/catalog.html. Also the only page without og:url, same reason.
- 5 og:url flags were false positives: index pages use directory canonical (`/agents/`, `/datasets/`, `/guides/`, `/printables/`, root) instead of `/index.html`. Correct canonical form.
- MakerWorld link (printables pages) returned 403 to curl (bot protection; page likely fine in browsers). Unverified, not counted broken.
- FRED API docs link returned 000 twice: TLS handshake blocked from this network, not a 404. Unverified, not counted broken. If it dies, it is on guides + tools pages referencing `fred.stlouisfed.org/docs/api/fred/`.
- HUDUSER xlsx downloads returned 202 (accepted/async), served fine.
- catalog.html: 47 Getly product links + 1 store link + 46 Fourthwall fallbacks present. All checked links live, including every category's first card (Data & AI, Spreadsheets, Print kits, Wallpapers, Guides).

## Fixes applied

None needed. No href typos, no dead products found, no sitemap orphans, no dup ids, no stale og:url.

## Budget

25 HTTP GETs (limit 40), $0, wall time ~40s, no sleeps.
