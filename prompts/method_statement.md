# Method Statement — instructions

This is the project's primary deliverable: a clear, modern statement of the method Mary Anne Atwood hints at in *A Suggestive Inquiry into the Hermetic Mystery* (1850) — what the work is done on, by what agent, what it requires of the operator, its stages, signs, impediments and result — illustrated by her own veiled expressions. It becomes the mdBook page `src/23_The_Method_in_Plain_Terms.md`.

The binding rules (`RULES`) apply in full. The book is the only source: no outside knowledge of alchemy, mesmerism, the Mysteries, the authors cited, or scholarship. Copy quotes verbatim from the inputs, with the refs the inputs give (e.g. III.2 ¶14, III.2 n7). Keep `stated` vs `interpreted` honest: combining Parts never upgrades an interpretation. Keep voices: Atwood's own position vs a cited authority (and whether she endorses it). The Appendix is a later layer (Table Talk, begun 1860): label every point drawn from it.

## Inputs
- `PART_METHODS`: the five checked method syntheses — Parts I, II, III, IV and the Appendix (`work/part_method/<P>.md`). Each is organised as decoding keys; subject; agent; operator; procedure and stages; signs; impediments; result; principles; tensions. They are your only material.

## Task
1. **Merge the decoding keys** across the five files into one set of chains (all the names the text gives to one thing). For each chain: the plain meaning, each name with its strongest verbatim span and ref, voice, and whether each link is stated or interpreted.
2. **State the method aspect by aspect**, deduplicated across Parts. Each point: plain modern statement (1–3 sentences), one or two of Atwood's expressions (verbatim, ref), label (stated/interpreted; voice; Appendix where relevant).
3. **Reconstruct the procedure** as an ordered sequence of stages, as far as the inputs support. For each stage: what happens in plain terms, the veiled names for it, its signs, and how firm the placement is (say where Parts give different schemes and the text doesn't map them onto each other).
4. **Keep the tensions.** Where Parts or authorities disagree, or the text leaves something open, give the competing readings and their basis. Don't resolve what the text doesn't.

## Output: one Markdown page
```
# The Method in Plain Terms

<One paragraph: what this page is; that every point is from the book alone, referenced; what the labels mean (stated / interpreted; ATWOOD / QUOTED / UNCLEAR; Appendix = later layer).>

## The method in brief
<About 300–500 words: the whole method as a short numbered sequence a modern reader can follow, each step referenced and labelled.>

## Reading the veil: decoding keys
## What the work is done on
## The agent
## The operator: what the work requires
## The procedure, stage by stage
## Signs of progress
## Impediments and dangers
## The result
## Governing principles
## How the Parts differ
<Short: what each Part contributes or changes; the Appendix as a later layer.>
## Open questions
```
Plain, clear prose for a modern reader; lists where the reader will scan. No praise, no assessment of your own. Length: about 6,000–10,000 words; compress by merging restatements, never by dropping distinct points, decoding keys or tensions.

Read the bundle once and write the result once. No rewrite or compression passes; no self-verification of quotes (a script and a checker do that). Write to the OUTPUT path; reply with only the path and the word count.
