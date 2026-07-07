#!/usr/bin/env python3
"""
Mahler-sea survey — STRUCTURE stage v3: targeted re-extraction for o14, o16, SN (2026-07-07).
  o14: counters are blocks 0 and 2 (shape [a,1,b,1^m,4,4,2]); within-epoch (a,b) exchange +
       sub-cycle a-start series (b-drop detection), x3/2 correction distribution.
  o16: shape [k, 1^m(sea), d(defect)]; sea law between defect==4 milestones; defect series.
  SN : all resets incl. 3-block phase [1,b,c]; does the x5/2 chain continue in b+c?
[OBSERVED]. Decides nothing.
"""
import sys
from collections import Counter
from msea_struct2 import parse, run_milestones, corr_dist

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000

    # --- o14 ---
    snaps = run_milestones("1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", 4, 'L', N)
    print(f"=== o14: {len(snaps)} milestones")
    pairs = [(s, b[0], b[2]) for s, b in snaps if len(b) >= 3 and b[1] == 1]
    da = Counter((pairs[i+1][1] - pairs[i][1], pairs[i+1][2] - pairs[i][2]) for i in range(len(pairs) - 1))
    print(f"  within-epoch (da,db) on blocks (0,2): {dict(da.most_common(5))}")
    # sub-cycle start: b (block 2) drops by a lot (merge/reset)
    astarts = [pairs[i+1] for i in range(len(pairs) - 1) if pairs[i+1][2] < pairs[i][2] - 2]
    aser = [a for _, a, _ in astarts]
    print(f"  sub-cycle starts (b-drop): {len(astarts)}; a series head: {aser[:12]} tail: {aser[-4:]}")
    corr_dist(aser, 3, 2, "o14 a-start")
    bmin = Counter(b for _, _, b in astarts)
    print(f"  b value at restart: {dict(bmin.most_common(6))}")
    print()

    # --- o16 ---
    snaps = run_milestones("1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE", 0, 'R', N)
    print(f"=== o16: {len(snaps)} milestones")
    tri = [(s, b[0], len(b) - 2, b[-1]) for s, b in snaps
           if len(b) >= 3 and all(x == 1 for x in b[1:-1])]
    print(f"  [k | 1^m sea | defect d] milestones: {len(tri)}")
    d4 = [(s, k, m) for s, k, m, d in tri if d == 4]
    ms = [m for _, _, m in d4]
    ks = [k for _, k, _ in d4]
    print(f"  defect==4 sub-cycle starts: {len(d4)}; sea m head: {ms[:12]} tail: {ms[-4:]}")
    print(f"    k at those: head {ks[:12]} tail {ks[-4:]}")
    corr_dist(ms, 3, 2, "o16 sea")
    dser = [d for _, _, _, d in tri]
    print(f"  defect series head: {dser[:16]} tail: {dser[-6:]}")
    print()

    # --- SN ---
    snaps = run_milestones("1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD", 0, 'L', N)
    print(f"=== SN: {len(snaps)} milestones")
    resets2 = [(s, b) for s, b in snaps if len(b) == 2 and b[0] == 1]
    resets3 = [(s, b) for s, b in snaps if len(b) == 3 and b[0] == 1]
    print(f"  2-block resets [1,b]: {[(s, b[1]) for s, b in resets2]}")
    print(f"  3-block resets [1,b,c] (first 10): {[(s, b[1], b[2]) for s, b in resets3][:10]}")
    # combined mass chain at resets: total = sum of blocks
    allr = sorted(resets2 + resets3)
    tser = [sum(b) - 1 for _, b in allr]
    print(f"  reset total-mass series (excl. lead 1): {tser}")
    corr_dist(tser, 5, 2, "SN reset mass")
    # 3-block generations census: how often does the epoch run in 3-block phase?
    n3 = sum(1 for _, b in snaps if len(b) == 3)
    n2 = sum(1 for _, b in snaps if len(b) == 2)
    print(f"  phase census: 2-block gens {n2}, 3-block gens {n3}")
    print()
    print("STRUCTURE v3 [OBSERVED]. No machine decided. No label upgraded.")
