# Reconciler — instructions

Two readers independently read the same chunk of Atwood's *A Suggestive Inquiry into the Hermetic Mystery* using `prompts/chunk_reader.md`. Your job: produce one reading that is better than either.

## Inputs
- `CHUNK` — the source chunk (the only authority).
- `READING_A`, `READING_B` — the two JSON readings.
- `prompts/chunk_reader.md` — the rules and output schema. Read it first; every rule there binds you too.

## How
1. Read the chunk in full, footnotes included.
2. Take the **union** of what A and B found, merging duplicates into the better-phrased, better-referenced entry.
3. Where A and B **disagree** (voice, plain meaning, stated vs interpreted, a term's meaning), go back to the cited passage and decide from the text. If the text genuinely supports both, move it to `ambiguities` with both readings and their basis.
4. **Drop** anything neither the text nor its reference supports, any outside knowledge (dates, identities, glosses not in the text), and any quote that is not verbatim — or fix the quote by copying it exactly from the chunk.
5. Add anything important both readers missed, especially method hints and asserted equivalences between terms.
6. Keep `notes` in the order of the text.

## Output
Write one JSON file in the exact schema of `chunk_reader.md` to the path you are given. Reply with only: the output path, and at most five short lines on the substantive disagreements you resolved and how.
