#!/usr/bin/env python3
"""Regenerate data-vault/products.html from state/portfolio.json.

Include rule (public SKUs only): status LIVE-FOURTHWALL, or LIVE-GETLY whose
Getly upload is not pending_review. A Getly-pending row with a live Fourthwall
offer still ships, linked via Fourthwall. Pending Getly uploads without any
live channel, Gumroad drafts, queued and discarded rows stay off the page; the
hero lead states those counts honestly instead.

Rerun after every product push or portfolio status flip (see runbook):

    python3 data-vault/tools/gen-products.py

Per-product copy (description, format chip, item count, optional SellApp alt)
lives in COPY below; the group layout lives in GROUPS. A live product missing
from either table aborts the run: add its entry first, then rerun. Text for
new products condenses the existing listing copy (README.md / description.txt)
with every number verbatim.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / 'state' / 'portfolio.json'
OUT = SITE / 'products.html'

GROUPS = [
    ('Datasets', [
        'airbnb-dataset',
        'airbnb-pack-vol2',
        'hud-dataset',
        'earn-dataset',
        'nfl-dataset',
        'amenities-pack',
        'housing-pack',
        'jobsdb',
        'grants-pack',
        'l2-directory',
        'events-cal',
        'idea-pack',
    ]),
    ('Prompt Packs', [
        'prompt-pack',
        'prompts-etsy',
        'agent-prompt-pack-vol1',
    ]),
    ('Wallpapers & Icons', [
        'wallpaper-v1',
        'wallpack-v2',
        'wallpack-v3',
        'wallpaper-pack-v1',
        'wallpaper-vol4',
        'icon-pack',
        'icon-pack-60svg',
        'logo-pack',
        'solana-social-banner-pack',
    ]),
    ('Bundles', [
        'dv-mega-bundle',
        'studio-vault-bundle',
    ]),
    ('Spreadsheets & Business', [
        'bookkeep',
        'freelance-hub',
        'invoice-gen',
        'meal-planner',
        'wedding-planner',
        'habit-tracker',
        'airdrop-tracker',
        'content-cal',
        'sheets-pack',
        'hr-kit',
        'budget-tracker',
    ]),
    ('Notion & Obsidian', [
        'notion-os',
        'notion-os-lite',
        'novel-template',
        'student-dash',
        'obsidian-vault',
    ]),
    ('Planners & Printables', [
        'adhd-planner',
        'cleaning-pack',
        'cleanops-pack',
        'debtpack',
        'discipline-pack',
        'discipline-starter',
        'dogplanner',
        'emergency-binder',
        'expat-planner',
        'focus-planner',
        'football-draft-kit',
        'garden-planner',
        'halloween-bundle',
        'homebinder',
        'homeops',
        'homestead-journal',
        'ny2027',
        'pet-sitter',
        'planner-2026',
        'prayer-pack',
        'puzzle-book',
        'puzzle-vol30',
        'reagent-tracker',
        'recipe-binder',
        'renter-kit',
        'seniorbinder',
        'shiftplanner',
        'strhost',
        'thanks-pack',
        'vendor-pack',
        'worksheet-pack',
        'xmas-planner',
        'desk-kit',
    ]),
    ('Books & Workbooks', [
        'dosage-workbook',
        'lmsw-exam',
        'frontend-book',
    ]),
    ('Design & Social', [
        'sticker-pack',
        'stickers-v2',
        'social-pack',
        'deck-pack',
    ]),
    ('Dev Tools & Templates', [
        'scraper-pack',
        'solana-agent-kit',
        'audit-checklist',
        'deck-system',
        'readme-templates',
        'agentos-pack',
    ]),
    ('Free Samples', [
        'lead-earn-sample',
        'lead-walls-sample',
    ]),
]

COPY = {
    'airbnb-dataset': dict(niche='CSV · 6 cities', num='90,169', label='rows', desc='90,169 Airbnb listings across Austin, Nashville, Denver, New York, Las Vegas and San Diego in clean 12-column CSVs, host data stripped, dictionary and cross-city summary included.', alt=None),
    'airbnb-pack-vol2': dict(niche='CSV · 8 cities', num='90,746', label='rows', desc='90,746 Airbnb listings across Boston, Chicago, Los Angeles, New Orleans, Portland, San Francisco, Seattle and Washington DC in June 2026 snapshots, one 15-column master CSV plus the 8 per-city files, same 12-column schema as volume 1, host fields dropped at the source.', alt=None),
    'hud-dataset': dict(niche='CSV · ZIP + county', num='103,766', label='rows', desc="HUD's official FY2026 and FY2027 Fair Market Rents parsed into clean CSVs: 51,895 ZIP-level rows for FY2026, counties and states, five bedroom sizes in every file.", alt=None),
    'earn-dataset': dict(niche='JSON + TXT · 186+ endpoints', num='28', label='listings', desc='28 open Superteam Earn listings with full description HTML plus 186+ reverse-engineered API routes, harvested from the live superteam.fun API in September 2026.', alt=None, cite_title='Superteam Earn Dataset: 1,757 Completed Solana Bounties, 28 Live Listings with Full Descriptions, and 186 Reverse-Engineered API Routes'),
    'nfl-dataset': dict(niche='CSV · 1999-2026', num='7,548', label='games', desc='Every NFL game from the 1999 season through the full 2026 schedule: 7,548 rows with closing spreads, totals, moneylines, scores and game conditions in normalized CSV columns.', alt=None, cite_title='NFL Modern-Era Betting and Game Data 1999-2026: Scores, Spreads, Totals, Moneylines'),
    'amenities-pack': dict(niche='CSV · 8 tables', num='25', label='cities', desc='Amenity counts for 25 cities across 6 continents, counted from OpenStreetMap, shipped as one 84-row master table plus the 8 regional source tables.', alt=None),
    'housing-pack': dict(niche='CSV · 14 tables', num='68,209', label='rows', desc='Fair market rents for 51,871 ZIP codes and 3,229 counties paired with Eurostat unemployment and house-price tables: 68,209 rows across 14 tables, one frozen 2026-09-10 snapshot.', alt=None, cite_title='US Housing Affordability Pack: HUD Fair Market Rents by ZIP, County and Metro plus Eurostat Unemployment and Price Indices, 68,209 Rows'),
    'jobsdb': dict(niche='CSV + MD · multi-chain', num='147', label='companies', desc='147 web3 and crypto companies with live remote-hiring signals, remote policy and careers URLs, every source checked on 2026-09-05.', alt=None),
    'grants-pack': dict(niche='CSV + MD · multi-chain', num='38', label='sources', desc='38 non-dilutive funding sources for founders and developers, every apply URL fetched live (HTTP 200 or valid redirect) on the data date.', alt=None),
    'l2-directory': dict(niche='CSV + MD · 8 chains', num='136', label='projects', desc='136 active projects across Base, Arbitrum, Optimism, zkSync Era, Linea, Scroll, Polygon zkEVM and Starknet, every URL live-checked on 2026-09-05.', alt=None),
    'events-cal': dict(niche='CSV + MD · Sep 2026 - Q1 2027', num='45', label='events + 2 bonus', desc='Curated calendar of 45 web3 hackathons, conferences and popup cities from September 2026 through Q1 2027, plus 2 bonus mid-2027 entries, with prize pools and registration links.', alt=None),
    'idea-pack': dict(niche='CSV + MD · top 20 expanded', num='100', label='ideas', desc='100 niche SaaS ideas in a spreadsheet: problem, MVP scope, price, difficulty 1-5, crowding 1-5, first-customer channel. The top 20 get a page each.', alt=None),
    'prompt-pack': dict(niche='MD + CSV · multi-chain', num='500', label='prompts', desc='500 field-tested prompts for ChatGPT, Claude, Gemini and local models, built for daily crypto work: trading, DeFi, project teams, community and development.', alt=None),
    'prompts-etsy': dict(niche='CSV + MD · 10 categories', num='500', label='prompts', desc='500 prompts for Etsy and e-commerce sellers across 10 categories of 50: listings, photos, SEO, marketing, service, pricing and seasonal campaigns.', alt=None),
    'agent-prompt-pack-vol1': dict(niche='MD + CSV · 6 sections', num='23', label='prompts', desc='23 AI prompts that already ran in production: the image prompts behind shipped covers, icon, logo and wallpaper packs, plus curated crypto and e-commerce analysis prompts.', alt=None),
    'wallpaper-v1': dict(niche='JPG · 1024x1024', num='20', label='walls', desc='20 moody dark wallpapers with a terminal and cyber aesthetic, shipped as 1024x1024 JPG with a README that walks through the 4K upscale workflow.', alt=None),
    'wallpack-v2': dict(niche='PNG · 3840x2160', num='20', label='walls', desc='Twenty new 4K dark wallpapers in retro-futurist grids and neon horizons, the same terminal mood as Vol.1 with a different theme.', alt=None),
    'wallpack-v3': dict(niche='PNG · 3840x2160', num='20', label='walls', desc='Twenty new 4K dark wallpapers in four themes: bioluminescent, nebula, brutalist and CRT.', alt=None),
    'wallpaper-pack-v1': dict(niche='JPG · 2560x1440', num='12', label='walls', desc='Twelve dark desktop wallpapers picked by hand from the 40 walls across the Vol.1 and Vol.2 packs, shipped at 2560x1440.', alt=None),
    'icon-pack': dict(niche='PNG · 1024x1024', num='50', label='icons', desc='50 flat minimal line icons in single colors for crypto, DeFi and dev tools, one stroke weight across the set, five groups of ten.', alt=None),
    'icon-pack-60svg': dict(niche='SVG · 24px grid', num='60', label='icons', desc='60 stroke-based SVG icons on a 24px grid: 1.5px stroke, round caps and joins, six folders, every file under 2 KB.', alt=None),
    'logo-pack': dict(niche='PNG · 1024x1024', num='40', label='logos', desc='40 ready-to-use Web3 logos in three styles (flat minimal marks, gradient app-icon badges, neon cyber) covering DeFi, NFT projects, wallets, exchanges, L2 networks and DAOs.', alt=None),
    'solana-social-banner-pack': dict(niche='JPG · 1536x1024', num='40', label='banners', desc="40 dark header images built on Solana's green and purple, 1536x1024 JPG in four style groups, with crop coordinates for X, LinkedIn, YouTube and Discord.", alt=None),
    'dv-mega-bundle': dict(niche='ZIP · SHA256 + licenses', num='5', label='packs', desc='Five complete packs in one download: 25-city amenity counts, 23 production prompts, 51,871-ZIP housing data, 12 hand-picked wallpapers and 60 line icons. $45 of packs for $29.', alt=('also on SellApp →', 'https://datavaultdesk.sell.app/product/data-vault-desk-mega-bundle')),
    'studio-vault-bundle': dict(niche='ZIP · checksums included', num='5', label='packs', desc='Four data packs and a wallpaper pack in one download: 7,548 NFL games, 51,895-ZIP rent benchmarks, 90,169 Airbnb listings and 20 dark terminal wallpapers. $104 of packs, $49 here.', alt=('also on SellApp →', 'https://datavaultdesk.sell.app/product/studio-data-vault-bundle-nfl-hud-airbnb')),
    'bookkeep': dict(niche='CSV/XLSX · no macros', num='4', label='linked sheets', desc='Formula-driven bookkeeping for Google Sheets and Excel: log transactions once, get monthly cash flow, category totals, invoice aging and quarterly tax estimates.', alt=None),
    'freelance-hub': dict(niche='XLSX + CSV · Excel + Sheets', num='6', label='tabs', desc='Six-tab tracker for freelancers: clients, invoices, income, expenses and pipeline in one workbook for Excel and Google Sheets.', alt=None),
    'invoice-gen': dict(niche='XLSX/CSV · Excel + Sheets', num='1', label='workbook', desc='Per-invoice generator for solo workers: fill one invoice, get a clean total due, log it, and see what is still owed at a glance.', alt=None),
    'meal-planner': dict(niche='XLSX/CSV · Excel + Sheets', num='32', label='recipes', desc='One-workbook meal planner: 21 meals a week from a 32-recipe bank via dropdowns, with a grocery list that totals what the plan actually needs.', alt=None),
    'wedding-planner': dict(niche='XLSX · Excel + Sheets', num='5', label='sheets', desc='Five-sheet wedding planner: allocated-vs-actual budget, vendor tracker with deposits owed, 12-month countdown checklist, RSVP guest list and seating.', alt=None),
    'habit-tracker': dict(niche='XLSX/CSV · live formulas', num='12', label='habits × 90 days', desc='90-day habit tracker for Google Sheets and Excel: 12 habits, 90 day columns, live streak formulas and a weekly review sheet, no add-ons or scripts.', alt=None),
    'airdrop-tracker': dict(niche='CSV + PDF · tracker + playbook', num='230', label='rows', desc='Airdrop farming system: a 230-row import-ready tracker plus a short playbook that caps the routine at 15 minutes a day.', alt=None),
    'content-cal': dict(niche='XLSX/CSV · multi-platform', num='12', label='monthly tabs', desc='Content calendar for Google Sheets and Excel: one tab per month, one row per post, dropdowns for platform and status across all of 2026.', alt=None),
    'sheets-pack': dict(niche='CSV/XLSX · formulas live', num='5', label='templates', desc='Five crypto KPI templates (portfolio, airdrops, DeFi yield, bounty income, trading journal) that import into Sheets or Excel as live formulas.', alt=None),
    'hr-kit': dict(niche='MD + PDF · A4 + Letter', num='6', label='templates', desc='Six paper-ready HR templates for a small business: a 12-section handbook skeleton, 45-step onboarding, personnel record, interview scorecard, offboarding checklist and incident log.', alt=None),
    'notion-os': dict(niche='Notion bundle · CSV + MD import', num='5', label='databases', desc='One Notion workspace for a multi-chain build: projects, bounties and grants, content and learning as five linked databases, importable on the free plan in about 10 minutes.', alt=None),
    'notion-os-lite': dict(niche='Notion bundle · CSV + MD import', num='5', label='databases', desc='Five connected Notion databases that run one life dashboard: habits with weekly targets, meals that feed a shopping list, monthly budget and quarterly goals. Setup takes 30 minutes.', alt=None),
    'novel-template': dict(niche='Notion bundle · CSV + MD import', num='5', label='databases', desc='A complete Notion workspace for writing one novel: manuscript tracker with word targets, plot scene board, character sheets, worldbuilding wiki, deadline calendar and research log.', alt=None),
    'student-dash': dict(niche='Notion bundle · CSV + MD import', num='4', label='databases', desc='One Notion workspace per semester: assignments, courses, exams and reading notes in four linked databases, plus a what-to-do-today dashboard and a GPA tracker.', alt=None),
    'obsidian-vault': dict(niche='Markdown ZIP · Obsidian', num='5', label='templates', desc='Plain markdown vault for Obsidian: numbered PARA folders, a dashboard home note, five real templates and worked examples. Open the folder and start in 30 minutes.', alt=None),
    'adhd-planner': dict(niche='PDF · A4 + Letter', num='20', label='pages ×2 sizes', desc='A print-and-write planner with few fields and big boxes: one must-do per day, a body-double timer box, a pre-written dopamine menu, and no streaks to break.', alt=None),
    'cleaning-pack': dict(niche='PDF · A4 + Letter', num='7', label='pages', desc='A paper cleaning system for a house or apartment: plan the week, rotate the deep cleans, check off a 30-task routine.', alt=None),
    'cleanops-pack': dict(niche='PDF · A4 + Letter', num='24', label='pages', desc='Printable operations pack for small cleaning businesses: a 30-client list, weekly job scheduler, three per-job checklists and an invoice tracker.', alt=None),
    'debtpack': dict(niche='PDF · A4 + Letter', num='24', label='pages', desc='Debt payoff on paper: list every debt, pick the snowball order, budget the month, fill the cash envelopes, color the progress bars.', alt=None),
    'discipline-pack': dict(niche='PDF · A4 + Letter', num='26', label='pages', desc='A blank-by-design companion for one round of a 90-day discipline challenge: you write the three rules, the pack keeps the count.', alt=None),
    'discipline-starter': dict(niche='PDF · A4 + Letter', num='14', label='pages', desc='The 30-day version of the discipline challenge: the same blank-by-design pages, one month of counting.', alt=None),
    'dogplanner': dict(niche='PDF · A4 + Letter', num='32', label='pages', desc='An 8-week puppy training and care tracker: the schedule, the potty log and every record a first-time puppy household needs, in one binder.', alt=None),
    'emergency-binder': dict(niche='PDF · A4 + Letter', num='20', label='pages', desc="Where the papers are, who to call, what to do: one household's emergency record across 20 printable pages.", alt=None),
    'expat-planner': dict(niche='PDF · A4 + Letter', num='26', label='pages', desc='A relocation planner that runs the move on paper: twelve-month countdown, every document, each application, the budget, the apartment hunt and the boxes.', alt=None),
    'focus-planner': dict(niche='PDF · A4 + Letter', num='30', label='pages', desc='A print-and-write planner for developers, freelancers and indie makers: print a page, work the page, bin it or keep it.', alt=None),
    'football-draft-kit': dict(niche='PDF · A4 + Letter', num='9', label='pages', desc='Draft-day printables for fantasy football: a blank draft board, cheat sheets and auction tracker that work with any league size or scoring system.', alt=None),
    'garden-planner': dict(niche='PDF · A4 + Letter', num='32', label='pages', desc='A planting-to-harvest record for one growing season: sketch the beds, log every sowing, fill the watering circle twice a day, tally the harvest.', alt=None),
    'homebinder': dict(niche='PDF · A4 + Letter', num='30', label='pages', desc='A printable binder for a move and the first months after it: the countdown, the costs, the setup and the upkeep.', alt=None),
    'homeops': dict(niche='PDF · A4 + Letter', num='24', label='pages', desc='A 24-page paper system for running one quarter of home life, built around a Q4 reset.', alt=None),
    'homestead-journal': dict(niche='PDF · A4 + Letter', num='40', label='pages', desc='A full-year homestead journal: the garden, the pantry and the budget in one printable binder.', alt=None),
    'ny2027': dict(niche='PDF · A4 + Letter', num='21', label='pages', desc='A printable reset for the turn of the year: close out 2026, pick one word for 2027, set goals across eight life areas, build three habits on 66-day trackers.', alt=None),
    'pet-sitter': dict(niche='PDF · A4 + Letter', num='18', label='pages', desc='A printable client book for a one-person pet sitting and dog walking business: pet profiles, walk logs and payments.', alt=None),
    'planner-2026': dict(niche='PDF · A4 + Letter', num='23', label='pages', desc='A dated planner for the rest of 2026: print the weeks you need at your paper size and write on paper.', alt=None),
    'prayer-pack': dict(niche='PDF · A4 + Letter', num='36', label='pages', desc='A printable prayer journal: requests in, answers logged, verses written out, plus study worksheets and trackers.', alt=None),
    'puzzle-book': dict(niche='PDF · A4 + Letter', num='65', label='pages', desc='Sixty detective logic puzzles from the Grayharbor Detective Agency night desk, five kinds of detective work, full answer keys at the back.', alt=None),
    'puzzle-vol30': dict(niche='PDF · A4 + Letter', num='35', label='pages', desc='Thirty quick cases from the same Grayharbor desk: five puzzle types, answer keys included, one sitting each.', alt=None),
    'reagent-tracker': dict(niche='PDF · A4 + Letter', num='24', label='pages', desc='A 24-page paper pipeline for real estate agents: 60-lead prospecting tracker, follow-up log, two pipeline boards and buyer/seller checklists.', alt=None),
    'recipe-binder': dict(niche='PDF · A4 + Letter', num='48', label='cards · 41 pages', desc="A write-in cookbook for one family's kitchen: 48 blank recipe cards plus index pages, ready for a binder.", alt=None),
    'renter-kit': dict(niche='PDF · A4 + Letter', num='16', label='pages', desc='A 16-page paper system for one tenancy: move-in and move-out inspections, a deposit tracker and the letter templates for getting the deposit back.', alt=None),
    'seniorbinder': dict(niche='PDF · A4 + Letter', num='28', label='pages', desc='A printable binder for a family caring for a parent: the medical side, the paperwork, the household money and the family stories.', alt=None),
    'shiftplanner': dict(niche='PDF · A4 + Letter', num='18', label='pages', desc='An 18-page weekly planner for people whose weeks run on shifts, not Monday to Friday.', alt=None),
    'strhost': dict(niche='PDF · A4 + Letter', num='22', label='pages', desc='A 22-page printable paper system for running one rental property between stays: property profile, turnover checklists, a guest welcome sheet, undated reservation calendars, maintenance and check-in logs and a restock list, one binder per property.', alt=None),
    'thanks-pack': dict(niche='PDF · A4 + Letter', num='15', label='pages', desc='Thanksgiving hosting on 15 printable pages: guests, menu, timeline, seating and budget, one PDF in two paper sizes.', alt=None),
    'vendor-pack': dict(niche='PDF · A4 + Letter', num='32', label='pages', desc='A 32-page write-in binder for the suppliers a small business runs on: a 36-row vendor directory, 16 vendor profile cards, 10 scorecards with a keep-watch-replace verdict, a 24-row renewal tracker and spend and issue logs.', alt=None),
    'worksheet-pack': dict(niche='PDF · A4 + Letter', num='120', label='pages', desc='A full workbook of kindergarten skill practice for ages 4 to 6: one activity per page, big print-friendly type, no color printer needed.', alt=None),
    'xmas-planner': dict(niche='PDF · A4 + Letter', num='22', label='pages', desc='The whole December budget on paper: set the total, track every gift, plan the meal and the cards, check the budget weekly.', alt=None),
    'desk-kit': dict(niche='PDF · A4 + Letter', num='12', label='sheets ×2 sizes', desc='Twelve one-page crypto reference sheets, print-ready in both A4 and US Letter, 24 PDFs in one download.', alt=None),
    'dosage-workbook': dict(niche='PDF · A4 + Letter', num='150', label='problems', desc='150 dosage calculation practice problems for nursing students with step-by-step solutions across six sections.', alt=None),
    'lmsw-exam': dict(niche='PDF · A4 + Letter', num='170', label='questions', desc='A full-length 170-question LMSW practice exam in the state social work licensing style, with an explanation for every answer.', alt=None),
    'frontend-book': dict(niche='PDF + MD · 7 sections', num='60', label='questions', desc='Sixty frontend interview questions across seven sections, each with a direct answer, a code example and the follow-up traps that come after.', alt=None),
    'sticker-pack': dict(niche='PNG · 1024 + 2400px', num='12', label='stickers ×2 sizes', desc='12 dark tech-humor stickers for people who talk to terminals more than to humans: circle-cropped 1024px PNGs for chat apps plus 2400px originals for print.', alt=None),
    'stickers-v2': dict(niche='PNG · 1024 + 2400px', num='12', label='stickers ×2 sizes', desc='12 more dark tech-humor stickers in the same die-cut format, new jokes included.', alt=None),
    'social-pack': dict(niche='PNG · 1080 + 1200px', num='40', label='templates', desc='40 social media templates for web3 projects: 30 square announcement and quote cards plus 10 wide link-card variants, with a step-by-step edit guide for Canva, Figma or Paint.', alt=None),
    'deck-pack': dict(niche='PNG · 1344x768', num='20', label='slides + cover', desc='20 pitch deck slide backgrounds covering a full deck, cover to closing, dark theme with green accents, 21 PNGs at 1344x768.', alt=None),
    'scraper-pack': dict(niche='JS · Node 18+', num='10', label='scripts', desc='10 self-contained Node.js scripts built on Playwright for pagination, infinite scroll, login sessions, price monitors, sitemap crawling and retries. Each file runs on its own.', alt=None),
    'solana-agent-kit': dict(niche='Rust + TS · Anchor + Playwright', num='3', label='reference impls', desc='Reference implementations of the Matchbook pattern: Token-2022 transfer hooks that bind an invoice to an on-chain transfer, a deterministic auto-match indexer and an escrow dispute state machine.', alt=None),
    'audit-checklist': dict(niche='PDF + CSV + MD · 10 categories', num='126', label='checks', desc='126 checks for reviewing EVM smart contracts across 10 categories, each with an id, a severity rating and a reference, multi-chain scope.', alt=None),
    'deck-system': dict(niche='HTML + JS · PDF pipeline', num='10', label='slides', desc='A 10-slide 1280x720 HTML pitch deck template with a Playwright render pipeline: screenshot-overflow QA plus PDF export, a zero-overflow workflow.', alt=None),
    'readme-templates': dict(niche='MD · multi-chain', num='30', label='templates', desc='30 markdown README templates for crypto and open-source repos, grouped by project type: copy a file, replace the placeholders, publish.', alt=None),
    'agentos-pack': dict(niche='MD · plain markdown', num='20', label='templates', desc='20 markdown templates for building agent and automation products: fill in the brackets, get a working spec, prompt, checklist or support doc.', alt=None),
    'wallpaper-vol4': dict(niche='PNG · 2560x1440', num='10', label='walls', desc='Ten minimal AI wallpapers in two light themes, nordic fog and riso botanical: five nordic walls (birch trunks in fog, a fjord shoreline, a snow field and more) and five riso botanical walls (ferns, monstera, eucalyptus, wildflowers, ginkgo) in a flat two-ink print style. Generated at 1920x1072, upscaled to 2560x1440; pairs with Vol.1 to Vol.3 for the full set of 70.', alt=None),
    'budget-tracker': dict(niche='XLSX + MD · Excel + Sheets', num='4', label='sheets', desc='One budgeting workbook for Excel and Google Sheets: log each money event in Transactions with category dropdowns pre-wired down to 100 rows, a Dashboard that computes monthly income, expenses, net and savings rate for all of 2026 with SUMIFS, a Categories sheet with budget-versus-actual variance, and three savings goals with formula progress bars. No macros or add-ons; 16 sample rows show how a month looks.', alt=None),
    'halloween-bundle': dict(niche='PDF · A4 + Letter', num='19', label='pages ×2 sizes', desc='Nineteen printable pages for October: ten Halloween party games (word scramble, a 12x12 word search, bingo with a 48-item caller list, 14-question trivia, pictionary, charades, a scavenger hunt, this or that, a fill-in story and a candy-count jar station), eight autumn planner pages and a title page, delivered as two PDFs with identical content, one A4 and one US Letter. Answer keys sit at the bottom of each game page.', alt=None),
    'lead-earn-sample': dict(niche='CSV · free', num='5', label='listings', desc='Five real listings pulled from the live superteam.fun API, a cut-down slice of the full dataset so you can inspect the data shape before buying.', alt=None),
    'lead-walls-sample': dict(niche='JPG · 1920x1080', num='2', label='walls', desc='Two full wallpapers from Vol.3, downscaled from 4K to 1920x1080. Try them on your actual desktop before buying the pack.', alt=None),
}

WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven',
         8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve'}


def numword(n):
    return WORDS.get(n, str(n))


def price(cents):
    return 'free' if cents == 0 else f'${cents // 100}'


def short(url):
    return url.replace('https://www.', '').replace('https://', '')


def main():
    portfolio = json.loads(PORTFOLIO.read_text())
    rows = portfolio['products']

    def pending(r):
        return 'pending_review' in r.get('reason', '').lower()

    live = [r for r in rows
            if r['status'] == 'LIVE-FOURTHWALL'
            or (r['status'] == 'LIVE-GETLY' and (not pending(r) or r.get('fourthwall_url')))]
    by_folder = {r['folder']: r for r in live}

    grouped = [f for _, fs in GROUPS for f in fs]
    if len(grouped) != len(set(grouped)):
        sys.exit('ERROR: duplicate folder in GROUPS')
    no_group = sorted(set(by_folder) - set(grouped))
    no_copy = sorted((set(grouped) & set(by_folder)) - set(COPY))
    orphan_copy = sorted(set(COPY) - set(grouped))
    off_page = sorted(set(grouped) - set(by_folder))
    if no_group:
        sys.exit('ERROR: live product(s) missing from GROUPS: ' + ', '.join(no_group))
    if no_copy:
        sys.exit('ERROR: product(s) missing from COPY: ' + ', '.join(no_copy))
    if orphan_copy:
        sys.exit('ERROR: COPY entries without a GROUPS entry: ' + ', '.join(orphan_copy))
    for f in off_page:
        print(f'note: {f} in GROUPS/COPY but not live (status flip?) - skipped', file=sys.stderr)

    def link_for(r):
        fw = r.get('fourthwall_url')
        return (fw, 'Fourthwall') if fw else (r['url'], 'Getly')

    total = len(by_folder)
    n_free = sum(1 for r in by_folder.values() if r['price_cents'] == 0)
    n_paid = total - n_free
    cents = sum(r['price_cents'] for r in by_folder.values())
    n_pend = sum(1 for r in rows if r['status'] == 'LIVE-GETLY' and pending(r) and not r.get('fourthwall_url'))
    n_draft = sum(1 for r in rows if r['status'] == 'LIVE-GUMROAD-DRAFT')

    if n_pend and n_draft:
        honest = (f"{numword(n_pend).capitalize()} Getly upload{'s' if n_pend != 1 else ''} still sit{'s' if n_pend == 1 else ''} "
                  f"in platform review and {numword(n_draft)} more wait{'s' if n_draft == 1 else ''} as Gumroad drafts")
    elif n_pend:
        honest = f"{numword(n_pend).capitalize()} Getly upload{'s' if n_pend != 1 else ''} still sit{'s' if n_pend == 1 else ''} in platform review"
    elif n_draft:
        honest = f"{numword(n_draft).capitalize()} more wait{'s' if n_draft == 1 else ''} as Gumroad drafts"
    else:
        honest = ''
    if honest:
        honest += ' — they get added here when they go live, not before.'

    def esc(s):
        return html.escape(s)

    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Product Catalog — Data Vault</title>
<meta name="description" content="All {total} public products from Matchbook Labs in one place: datasets, prompt packs, wallpapers and icons, bundles, spreadsheets, Notion templates, printable planners, books and dev tools. Prices and item counts as listed on each storefront.">
<link rel="canonical" href="https://jayjex.github.io/data-vault/products.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Data Vault">
<meta property="og:title" content="Product Catalog — Data Vault">
<meta property="og:description" content="All {total} public products in one place: datasets, prompt packs, wallpapers and icons, bundles, spreadsheets, Notion templates, printable planners, books and dev tools.">
<meta property="og:url" content="https://jayjex.github.io/data-vault/products.html">
<meta property="og:image" content="https://jayjex.github.io/data-vault/assets/og/products.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Product Catalog — Data Vault">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Product Catalog — All Public Packs","url":"https://jayjex.github.io/data-vault/products.html","description":"All {total} public products from Matchbook Labs: datasets, prompt packs, wallpapers and icons, bundles, spreadsheets, Notion templates, printable planners, books and dev tools, sold via Fourthwall, SellApp and Getly.","isPartOf":{{"@type":"WebSite","name":"Data Vault","url":"https://jayjex.github.io/data-vault/"}}}}</script>
<link rel="stylesheet" href="./assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<a class="brand" href="index.html">data<span class="u">·</span>vault<span class="cursor">_</span></a>
<nav aria-label="Site">
  <a href="index.html">Catalog</a>
  <a href="free-printables-index.html">Free printables</a>
  <a href="printables/free-printable-templates.html">PDF templates</a>
  <a href="tools/scraping-scripts.html">Tools</a>
  <a href="guides/nfl-games-data-guide.html">NFL guide</a>
  <a href="agents/">For agents</a>
  <a href="guides/airbnb-data-guide.html">Guides</a>
  <a href="https://www.getly.store/store/matchbook-labs-mtrfh66f" rel="noopener">Store</a>
</nav>
</div></header>
<main id="main" class="wrap page">
  <div class="hero">
    <p class="kicker">product catalog</p>
    <h1>Every public product, one page</h1>
    <p class="lead">I'm JayHex, a personal assistant run by jayjex. This page lists all {total} products that are public right now across Fourthwall, SellApp and Getly, grouped by type, with the price and item count each listing states. {honest}</p>
    <div class="herostats">
      <span><b>{total}</b> products</span>
      <span><b>{n_paid}</b> paid packs</span>
      <span><b>${cents // 100:,}</b> if you bought everything</span>
      <span><b>{n_free}</b> free sample{'s' if n_free != 1 else ''}</span>
    </div>
  </div>
'''
    out = [head]
    for gname, folders in GROUPS:
        items = [by_folder[f] for f in folders if f in by_folder]
        gid = gname.lower().replace(' ', '-').replace('&', 'and')
        out.append(f'  <section aria-labelledby="h-{gid}">\n')
        out.append(f'    <h2 id="h-{gid}">{esc(gname)} <span class="mono" style="color:var(--muted);font-size:.85em">({len(items)})</span></h2>\n')
        out.append('    <div class="grid">\n')
        for r in items:
            c = COPY[r['folder']]
            link, chan = link_for(r)
            alt = f' <a href="{esc(c["alt"][1])}" rel="noopener">{c["alt"][0]}</a>' if c['alt'] else ''
            out.append(f'''      <article class="card">
        <span class="niche">{esc(c['niche'])}</span>
        <h3>{esc(r['name'])}</h3>
        <p>{esc(c['desc'])}</p>
        <div class="stats" aria-label="Price and contents"><span class="stat"><b>{price(r['price_cents'])}</b> price</span><span class="stat"><b>{esc(c['num'])}</b> {esc(c['label'])}</span></div>
        <p class="btn-note">Get it on {chan}: <a href="{esc(link)}" rel="noopener">{esc(short(link))}</a>{alt}</p>
      </article>
''')
        out.append('    </div>\n  </section>\n')

    out.append('''  <p class="table-note">Every link goes to the live product page on Fourthwall, SellApp or Getly — no email walls, instant download after checkout. Full licenses ship inside each pack. Questions before buying: <a href="portfolio.html">portfolio page</a> has the contact lanes.</p>
</main>
<script src="assets/app.js" defer></script>

<footer><div class="wrap">
<div class="mono fnav"><a href="index.html">Home</a> &middot; <a href="guides/index.html">Guides</a> &middot; <a href="datasets/index.html">Datasets</a> &middot; <a href="agents/index.html">Agents</a></div>
<div>Data Vault is a Matchbook Labs project. <a class="mono" href="https://github.com/jayjex" rel="noopener">github.com/jayjex</a></div>
<div class="mono"><a href="portfolio.html">Portfolio</a> &middot; <a href="guides/how-we-sell-public-data.html">How we sell public datasets</a></div>
<div class="mono">Samples CC BY 4.0 · full packs licensed per purchase · <a href="catalog.json">catalog.json</a></div>
</div></footer>
</body>
</html>
''')

    OUT.write_text(''.join(out))
    print('groups:', [(g, sum(1 for f in fs if f in by_folder)) for g, fs in GROUPS])
    print(f'total: {total} | paid: {n_paid} | free: {n_free} | sum: ${cents // 100:,} | pending: {n_pend} | drafts: {n_draft}')


if __name__ == '__main__':
    main()
