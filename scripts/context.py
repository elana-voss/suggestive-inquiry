"""Per-chunk context: table of contents + last paragraph of the preceding chunk -> work/context/<id>.md"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx = json.load(open(os.path.join(ROOT, 'chunks', 'index.json'), encoding='utf-8'))
toc = open(os.path.join(ROOT, 'input', '0000_front_matter_toc.txt'), encoding='utf-8').read().strip()
out = os.path.join(ROOT, 'work', 'context'); os.makedirs(out, exist_ok=True)
prev = None
for c in idx:
    doc = f"# Context for {c['chunk']}\n\n## Table of contents\n\n{toc}\n\n## Last paragraph of the preceding chunk\n\n"
    if prev:
        body = open(os.path.join(ROOT, 'chunks', prev + '.md'), encoding='utf-8').read().split('## Footnotes')[0]
        paras = re.split(r'\n\n(?=\[)', body.strip())
        doc += f"(from {prev})\n\n{paras[-1].strip()}\n"
    else:
        doc += "(none: this is the first chunk of the book)\n"
    open(os.path.join(out, c['chunk'] + '.md'), 'w', encoding='utf-8', newline='\n').write(doc)
    prev = c['chunk']
print(len(idx), 'context files')
