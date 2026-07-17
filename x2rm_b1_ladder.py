#!/usr/bin/env python3
"""x2rm_b1_ladder.py -- AUDIT B1: is §5o's "comb-at-carry LADDER (128,64,...,1)"
actually measured over CARRIES, or over CHEW-STARTS?

§5o (lean/X2.lean:2653-2656) and x2fr_register.py:13 both claim:
   "carries fire at comb=2^m-1 with multiplicities 128,64,32,16,8,4,2,1"
Sum = 255.  But Cfaithful(10) = 192.  A histogram of carry events must sum to the
number of carry events.  255 != 192  =>  the ladder is NOT a carry histogram.

This probe recomputes, from x2bd_sim.build(2) (K=10), BOTH histograms separately.
"""
import sys
from collections import Counter
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs

def measure(g):
    sim = build(g); sim.step()
    miles = 0
    starts = []
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6: break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            starts.append((right_first_block(sim), left_comb_pairs(sim)))
        if not sim.step():
            break
    # chew-starts (x2fr_counts definition, verbatim)
    cs = []
    for i in range(len(starts)):
        blk = starts[i][0]
        p  = starts[i-1][0] if i > 0 else -1
        nx = starts[i+1][0] if i+1 < len(starts) else -1
        if blk >= 5 and blk > p and blk >= nx:
            cs.append(starts[i])
    # carries = up-regenerations (ripple), recording the comb AT EACH CARRY EVENT
    ncarry = 0; depths = {}; carry_combs = []
    i = 0
    while i < len(cs):
        if i > 0 and cs[i][0] > cs[i-1][0]:
            d = 1; j = i
            carry_combs.append(cs[i][1])          # the comb at this carry event
            while j+1 < len(cs) and cs[j+1][0] > cs[j][0]:
                d += 1; j += 1
                carry_combs.append(cs[j][1])      # ... and at each ripple level
            depths[d] = depths.get(d,0)+1
            ncarry += d
            i = j+1
        else:
            i += 1
    return cs, ncarry, depths, carry_combs

for g, K in ((2, 10), (3, 11)):
    cs, ncarry, depths, carry_combs = measure(g)
    print("="*70)
    print(f"g={g}  K={K}   chew-starts T={len(cs)}   carries C={ncarry}   depths={depths}")
    print()
    # (a) THE HISTOGRAM x2fr_counts.py ACTUALLY COMPUTES (label: "comb-at-carry")
    mislabeled = Counter(c for b, c in cs if c > 0)
    print("(a) x2fr_counts.py:47  `Counter(c for b,c in cs if c>0)`  [labelled 'comb-at-carry']")
    print(f"    -> {dict(sorted(mislabeled.items()))}")
    print(f"    domain = CHEW-STARTS (cs), comb=0 dropped by the `if c>0` filter")
    print(f"    sum = {sum(mislabeled.values())}   (vs C={ncarry}, T={len(cs)})")
    print()
    # (b) the SAME over chew-starts WITHOUT the c>0 filter
    cs_all = Counter(c for b, c in cs)
    print(f"(b) chew-start comb histogram, NO filter -> {dict(sorted(cs_all.items()))}")
    print(f"    sum = {sum(cs_all.values())} = T = {len(cs)}  [consistent: partitions chew-starts]")
    print()
    # (c) the TRUE comb-at-CARRY histogram
    true_carry = Counter(carry_combs)
    print(f"(c) TRUE comb-at-CARRY histogram (comb recorded at each carry event)")
    print(f"    -> {dict(sorted(true_carry.items()))}")
    print(f"    sum = {sum(true_carry.values())} = C = {ncarry}  [consistent: partitions carries]")
    print(f"    events at comb=0: {true_carry.get(0,0)}      events at comb=3: {true_carry.get(3,0)}")
    print()
    # (d) THE LADDER LAW: is it exact over chew-starts at comb=2^m-1?
    print("(d) LADDER LAW  `multiplicity(comb=2^m-1) == 2^(K-1-m)`  tested on BOTH domains:")
    print(f"    {'m':>2} {'comb=2^m-1':>10} {'2^(K-1-m)':>10} | {'chew-starts':>12} {'carries':>8}")
    for m in range(1, 11):
        comb = 2**m - 1
        pred = 2**(K-1-m) if K-1-m >= 0 else None
        got_cs = cs_all.get(comb, 0)
        got_ca = true_carry.get(comb, 0)
        mark = "OK " if pred == got_cs else "NO "
        print(f"    {m:>2} {comb:>10} {str(pred):>10} | {got_cs:>12} {mark} {got_ca:>8}")
    print()
    print(f"    §5o's claimed ladder 128,64,32,16,8,4,2,1 sums to {sum(2**(K-1-m) for m in range(1,9))}")
    print(f"    Cfaithful(10) = 192 (§5o closed form 3*2^(K-4) = 3*2^6 = {3*2**6})")
