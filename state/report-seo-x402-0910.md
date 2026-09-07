# Report — SEO x402-data-api guide (2026-09-10)

Deliverable: `guides/x402-data-api.html` — technical explainer for "x402 api" / "pay per call api" / "http 402 payments", dari sudut pelaku nyata (kita jualan API-nya, jadi quote-nya live, bukan dokumentasi orang). $0 spent. Gak sentuh journal/STATUS/Getly API/matchbook-labs.

## Page angle
- Apa itu x402: HTTP 402 yang dulu reserved, x402 v2 isi kontrak machine-readable (challenge → payment → settle, 3 step).
- **Quote VERBATIM dari API live**: curl unpaid `GET /hud/fmr?zip=76437` → HTTP/2 402 + `PAYMENT-REQUIRED` header (base64, awalan 80-char asli) + body JSON verbatim (error string `PAYMENT-SIGNATURE header is required`, resource.url tunnel, tags, accepts[0] lengkap: scheme exact / eip155:8453 / amount "10000" / asset 0x833589fC... / payTo / maxTimeoutSeconds 60 / extra USDC v2). `extensions.bazaar` di-elide dengan penanda eksplisit. Di-replay live hari ini via tunnel `bookstore-buys-sees-journey` (service `x402-rest` active, 200/402 dua-duanya jalan).
- Buyer snippet dari README x402-rest VERBATIM (`@x402/fetch` wrapFetchWithPayment, auto 402 → sign → retry).
- Tabel decode accepts fields (amount 10000 = 0.01 USDC 6-decimals, network = Base mainnet, dst).
- Honest status section: 402 live ✓, header decode ke shape v2 ✓, facilitator verify roundtrip (fake signature → `payment verification failed: invalid_payload`) ✓, settle PENDING FIRST PAYER (tanpa funded wallet) — ditulis apa adanya.
- Caveat tunnel URL rotate saat restart, ditulis.
- Pay-per-call vs subscription: tabel 10/100/1.000/10.000 calls, breakeven ~2.500 calls vs tier 25-dollar; per-call menang untuk spiky/agent/CI, flat tier untuk steady. $ sign CUMA di rate contoh teknis $0.01/call (5 kemunculan, semuanya rate itu); NOL harga produk sendiri, NOL link Getly di page.
- Link internal: nfl-data-apis (2x), public-data-apis-list (byline), open-data-api-alternative, plus backlink dari keduanya (lihat bawah).

## Checklist
- JSON-LD Article + BreadcrumbList + FAQPage(3): json.loads-validated ✓
- FAQ visible == JSON-LD verbatim: script-compare, 3/3 identik ✓
- Sitemap: 122 → **123** url, `<guides/x402-data-api.html>` lastmod 2026-09-10 ✓ (grep-count 123)
- llms.txt: +1 line di Guides (setelah public-data-apis-list line) ✓
- Cross-link 2 arah ✓:
  - x402 page → nfl-data-apis (2x: byline + NFL-route paragraph) dan → public-data-apis-list (byline)
  - nfl-data-apis → x402 (tail paragraf official-API-401 section)
  - public-data-apis-list → x402 (paragraf "Where to go next", setelah csv-vs-api)
- NO PRICE produk sendiri: $0.01/call cuma contoh teknis (diizinkan brief); sisanya "cents/dollars" kata-kata. 0 dollar sign selain rate itu ✓
- No self-AI-reference ✓; banned slop words: 0 hit; em dash: 0 ✓

## Verify
- Page live 200: https://jayjex.github.io/data-vault/guides/x402-data-api.html (cek setelah push, lihat commit hash di git log)
- JSON-LD valid + FAQ mirror + sitemap 123: script-checked pre-commit
- Cross-link target pages untouched selain 1 kalimat backlink masing-masing

## Files
- `guides/x402-data-api.html` (new)
- `guides/nfl-data-apis.html` (+1 sentence backlink)
- `guides/public-data-apis-list.html` (+1 sentence backlink)
- `sitemap.xml` (+1 url, 123 total)
- `llms.txt` (+1 guide line)

$0 terpakai. 0 signup, 0 mutasi fiat/Getly/journal/STATUS/matchbook-labs.
