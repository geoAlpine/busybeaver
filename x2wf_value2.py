#!/usr/bin/env python3
"""x2wf_value2.py -- is there a STRUCTURAL odometer VALUE V (decoded from the tape,
NOT the step count) that strictly increases every outer tick, giving a clean
well-founded measure mu = Vtarget - V ?

Binary-counter reading:  the LEFT comb (pairs) is the low accumulator; every
cascade block 1^{2^j-3} to the RIGHT of the head is a placed 'digit' of weight
2^j.  We test V = comb + sum over RIGHT blocks of 2^{level}, level=log2(len+3),
and also the pure comb-accumulator, for strict monotonicity across E-on-0 ticks
and across chew-starts.
"""
import sys, math
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, total_ones, left_comb_pairs


def blocks_right(sim):
    bits = [sim.h] + sim.R[::-1]
    runs = []
    i = 0
    while i < len(bits):
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b:
            j += 1
        if b == 1:
            runs.append(j - i)
        i = j
    return runs


def odo_value(sim):
    """weighted odometer value: sum over right blocks of 2^level (level from length),
    plus the left comb as the low digit."""
    v = 0
    for L in blocks_right(sim):
        lvl = round(math.log2(L + 3)) if L >= 1 else 0
        v += 1 << lvl
    return v


def run(g):
    sim = build(g); sim.step()
    miles = 0
    e0 = []           # (n, blk, comb, Vodo, Lones, ones)
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6:
                break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            e0.append((sim.n, right_first_block(sim), left_comb_pairs(sim),
                       odo_value(sim), sum(sim.L), total_ones(sim)))
        if not sim.step():
            break
    return e0


def mono_report(name, seq):
    inc = dec = eq = 0
    mindelta = 10**18; maxdelta = -10**18
    for i in range(1, len(seq)):
        d = seq[i] - seq[i-1]
        if d > 0: inc += 1
        elif d < 0: dec += 1
        else: eq += 1
        mindelta = min(mindelta, d); maxdelta = max(maxdelta, d)
    print(f"  {name:<24} steps={len(seq)-1:<7} inc={inc:<7} dec={dec:<6} eq={eq:<6} "
          f"delta in [{mindelta},{maxdelta}]  nondecreasing={dec==0}")


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    e0 = run(g)
    print(f"=== g={g}: {len(e0)} E-on-0 ticks. monotonicity of candidate measures ===")
    mono_report("comb pairs", [t[2] for t in e0])
    mono_report("Lones (left ones)", [t[4] for t in e0])
    mono_report("total ones", [t[5] for t in e0])
    mono_report("Vodo (weighted)", [t[3] for t in e0])
    # chew-starts only
    cs = []
    prev = -1
    for i, t in enumerate(e0):
        blk = t[1]
        nxt = e0[i+1][1] if i+1 < len(e0) else -1
        if blk >= 5 and blk > prev and blk >= nxt:
            cs.append(t)
        prev = blk
    print(f" chew-starts only ({len(cs)}):")
    mono_report("Vodo @ chew-starts", [t[3] for t in cs])
    mono_report("comb @ chew-starts", [t[2] for t in cs])
    # cumulative comb deposits: total left-ones is the true monotone build?
    print(" first/last Lones:", e0[0][4], e0[-1][4], " min:", min(t[4] for t in e0))
