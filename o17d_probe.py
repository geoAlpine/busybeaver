#!/usr/bin/env python3
"""
o17 DECISION ATTEMPT probe (2026-07-10).  [B3 symbolic gate extension]

Goal: resolve the FINITE-STATE-vs-VALUE crux for o17's gate-safety condition.
  o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB   (halt = F reads 0)

The gate-to-gate map is F(mu, d) = (mu', d', T, steps), the EXACT deterministic
dynamics on the milestone coordinates (marker mu in {3,5}, digit vector d).
Safety: at every marker-5 gate we need mu' = 3 (not 8 = HALT).

This probe:
  (1) iterates exact F on the real blank orbit to the last simulable gate (gate 8,
      ~1.07M steps), printing (mu, d) with the DIGIT MAGNITUDES and vector LENGTH --
      the first question for any scalar/fixed-base encoding is whether digits stay
      bounded (fixed base possible) or grow (no fixed base -> no scalar mod-M value).
  (2) records the marker-5 exposures and their outcomes on the real orbit.

Everything below is an exact finite TM computation. Nothing about halting decided.
"""
import sys
from collections import Counter

SPEC = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else
                       (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse(SPEC)

def decode(tape, pos, hi):
    bl = []
    i = pos + 1
    while i <= hi:
        while i <= hi and tape[i] == 0:
            i += 1
        j = i
        while j <= hi and tape[j] == 1:
            j += 1
        if j > i:
            bl.append((i, j - i))
        i = j
    if not bl:
        return 0, []
    for (s1, l1), (s2, l2) in zip(bl, bl[1:]):
        if s2 - (s1 + l1) != 1:
            return None, None
    marker = bl[0][1]
    digs = []
    for _, l in bl[1:]:
        if l % 3 != 2:
            return None, None
        digs.append((l - 2) // 3)
    return marker, digs

def F(mu, digs, cap=200_000_000):
    width = mu + sum(3 * d + 2 for d in digs) + len(digs) + 1
    SZ = 1 << max(14, (width * 8).bit_length())
    tape = bytearray(SZ)
    off = SZ // 3
    p = off + 1
    for i in range(mu):
        tape[p] = 1; p += 1
    for d in digs:
        p += 1
        for i in range(3 * d + 2):
            tape[p] = 1; p += 1
    pos = off; st = 0; step = 0; hi = p - 1; prevdir = 0
    n = 0
    L1 = off + 1
    while step < cap:
        r = tape[pos]
        if st == 5 and r == 0:
            return dict(kind='HALT', steps=step, ticks=n, mu=8, digs=None)
        if step and st == 0 and r == 0 and pos < L1:
            mu2, d2 = decode(tape, pos, hi)
            return dict(kind='M', steps=step, ticks=n, mu=mu2, digs=d2)
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            n += 1
        prevdir = d
        if ww == 1:
            if pos < L1:
                L1 = pos
        elif ww == 0 and pos == L1:
            q = pos + 1
            while q <= hi and tape[q] == 0:
                q += 1
            L1 = q if q <= hi else SZ
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos > hi: hi = pos
    return dict(kind='CAP', steps=step, ticks=n, mu=None, digs=None)

def main():
    print("=== (1) real blank orbit, exact F-iteration to the last simulable gate ===")
    mu, digs = 3, []
    t = 5
    k = 0
    print(f"  gate {k:2d}: t={t:>10,}  mu={mu}  m={len(digs):2d}  "
          f"maxdig={max(digs) if digs else 0:>4}  S={sum(digs):>4}")
    five_events = []
    while True:
        if mu == 5:
            five_events.append((k, list(digs)))
        r = F(mu, digs, cap=3_000_000)
        if r['kind'] == 'CAP':
            print(f"  gate {k+1}: excursion exceeds sim cap ({r['steps']:,} steps, "
                  f"ticks={r['ticks']}) -- BEYOND DIRECT SIMULATION")
            break
        if r['kind'] == 'HALT':
            print(f"  gate {k+1}: HALT")
            break
        t += r['steps']; mu, digs = r['mu'], r['digs']; k += 1
        print(f"  gate {k:2d}: t={t:>12,}  mu={mu}  m={len(digs):2d}  "
              f"maxdig={max(digs) if digs else 0:>5}  S={sum(digs):>5}  "
              f"d={digs[:10]}{'...' if len(digs) > 10 else ''}  T={r['ticks']}")
    print()
    print("  -- marker-5 exposures on the real orbit (safety = each must map to mu'=3) --")
    for gk, d in five_events:
        r = F(5, d, cap=3_000_000)
        out = r['mu'] if r['kind'] != 'CAP' else '?'
        print(f"    gate {gk}: mu=5, m={len(d)}, d={d[:12]} -> mu'={out}  "
              f"({'SAFE' if out == 3 else 'HALT' if out == 8 else 'unresolved'})")
    print()
    print("  DIGIT-MAGNITUDE VERDICT: if maxdig grows with k, no fixed-base scalar")
    print("  encoding exists (a base-b odometer needs digits < b, bounded).")

if __name__ == "__main__":
    main()
