# Part Method Synthesis — instructions

The project's main goal is a clear, modern statement of the method Mary Anne Atwood hints at in *A Suggestive Inquiry into the Hermetic Mystery* (1850): what the work is done on, by what agent, what it requires of the operator, its stages, signs, impediments and result — illustrated by her own veiled expressions. Chapter-level method summaries exist; you merge those of one Part (or the Appendix) into one synthesis. A final stage will combine the five syntheses into the book's method statement.

Read `prompts/chunk_reader.md` first: its rules bind you. The book is the only source — no outside knowledge of alchemy, the authors cited, or scholarship. Verbatim quotes only, with references (e.g. III.2 ¶14, III.2 n7). Keep `stated` vs `interpreted` honest: merging never upgrades an interpretation. Keep voices: Atwood's own position vs a cited authority (and whether she endorses it). The Appendix is a later layer (Table Talk, begun 1860): label it as such.

## Inputs
- `METHOD_FILES`: the chapter method summaries of this Part (`work/method/<ch>.md`).
- `SOURCE`: the source chunks, for checking a passage where the summaries disagree or are unclear.

## Task
1. **Decoding keys first.** Gather every asserted identity ("X = Y") across the Part's chapters and group them into chains of equivalent names (e.g. all names the text gives to the one agent). For each chain: the names, the strongest verbatim span asserting each link, refs, voice. Note where links are only interpreted.
2. **The method by aspect.** For each aspect (subject, agent, operator, procedure/stages, signs, impediments, result, principles), merge the chapters' points into a deduplicated list. Each point: plain modern statement (1–3 sentences), the best one or two verbatim expressions with refs, label (stated/interpreted; voice). Where chapters give a sequence of stages, reconstruct the order the text supports and say how firmly.
3. **Tensions and open questions.** Where chapters or authorities disagree, or the text leaves something open, state it with the competing readings and their basis. Don't resolve what the text doesn't resolve.

## Output
Markdown, sections in this order: `# Method synthesis — <Part>`, `## Decoding keys`, `## Subject`, `## Agent`, `## Operator`, `## Procedure and stages`, `## Signs`, `## Impediments and dangers`, `## Result`, `## Principles`, `## Tensions and open questions`.
Length: at most about 7,000 words. Compress by merging restatements, never by dropping distinct points or decoding keys.

Write to the OUTPUT path; reply with only the path and the word count.
