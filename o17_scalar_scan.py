#!/usr/bin/env python3
"""
o17 TEST 1 re-verification (2026-07-22): is the gate-safety branch b(d) a function of
any scalar residue N = sum d_i * base^i  mod M?

Uses the audited reference oracle (o17_ref_audit.ref_run), not o17d's Fmu.
Extends the recorded sweep: bases 2..12 (recorded 2..8), M 2..256 (recorded 2..64),
LSB- and MSB-first.  Also reports the exact count of (base, M, order) settings tested,
because the record states "0/112" whose provenance is unclear.
"""
from itertools import product
from collections import defaultdict
from o17_ref_audit import ref_run


def build(maxlen, maxdig):
    br = {}
    for m in range(1, maxlen + 1):
        for d in product(range(maxdig + 1), repeat=m):
            v, _s, _t = ref_run(5, list(d))
            if v in (3, 8):
                br[d] = v
    return br


def sweep(branch, bases, mods, tag):
    tested = 0
    hits = []
    for base in bases:
        for order in ('LSB', 'MSB'):
            for M in mods:
                tested += 1
                g = defaultdict(set)
                for d, b in branch.items():
                    dd = d if order == 'LSB' else tuple(reversed(d))
                    N = sum(x * base ** i for i, x in enumerate(dd))
                    g[N % M].add(b)
                if all(len(v) == 1 for v in g.values()):
                    hits.append((base, order, M))
    print(f"  {tag}: {len(hits)} deciding settings out of {tested} (base,order,M) triples "
          f"= {len(bases)} bases x 2 orders x {len(mods)} moduli")
    if hits:
        print(f"    DECIDING SETTINGS FOUND: {hits[:20]}")
    return len(hits), tested


def main():
    for (ml, md) in [(4, 4), (5, 3)]:
        branch = build(ml, md)
        n8 = sum(1 for v in branch.values() if v == 8)
        print(f"=== ensemble mu=5, len 1..{ml}, dig 0..{md}: {len(branch)} configs, "
              f"HALT {n8} ({100.0*n8/len(branch):.1f}%), safe {len(branch)-n8} "
              f"({100.0*(len(branch)-n8)/len(branch):.1f}%) ===")
        sweep(branch, range(2, 9), range(2, 65), "recorded range (base 2..8, M<=64)")
        sweep(branch, range(2, 13), range(2, 257), "extended  range (base 2..12, M<=256)")
        print()


if __name__ == "__main__":
    main()
