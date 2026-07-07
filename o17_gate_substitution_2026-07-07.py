#!/usr/bin/env python3
"""
o17 sqrt-step lens (2026-07-07): (i) rigid-island stress test for the 5-branch
(m<=2 digit vectors with LARGE digit values), (ii) carry-front depth profile over
the post-gate void on the blank orbit, (iii) substitution test: digit-string
snapshots at geometric tick times -- prefix stability / self-similarity.
[All exact finite runs; conclusions OBSERVED on stated ranges.  Nothing decided.]
"""
import sys
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

def excursion(mu, digs, cap=200_000_000):
    width = mu + sum(3 * d + 2 for d in digs) + len(digs) + 1
    SZ = 1 << max(15, (width * 8).bit_length())
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
            return dict(kind='HALT', steps=step, T=n, mu=8)
        if step and st == 0 and r == 0 and pos < L1:
            bl = []
            i = pos + 1
            while i <= hi:
                while i <= hi and tape[i] == 0: i += 1
                j = i
                while j <= hi and tape[j] == 1: j += 1
                if j > i: bl.append(j - i)
                i = j
            return dict(kind='M', steps=step, T=n, mu=bl[0] if bl else 0,
                        digs=[(x - 2) // 3 for x in bl[1:]])
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            n += 1
        prevdir = d
        if ww == 1:
            if pos < L1: L1 = pos
        elif ww == 0 and pos == L1:
            q = pos + 1
            while q <= hi and tape[q] == 0: q += 1
            L1 = q if q <= hi else SZ
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos > hi: hi = pos
    return dict(kind='CAP', steps=step, T=n, mu=None)

def main():
    print("=== (i) rigid-island stress test: 5-branch at m<=2, large digits ===")
    for d in (50, 100, 500, 1000):
        r = excursion(5, [d])
        print(f"  F(5,[{d}]) -> mu'={r['mu']} (T={r['T']})", "SAFE" if r['mu'] == 3 else "")
    for pair in ([7, 7], [10, 3], [50, 50], [100, 7], [7, 100], [200, 200], [1000, 0], [0, 1000]):
        r = excursion(5, pair)
        print(f"  F(5,{pair}) -> mu'={r['mu']} (T={r['T']})", "FATAL" if r['mu'] == 8 else "<-- exception!")
    for d in (50, 100, 1000):
        r = excursion(3, [d])
        print(f"  F(3,[{d}]) -> mu'={r['mu']} (T={r['T']})")
    print()

    print("=== (ii)+(iii) blank orbit: front-depth profile + geometric snapshots ===")
    # run blank orbit, record per tick: leftmost changed block index; snapshot at 2^k*500
    SZ = 1 << 22
    tape = bytearray(SZ)
    off = SZ // 4
    pos = off; st = 0; step = 0; hi = pos; prevdir = 0
    n = 0
    L1 = SZ
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 250_000_000
    snap_at = {500 * (2 ** k) for k in range(6)}   # 500..16000
    prev_blocks = None
    fronts_min_since_gate = 10 ** 9
    front_hist = defaultdict(int)
    window_min = []   # (tick range, min front)
    WIN = 500
    curmin = 10 ** 9
    snaps = {}
    def decode_all():
        out = []
        i = L1 if L1 < SZ else pos
        while i <= hi:
            while i <= hi and tape[i] == 0: i += 1
            j = i
            while j <= hi and tape[j] == 1: j += 1
            if j > i: out.append(j - i)
            i = j
        return out
    while step < cap:
        r = tape[pos]
        if st == 5 and r == 0:
            print(f"  HALT at {step}"); break
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            n += 1
            bl = decode_all()
            if prev_blocks is not None:
                f = None
                for i in range(min(len(bl), len(prev_blocks))):
                    if bl[i] != prev_blocks[i]:
                        f = i; break
                if f is None and len(bl) != len(prev_blocks):
                    f = min(len(bl), len(prev_blocks))
                if f is not None and not (len(bl) == len(prev_blocks) and f == len(bl) - 1):
                    front_hist[f] += 1
                    curmin = min(curmin, f)
            prev_blocks = bl
            if n % WIN == 0:
                window_min.append((n, curmin)); curmin = 10 ** 9
            if n in snap_at:
                snaps[n] = bl
        prevdir = d
        if ww == 1:
            if pos < L1: L1 = pos
        elif ww == 0 and pos == L1:
            q = pos + 1
            while q <= hi and tape[q] == 0: q += 1
            L1 = q if q <= hi else SZ
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos > hi: hi = pos
    print(f"  ran {step:,} steps, {n:,} ticks")
    print(f"  carry-front histogram (block index -> #events), first 12 indices:")
    for i in sorted(front_hist)[:12]:
        print(f"    front={i:>3}: {front_hist[i]:>7}")
    print(f"  window (per {WIN} ticks) MIN front (tick, min):")
    print("   ", window_min[:40])
    print()
    print("  -- geometric snapshots: block value lists (marker first; B=non-digit block) --")
    def val(x): return (x - 2) // 3 if x % 3 == 2 else f"B{x}"
    for k in sorted(snaps):
        bl = snaps[k]
        vs = [val(x) for x in bl]
        print(f"  tick {k:>6}: m={len(bl)-1:>4} marker={bl[0]}  head8={vs[:8]} tail6={vs[-6:]}")
    ks = sorted(snaps)
    print("\n  -- prefix stability across doublings --")
    for a, b in zip(ks, ks[1:]):
        A, B = snaps[a], snaps[b]
        cp = 0
        while cp < min(len(A), len(B)) and A[cp] == B[cp]:
            cp += 1
        print(f"  common prefix of s({a}) vs s({b}): {cp} blocks (lens {len(A)}, {len(B)})")

if __name__ == "__main__":
    main()
