"""Assemble one input bundle for an agent: python3 scripts/bundle.py OUT 'LABEL=path[,path...]' ..."""
import sys
out=sys.argv[1]; parts=[]
for spec in sys.argv[2:]:
    label,paths=spec.split('=',1)
    parts.append(f'\n\n######## {label} ########\n')
    for p in paths.split(','):
        parts.append(f'\n=== FILE: {p} ===\n'+open(p,encoding='utf-8').read())
open(out,'w',encoding='utf-8').write(''.join(parts))
print(out, sum(len(x) for x in parts))
