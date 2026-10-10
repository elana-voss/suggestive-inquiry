"""Split input/ chapters into chunks with paragraph IDs and attached footnotes.
Output: chunks/<ID>_<nn>.md + chunks/index.json. Source text is kept line-for-line."""
import re, json, glob, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN, OUT = os.path.join(ROOT, 'input'), os.path.join(ROOT, 'chunks')
TARGET, HARDMAX = 2200, 3800      # words of main text / text+notes
HEAD = re.compile(r'^(Section \w+|THE \w+ KEY ~)$')
FULL = 80                          # lines >= this are wrapped prose

def chap_id(fn):
    if 'appendix' in fn: return 'APP'
    m = re.search(r'part_(\w+?)_chapter_(\w+)', fn)
    roman = {'I':1,'II':2,'III':3,'IV':4}
    return f"{m.group(1)}.{roman[m.group(2)]}"

def paragraphs(lines):
    """Return list of (start, end) 0-based inclusive line ranges."""
    paras, cur, mode = [], None, None
    for i, l in enumerate(lines):
        if not l.strip():
            if cur: paras.append(cur); cur = None
            continue
        if HEAD.match(l.strip()):            # headings always stand alone
            if cur: paras.append(cur)
            paras.append((i, i)); cur, mode = None, 'closed'; continue
        full = len(l.rstrip()) >= FULL
        if full:
            if mode == 'verse' and cur: paras.append(cur); cur = None
            cur = (cur[0], i) if cur else (i, i); mode = 'prose'
        else:
            if mode == 'prose' and cur:
                paras.append((cur[0], i)); cur = None; mode = 'closed'
            else:
                cur = (cur[0], i) if cur else (i, i); mode = 'verse'
    if cur: paras.append(cur)
    return paras

def parse_notes(path):
    notes = {}
    if not os.path.exists(path): return notes
    cur = None
    for l in open(path, encoding='utf-8').read().split('\n')[1:]:
        m = re.match(r'^\s*(?:\((\d+)\)|(\d+)\.)\s*(.*)', l)
        if m:
            cur = int(m.group(1) or m.group(2)); notes[cur] = [m.group(3)]
        elif cur is not None and l.strip():
            notes[cur].append(l)
    return {k: '\n'.join(v).strip() for k, v in notes.items()}

wc = lambda s: len(s.split())
os.makedirs(OUT, exist_ok=True)
index, problems = [], []
for path in sorted(glob.glob(os.path.join(IN, '0*.txt'))):
    fn = os.path.basename(path)
    if fn.startswith('0000') or fn.endswith('_footnotes.txt'): continue
    cid = chap_id(fn)
    lines = open(path, encoding='utf-8').read().split('\n')
    notes = parse_notes(path.replace('.txt', '_footnotes.txt'))
    paras = paragraphs(lines)
    ptext = ['\n'.join(lines[a:b+1]) for a, b in paras]
    pnotes = [sorted({int(n) for n in re.findall(r'\((\d+)\)', t)} & notes.keys()) if cid != 'APP' else [] for t in ptext]
    seen = set()                       # each note goes to its first referencing paragraph
    for i, ns in enumerate(pnotes):
        pnotes[i] = [n for n in ns if n not in seen]; seen.update(pnotes[i])
    # unreferenced notes -> paragraph that references the nearest lower note
    used = {n for ns in pnotes for n in ns}
    for n in sorted(notes.keys() - used):
        host = max((i for i, ns in enumerate(pnotes) if any(x < n for x in ns)), default=0)
        pnotes[host] = sorted(pnotes[host] + [n])
    # forced breaks: Golden Treatise sections
    force = {i for i, t in enumerate(ptext) if re.match(r'^Section \w+$', t.strip().split('\n')[0])}
    groups, cur, tw, nw = [], [], 0, 0
    for i, t in enumerate(ptext):
        w, n = wc(t), sum(wc(notes[x]) for x in pnotes[i])
        joined = cur and not re.search(r'[.!?)\'"’”\]]$', ptext[cur[-1]].strip())  # keep intro with its quote
        if cur and not (joined and tw + nw + w + n <= HARDMAX + 800) and (i in force and tw + nw > 1500 or tw >= TARGET or tw + nw + w + n > HARDMAX):
            groups.append(cur); cur, tw, nw = [], 0, 0
        cur.append(i); tw += w; nw += n
    if cur:
        if groups and tw < 500: groups[-1] += cur   # avoid tiny tail
        else: groups.append(cur)
    for k, g in enumerate(groups, 1):
        a, b = paras[g[0]][0], paras[g[-1]][1]
        body = '\n\n'.join(f"[{cid} ¶{i+1}] " + ptext[i] for i in g)
        ns = [x for i in g for x in pnotes[i]]
        nbody = '\n\n'.join(f"[{cid} n{x}] {notes[x]}" for x in ns)
        cidk = f"{cid}_{k:02d}"
        hdr = (f"---\nchunk: {cidk}\nsource: input/{fn}\nlines: {a+1}-{b+1}\n"
               f"paragraphs: {g[0]+1}-{g[-1]+1}\nfootnotes: {ns if ns else 'none'}\n"
               f"words_text: {sum(wc(ptext[i]) for i in g)}\nwords_notes: {wc(nbody)}\n---\n\n")
        doc = hdr + '## Text\n\n' + body + ('\n\n## Footnotes\n\n' + nbody if ns else '') + '\n'
        open(os.path.join(OUT, cidk + '.md'), 'w', encoding='utf-8').write(doc)
        index.append(dict(chunk=cidk, chapter=cid, source=fn, lines=[a+1, b+1],
                          paragraphs=[g[0]+1, g[-1]+1], footnotes=ns,
                          words_text=sum(wc(ptext[i]) for i in g), words_notes=wc(nbody)))
    # integrity: every non-blank line exactly once, every note exactly once
    covered = sorted(j for a, b in paras for j in range(a, b+1) if lines[j].strip())
    if covered != [j for j, l in enumerate(lines) if l.strip()]: problems.append(f'{fn}: line coverage')
    allnotes = sorted(x for ns in pnotes for x in ns)
    if allnotes != sorted(notes): problems.append(f'{fn}: note coverage')
json.dump(index, open(os.path.join(OUT, 'index.json'), 'w', encoding='utf-8'), indent=1)
print(len(index), 'chunks;', 'problems:', problems or 'none')
