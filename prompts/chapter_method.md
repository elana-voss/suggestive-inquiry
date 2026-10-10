# Chapter Method Summary — instructions

The project's main goal is to state, in clear modern terms, the method (process, requirements, stages, signs, impediments, result) that Mary Anne Atwood hints at in *A Suggestive Inquiry into the Hermetic Mystery*, illustrated by her own veiled expressions. You prepare one chapter's contribution. A later stage combines all chapters into the book-level method statement.

## Inputs
- `READINGS`: this chapter's verified chunk readings as JSON (`work/final/<id>.json`). Use their `method`, `terms` (especially `equivalences`), `ambiguities`, and `notes`.
- `SOURCE`: the source chunks, to check context where needed.
- Read `prompts/chunk_reader.md` first: its rules bind you (the book is the only source; verbatim quotes; references; voices; stated vs interpreted).

## Task
Merge the chapter's method material into one structured summary. Combine entries that make the same point across chunks; keep every distinct point. Keep the strongest verbatim expression for each point, with its reference, and list other expressions briefly. Preserve `stated`/`interpreted` honestly: merging never upgrades an interpreted reading to stated. Keep voices: say whether a point is Atwood's own or a cited authority's (and whether she endorses it).

## Output: Markdown, this structure
```
# Method material — <chapter id> <chapter title>

## The subject (what the work is done on)
## The agent (what does the work: fire, spirit, light, intellect…)
## The operator (requirements: knowledge, moral state, will, guidance, secrecy…)
## The procedure and its stages (in the order the chapter gives, if it gives one)
## Signs (what shows the work is proceeding)
## Impediments and dangers
## The result
## Principles (general laws of the work)
## Identities asserted
<Every identity the text asserts that bears on the method: "X = Y" — verbatim span (ref) — voice. These are the decoding keys; list them all.>
## Open questions
<Ambiguities that matter for the method, with the competing readings and their basis.>
```
Each point: one or two sentences of plain meaning, then the verbatim expression(s) with refs, then the label (stated / interpreted; voice). Leave a section empty with "—" if the chapter has nothing for it. No length cap, but no padding: merge restatements.

Write the file to the OUTPUT path and reply with only the path and a one-line count of points per section.
