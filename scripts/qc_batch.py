"""Quote-check readings: python qc_batch.py READING.json [...] -> writes work/qc/<chunk>.txt, prints one line each."""
import io, os, sys, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quote_check
CH = '/mnt/user-data/uploads/atwood/chunks'
QC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'work', 'qc')
os.makedirs(QC, exist_ok=True)
for p in sys.argv[1:]:
    b = os.path.basename(p)[:-5]                       # I.1_01.A  or  I.1_01
    chunk = __import__('re').match(r'^(.*?_\d\d)', b).group(1)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): quote_check.check(f'{CH}/{chunk}.md', p)
    except Exception as e:
        buf.write(f'{p}: ERROR {e}\n')
    open(f'{QC}/{chunk}.txt', 'w', encoding='utf-8').write(buf.getvalue())
    print(buf.getvalue().splitlines()[0])
