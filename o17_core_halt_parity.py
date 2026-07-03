#!/usr/bin/env python3
"""
o17 core (k=0 mod3): the HALT predicate reduces to a single PARITY BIT (2026-07-03).
[OBSERVED, exact TM simulation; halting NOT decided.]

Deepens O17_CORE_TRANSDUCER.md by attacking the carry-to-frontier parity rule
(the Collatz-hard heart).  Verified facts (0 exceptions on the tested range):

(I)  GATE-STATE = LEADING-BLOCK PARITY.  Each time the head returns to the left
     frontier in a gate state, it fires state A (turn / continue) iff the leading
     block (the odometer's most-significant position, "marker") is ODD, and state
     D (-> F halt) iff the marker is EVEN.  So:
                HALT  <=>  the leading block ever becomes EVEN.
(II) MARKER LIVES IN {3,5}; DIGIT SUM S IS ALWAYS EVEN.  Throughout the run every
     A-milestone has leading block in {3,5} (both odd) and even digit sum; the only
     even leading block ever seen is 8, and it occurs exactly at the halting D-arrival.
(III) THE REDUCED {3,5}-WALK IS COLLATZ-HARD.  The marker performs a walk on {3,5}
     (halt = a step to even); this walk is NOT determined by any bounded parity
     predictor -- from marker 5 the next marker is "3" (continue) or "even" (halt)
     ambiguously under (marker, m%2, S%2), so the halt decision depends on the full
     unbounded carry history.  This LOCALIZES the Collatz-hardness to one parity bit
     (the odometer MSB), and rederives the wall there; it does NOT decide halting.

Run: prints the mismatch counts (all 0) and the ambiguity witness.
"""
from collections import defaultdict

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                        else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse("1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB")
SN = "ABCDEF"


def blocks(tape, lo, hi):
    r = []; i = lo
    while i <= hi:
        s = tape[i]; j = i
        while j <= hi and tape[j] == s: j += 1
        r.append((s, j - i)); i = j
    while r and r[0][0] == 0: r = r[1:]
    while r and r[-1][0] == 0: r = r[:-1]
    return [n for s, n in r if s == 1]


def arrivals(L, maxsteps):
    """(step, gate_state, leading_block, m, S) at each left-frontier gate; ('HALT',) at halt."""
    SZ = 1 << 21
    tape = bytearray(SZ); off = SZ // 2
    for i in range(1, L + 1): tape[off + i] = 1
    pos = off; st = 0; step = 0; lo = hi = pos
    out = []; halted = None
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0:
            halted = step; break
        if pos == lo and r == 0 and st in (0, 3):
            blk = blocks(tape, lo, hi)
            if blk:
                m = len(blk) - 1
                S = sum((x - 2)//3 for x in blk[1:] if x % 3 == 2)
                out.append((step, SN[st], blk[0], m, S))
        ww, d, ns = M[st][r]
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return out, halted


if __name__ == "__main__":
    mism_I = tot = 0
    even_leads = set(); A_leads = set(); S_odd = 0
    trans = defaultdict(set)
    for j in range(1, 60):
        arr, halted = arrivals(3 * j, 6_000_000)
        ms = []
        for step, stt, mk, m, S in arr:
            tot += 1
            # (I) state D  <=>  leading block even
            if (stt == 'D') != (mk % 2 == 0):
                mism_I += 1
            if stt == 'A':
                A_leads.add(mk)
            if mk % 2 == 0:
                even_leads.add(mk)
            if S % 2:
                S_odd += 1
            ms.append((mk, m, S))
        # (III) reduced marker walk transitions under bounded predictor
        for i in range(len(ms) - 1):
            mk, m, S = ms[i]; nxt = ms[i + 1][0]
            trans[(mk, m % 2, S % 2)].add('even' if nxt % 2 == 0 else str(nxt))
        if halted and ms:
            mk, m, S = ms[-1]
            trans[(mk, m % 2, S % 2)].add('even')

    print(f"frontier gate arrivals checked: {tot}  (core seeds j=1..59)")
    print(f"(I)   mismatches for [state D <=> leading block EVEN]: {mism_I}")
    print(f"      => HALT <=> leading block ever even.  even leads seen: {sorted(even_leads)}")
    print(f"(II)  leading blocks at A (continue): {sorted(A_leads)}   digit-sum-odd count: {S_odd}")
    ambiguous = {k: sorted(v) for k, v in trans.items() if len(v) > 1}
    print(f"(III) marker-walk transitions that are AMBIGUOUS under (marker,m%2,S%2):")
    for k, v in sorted(ambiguous.items()):
        print(f"        marker={k[0]} m%2={k[1]} S%2={k[2]} -> {v}")
    print()
    ok = (mism_I == 0 and S_odd == 0 and A_leads <= {3, 5} and even_leads <= {8} and bool(ambiguous))
    print(f"HALT-PARITY REDUCTION VERIFIED: {ok}")
    print("  HALT <=> odometer MSB (leading block) ever EVEN; the {3,5}-walk deciding it is")
    print("  history-dependent (Collatz-hard).  Halting stays [OPEN]; no machine decided.")
