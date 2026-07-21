#!/usr/bin/env python3
"""
o17 Myhill-Nerode re-verification (2026-07-22), using the audited reference oracle
from o17_ref_audit.py (0/780 mismatch vs o17d_finite_state.Fmu, lean anchors green).

Purpose: the recorded index sequences in O17_GATE_DECISION_ATTEMPT_2026-07-10.md
  digits 0..3 : 1,2,6,19,54,132
  digits 0..4 : 1,2,7,25,77
do NOT reproduce under the script's documented default suffix battery (len 0..3, dig 0..3),
which gives 1,2,6,19,60,153 and 1,2,7,26,88.  This script scans the suffix-battery
parameter space to identify what the recorded run actually used, and reports the
best (largest-battery) lower bounds on the Nerode index.
"""
import sys
from itertools import product
from o17_ref_audit import ref_run

CACHE = {}
NONE_HITS = set()


def b(d):
    if d not in CACHE:
        r, _s, _t = ref_run(5, list(d))
        if r not in (3, 8):
            NONE_HITS.add(d)
        CACHE[d] = r
    return CACHE[d]


def nerode(maxlen, maxdig, suf_len, suf_dig):
    suffixes = [tuple(s) for sl in range(0, suf_len + 1)
                for s in product(range(suf_dig + 1), repeat=sl)]
    out = []
    for plen in range(0, maxlen + 1):
        classes = set()
        for p in product(range(maxdig + 1), repeat=plen):
            classes.add(tuple(b(tuple(p) + s) for s in suffixes))
        out.append(len(classes))
    return out, len(suffixes)


def main():
    print("=== A. reproduce with the script's DOCUMENTED default battery (len<=3, dig<=3) ===")
    for (ml, md, rec) in [(5, 3, [1, 2, 6, 19, 54, 132]), (4, 4, [1, 2, 7, 25, 77])]:
        got, ns = nerode(ml, md, 3, 3)
        print(f"  digits 0..{md}, maxlen {ml}, battery {ns}: got {got}")
        print(f"                                    recorded {rec}   MATCH={got == rec}")

    print("\n=== B. scan suffix-battery params to locate the recorded run ===")
    for (ml, md, rec) in [(5, 3, [1, 2, 6, 19, 54, 132]), (4, 4, [1, 2, 7, 25, 77])]:
        print(f"  -- target digits 0..{md}, maxlen {ml}: recorded {rec}")
        for sl in range(0, 5):
            for sd in range(0, 5):
                if (sd + 1) ** sl > 400:
                    continue
                got, ns = nerode(ml, md, sl, sd)
                flag = "  <<< MATCHES RECORD" if got == rec else ""
                print(f"     suflen={sl} sufdig={sd} (battery {ns:>4}): {got}{flag}")

    print("\n=== C. best available lower bounds (largest battery run) ===")
    for (ml, md) in [(5, 3), (4, 4), (6, 3)]:
        got, ns = nerode(ml, md, 4, 3)
        ratios = [round(got[i + 1] / got[i], 2) for i in range(len(got) - 1)]
        print(f"  digits 0..{md}, maxlen {ml}, battery {ns}: {got}   ratios {ratios}")

    print(f"\n  oracle calls cached: {len(CACHE)};  non-{{3,8}} (cap/off-language) results: "
          f"{len(NONE_HITS)}")
    if NONE_HITS:
        print(f"    WARNING: {len(NONE_HITS)} configs did not resolve to a branch; "
              f"examples {sorted(NONE_HITS)[:5]}")


if __name__ == "__main__":
    main()
