#!/usr/bin/env python3
"""x2au_ladder.py -- claim audit probe #3 for lean/X2.lean §5o.

X2.lean §5o (~line 2652) claims, as "the load-bearing evidence":

  "The load-bearing evidence is the comb-at-carry LADDER (main-loop independently
   inspected, g=2 K=10): carries fire at `comb = 2^m-1` with multiplicities
   128,64,32,16,8,4,2,1 = 2^(K-1-m) across 8 levels"

and earlier: "the comb-at-carry profile is a clean power-of-2 ladder (carry at
`comb=2^m-1` fires exactly `2^(K-1-m)` times)".

This probe separates the two populations the prose conflates:
  (a) the CHEW-START comb histogram (what x2fr_counts.py's `combhist` actually
      computes: Counter(c for b,c in cs) over ALL chew-starts), and
  (b) the comb histogram restricted to the CARRY events (the up-regenerations
      that Cfaithful counts).

If the ladder 128,...,1 belongs to (a) and not (b), the word "carry" in the §5o
prose is a mislabel: the ladder's total is 255+2 = 257, whereas Cfaithful 10 = 192.
"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs


def chew_starts(g):
    sim = build(g); sim.step()
    miles = 0
    starts = []
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6:
                break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            starts.append((right_first_block(sim), left_comb_pairs(sim)))
        if not sim.step():
            break
    cs = []
    for i in range(len(starts)):
        blk = starts[i][0]
        p = starts[i - 1][0] if i > 0 else -1
        nx = starts[i + 1][0] if i + 1 < len(starts) else -1
        if blk >= 5 and blk > p and blk >= nx:
            cs.append(starts[i])
    return cs


def analyze(g):
    K = g + 8
    cs = chew_starts(g)
    # (a) chew-start comb histogram (x2fr_counts.py's `combhist`)
    hist_all = Counter(c for b, c in cs if c > 0)
    # (b) carry events: the up-regeneration runs (x2fr_counts.py's carry definition)
    carry_idx = []
    i = 0
    while i < len(cs):
        if i > 0 and cs[i][0] > cs[i - 1][0]:
            j = i
            carry_idx.append(i)
            while j + 1 < len(cs) and cs[j + 1][0] > cs[j][0]:
                j += 1
                carry_idx.append(j)
            i = j + 1
        else:
            i += 1
    hist_carry = Counter(cs[i][1] for i in carry_idx)
    ncarry = len(carry_idx)

    def Cf(K): return 3 * 2 ** (K - 4) + (0 if K % 2 == 0 else 2)

    print(f"=== g={g}  K={K} ===")
    print(f"  total chew-starts        = {len(cs)}")
    print(f"  total carries (Cfaithful)= {ncarry}   closed form Cfaithful({K}) = {Cf(K)}"
          f"   -> {'MATCH' if ncarry == Cf(K) else 'MISMATCH'}")
    print()
    print(f"  (a) comb histogram over ALL CHEW-STARTS  (x2fr_counts.py `combhist`):")
    print(f"      {dict(sorted(hist_all.items()))}")
    lad = {c: n for c, n in sorted(hist_all.items()) if (c + 1) & c == 0}
    print(f"      restricted to comb = 2^m-1 : {lad}   sum = {sum(lad.values())}")
    print(f"      §5o ladder law 2^(K-1-m):")
    for c, n in lad.items():
        m = (c + 1).bit_length() - 1
        pred = 2 ** (K - 1 - m)
        print(f"        comb={c:4d} (m={m})  measured={n:4d}  2^({K}-1-{m})={pred:4d}"
              f"  {'OK' if n == pred else 'MISMATCH'}")
    print()
    print(f"  (b) comb histogram over CARRY EVENTS only:")
    print(f"      {dict(sorted(hist_carry.items()))}   sum = {sum(hist_carry.values())}")
    print()
    print(f"  VERDICT: the 128,64,32,16,8,4,2,1 ladder lives in population (a)")
    print(f"           (chew-starts, total {sum(lad.values())}), NOT in the carry")
    print(f"           population (b) (total {ncarry} = Cfaithful {K}).")
    print(f"           128+64+32+16+8+4+2+1 = {128+64+32+16+8+4+2+1} != Cfaithful({K}) = {Cf(K)}")


if __name__ == '__main__':
    analyze(2)
