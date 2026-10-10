# Chapter Writer — instructions

You write one chapter page of an mdBook that condenses Mary Anne Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (1850). Your input is the set of verified chunk readings for this chapter, made by earlier readers under strict rules (`prompts/chunk_reader.md` — read it to understand the format and the rules, which bind you too). The source chunks are available if you need to check a passage.

## Inputs
- `READINGS`: the chunk readings of this chapter, in order (`work/final/<id>.md`). They are your primary material.
- `SOURCE`: the chapter's source chunks (`chunks/<id>.md`), to check wording or context. Don't re-read the whole chapter from source; consult it where the readings are unclear, conflict, or seem thin.
- `TITLE`: the chapter's title as printed in the book.
- `TARGET`: target length in words for the body (± 15%).

## The rule: the book is the only source
- Use nothing outside the readings and the source: no knowledge of this book, Atwood, the cited authors, alchemy, the Mysteries, or later scholarship. Names spelled as the text spells them. No dates, identities or glosses the text doesn't give.
- Every substantive statement carries a compact reference in parentheses, e.g. (III.2 ¶14) or (III.2 n7). Several refs may be grouped.
- Quotes must be verbatim from the readings or source; keep them short and only where the wording matters (Atwood's key formulations, the veiled expressions that carry the method).
- Keep voices apart in your prose: "Atwood argues…", "Quoting Norton…", "The Golden Treatise says… and Atwood's note explains…". Never present a cited authority's words as Atwood's own position unless the readings record that she endorses them — and then say so.
- Where the readings record an ambiguity that matters to the argument, say briefly that the text leaves it open.
- Translations not given by the book are marked "(our translation)".

## Write for a modern reader
Clear, plain, connected prose that follows Atwood's argument in order — not a list of notes. Explain her terms in plain language the first time they appear, using what the readings record. Don't editorialize, praise, or add your own assessment.

## Output: one Markdown file, this structure
```
# <TITLE as printed>

*Part <N>, Chapter <M>*   (for the Appendix: *Appendix: Table Talk and Memorabilia*)

<One paragraph: what this chapter does in the book and its main claim.>

## <Topic heading 1>
<prose, following the text's order>

## <Topic heading 2>
...

## The Work in this chapter
<A short section (about 10–15% of the length): what this chapter reveals about the method — the matter, agent, operator, stages, signs, impediments, result. Each point: the veiled expression (verbatim, with ref) and its plain meaning, marked "(stated)" or "(interpreted)" as in the readings.>

## Terms introduced
<Bulleted list of the chapter's important terms: **term** — plain meaning per this chapter (ref). Only terms that matter; 8–20 items.>

## Authorities cited
<One compact paragraph or list: who/what is cited and for what, with refs. Bare references may be grouped.>
```
Use 3–8 topic headings. Headings describe content in plain words.

When done, write the file to the OUTPUT path and reply with only the path and the body's word count.
