#!/usr/bin/env python3
"""
o17 tick-level rewrite rule (2026-07-07).  Watch the odometer tick: decode the tape
(1-run lengths + gap sizes) at every tick (right-end (E,0) reversal) during excursions
between milestones, to extract the per-tick digit-string rewrite rule and test the
mixed-radix product law for the excursion tick-count T.

[OBSERVED/exact finite simulation; nothing decided.]
"""
import sys
from itertools import product
from collections import defaultdict

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

def raw_blocks(tape, lo, hi):
    """[(runlen, gap_after), ...] for 1-runs left->right; gap_after=-1 for last."""
    out = []
    i = lo
    while i <= hi and tape[i] == 0:
        i += 1
    while i <= hi:
        j = i
        while j <= hi and tape[j] == 1:
            j += 1
        k = j
        while k <= hi and tape[k] == 0:
            k += 1
        out.append((j - i, (k - j) if k <= hi else -1))
        i = k
    return out

def excursion_trace(mu, digs, cap=5_000_000, dump=None):
    """Run from milestone (mu,digs); at every tick decode raw blocks.
    Returns (kind, T, steps, mu', digs', tickstrings)."""
    width = mu + sum(3 * d + 2 for d in digs) + len(digs) + 1
    SZ = 1 << max(15, (width * 16).bit_length())
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
    ticks = []
    while step < cap:
        r = tape[pos]
        if st == 5 and r == 0:
            return 'HALT', n, step, 8, None, ticks
        if step and st == 0 and r == 0 and pos < L1:
            bl = raw_blocks(tape, min(pos, L1) , hi)
            marker = bl[0][0] if bl else 0
            digs2 = [(x - 2) // 3 for x, _ in bl[1:]]
            return 'M', n, step, marker, digs2, ticks
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            n += 1
            ticks.append(raw_blocks(tape, L1 if L1 < SZ else pos, hi))
        prevdir = d
        if ww == 1:
            if pos < L1: L1 = pos
        elif ww == 0 and pos == L1:
            q = pos + 1
            while q <= hi and tape[q] == 0:
                q += 1
            L1 = q if q <= hi else SZ
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos > hi: hi = pos
    return 'CAP', n, step, None, None, ticks

def fmt(bl):
    """pretty: runlen^gap ... ; digits shown as value when len%3==2"""
    parts = []
    for L, g in bl:
        v = f"{(L-2)//3}" if L % 3 == 2 else f"[{L}]"
        parts.append(v + ("" if g in (1, -1) else f"({g})"))
    return " ".join(parts)

def main():
    print("=== tick-by-tick raw block strings (leftmost block = marker side) ===")
    for mu, digs in [(3, [0]), (3, [0, 2]), (3, [2, 0, 4]), (5, [0, 0, 2, 2, 6])]:
        kind, T, steps, mu2, digs2, ticks = excursion_trace(mu, digs)
        print(f"\n-- excursion from ({mu},{digs}) -> {kind} mu'={mu2} d'={digs2}  T={T} steps={steps}")
        show = range(len(ticks)) if len(ticks) <= 30 else \
               list(range(15)) + ['...'] + list(range(len(ticks) - 15, len(ticks)))
        for i in show:
            if i == '...':
                print("     ...")
                continue
            print(f"   tick {i+1:>4}: {fmt(ticks[i])}")
    print()

    print("=== product-law tests for T over the synthetic ensemble ===")
    # gather (mu, digs) -> (T, mu') on ensemble
    ens = []
    for m in range(0, 4):
        for digs in product(range(5), repeat=m):
            ens.append(list(digs))
    data = []
    for mu0 in (3, 5):
        for digs in ens:
            kind, T, steps, mu2, digs2, _ = excursion_trace(mu0, digs, cap=20_000_000)
            data.append((mu0, tuple(digs), T, mu2, steps))
    import math
    def prod(xs):
        r = 1
        for x in xs: r *= x
        return r
    cands = {
        'prod(d+2)': lambda d: prod(x + 2 for x in d),
        'prod(d+1)': lambda d: prod(x + 1 for x in d),
        'prod(ceil((d+2)/2))': lambda d: prod((x + 3) // 2 for x in d),
        'prod over even>=2 of (d/2+1)': lambda d: prod(x // 2 + 1 for x in d if x >= 2 and x % 2 == 0),
        'prod((d+2+d%2)/2)': lambda d: prod((x + 2 + x % 2) // 2 for x in d),
    }
    for mu0 in (3, 5):
        rows = [(d, T) for m0, d, T, mu2, _ in data if m0 == mu0 and T is not None]
        print(f"  mu={mu0}, {len(rows)} events:")
        for name, f in cands.items():
            hits = sum(1 for d, T in rows if f(list(d)) == T)
            hits1 = sum(1 for d, T in rows if f(list(d)) == T + 1)
            hitsm1 = sum(1 for d, T in rows if f(list(d)) == T - 1)
            print(f"    T == {name:>28}: {hits}/{len(rows)}   (+1: {hits1}, -1: {hitsm1})")
    print()
    print("  raw (mu=3, m<=2) T table for law-reading:")
    for m0, d, T, mu2, steps in data:
        if m0 == 3 and len(d) <= 2:
            print(f"    3,{list(d)!s:>8} -> T={T:>4}  mu'={mu2}  steps={steps}")

if __name__ == "__main__":
    main()
