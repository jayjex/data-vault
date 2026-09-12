---
name: pdf-graph-qa
description: Validate a generated PDF by walking its page tree graph instead of counting streams, so broken or blank documents never ship. Use before publishing any PDF built by a script (fpdf2, reportlab, weasyprint, wkhtmltopdf), when a PDF opens blank in some viewers, or when a QA pass claims a PDF is fine but a buyer reports it is not.
---

# PDF Graph QA

Stream count is not a PDF check. A file can hold 12 content streams and render 0 pages if the page tree is broken. Validate the graph.

## What a valid page tree looks like

- Root `/Pages` node has `/Kids` pointing at page objects (possibly through nested `/Pages`)
- Every reachable object in that tree is `/Type /Page` (leaf) or `/Pages` (branch)
- Every `/Page` has `/Contents` pointing at a stream object, or is legitimately empty (rare, and blank-looking)
- `/Count` on the root equals the number of reachable leaves
- No `/Type /Page` object sits in the xref table unreachable from the root (orphan pages = viewer-specific blank output)

## The four checks

Run a validator that parses the classic xref table and walks the tree:

```
python3 pdfcheck.py guide-A4.pdf
```

Report per file: `kids N/N resolved`, `contents N/N stream`, `orphans 0`, `reachable == /Count`. Exit 0 only when orphans are 0 and counts match.

Checklist to reproduce in your own validator:

1. Read the raw bytes, find `startxref`, parse offset/generation entries, keep object numbers with `n`.
2. Extract object bodies (regex on `^(\d+) 0 obj` up to `endobj`; handle streams by byte offset, not line count).
3. Walk from the root `/Pages` through every `/Kids` reference, resolving `/ObjR` style numbers.
4. Flag any page object never visited: orphan.
5. Flag any `/Contents` reference that does not resolve to an object containing `stream`.
6. Compare visited leaf count against `/Count`.
7. Optional but useful: inflate each stream (`zlib`) and confirm it is not empty and ends with `ET`/`Q`.

## Failure modes seen in the wild

- Library wrote pages then a second pass added pages without updating `/Kids` or `/Count`. Result: correct stream count, blank tail pages.
- A font-embedding retry rewrote objects and left an older page object dangling as an orphan.
- Manual byte patching of `/Count` after a merge, with no tree rewrite.
- Linearized or cross-reference-stream PDFs where the classic parser bails. Do not treat "parser cannot read" as pass. Fail closed, then fix the parser or re-render.

## Pipeline rule

Wire the graph check into the build's QA step so no PDF is marked READY until it passes, and re-run it after any change to the PDF library version. Keep the checker output in the QA log with the file hash so a later rebuild cannot be confused with the validated artifact.
