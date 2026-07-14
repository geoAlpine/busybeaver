#!/usr/bin/env python3
"""x2cu_anchors.py -- DECISIVE EXPERIMENT part 1.

List every E-on-0 anchor (odometer boundary) in a window, with the step-gap from
the previous anchor, the right-leading block length, left comb-pair count, and the
first few left/right run tokens.  This lets us see the tick/carry structure and
locate the no-carry runs, embedded lower carries, CORE (sweepEF) and residual glue.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def right_first_block(sim):
    seq = [sim.h] + sim.R[::-1]
    i = 0
    while i < len(seq) and seq[i] == 0:
        i += 1
    j = i
    while j < len(seq) and seq[j] == 1:
        j += 1
    return j - i


def left_comb_pairs(sim):
    L = sim.L
    n = len(L)
    pairs = 0
    i = 0
    while i + 1 < n and L[-1 - i] != L[-1 - (i + 1)]:
        pairs += 1
        i += 2
    return pairs


def runs(seq, k):
    out = []
    i = 0
    while i < len(seq) and len(out) < k:
        b = seq[i]
        j = i
        while j < len(seq) and seq[j] == b:
            j += 1
        out.append((b, j - i))
        i = j
    return out


def rtok(sim, k=6):
    return runs([sim.h] + sim.R[::-1], k)


def ltok(sim, k=8):
    L = sim.L
    return runs([L[-1 - i] for i in range(len(L))], k)


def main():
    n0 = int(sys.argv[1]) if len(sys.argv) > 1 else 6480
    n1 = int(sys.argv[2]) if len(sys.argv) > 2 else 8100
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    prev_n = None
    print(f"# E-on-0 anchors in n=[{n0},{n1}]   (gap = steps since prev anchor)")
    print(f"#  n      gap   blk  comb  pos    Lruns                     Rruns")
    while sim.n <= n1:
        if sim.st == 'E' and sim.h == 0:
            gap = '' if prev_n is None else (sim.n - prev_n)
            lt = ltok(sim); rt = rtok(sim)
            print(f"  {sim.n:<7}{str(gap):<6}{right_first_block(sim):<5}"
                  f"{left_comb_pairs(sim):<6}{sim.pos:<7}{str(lt):<26}{rt}")
            prev_n = sim.n
        if not sim.step():
            break


if __name__ == "__main__":
    main()
