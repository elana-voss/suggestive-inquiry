# Dictionary Writer — instructions

You write a batch of entries for the dictionary of Mary Anne Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (1850). The binding rules (`RULES`) apply: the book is the only source; your only evidence is the `PACKETS` in your bundle (records extracted from the book by earlier readers, with verbatim quotes and refs). Use nothing else.

## Input (`PACKETS`)
One section per entry: `## <id> | <kind> | <headword>`, then `forms`, sometimes readers' `variants` (these may wrongly include other names), then records:
- `[VOICE] term: meaning | “quote” @ref; … | = other name (“quote” @ref)` — a term record. VOICE is `ATWOOD`, `QUOTED: <name>` or `UNCLEAR`.
- `[cited] name — work: …: use | “quote” @refs` — a citation of a person, work or group voice and how Atwood uses it.

Kinds: `term` (a concept or expression), `person`, `treatise` (a named work), `collective` (anonymous or group voices: "the adepts", "the Greeks").

## Write, per entry
- `forms` — the spellings/forms of **this** headword found in the packet (case, spelling, inflection, Latin/English form of the same word). Drop other names wrongly listed as variants. Max 10, most useful first; these become lookup keys.
- `summary` — one sentence, ≤35 words: what the book says this is (term) or who/what it is and how Atwood uses it (person/treatise/collective). No refs needed here.
- `body` — Markdown prose, refs inline in brackets: `[III.2 ¶14]`, `[I.3 n52]`.
  - Terms: what the text says it is and does, its role in the method where the records show one; key verbatim quotes (in “…”, copied exactly from the packet, each with its ref); asserted identities with other names (“= …” records) with their refs; competing readings where the records differ — don't force one.
  - Persons/treatises/collectives: what the book says about them, what Atwood takes from them and whether she endorses, qualifies or rejects it. No dates, identities or facts the packet doesn't give.
  - Voices: say who speaks — Atwood, or a quoted authority (name it). Refs beginning `APP` are the Appendix (Table Talk, begun 1860), a later layer: label them so.
  - Plain meaning: if a record's meaning is the reader's inference rather than the text's own statement, write it as such ("apparently", "the context suggests") — never as stated.
  - Length follows the material: 1–2 sentences for a single slight record; up to ~250 words for rich entries; up to ~400 only for the few with very many records. Merge repeated points; keep every distinct point and every asserted identity.

Quote only spans that appear in the packet, exactly as given (the readers already checked them against the book). Paraphrase anything else without quotation marks.

## Output
Write JSON to the OUTPUT path, keys in packet order:
```
{"E0005": {"forms": ["ablative reasoning"], "summary": "…", "body": "…"}, …}
```
Every entry in the packet gets an object. Read the bundle once and write the result once — no rewrite passes, no self-verification of quotes (a script and a checker do that). Reply with only the path and the entry count.
