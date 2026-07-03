#!/usr/bin/env python3
"""
BB(6) 1104-holdout structural census (2026-07-04).  [OBSERVED, recon only]
Partition the 1104 undecided holdouts by their blank-tape DYNAMICS: halt/no-halt within a
cap, and tape-width growth exponent  width ~ step^a, giving a coarse class:
  a~0  : bounded/cycler-ish (should be decided already; flag if seen)
  a<0.4: sub-sqrt (nested counters, Space-Needle-class)
  ~0.5 : sqrt-t bouncer (o2/o3/o7/o11.. class)
  ~1.0 : linear (translated-cycler / simple counter)
  >1.2 : super-linear / exponential width (Antihydra-class fast Mahler)
This is RECON (crude milestone extraction can mislabel); it partitions the frontier, it does
NOT decide anything.
"""
import math, sys

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                        else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M


def run(spec, maxsteps, SZ=1 << 21):
    M = parse(spec)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    checks = []  # (step, width) sampled at geometric steps
    nexts = 1000
    while step < maxsteps:
        r = tape[pos]
        row = M[st]
        act = row[r] if r < 2 else None
        if act is None:
            return ('HALT', step, hi - lo + 1, checks)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if step >= nexts:
            checks.append((step, hi - lo + 1)); nexts = int(nexts * 1.7)
    return ('MAX', step, hi - lo + 1, checks)


def expo(checks):
    pts = [(s, w) for s, w in checks if s > 500 and w > 2]
    if len(pts) < 5:
        return None
    n = len(pts)
    lx = [math.log(s) for s, w in pts]; ly = [math.log(w) for s, w in pts]
    mx = sum(lx)/n; my = sum(ly)/n
    den = sum((lx[i]-mx)**2 for i in range(n))
    if den == 0: return None
    return sum((lx[i]-mx)*(ly[i]-my) for i in range(n))/den


def classify(a):
    if a is None: return 'flat/short'
    if a < 0.12: return 'bounded~cycler'
    if a < 0.40: return 'sub-sqrt'
    if a < 0.62: return 'sqrt-t bouncer'
    if a < 0.85: return 'inter(.6-.85)'
    if a < 1.15: return 'linear'
    return 'super-linear/exp'


if __name__ == "__main__":
    specs = [l.strip() for l in open('/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt') if l.strip()]
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 400_000
    from collections import Counter
    cls = Counter(); halts = []; rows = []
    for i, sp in enumerate(specs):
        out, step, W, checks = run(sp, cap)
        if out == 'HALT':
            halts.append((sp, step)); cls['HALTED'] += 1; rows.append((sp, 'HALT', step, W, None)); continue
        a = expo(checks); c = classify(a)
        cls[c] += 1; rows.append((sp, c, step, W, a))
        if (i+1) % 200 == 0:
            print(f"  {i+1}/1104 ...", file=sys.stderr)
    print(f"=== 1104-holdout structural census (blank tape, cap={cap}) ===")
    for k, v in cls.most_common():
        print(f"  {k:20}: {v}")
    print(f"\nHALTED within cap (slow halters or mislabels): {len(halts)}")
    for sp, s in halts[:20]:
        print(f"  HALT@{s}: {sp}")
    # save rows for follow-up
    import json
    json.dump([(sp, c, step, W, a) for sp, c, step, W, a in rows],
              open('/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/dc5bdff5-0204-422a-affb-14b213107eb8/scratchpad/census_rows.json', 'w'))
    print("\nrows saved to census_rows.json")
