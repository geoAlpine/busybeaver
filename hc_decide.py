#!/usr/bin/env python3
"""hc_decide.py -- run the trusted suite.verdict on a targeted list (fork-parallel).
Any HALTS / NEVER_HALTS is a SOUND candidate decision -> flag for red-team."""
import sys, multiprocessing as mp
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from suite import verdict


def work(sp):
    try:
        v, w = verdict(sp, sim_cap=2_000_000, bsteps=20_000, bmacro=3000)
        return (sp, v, str(w))
    except Exception as e:
        return (sp, 'ERR', str(e)[:60])


if __name__ == "__main__":
    path = sys.argv[1]
    specs = [l.strip() for l in open(path) if l.strip()]
    ctx = mp.get_context('fork')
    with ctx.Pool(8) as pool:
        res = pool.map(work, specs)
    from collections import Counter
    c = Counter(v for _, v, _ in res)
    print(f"=== suite.verdict on {len(specs)} machines ===")
    for k, v in c.most_common():
        print(f"  {k}: {v}")
    for sp, v, w in res:
        if v not in ('HOLDOUT',):
            print(f"  ** {v} {w}: {sp}")
