# SEO report — FY2027 HUD FMR guide — 2026-09-10

Page: `guides/hud-fmr-2027.html`
Keyword targets: "hud fmr 2027", "2027 fair market rent"
Angle: timely first-mover — FY2027 release (FY27_FMRs.xlsx posted Aug 26 2026, fy2027_safmrs.xlsx Aug 31 2026, effective Oct 1 2026), year-over-year diff worked from the real CSVs.

## Numbers — all re-computed 2026-09-10 from money-mission/artifacts/products/hud-dataset CSVs (not copied from any report)

- fmr-by-zip-2027.csv: 51,871 rows; fmr-by-county-2027.csv: 3,229 rows; state-summary-2027.csv: 52 rows. All verified.
- Join on (zip, hud_area_code): 51,819 FY27 rows match FY26; 51,800 changed in at least one bedroom size (matches the figure already on hud-fmr-data-downloads.html).
- Median 2BR change across matched pairs: 3.2967% → stated as +3.30% on page (also stated +3.3% in llms.txt line as rounded form — median is 3.30% at 2dp).
- Median 2BR level: 1,150 → 1,190.
- 2BR direction: 36,101 up, 13,885 down, 1,833 flat.
- Max: ZIP 12461, Kingston NY MSA (METRO28740M28740), 2BR 1,620 → 2,760 = +70.37%. Verbatim rows quoted on page. Context: ZIP-specific (12401 +160, 12402 +60), not metro-wide.
- Steepest cuts all exactly -10.00% (30331 Atlanta, 78655 San Antonio, 06824 Bridgeport). Flagged on page as reading like a floor; readers told to verify specific ZIPs against the official workbook.
- ZIP churn: 14 dropped / 14 added vs FY26 — why the diff keys on zip+area_code, not zip alone.
- ZIP 76437 Abilene TX side-by-side, all 5 bedrooms: 850→910, 880→920, 1,090→1,150, 1,420→1,490, 1,710→1,790. Both CSV lines quoted verbatim.
- State medians quoted: NY 1,430→1,500; TX 1,190→1,220; AL 980→1,020; CO 1,620→1,650; AZ 1,610→1,520; CA 2,635→2,600; AK flat 1,510.
- 194 matched areas ≥ +30% 2BR; VT 19, ND 10 top.

## Sources cited on page

- huduser.gov FY27 workbooks (linked; files on disk since 2026-09-08, SHA-256 in data-dictionary-2027.md; huduser serves HTTP 202 to curl/bots, so page byline claims "downloaded 2026-09-08 and SHA-256 verified", not "HTTP 200").
- Zenodo DOI 10.5281/zenodo.22649503 — curl -I checked 2026-09-10: 200.
- NO PRICE: 0 dollar signs on page (script-counted). FY2027 not on Getly yet; CTA is Zenodo (free) + FY2026 dataset page. No self-AI-reference.

## Structure

- JSON-LD: Article + BreadcrumbList + FAQPage(3), json.loads-validated.
- FAQ visible dl == JSON-LD text (script-compared: all 3 Q and A exact match).
- H2s: short answer / what changed / Kingston outlier / ZIP 76437 lookup side-by-side / run the diff (Python snippet, verbatim output `51819 3.3`) / where to get FY2027 / FAQ / get the data.
- MCP status stated honestly: dataset-mcp still serves hud-fmr-2026; FY2027 lands with pack release.

## Cross-links (two-way)

- hud-fmr-data-downloads.html: FY2027 pre-release paragraph tail now links to hud-fmr-2027.html. New page links back in "Run the diff" + "Where to get" sections.
- fmr-dataset-download.html: state-summary merge paragraph tail now links to hud-fmr-2027.html. New page links back in "Run the diff".
- Also links: safmr-vs-fmr.html, fmr-payment-standard.html, datasets/hud-fmr-2026.html, DOI.

## Index changes

- sitemap.xml: 123 → 124 urls, new entry lastmod 2026-09-10 (XML validated).
- llms.txt: +1 guide line in header block, after the metro-definition guide line.

## Verification

- Dollar signs on page: 0. Em dashes: 0. Banned-word scan: clean.
- JSON-LD parse: OK (3 blocks). FAQ mirror: exact.
- Sitemap: 124 urls, minidom valid.
- Live check post-push: https://jayjex.github.io/data-vault/guides/hud-fmr-2027.html → HTTP 200 (pending, below).

## Deploy

Targeted add: guides/hud-fmr-2027.html, guides/hud-fmr-data-downloads.html, guides/fmr-dataset-download.html, sitemap.xml, llms.txt, state/report-seo-fy27-0910.md. pull --rebase --autostash before push.
