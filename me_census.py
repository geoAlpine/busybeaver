#!/usr/bin/env python3
"""
me_census.py -- run the (GATE-FAILED) multiplier extractor across the 1104 BB(6) holdouts in
STRICT OBSERVE-ONLY mode. Because me_extract.py did NOT pass its validation gate (0/16 known
multipliers recovered by the primary estimator; the slow-side estimator is non-identifying --
Antihydra and o15 collide at R~6.88), this run produces NO trusted engine assignments. It only
CHARACTERIZES the width-independent signal at 1104-scale to quantify the collapse obstruction:
  - does a growing fast-side milestone signal exist?
  - rho_time distribution (predicted ~1 for the digit-string polynomial-width majority)
  - slow-side geometric signal presence + best (p/q)^m proxy (non-identifying)
Every number is [OBSERVED, extractor proxy]. Decides NO halting. No engine is assigned.
Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
No machine decided. No label upgraded.
"""
import sys, json, math
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from me_extract import extract
from fractions import Fraction

HOLD = '/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt'


def work(args):
    i, sp, cap = args
    try:
        c = extract(sp, cap=cap, sample_val=False)
    except Exception as e:
        return dict(spec=sp, err=str(e))
    return dict(spec=sp, out=c['out'], nfast=c['nfast'], nslow=c['nslow'],
                rho_time=c['rho_time'], rho_slow=c['rho_slow'],
                slow_hits=c['slow_hits'])


if __name__ == "__main__":
    import multiprocessing as mp
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 1_500_000
    OUT = sys.argv[2] if len(sys.argv) > 2 else '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad/me_census_rows.json'
    specs = [l.strip() for l in open(HOLD) if l.strip()]
    args = [(i, sp, cap) for i, sp in enumerate(specs)]
    ctx = mp.get_context('fork')
    with ctx.Pool(8) as pool:
        rows = pool.map(work, args, chunksize=8)
    json.dump(rows, open(OUT, 'w'))

    n = len(rows)
    halted = [r for r in rows if r.get('out') == 'HALT']
    errs = [r for r in rows if 'err' in r]
    # rho_time signal
    rt = [r['rho_time'] for r in rows if r.get('rho_time')]
    rt_flat = [x for x in rt if x is not None and 0.9 < x < 1.1]   # ~1 (digit-string/poly)
    rt_geo = [x for x in rt if x is not None and x >= 1.1]          # genuinely geometric time
    # slow-side geometric signal present
    has_slow = [r for r in rows if r.get('rho_slow') and r['rho_slow'] > 1.05]
    # best proxy engine from slow hits (NON-IDENTIFYING; recorded only for the census)
    from collections import Counter
    slowtags = Counter()
    for r in rows:
        for name, m in (r.get('slow_hits') or [])[:1]:
            slowtags[name] += 1

    print(f"=== me_census: 1104 holdouts, OBSERVE-ONLY (extractor GATE FAILED) cap={cap} ===")
    print(f"machines            : {n}")
    print(f"HALT within cap     : {len(halted)}   (sound only if simulate reached halt)")
    print(f"errors/overflow     : {len(errs)}")
    print(f"--- primary estimator rho_time (per-macro-period step-gap ratio) ---")
    print(f"  rho_time ~ 1 (flat/poly, digit-string signature): {len(rt_flat)}")
    print(f"  rho_time >= 1.1 (genuinely geometric TIME=unary?): {len(rt_geo)}")
    if rt_geo:
        print(f"    geometric-time rho_time values (sorted): "
              f"{[round(x,3) for x in sorted(rt_geo)][:40]}")
    print(f"--- slow-side geometric cross-check (NON-IDENTIFYING: (p/q)^m, m unknown) ---")
    print(f"  machines with a slow-side geometric signal (R>1.05): {len(has_slow)}")
    print(f"  slow best-tag histogram (PROXY ONLY, do not trust): {dict(slowtags)}")
    print(f"--- CERTIFIED engine assignments: 0 (gate failed; nothing trusted) ---")
    print(f"rows -> {OUT}")
    print("No machine decided. No label upgraded.")
