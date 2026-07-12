#!/usr/bin/env python3
"""x2ca_repack.py -- confirm the culminating carry repack is exactly sweepEF(2^j-2)
on the real orbit at each level j (single forward pass, no peeking).

A sweepEF tile = 2 steps E:0->1RF, F:1->1RE (pos +2, E on next 0).  We track a
running tile-count whenever we are E-on-0 with a (10) to the right; a maximal run
of length m corresponds to sweepEF m repacking (10)^m -> 1^{2m}.  Report first
occurrence of each m and the window [n0,n0+2m].
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def scan(g):
    sim = build(g); sim.step()
    miles = 0
    firsts = {}
    run_start_n = None
    run_len = 0
    prev = None  # ('E0start', pos)
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6:
                break
        if miles >= 5:
            # at an E-on-0 with a 1 to the right -> a tile is about to fire
            is_tile = (sim.st == 'E' and sim.h == 0 and sim.R and sim.R[-1] == 1)
            if is_tile:
                if run_len == 0:
                    run_start_n = sim.n
                run_len += 1
                # execute the 2-step tile
                if not sim.step():
                    break
                if not sim.step():
                    break
                continue
            else:
                if run_len >= 3:
                    m = run_len
                    if m not in firsts:
                        firsts[m] = (run_start_n, run_start_n + 2 * m)
                run_len = 0
        if not sim.step():
            break
    return firsts


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    firsts = scan(g)
    print(f"g={g}: first occurrence of each maximal sweepEF-run length m:")
    for j in range(3, 8):
        m = 2 ** j - 2
        if m in firsts:
            n0, n1 = firsts[m]
            print(f"  j={j} m={m} (block 2m={2*m}=2^{j+1}-4): n=[{n0},{n1}] {n1-n0} steps  == sweepEF {m}")
        else:
            mx = max(firsts) if firsts else 0
            print(f"  j={j} m={m}: NOT FOUND (max m seen = {mx})")
    print(f"  all run-lengths seen: {sorted(firsts)}")
