#!/usr/bin/env python3
"""
mse_census.py -- run the PROPER milestone-form extractor (mse_extract.extract) over all 1104
BB(6) holdouts, OBSERVE-ONLY. Reports: detection rate (machines whose milestone-form the tool
cleanly reads), engine census over detected machines, and the collapse count
(known-engine instances / candidate-new-with-multiplier / undetected-needs-hand-analysis).

STRICT: every assignment is [OBSERVED, extractor], NOT a certified reduction; decides NO
halting. The tool is trusted only for the classes it recovered on the 17-named gate
(13/16, 0 WRONG). Fork-parallel, memory-bounded. No machine decided. No label upgraded.
"""
import sys, json
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import extract, ENGINES
from fractions import Fraction

HOLD = '/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt'
OUT = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad/mse_census_rows.json'


def work(args):
    i, sp, cap = args
    try:
        c = extract(sp, cap=cap)
    except Exception as e:
        return dict(spec=sp, err=str(e), reported=None)
    return dict(spec=sp, outc=c['outc'], nfast=c['nfast'],
                transfer=str(c['transfer']) if c['transfer'] else None,
                saw=(round(c['sawtooth'][0], 4), c['sawtooth'][3]) if c['sawtooth'] else None,
                reported=c['reported'], rho=(round(c['rho'], 4) if c['rho'] else None),
                src=c['src'], conf=c['conf'])


if __name__ == "__main__":
    import multiprocessing as mp
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 4_000_000
    specs = [l.strip() for l in open(HOLD) if l.strip()]
    args = [(i, sp, cap) for i, sp in enumerate(specs)]
    ctx = mp.get_context('fork')
    with ctx.Pool(8) as pool:
        rows = pool.map(work, args, chunksize=4)
    json.dump(rows, open(OUT, 'w'))

    detected = [r for r in rows if r.get('reported')]
    known = [r for r in detected if not r['reported'].startswith('~')]
    cand = [r for r in detected if r['reported'].startswith('~')]
    undet = [r for r in rows if not r.get('reported')]

    print(f"=== mse_census: PROPER milestone extractor over 1104 (cap={cap}) ===\n")
    print(f"total machines          : {len(rows)}")
    print(f"DETECTION RATE (engine read cleanly): {len(detected)}/{len(rows)} "
          f"= {100*len(detected)/len(rows):.1f}%")
    print(f"  -> matched a KNOWN engine {{3/2,4/3,8/3,5/2}} : {len(known)}")
    print(f"  -> candidate-new multiplier                 : {len(cand)}")
    print(f"  -> undetected (needs hand-analysis)         : {len(undet)}\n")

    from collections import Counter
    print("engine census over DETECTED (known):")
    ec = Counter(r['reported'] for r in known)
    for eng, n in ec.most_common():
        print(f"   {eng:8}: {n}")
    print("\ncandidate-new multipliers:")
    cc = Counter(r['reported'] for r in cand)
    for eng, n in cc.most_common():
        print(f"   {eng:14}: {n}")
    print("\nconfidence breakdown over DETECTED:")
    for conf, n in Counter(r['conf'] for r in detected).most_common():
        print(f"   {conf:26}: {n}")
    print("\nsignal source over DETECTED:")
    for s, n in Counter(r['src'] for r in detected).most_common():
        print(f"   {s:10}: {n}")

    print("\n--- COLLAPSE COUNT ---")
    print(f"known-engine instances (collapse to {{3/2,4/3,8/3,5/2}}) : {len(known)}")
    print(f"candidate-new-species with a multiplier                 : {len(cand)}")
    print(f"undetected / needs hand-analysis                        : {len(undet)}")
    print(f"\nrows -> {OUT}")
