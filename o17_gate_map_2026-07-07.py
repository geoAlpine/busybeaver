#!/usr/bin/env python3
"""
o17 gate/milestone map F (2026-07-07).  [Formulation task 1+2: gate-time law + 5-branch determinant]

FACTS USED (O17_CORE_TRANSDUCER.md):
  * [OBSERVED, 0 exc] every milestone (state A reads 0 at the true left frontier) is a word
    in  L = (3|5) . (0 1^{3d+2})*  -- so a milestone config is FULLY parameterized by
    (marker mu, digit vector d) and the milestone-to-milestone map
        F(mu, d)  =  (mu', d')     [+ tick count T and step count DT of the excursion]
    is THE exact dynamics (deterministic TM).  Each evaluation of F below is an exact
    finite simulation => every printed F-value is a [PROVEN] finite computation; the
    *choice of domain* (synthetic vectors) is ours, so any pattern over the synthetic
    ensemble is [OBSERVED on that ensemble].
  * Halt <=> the excursion ends with D at the frontier (marker even, = 8).

WHAT THIS SCRIPT DOES
  (1) Validates F against the real blank orbit (blank = j=1 seed shifted 5 steps):
      iterating F from (3,[]) must reproduce the known gate steps 5,22,44,101,314,724,
      2005,1072566 as cumulative step counts.
  (2) Tabulates F over synthetic ensembles:  mu in {3,5}, m=0..3 digits in 0..6, plus
      m=4 digits in 0..3, plus structured families ([0]*m, [d], [d,0], [0,d], [d]*m).
  (3) 5-branch determinant: is next-marker a function of a *bounded* projection of
      (mu,d)?  Tests prefixes (d1),(d1,d2),(d1,d2,d3), suffixes (dl),(dl1,dl),
      (m,S) and parities, and arithmetic recodings (valuations of N=sum d_i 3^i etc).
  (4) Gate-time law: is T an exact function of simple statistics (m, S, m+S, N...)?
      Prints structured-family T tables for law-guessing, and least-squares checks.
  (5) No-jump on synthetic domain: what are the observed mu -> mu' edges?

No machine decided; nothing about halting claimed beyond finite checked runs.
"""
import sys
from collections import defaultdict, Counter
from itertools import product

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
    """blocks right of head at a milestone -> (marker, digits). None if not in L."""
    bl = []
    i = pos + 1
    while i <= hi:
        while i <= hi and tape[i] == 0:
            i += 1
        j = i
        while j <= hi and tape[j] == 1:
            j += 1
        if j > i:
            # gap check: single-0 separators
            bl.append((i, j - i))
        i = j
    if not bl:
        return 0, []
    # verify single-0 separators
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

def F(mu, digs, cap=200_000_000, want_depth=False):
    """Exact milestone-to-milestone map.  Start: head A on frontier-0, then 1^mu,
    then (0 1^{3d+2}) per digit.  Returns dict with kind in {'M','HALT','CAP'}."""
    width = mu + sum(3 * d + 2 for d in digs) + len(digs) + 1
    SZ = 1 << max(14, (width * 8).bit_length())
    tape = bytearray(SZ)
    off = SZ // 3
    p = off + 1
    for i in range(mu):
        tape[p] = 1; p += 1
    for d in digs:
        p += 1  # separator 0
        for i in range(3 * d + 2):
            tape[p] = 1; p += 1
    pos = off; st = 0; step = 0; lo = pos; hi = p - 1; prevdir = 0
    n = 0
    depths = []          # per-tick leftward penetration (min pos since last tick)
    minpos_since = pos
    L1 = off + 1         # leftmost 1 (exact, maintained)
    while step < cap:
        r = tape[pos]
        if st == 5 and r == 0:
            return dict(kind='HALT', steps=step, ticks=n, mu=8, digs=None,
                        depths=depths if want_depth else None)
        if step and st == 0 and r == 0 and pos < L1:
            mu2, d2 = decode(tape, pos, hi)
            return dict(kind='M', steps=step, ticks=n, mu=mu2, digs=d2,
                        depths=depths if want_depth else None)
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            n += 1
            if want_depth:
                depths.append(minpos_since - off)
                minpos_since = pos
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
        if pos < lo: lo = pos
        if pos > hi: hi = pos
        if want_depth and pos < minpos_since:
            minpos_since = pos
    return dict(kind='CAP', steps=step, ticks=n, mu=None, digs=None,
                depths=depths if want_depth else None)

