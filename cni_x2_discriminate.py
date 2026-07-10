#!/usr/bin/env python3
"""For each near-x2 machine, decide at the TAIL whether the reported observable is
ARITHMETIC (linear counter -> the x2 is a transient artifact) or GEOMETRIC (genuine
value-doubling). Method: over the last N fast milestones, look at consecutive diffs
and ratios of the observable. Arithmetic => diffs ~const, ratios ->1. Geometric =>
ratios ~const>1. Also report step-gap growth (steps between milestones):
linear counter: step-gap grows linearly (per-milestone work ∝ index).
"""
import sys, json
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
from fractions import Fraction

def sim(spec, maxsteps, SZ=1 << 24):
    M = parse(spec); tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    Lf = []; Rf = []
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None:
            return ('HALT', step, Lf, Rf)
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo or pos > hi:
            if pos < lo: lo = pos; F = Lf
            else: hi = pos; F = Rf
            rr = rle(tape, lo, hi)
            tot1 = sum(n for c, n in rr if c == 1)
            mx = max((n for c, n in rr if c == 1), default=0)
            w = hi - lo + 1
            rec = (step, tot1, mx, w)
            if F and F[-1][0] == step - 1:
                F[-1] = rec
            else:
                F.append(rec)
        if pos < 8 or pos > SZ - 8:
            return ('OVR', step, Lf, Rf)
    return ('MAX', step, Lf, Rf)

def classify(spec, cap, obsname):
    outc, step, Lf, Rf = sim(spec, cap)
    fast = Rf if len(Rf) >= len(Lf) else Lf
    idx = {'total1': 1, 'maxrun': 2, 'width': 3}[obsname]
    vals = [f[idx] for f in fast]
    steps = [f[0] for f in fast]
    N = min(40, len(vals) - 2)
    tv = vals[-N:]; ts = steps[-N:]
    diffs = [tv[i+1]-tv[i] for i in range(len(tv)-1)]
    ratios = [tv[i+1]/tv[i] for i in range(len(tv)-1) if tv[i] > 0]
    # step gaps
    sg = [ts[i+1]-ts[i] for i in range(len(ts)-1)]
    sgd = [sg[i+1]-sg[i] for i in range(len(sg)-1)]  # 2nd diff of steps
    import statistics as S
    med_diff = S.median(diffs) if diffs else 0
    med_ratio = S.median(ratios) if ratios else 0
    # arithmetic test: diffs roughly constant & ratio near 1
    diff_cv = (S.pstdev(diffs)/abs(med_diff)) if med_diff else 99
    verdict = 'ARITH(linear)' if (med_ratio < 1.05 and abs(med_diff) < 5) or (diff_cv < 0.3 and med_ratio<1.2) else ('GEOM(x'+str(round(med_ratio,2))+')' if med_ratio>1.3 else 'AMBIG')
    return dict(outc=outc, nfast=len(fast), obs=obsname, tail_vals=tv[-8:],
                med_diff=med_diff, med_ratio=round(med_ratio,4), diff_cv=round(diff_cv,3),
                sg_tail=sg[-5:], verdict=verdict)

if __name__ == "__main__":
    rows = json.load(open('mse_census_rows.json'))
    cand = [r for r in rows if r.get('reported') and r['reported'].startswith('~2(')]
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 4_000_000
    print(f"cap={cap}, {len(cand)} near-x2 machines\n")
    results = []
    for r in cand:
        obs = r['saw'][1] if r['saw'] else 'maxrun'
        c = classify(r['spec'], cap, obs)
        results.append((r['spec'], r['rho'], obs, c))
        print(f"rho={r['rho']:.3f} obs={obs:6} {c['verdict']:16} med_diff={c['med_diff']:>7} med_ratio={c['med_ratio']} tail={c['tail_vals'][-4:]} sg={c['sg_tail']}")
        print(f"    {r['spec']}")
    from collections import Counter
    print("\nVERDICT TALLY:", Counter(c[3]['verdict'].split('(')[0] for c in results))
    json.dump([(s,rho,obs,c) for s,rho,obs,c in results], open('x2_discriminate_out.json','w'))
