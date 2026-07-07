#!/usr/bin/env python3
"""
o17 5-branch determinant: localize WHERE the branch is decided (2026-07-07).

The excursion from a milestone (mu, d) is a sequence of T odometer ticks; the
milestone/gate fires when a carry finally consumes the leading region.  Questions:
  (A) BREAKTHROUGH WINDOW: is the branch mu' a function of a bounded LEFT WINDOW of
      the digit string at the FINAL tick (the tick after which the head reaches the
      frontier)?  Tested windows: first K list entries, K=1..5 (list = raw block
      values at the tick moment, marker block included).
  (B) carry-front statistics: leftmost changed block-index between consecutive
      ticks (excluding pure LSB growth) -- the timing signature of the cascade.
  (C) contraction: m at the final tick vs m at the start.
[Every run exact; conclusions OBSERVED on the stated ensemble.  Nothing decided.]
"""
import random
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

def excursion(mu, digs, cap=50_000_000, keep_ticks=True):
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
            return dict(kind='HALT', steps=step, T=n, mu=8, digs=None, ticks=ticks)
        if step and st == 0 and r == 0 and pos < L1:
            bl = decode_all()
            mu2 = bl[0] if bl else 0
            d2 = [(x - 2) // 3 for x in bl[1:]]
            return dict(kind='M', steps=step, T=n, mu=mu2, digs=d2, ticks=ticks)
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            n += 1
            if keep_ticks:
                ticks.append(decode_all())
        prevdir = d
        if ww == 1:
            if pos < L1: L1 = pos
        elif ww == 0 and pos == L1:
            q = pos + 1
            while q <= hi and tape[q] == 0: q += 1
            L1 = q if q <= hi else SZ
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos > hi: hi = pos
    return dict(kind='CAP', steps=step, T=n, mu=None, digs=None, ticks=ticks)

def blockval(x):
    return (x - 2) // 3 if x % 3 == 2 else ('B%d' % x)

def main():
    random.seed(7)
    # ensemble of start milestones
    starts = []
    for mu0 in (3, 5):
        for m in range(0, 5):
            for _ in range(120 if m else 1):
                starts.append((mu0, [random.randint(0, 8) for _ in range(m)]))
        for m in (5, 6):
            for _ in range(60):
                starts.append((mu0, [random.randint(0, 6) for _ in range(m)]))
    # dedupe
    starts = sorted(set((mu0, tuple(d)) for mu0, d in starts))
    print(f"ensemble: {len(starts)} start milestones")

    events = []
    for mu0, d0 in starts:
        r = excursion(mu0, list(d0))
        if r['kind'] == 'CAP':
            continue
        events.append((mu0, d0, r))
    print(f"completed excursions: {len(events)}")
    print()

    print("=== (A) branch as a function of the FINAL-TICK left window ===")
    for mu0 in (5, 3):
        evs = [(d0, r) for m0, d0, r in events if m0 == mu0 and r['ticks']]
        outs = defaultdict(int)
        for _, r in evs:
            outs[r['mu']] += 1
        print(f"  mu={mu0}: {len(evs)} excursions with >=1 tick, outcomes {dict(outs)}")
        for K in range(1, 6):
            g = defaultdict(set)
            for d0, r in evs:
                last = r['ticks'][-1]
                key = tuple(blockval(x) for x in last[:K]) + (('LEN<=K',) if len(last) <= K else ())
                g[key].add(r['mu'])
            bad = {k: sorted(v) for k, v in g.items() if len(v) > 1}
            print(f"    window K={K}: {len(g)} keys, ambiguous {len(bad)}"
                  + ("   <-- DECIDES" if not bad else ""))
            if bad and K in (2, 3):
                for k, v in list(bad.items())[:4]:
                    print(f"        clash {k} -> {v}")
        # also: window at final tick + T parity
        for K in (2, 3):
            g = defaultdict(set)
            for d0, r in evs:
                last = r['ticks'][-1]
                key = (tuple(blockval(x) for x in last[:K]), r['T'] % 2, len(last) <= K)
                g[key].add(r['mu'])
            bad = sum(1 for v in g.values() if len(v) > 1)
            print(f"    window K={K} + T%2: ambiguous {bad}" + ("   <-- DECIDES" if not bad else ""))
    print()

    print("=== (B) carry-front statistics (leftmost changed block index per tick) ===")
    # use a few long excursions
    long_evs = sorted(((m0, d0, r) for m0, d0, r in events if r['T'] >= 30),
                      key=lambda x: -x[2]['T'])[:6]
    for m0, d0, r in long_evs:
        fronts = []
        tk = r['ticks']
        for a, b in zip(tk, tk[1:]):
            f = None
            for i in range(min(len(a), len(b))):
                if a[i] != b[i]:
                    f = i
                    break
            if f is None and len(a) != len(b):
                f = min(len(a), len(b))
            # exclude pure LSB growth: change only in the final block of equal-length lists
            if f is not None and not (len(a) == len(b) and f == len(a) - 1):
                fronts.append(f)
            else:
                fronts.append(None)
        touch = [f for f in fronts if f is not None]
        mins = []
        cur = 10 ** 9
        for f in touch:
            cur = min(cur, f)
            mins.append(cur)
        print(f"  ({m0},{list(d0)}): T={r['T']}, carry events={len(touch)}, "
              f"front seq (first 30): {touch[:30]}")
        print(f"      running min: {mins[:30]}  -> final min {mins[-1] if mins else '-'}")
    print()

    print("=== (C) contraction: m at final tick vs at start ===")
    ms = [(len(d0), len(r['ticks'][-1]) - 1) for _, d0, r in events if r['ticks']]
    bym = defaultdict(list)
    for m0, mf in ms:
        bym[m0].append(mf)
    for m0 in sorted(bym):
        v = bym[m0]
        print(f"  start m={m0}: final-tick m: min {min(v)}, max {max(v)}, mean {sum(v)/len(v):.2f}  (n={len(v)})")

if __name__ == "__main__":
    main()
