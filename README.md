# Suggestive Inquiry: Summaries and Hermetic Lorebook

A structured digest of Mary Anne Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (1850), published as an mdBook, with a SillyTavern worldbook built from its lexicon. The book is the only source: quotations are verbatim with paragraph/footnote references, and nothing is added from outside knowledge.

Read the book online: <https://elana-voss.github.io/suggestive-inquiry/>

## Lorebook

[`lorebook/Atwood_Hermetic_Mystery.json`](https://raw.githubusercontent.com/elana-voss/suggestive-inquiry/main/lorebook/Atwood_Hermetic_Mystery.json) — one entry per term, person, work or voice in the Master Lexicon. Download it and import it in SillyTavern under World Info, Import.

Entries ship in Normal mode and trigger on the forms of each headword found in the text. If those terms rarely come up naturally in your chats, switching entries to Vectorized may give better results (requires embeddings under Data Bank / Vector Storage).

## How it was made

- `input/` — the book's text, split into chapters and footnotes; `chunks/` — the same, cut into referenced chunks.
- `prompts/` — instructions for the reading, synthesis, dictionary and checking agents; `prompts/rules_core.md` holds the binding rules.
- `scripts/` — chunking, bundling, verbatim quote checks, dictionary extraction/rendering, and worldbook generation.
- `PLAN.md` — the method; `RUNBOOK.md` — run notes.

Every chunk was read by one or two independent agents and reconciled; every synthesized page and dictionary batch was checked against its inputs by a separate checker agent and by a script that verifies each quotation verbatim against the source.

Regenerate the lexicon page and worldbook from the checked dictionary batches (kept outside git in `work/`):

```bash
python3 scripts/dict_render.py all      # src/22_Master_Lexicon_and_Concordance.md + work/dict/dictionary.json
python3 scripts/dict_worldbook.py       # lorebook/Atwood_Hermetic_Mystery.json
```
