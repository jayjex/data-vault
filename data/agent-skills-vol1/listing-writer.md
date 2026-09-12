---
name: listing-writer
description: Write marketplace listing copy for a digital product (title, description, tags, cover alt text) from the artifact folder alone. Use when a build is finished and needs a storefront listing, or when an existing listing gets views but no clicks and needs a rewrite. Keeps counts and formats factual, strips promo filler.
---

# Listing Writer

Goal: one buyer reads the listing in 15 seconds and knows exactly what downloads and what it costs. Sell on specifics, never on adjectives.

## Inputs to collect first

Read from the product folder, do not invent:

- file list from the zip (`unzip -l pack.zip`) with real counts: prompts, rows, tabs, pages, images, formulas
- formats shipped (`.md`, `.csv`, `.xlsx`, `.pdf`, `.png`, `.cube`)
- license terms from `LICENSE.txt`
- data snapshot date if the product contains data ("2026 snapshots", "checked 2026-09-11")
- price in cents from the queue/portfolio row

Anything you cannot read from the folder does not go in the copy.

## Title

Pattern: `<Number/Name> + <what it is> + <format or count> + <one qualifier>`.

- Good: "Cinematic LUT Pack Vol.1: 10 Video LUTs (.cube) + 10 Lightroom Presets (.xmp)"
- Bad: "Ultimate Cinematic Color Grading Collection"

Keep under 100 characters. Put the searchable noun in the first 40.

## Description (900-1200 characters)

Five moves, in this order:

1. Problem line, one sentence, in the buyer's words.
2. What the pack is, with the count and the formats.
3. What is inside, named. List the actual items or categories.
4. Compatibility and limits. Which software reads the file type, what needs converting first, what the pack does not do. Limits build trust and cut refund tickets.
5. Delivery and price line: file count, license scope, price, instant download.

Rules:

- Numbers over nouns. "651 formula cells across 5 tabs" beats "powerful tracking".
- Active voice with a human subject. "Swap in your own coin" not "the variables are populated".
- No promises you cannot verify from the folder (no "pays in 30 days", no "rank #1").
- Say "personal and commercial use, no resale" instead of legal fog.
- One short paragraph per move. No headings, no emoji, no asterisk emphasis.

## Tags

10 to 13 tags, buyer search phrases, not internal labels. Mix broad ("excel crypto tracker") and longtail ("13 week cash flow template"). Give each product a unique tag core so your own listings do not cannibalise each other in site search. Reuse the first three tags in the title where it reads naturally.

## Cover alt text

One sentence: background, layout, subject count, title text shown. This feeds image search and screen readers.

## QA pass before handing off

- character count of description: `wc -c description.txt` target 900-1200
- run the slop-scan skill over title, description, tags, alt text. Zero banned words, zero em dashes, no CTA filler
- every number in the copy traces to a file in the folder
- no username, store URL, email, or API path inside the listing text

## Common misses

- Copy describes the making of the product instead of the buyer's use
- Counts left vague ("dozens of templates")
- Missing limits, so the buyer blames the listing
- Promo links pasted into the description on platforms that flag them
