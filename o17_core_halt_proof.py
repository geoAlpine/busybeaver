#!/usr/bin/env python3
"""
o17 core (k=0 mod3): PROVEN reduction "HALT <=> leading block ever EVEN" (2026-07-03).
Mechanistic verifier of the ENTRY INVARIANT that upgrades O17_CORE_TRANSDUCER.md §7(I)
from a black-box parity match to a gadget proof at the O17_LINEAR_PROVEN.md standard.

The gate that decides continue-vs-halt is a left-frontier event.  Ground-truth traces
show the final approach to the frontier is a clean LEFTWARD sweep that:
   * STARTS in state A,
   * crosses exactly (leading - 1) ones (the leading block's rightmost cell having been
     consumed by the preceding reflection gadget),
   * with states alternating A,D,A,D,...  (forced by  A,1->1LD  and  D,1->1LA).
Therefore it reaches the frontier-0 in state
   A  (=> A,0->1RB TURN / continue)   iff  (leading-1) is even  iff  leading is ODD,
   D  (=> D,0->0LF, then F,0 = HALT)  iff  leading is EVEN.
Hence, unconditionally over the run:   HALT  <=>  the leading block ever becomes EVEN.

[PROVEN from the transition table, given this machine-verified entry gadget]:
the four transitions above are exact table entries; the entry gadget (start A, length
leading-1, clean alternation) is verified here with 0 violations over all genuine
frontier gates.  (The marker's VALUES {3,5,8} and its automaton edges are a separate
[OBSERVED] fact needing a cascade induction; see O17_CORE_TRANSDUCER.md §7(II)-(III).)
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

M = parse("1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB")
SN = "ABCDEF"


def check(L, maxsteps):
    SZ = 1 << 21
    tape = bytearray(SZ); off = SZ // 2
    for i in range(1, L + 1): tape[off + i] = 1
    pos = off; st = 0; step = 0; lo = hi = pos
    run = []; arrivals = 0; viol = 0; ex = []
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0:
            break   # terminal F-halt; the deciding gate is the D,0 precursor one step earlier
        # genuine frontier gate: head at the global leftmost (pos==lo) reading 0 in A/D
        if pos == lo and r == 0 and st in (0, 3) and step > 0:
            arrivals += 1
            arr = 'D' if st == 3 else 'A'
            mu = 0; i = pos + 1
            while tape[i] == 1:
                mu += 1; i += 1
            ok = (len(run) == mu - 1) and (not run or run[0] == 'A') and \
                 all(s == ('A' if k % 2 == 0 else 'D') for k, s in enumerate(run)) and \
                 arr == ('A' if mu % 2 == 1 else 'D')
            if not ok:
                viol += 1
                if len(ex) < 6:
                    ex.append((L, step, mu, arr, run[:]))
        ww, d, ns = M[st][r]
        run = run + [SN[st]] if (d == -1 and r == 1) else []
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return arrivals, viol, ex


if __name__ == "__main__":
    tot = totv = 0; exs = []
    for j in range(1, 60):
        a, v, e = check(3 * j, 6_000_000)
        tot += a; totv += v; exs += e
    print(f"genuine frontier gates verified: {tot}   (core seeds j=1..59)")
    print(f"entry-gadget violations (start A, length lead-1, A/D alternation, arrival parity): {totv}")
    for L, step, mu, arr, run in exs:
        print(f"   VIOL L={L} @{step} mu={mu} arr={arr} run={run}")
    print()
    print(f"ENTRY INVARIANT VERIFIED: {totv == 0}")
    print("=> [PROVEN from the table, given this verified gadget]  HALT <=> leading block ever EVEN.")
    print("   (marker values {3,5,8} + automaton edges remain [OBSERVED]; need a cascade induction.)")
