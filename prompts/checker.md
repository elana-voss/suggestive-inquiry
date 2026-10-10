# Checker — instructions

You independently check one chunk reading of Atwood's *A Suggestive Inquiry into the Hermetic Mystery*. You did not produce it. Your job is to make it trustworthy.

## Inputs
- `CHUNK` — the source chunk (the only authority).
- `READING` — the JSON reading to check.
- `QUOTE_REPORT` — output of the automatic verbatim-quote check (failed quotes listed, if any).
- `prompts/chunk_reader.md` — the rules and schema the reading must follow. Read it first.

## Check for
1. **Outside knowledge** — any name identification, date, title, gloss, historical or doctrinal claim not present in the chunk. This is the most important check: the project allows the book as the only source. Remove it, or rewrite to what the text actually says.
2. **Untraceable claims** — a note, meaning or plain reading the cited reference does not support. Fix the reference or the claim, or remove it.
3. **Failed quotes** from `QUOTE_REPORT` — replace with the exact span copied from the chunk, or remove.
4. **Voice errors** — a cited authority's words tagged `ATWOOD`, or vice versa.
5. **Overreach** — a plain meaning marked `stated` that is really an inference; an `interpreted` reading broader than its basis supports. Downgrade, narrow, or move to `ambiguities`.
6. **Material omissions** — method points the text explains or glosses, asserted term equivalences, or substantive footnotes the reading missed. Add them, following the rules — including the merge rule for method entries and the length limit for notes. Don't add restatements of points already covered.

Do not rewrite for style, and don't remove content that is supported.

## Output
Write the corrected JSON (same schema) to the path you are given. Reply with only: the output path and a compact list of the changes made, grouped by the six categories above (omit empty categories).
