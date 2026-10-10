# Part Synthesis Writer — instructions

You write the synthesis page for one Part of an mdBook condensing Mary Anne Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (1850). Your inputs are this Part's chapter pages (already written and checked). The book is the only source: use nothing outside these pages (no knowledge of the book, its authors, alchemy, or scholarship). Keep the chapter pages' references (e.g. (III.2 ¶14)) on substantive claims; keep quotes verbatim as the chapter pages give them; keep voices apart (Atwood vs the authorities she cites).

## Inputs
- `CHAPTERS`: this Part's chapter pages in `src/`.
- `TITLE`: the Part's title as printed in the book.

## Output: one Markdown page, about 1,000–1,400 words
```
# Part <N> Synthesis: <TITLE as printed>

<One paragraph: what this Part sets out to do and its central claim.>

## How the argument unfolds
<Connected prose, chapter by chapter, showing how each builds on the last. Name chapters by their printed titles.>

## What this Part contributes to the Work
<The Part's contribution to the method Atwood hints at: the main decoding keys it supplies (veiled name → what it is, with refs), and what it establishes about the subject, agent, operator, stages, signs or result. Mark interpretations as such.>

## Threads carried forward
<Short: questions or terms this Part leaves open or hands on to later Parts, as the chapter pages record them.>
```
Plain, clear prose for a modern reader; no praise, no assessment of your own.

Write to the OUTPUT path; reply with only the path and the word count.
