# Chunk Reader — instructions

You are reading **one chunk** of Mary Anne Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (1850), a book on Hermetic philosophy and alchemy. Many independent readers each handle one chunk; later stages build chapter summaries, a dictionary, and — most importantly — a plain-language statement of the **method** Atwood hints at, all from your output. What you miss is lost; what you invent poisons everything above you.

## Inputs
- `CHUNK`: the chunk file. Main text paragraphs are marked `[III.1 ¶12]`; footnotes `[III.1 n7]`. Footnote markers in the text look like `(7)`.
- `CONTEXT`: the table of contents and the last paragraph of the preceding chunk. Context only — do not summarize it, do not take terms or claims from it.

Read the whole chunk, footnotes included, before writing anything.

## The one rule: this text is the only source
- Use **only** what the chunk says. Do not use anything you know about this book, Atwood, the authors and works she cites, alchemy, the Mysteries, mesmerism, or later scholarship.
- If you recognize a name, work or term, record **only what this text says** about it. Do not add dates, identities, titles, glosses or explanations the text doesn't give. Write names exactly as the text spells them.
- Test every statement you write: *can a reader verify it from the reference I give?* If not, cut it.
- Quotes are **verbatim**: copy exact spelling, archaic forms, punctuation and even apparent typos. Replace line breaks with single spaces. One contiguous span per quote, no ellipses, no more than ~40 words. Never quote from memory — copy from the chunk.
- Every item carries references: `III.1 ¶12`, `III.1 n7`. Use the reference of the paragraph/footnote the quoted words actually appear in.

## Voices
Tag every note, method hint and term with who is speaking:
- `ATWOOD` — Atwood's own statement or position (including when she clearly endorses a cited view as her own).
- `QUOTED: <name as given>` — a cited authority speaking or a view she reports. Note whether she endorses, qualifies or rejects it if the text shows this.
- `UNCLEAR` — when you cannot tell from the text.
Determine voice from the text itself (quotation marks, "says", "as … observes", verse set off, the chapter heading), not from outside knowledge. Footnotes may contain either voice; tag accordingly.

## Plain meaning
The project's main goal is to state Atwood's method clearly for a modern reader. So for every veiled or symbolic expression bearing on the method, give its plain meaning — but only as far as the text supports it:
- `stated` — the text itself says what the expression means (e.g. "by X they mean Y", or Atwood explains it directly).
- `interpreted` — you infer the meaning; then `basis` must cite the specific passages that support the inference. Prefer the narrowest reading the text supports.
- If several readings are defensible, put the expression in `ambiguities` with each reading and its textual basis, rather than choosing.

## Translations
For passages in Latin, Greek, French, Middle English or other non-modern language: if the book gives its own translation, record that (`by: "book"`). Otherwise give a modern English rendering marked `by: "ours"`. Translations are aids, not evidence: never build a claim on an `ours` translation alone without saying so.

## Output
Write **one JSON file** to the path you are given, valid UTF-8 JSON, exactly this shape (empty arrays are fine; don't pad):

```json
{
  "chunk": "III.1_02",
  "gist": "One or two sentences: what this chunk does in Atwood's argument.",
  "notes": [
    {"point": "Condensed statement of one step of the argument.", "refs": ["III.1 ¶12"], "voice": "ATWOOD"}
  ],
  "method": [
    {
      "aspect": "subject | agent | operator | procedure | stage | sign | impediment | result | principle",
      "veiled": "verbatim expression from the text",
      "ref": "III.1 ¶14",
      "plain": "What it means in plain modern terms.",
      "status": "stated | interpreted",
      "basis": "Where the text supports this reading (refs + brief reason). Required for interpreted.",
      "voice": "ATWOOD",
      "also": [{"text": "another verbatim expression making the same point", "ref": "III.1 ¶16"}]
    }
  ],
  "terms": [
    {
      "term": "First Matter",
      "variants": ["first matter", "Prima Materia"],
      "meaning": "What the term means according to this chunk only.",
      "equivalences": [{"with": "Ether", "quote": "verbatim span asserting the identity", "ref": "III.1 ¶13"}],
      "quotes": [{"text": "verbatim span", "ref": "III.1 ¶13"}],
      "voice": "ATWOOD"
    }
  ],
  "sources": [
    {"name": "as spelled in the text", "work": "title as given, or null", "quote": "short verbatim span attributed to it, or null", "use": "What Atwood uses it for: supports / illustrates / contrasts / is criticized — and what point.", "refs": ["III.1 n4"]}
  ],
  "ambiguities": [
    {"quote": "verbatim span", "ref": "III.1 ¶15", "readings": ["reading A", "reading B"], "basis": "textual support for each"}
  ],
  "translations": [
    {"ref": "III.1 ¶11", "original": "verbatim foreign passage", "translation": "...", "by": "book | ours"}
  ],
  "threads": [
    {"ref": "III.1 ¶16", "note": "Points to something outside this chunk (\"as before shown\", \"we shall see\") — what it points to, as stated."}
  ]
}
```

### What goes where
- **notes**: the argument in order, condensed but complete. Cover footnotes that carry substance; bare bibliographic references go only in `sources`. Length: at most 1 word of notes per 5 words of substantive source text (main text plus substantive footnotes), and never more than 900 words in total. Don't paraphrase into vagueness — keep the specific claims, images and distinctions, and cut repetition instead.
- **method**: statements about what the work is done on, by what agent, by whom (requirements of the operator), how, in what stages, with what signs, against what impediments, to what end. Include veiled images (dragons, ravens, fire, waters, keys) when the text relates them to the work.
  - **One entry per distinct point, not per sentence.** When several expressions make the same point, merge them: put the most telling one in `veiled` and the others in `also`.
  - **Prioritize decoding.** The most valuable entries are those where the text itself explains, glosses or identifies something (X is Y; by X they mean Y; this is that). Never skip one of these.
  - A veiled image the chunk does not explain gets an entry only if it marks a recognizable step, sign or agent of the work; then say briefly that this chunk does not explain it. Don't restate general exhortations already covered by another entry.
  - Typical result: 15–30 entries per chunk. More only if the chunk is unusually dense in distinct, explained points.
- **terms**: the specialized vocabulary — alchemical, philosophical, theological, and any ordinary word used in a special sense. Record identities the text asserts ("X, which is Y") in `equivalences`; these are vital, since the tradition gives one thing many names. Include persons and works only in `sources`, not here. `variants` holds only other spellings or forms of the same word that occur in this chunk; a different name for the same thing goes in `equivalences`, and only when the text itself asserts the identity (not because two names appear near each other or play a similar role).
- **sources**: every author, work, oracle, scripture or tradition cited, including bare footnote references (then `use` can be "reference only").
- **threads**: cross-references the later chapter stage will need.

When done, reply with only: the output path and a one-line count (notes / method / terms / sources / ambiguities).
