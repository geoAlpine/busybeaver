"""Cross-reference: how does the SIMULATION census classify the 18 machines that the
EXACT structural (Atoms) scan found?  If most are 'UNRESOLVED', the syntactic classifier
is seeing what 5e6 steps of simulation cannot."""
import importlib.util
spec = importlib.util.spec_from_file_location("rc", "residual_census.py")
rc = importlib.util.module_from_spec(spec)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    try: spec.loader.exec_module(rc)
    except SystemExit: pass
from atoms_flex_scan import flex_scan
HOLD = "/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt"
hits = []
with open(HOLD) as fh:
    for line in fh:
        s = line.strip().split()[0] if line.strip() else ""
        if not s or s.count('_') != 5: continue
        if flex_scan(s)[0] == 6: hits.append(s)
print(f"Atoms hits: {len(hits)}")
from collections import Counter
c = Counter()
for s in hits:
    st, r, det = rc.ratio(s, 5*10**6, 1 << 22)
    lab = st if st == 'UNRESOLVED' else rc.label(r)
    c[lab] += 1
    print(f"  {s}  census -> {lab}" + (f" ({r:.4f})" if r else ""))
print()
print("census verdict on the 18 exact hits:", dict(c))
