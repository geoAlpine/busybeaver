#!/usr/bin/env python3
"""
o17 core (k=0 mod3): the HALT predicate reduces to a single PARITY BIT (2026-07-03).
[OBSERVED, exact TM simulation; halting NOT decided.]

Deepens O17_CORE_TRANSDUCER.md by attacking the carry-to-frontier parity rule
(the Collatz-hard heart).  Verified facts (0 exceptions on the tested range):

(I)  GATE-STATE = LEADING-BLOCK PARITY.  [PROVEN from the transitions + OBSERVED
     entry invariant.]  A head moving LEFT over a run of 1s alternates state
     A<->D one step/cell (A,1->1LD ; D,1->1LA), and the gate is A,0->1RB (turn/
     continue) vs D,0->0LF->F,0 HALT.  The final leftward run reaching the frontier
     always starts in state A with length (leading_block - 1) [OBSERVED, 0 exc], so
     the head arrives in A iff the leading block is ODD, D (halt) iff EVEN.  The gate
     reads exactly ONE BIT -- the parity of the leading ("marker") block -- and
     NOTHING about the digit string (S, m, digit values all irrelevant).  So:
                HALT  <=>  the leading (marker) block ever becomes EVEN.
(II) THE MARKER IS A 3-STATE AUTOMATON {3,5,8}.  Writing marker = 2 + 3e (the
     odometer's TOP digit): 3 and 5 are odd (e=?,1 -> continue), 8 is the unique even
     value (e=2 -> halt).  Observed edges (0 exc): 3 -> {3,5}, 5 -> {3, 8=HALT},
     8 = HALT; start 3.  Every halter's gate sequence ends ... A3 A5 D8 = HALT.
     Also: digit sum S is always even at milestones.
(III) THE 5->8 STEP IS COLLATZ-HARD.  Halt <=> a bounce with marker 5 whose returning
     carry INCREMENTS the top digit (5->8, a parity-flipping +3) rather than RESETS it
     (5->3).  This 5->8-vs-5->3 choice is NOT a function of any bounded local feature
     (marker, m%2, S%2 all coincide on halting and continuing marker-5 milestones); it
     is emitted by the full unbounded carry cascade (o17_core_counter.py).  So halting
     = "the top-digit automaton ever steps 5->8", driven by the Collatz-hard carry
     stream.  Localizes the wall to ONE parity bit; does NOT decide halting.

Run: prints the mismatch counts (all 0), the automaton edges, and the ambiguity witness.
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
    mism_I = mism_par = tot = 0
    even_leads = set(); A_leads = set(); S_odd = 0
    edges = defaultdict(set); trans = defaultdict(set)
    for j in range(1, 60):
        arr, halted = arrivals(3 * j, 6_000_000)
        ms = []
        for step, stt, mk, m, S in arr:
            tot += 1
            # (I) state D  <=>  leading block even ; and gate == (A iff leading odd)
            if (stt == 'D') != (mk % 2 == 0):
                mism_I += 1
            if stt != ('A' if mk % 2 == 1 else 'D'):
                mism_par += 1
            if stt == 'A':
                A_leads.add(mk)
            if mk % 2 == 0:
                even_leads.add(mk)
            if S % 2:
                S_odd += 1
            ms.append((mk, m, S))
        # (II) marker automaton edges ; (III) bounded-predictor ambiguity
        for i in range(len(ms) - 1):
            mk, m, S = ms[i]; nxt = ms[i + 1][0]
            edges[mk].add(nxt)
            trans[(mk, m % 2, S % 2)].add('even' if nxt % 2 == 0 else str(nxt))
        if halted and ms:
            mk, m, S = ms[-1]
            edges[mk].add(8)
            trans[(mk, m % 2, S % 2)].add('even')

    print(f"frontier gate arrivals checked: {tot}  (core seeds j=1..59)")
    print(f"(I)   mismatches for [gate state == (A iff leading ODD, D iff EVEN)]: {mism_par}")
    print(f"      => HALT <=> leading (marker) block ever even.  even leads seen: {sorted(even_leads)}")
    print(f"(II)  marker automaton edges: {{{', '.join(f'{k}->{sorted(v)}' for k,v in sorted(edges.items()))}}}")
    print(f"      leading blocks at A (continue): {sorted(A_leads)}   digit-sum-odd count: {S_odd}")
    ambiguous = {k: sorted(v) for k, v in trans.items() if len(v) > 1}
    print(f"(III) marker-5 step is AMBIGUOUS under (marker,m%2,S%2) => Collatz-hard:")
    for k, v in sorted(ambiguous.items()):
        print(f"        marker={k[0]} m%2={k[1]} S%2={k[2]} -> {v}")
    print()
    edges_ok = (dict(edges).get(3, set()) <= {3, 5} and dict(edges).get(5, set()) <= {3, 8})
    ok = (mism_par == 0 and mism_I == 0 and S_odd == 0 and A_leads <= {3, 5}
          and even_leads <= {8} and edges_ok and bool(ambiguous))
    print(f"HALT-PARITY REDUCTION VERIFIED: {ok}")
    print("  HALT <=> odometer MSB (marker) reaches 8 (even); the top-digit automaton")
    print("  {3->{3,5}, 5->{3,8}} is driven by the Collatz-hard carry stream.  Halting [OPEN].")