def v3(x):
    if x == 0: return 99
    v = 0
    while x % 3 == 0: x //= 3; v += 1
    return v

def v2(x):
    if x == 0: return 99
    v = 0
    while x % 2 == 0: x //= 2; v += 1
    return v

def main():
    # ---------- (1) validation against the real blank orbit ----------
    print("=== (1) F-iteration reproduces the blank-orbit gate steps ===")
    known = [5, 22, 44, 101, 314, 724, 2005, 1072566]
    mu, digs = 3, []
    t = 5   # blank orbit reaches milestone (3,[]) at step 5 [PROVEN 5-step trace]
    seq = [(t, mu, list(digs))]
    ok = True
    for k in range(7):
        r = F(mu, digs, cap=5_000_000)
        if r['kind'] != 'M':
            print(f"  iteration {k}: kind={r['kind']} (unexpected)"); ok = False; break
        t += r['steps']; mu, digs = r['mu'], r['digs']
        seq.append((t, mu, list(digs)))
    got = [s for s, _, _ in seq]
    print(f"  known gate steps : {known}")
    print(f"  F-iterated steps : {got}")
    print(f"  MATCH: {got == known}")
    for s, m_, d_ in seq:
        print(f"    t={s:>9,}  marker={m_}  m={len(d_):2d}  S={sum(d_):3d}  d={d_[:8]}{'...' if len(d_)>8 else ''}")
    print()

    # ---------- (2) tabulate F on synthetic ensembles ----------
    print("=== (2) synthetic F tabulation ===")
    ensemble = []
    for m in range(0, 4):
        for digs in product(range(7), repeat=m):
            ensemble.append(list(digs))
    for digs in product(range(4), repeat=4):
        ensemble.append(list(digs))
    results = {}   # (mu, tuple(d)) -> result
    for mu0 in (3, 5):
        for digs in ensemble:
            r = F(mu0, digs, cap=20_000_000)
            results[(mu0, tuple(digs))] = r
    ncap = sum(1 for r in results.values() if r['kind'] == 'CAP')
    print(f"  configs evaluated: {len(results)}  (CAP-hit: {ncap})")
    edges = Counter()
    for (mu0, d0), r in results.items():
        if r['kind'] != 'CAP':
            edges[(mu0, r['mu'])] += 1
    print(f"  marker edges observed (synthetic domain): {dict(sorted(edges.items()))}")
    print()

    # ---------- (3) branch determinant ----------
    print("=== (3) branch determinant: next-marker as a function of projections ===")
    def proj_tests(mu0):
        evs = [(d0, r) for (m0, d0), r in results.items()
               if m0 == mu0 and r['kind'] != 'CAP']
        outs = Counter(r['mu'] for _, r in evs)
        print(f"  mu={mu0}: {len(evs)} events, outcomes {dict(outs)}")
        def N(d): return sum(x * 3**i for i, x in enumerate(d))
        def Nrev(d): return sum(x * 3**i for i, x in enumerate(reversed(d)))
        projs = {
            'd1': lambda d: d[0] if d else -1,
            '(d1,d2)': lambda d: (d[0] if d else -1, d[1] if len(d) > 1 else -1),
            '(d1,d2,d3)': lambda d: tuple(d[:3]) + (-1,) * (3 - min(3, len(d))),
            'dl': lambda d: d[-1] if d else -1,
            '(dl1,dl)': lambda d: (d[-2] if len(d) > 1 else -1, d[-1] if d else -1),
            'm': lambda d: len(d),
            'S': lambda d: sum(d),
            '(m,S)': lambda d: (len(d), sum(d)),
            'm+S': lambda d: len(d) + sum(d),
            '(m+S)%2': lambda d: (len(d) + sum(d)) % 2,
            '(m+S)%3': lambda d: (len(d) + sum(d)) % 3,
            'S%2': lambda d: sum(d) % 2,
            'm%2': lambda d: len(d) % 2,
            '(m%2,S%2)': lambda d: (len(d) % 2, sum(d) % 2),
            'N%2': lambda d: N(d) % 2,
            'N%3': lambda d: N(d) % 3,
            'N%9': lambda d: N(d) % 9,
            'v3(N+1)': lambda d: v3(N(d) + 1),
            'v2(N+1)': lambda d: v2(N(d) + 1),
            'Nrev%2': lambda d: Nrev(d) % 2,
            'Nrev%3': lambda d: Nrev(d) % 3,
            '#d==0': lambda d: sum(1 for x in d if x == 0),
            'allzero': lambda d: all(x == 0 for x in d) if d else True,
            'd1%3': lambda d: d[0] % 3 if d else -1,
            'dl%3': lambda d: d[-1] % 3 if d else -1,
        }
        deciding = []
        for name, f in projs.items():
            g = defaultdict(set)
            for d0, r in evs:
                g[f(list(d0))].add(r['mu'])
            if all(len(v) == 1 for v in g.values()):
                deciding.append(name)
        print(f"    deciding projections: {deciding or 'NONE'}")
        # minimal prefix length that decides
        for k in range(0, 6):
            g = defaultdict(set)
            for d0, r in evs:
                g[tuple(d0[:k])].add(r['mu'])
            if all(len(v) == 1 for v in g.values()):
                print(f"    first deciding PREFIX length: {k}")
                break
        else:
            print("    no prefix of length <=5 decides (full vector needed on this ensemble)")
        # minimal suffix
        for k in range(0, 6):
            g = defaultdict(set)
            for d0, r in evs:
                g[tuple(d0[-k:]) if k else ()].add(r['mu'])
            if all(len(v) == 1 for v in g.values()):
                print(f"    first deciding SUFFIX length: {k}")
                break
        else:
            print("    no suffix of length <=5 decides")
        return evs
    evs3 = proj_tests(3)
    evs5 = proj_tests(5)
    print()
    print("  -- mu=5 outcome table, m<=2 (raw, for rule-reading) --")
    for d0, r in sorted(evs5, key=lambda x: (len(x[0]), x[0])):
        if len(d0) <= 2:
            print(f"    5,{list(d0)!s:>10} -> mu'={r['mu']}  T={r['ticks']:>6}  steps={r['steps']:>9}")
    print()

    # ---------- (4) gate-time law ----------
    print("=== (4) gate-time (excursion tick count T) law ===")
    def stat_tests(mu0):
        evs = [(list(d0), r) for (m0, d0), r in results.items()
               if m0 == mu0 and r['kind'] == 'M']
        stats = {
            'S': lambda d: sum(d),
            'm': lambda d: len(d),
            'm+S': lambda d: len(d) + sum(d),
            '(m,S)': lambda d: (len(d), sum(d)),
            'N': lambda d: sum(x * 3**i for i, x in enumerate(d)),
            'Nrev': lambda d: sum(x * 3**i for i, x in enumerate(reversed(d))),
            'full': lambda d: tuple(d),
        }
        print(f"  mu={mu0}: is T an exact function of ...")
        for name, f in stats.items():
            g = defaultdict(set)
            for d0, r in evs:
                g[f(d0)].add(r['ticks'])
            fn = all(len(v) == 1 for v in g.values())
            print(f"    {name:>6}: {'YES' if fn else 'no'}"
                  + ("" if fn or name == 'full' else
                     f"   (example clash: {next((k, sorted(v)) for k, v in g.items() if len(v) > 1)})"))
        return evs
    ev3 = stat_tests(3)
    ev5 = stat_tests(5)
    print()
    print("  -- structured families (mu=3): T and steps --")
    fams = {
        '[0]*m': [[0] * m for m in range(0, 10)],
        '[d]': [[d] for d in range(0, 10)],
        '[d,0]': [[d, 0] for d in range(0, 8)],
        '[0,d]': [[0, d] for d in range(0, 8)],
        '[d,d]': [[d, d] for d in range(0, 8)],
    }
    for name, fam in fams.items():
        row = []
        for digs in fam:
            key = (3, tuple(digs))
            r = results.get(key) or F(3, digs, cap=50_000_000)
            results[key] = r
            row.append((r['ticks'], r['mu']))
        print(f"    {name:>7}: T={[t for t, _ in row]}")
        print(f"    {'':>7}  mu'={[m_ for _, m_ in row]}")
    print()

    # ---------- (5) larger digits: does the branch stabilize in d1? ----------
    print("=== (5) single-digit scan to d1=25 (both markers): mu' and T ===")
    for mu0 in (3, 5):
        rows = []
        for d in range(26):
            key = (mu0, (d,))
            r = results.get(key) or F(mu0, [d], cap=50_000_000)
            results[key] = r
            rows.append((d, r['mu'], r['ticks']))
        print(f"  mu={mu0}: d1 -> mu' : {[(d, m_) for d, m_, _ in rows]}")
        print(f"          d1 -> T   : {[(d, t) for d, _, t in rows]}")

if __name__ == "__main__":
    main()
