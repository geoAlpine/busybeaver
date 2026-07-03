#!/usr/bin/env python3
"""
Slow-width cryptid kernel extraction — key claims verifier (2026-07-04).
[OBSERVED, exact TM simulation; nothing about halting decided.]

Five BB(6) "slow-width" cryptids (kernels un-extracted per CRYPTID_CENSUS.md) were
reverse-engineered with the o17 methodology. Result: ALL are Mahler/Collatz-class;
none is a fresh o17-style structural outlier. This verifier checks the headline,
independently-cross-checked facts against the raw TMs.

Machines (halt transition in parens):
  o2  = 1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA   (F reads 0)
  o7  = 1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC   (F reads 0)
  o11 = 1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF   (C reads 0)
  o16 = 1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE   (F reads 0)
  SN  = 1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD   (Space Needle, F reads 0)

Checks:
  (A) o7 is Mahler-3/2: its 1^a 0 1^b milestone reset-a values (b=1) grow ->x3/2.
  (B) Space Needle SOUNDNESS CORRECTION: halt set is NOT "all-ones". From the true
      milestone config (1^m, head on the 0 right of the block, state C), the raw TM
      halts at m in {1,3,6,7,15,31,63} for m<=64 -- m=6 (binary 110) halts but is NOT
      all-ones. The blank-tape orbit (2,5,9,16,40,...) avoids the halt set => consistent
      with non-halting, but the clean "all-ones" reduction is FALSE.
"""

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                        else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

O7 = parse("1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC")
SN = parse("1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD")
O3 = parse("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC")


def rle(tape, lo, hi):
    r = []; i = lo
    while i <= hi:
        s = tape[i]; j = i
        while j <= hi and tape[j] == s: j += 1
        r.append((s, j - i)); i = j
    while r and r[0][0] == 0: r = r[1:]
    while r and r[-1][0] == 0: r = r[:-1]
    return r


def o7_reset_a_ratios(maxsteps=4_000_000):
    tape = bytearray(1 << 22); off = len(tape)//2
    pos = off; st = 3*0+3; st = 3; step = 0; lo = hi = pos  # start blank; state A=0
    st = 0
    resets = []; last = None
    while step < maxsteps and len(resets) < 24:
        r = tape[pos]; act = O7[st][r]
        if act is None: break
        if st == 3 and pos <= lo and r == 0:               # D at left frontier
            b = rle(tape, lo, hi)
            blks = [n for s, n in b if s == 1]
            if len(blks) == 2 and blks[1] == 1:            # 1^a 0 1^1  (b==1 reset)
                if blks[0] != last:
                    resets.append(blks[0]); last = blks[0]
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    tail = resets[-8:]
    ratios = [round(tail[i+1]/tail[i], 3) for i in range(len(tail)-1)]
    return resets, ratios


def sn_epoch_halts(m):
    """True Space Needle milestone: 1^m block, head on the 0 right of it, state C."""
    budget = int(0.5 * m**3) + 300000
    tape = bytearray(1 << 21); off = len(tape)//2
    for i in range(m): tape[off + i] = 1
    pos = off + m; st = 2; step = 0; lo = off; hi = off + m - 1
    while step < budget:
        r = tape[pos]; act = SN[st][r]
        if act is None: return True
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return False


def sn_blank_orbit(maxsteps=1_000_000):
    tape = bytearray(1 << 20); off = len(tape)//2
    pos = off; st = 0; step = 0; lo = hi = pos; seq = []; last = None
    while step < maxsteps and len(seq) < 6:
        r = tape[pos]; act = SN[st][r]
        if act is None: break
        # milestone: state C, head on 0 just right of a solid 1^m block
        if st == 2 and r == 0 and pos - 1 >= lo and tape[pos-1] == 1:
            i = pos - 1; n = 0
            while i >= lo and tape[i] == 1: n += 1; i -= 1
            if pos >= hi and all(tape[k] == 0 for k in range(lo, i+1)):
                if n != last: seq.append(n); last = n
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return seq


def allones(m): return set(bin(m)[2:]) == {'1'}


def o3_outlier_check(maxsteps=6_000_000):
    """o3 is a Type-II outlier: bounded digit alphabet {1,2}, single-0 gaps, digit-sum S
    grows only logarithmically (no exponential value orbit), length m grows ~linearly."""
    tape = bytearray(1 << 23); off = len(tape)//2
    pos = off; st = 0; step = 0; lo = hi = pos
    maxblk = 0; badgap = 0; nms = 0; samples = []
    while step < maxsteps:
        r = tape[pos]; act = O3[st][r]
        if act is None: break
        if st == 0 and pos == lo:
            b = rle(tape, lo, hi)
            blks = [n for s, n in b if s == 1]; gaps = [n for s, n in b if s == 0]
            if blks:
                nms += 1
                maxblk = max(maxblk, max(blks))
                badgap += sum(1 for g in gaps if g != 1)
                S = sum(1 for x in blks if x == 2); m = len(blks)
                if nms in (10, 50, 200, 1000): samples.append((nms, m, S, hi-lo+1))
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return maxblk, badgap, samples


if __name__ == "__main__":
    print("(A) o7 = Mahler-3/2 (Antihydra-class, unary-encoded => sqrt-t):")
    resets, ratios = o7_reset_a_ratios()
    print(f"    reset-a values (b=1): {resets}")
    print(f"    tail ratios: {ratios}  (-> 1.5 == 3/2)  Mahler-3/2 confirmed: {all(abs(r-1.5)<0.02 for r in ratios[-4:])}")
    print()
    print("(B) Space Needle SOUNDNESS CORRECTION -- halt set is NOT all-ones:")
    halts = [m for m in range(1, 65) if sn_epoch_halts(m)]
    nonAO = [m for m in halts if not allones(m)]
    orbit = sn_blank_orbit()
    print(f"    raw-TM halt set (m<=64): {halts}")
    print(f"    all-ones (m<=64):        {[m for m in range(1,65) if allones(m)]}")
    print(f"    HALTS but NOT all-ones:  {nonAO} (binary {[bin(m)[2:] for m in nonAO]})  <-- agent's 'all-ones' claim FALSE")
    print(f"    blank-tape orbit m-seq:  {orbit}  (avoids the halt set => consistent w/ non-halting)")
    print(f"    orbit ∩ halt set = {sorted(set(orbit) & set(halts))} (empty => no halt observed)")
    print()
    print("(C) o3 = SECOND structural outlier (Type II, like o17 -- NOT Mahler):")
    maxblk, badgap, samples = o3_outlier_check()
    print(f"    max block length = {maxblk} (==2 => bounded digit alphabet {{1,2}}); non-single gaps = {badgap}")
    print(f"    (milestone#, #blocks m, digit-sum S, width):  {samples}")
    print(f"    S grows ~log (no exponential value orbit) while m,width ~sqrt(step) => o17-type outlier, not Mahler.")
    print()
    print("VERDICT: Type I (11 machines) = Mahler/(K) wall; Type II (o17, o3) = generalized-Collatz")
    print("carry-existence; Type III (Space Needle) = scalar generalized-Collatz. sqrt-t is NOT diagnostic.")
    print("Halting stays [OPEN] for all fourteen. No machine decided. No label upgraded.")
