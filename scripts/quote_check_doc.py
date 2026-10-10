"""Check that every quotation (4+ words, in “…” or "…") in Markdown files appears verbatim somewhere in the source chunks.
Usage: python quote_check_doc.py FILE.md [...]"""
import glob, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quote_check import norm
CH = '/mnt/user-data/uploads/atwood/chunks'
corpus = ' '.join(norm(re.sub(r'^\[[^\]]+\] ', '', open(f, encoding='utf-8').read(), flags=re.M)) for f in glob.glob(f'{CH}/*.md'))
corpus = re.sub(r'-\s+', '-', corpus)
corpus = corpus.replace('"', '').replace("'", '').lower()
bad_total = 0
for path in sys.argv[1:]:
    txt = open(path, encoding='utf-8').read()
    qs = re.findall(r'“([^”]+)”', txt) + re.findall(r'"([^"\n]+)"', txt)
    qs = [q for q in qs if len(q.split()) >= 4]
    bad = []
    for q in qs:
        parts = [p.strip(' ,.;:') for p in re.split(r'\s*(?:\.\.\.|…)\s*', q)]
        for p in parts:
            n = re.sub(r'-\s+', '-', norm(p)).replace('"', '').replace("'", '').strip(' ,.;:!?').lower()
            if len(n.split()) >= 3 and n not in corpus: bad.append(q[:90]); break
    bad_total += len(bad)
    print(f'{os.path.basename(path)}: {len(qs)} quotes, {len(bad)} not found')
    for b in bad: print('   NOT FOUND:', b)
sys.exit(1 if bad_total else 0)
