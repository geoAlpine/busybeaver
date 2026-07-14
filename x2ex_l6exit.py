#!/usr/bin/env python3
"""Extract EXIT(6) = [12709, carry6_end] and its block-final terminal gap; test
TERM(k)=2^{k+1}+k+5 at k=7 (predict 271).  Also dump the produced top block."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def left_solid(sim):
    L = sim.L; i = 0
    while i < len(L) and L[-1-i] == 1:
        i += 1
    return i


def main():
    sim = build(2); sim.step()
    core_end = 12709
    while sim.n < core_end:
        assert sim.step()
    # walk anchors until we hit the next big fold-peak (lsolid jumps huge) = next core
    anchors = []
    while sim.n < 15600:
        if sim.st == 'E' and sim.h == 0:
            anchors.append((sim.n, left_solid(sim), sim.left_ones(),
                            sim.right_runs(6)))
        if not sim.step():
            break
    # skip the initial core-end anchor (lsolid=124), then stop at next core
    # buildup (lsolid climbs past ~100 again = level-7 MIDDLE core sweep)
    end_idx = len(anchors)
    for i in range(1, len(anchors)):
        if anchors[i][1] > 100:
            end_idx = i
            break
    anchors = anchors[:end_idx+1]
    # terminal = maximal gap in the EXIT
    gaps = [(anchors[i+1][0]-anchors[i][0], anchors[i][0], anchors[i+1][0])
            for i in range(len(anchors)-1)]
    biggest = max(gaps)
    print(f"EXIT(6) core_end={core_end}")
    print(f"  #anchors={len(anchors)}, span to n={anchors[-1][0]}")
    print(f"  BLOCK-FINAL terminal gap = {biggest[0]}  [{biggest[1]}->{biggest[2]}]")
    print(f"  predicted TERM(k=7)=2^8+7+5 = {2**8+7+5}")
    # produced top block: right runs at the anchor after the terminal
    aft = next(a for a in anchors if a[0] == biggest[2])
    rr = " ".join(f"{'1' if b else '0'}^{c}" for b, c in aft[3])
    print(f"  after terminal: lsolid={aft[1]} lones={aft[2]} right={rr}")
    # list the biggest few gaps to see the terminal sequence
    print("  biggest gaps in EXIT(6):")
    for g, s, e in sorted(gaps, reverse=True)[:6]:
        af = next(a for a in anchors if a[0] == e)
        rr = " ".join(f"{'1' if b else '0'}^{c}" for b, c in af[3])
        print(f"    gap {g:>4} [{s}->{e}]  after: lones={af[2]} right={rr}")


if __name__ == "__main__":
    main()
