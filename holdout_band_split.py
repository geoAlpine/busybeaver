#!/usr/bin/env python3
"""
A6: refined Type-I/II proxy over the bounded-digit (B<=6) band of the 1104 holdouts.
Multi-signal per machine: max-block-ever Bmax; digit-sum (#blocks len>=2) growth exponent;
#blocks growth exponent.  Classify with honest confidence.  [OBSERVED proxy; not a proof.]
"""
import json, math, sys
sys.path.insert(0, '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/dc5bdff5-0204-422a-affb-14b213107eb8/scratchpad')

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                        else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M


def signals(spec, maxsteps=1_500_000):
    M = parse(spec); SZ = 1 << 21
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    Bmax = 0; checks = []; nx = 3000
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None: break
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if step >= nx:
            S = 0; N = 0; i = lo
            while i <= hi:
                if tape[i] == 1:
                    n = 0
                    while i <= hi and tape[i] == 1: n += 1; i += 1
                    N += 1
                    if n >= 2: S += 1
                    if n > Bmax: Bmax = n
                else: i += 1
            checks.append((step, S, N)); nx = int(nx * 2)
    return Bmax, checks


def expo(checks, idx):
    pts = [(s, v[idx]) for s, *v in [(c[0], c[1], c[2]) for c in checks] if v[idx] > 1 and s > 2000] \
        if False else [(c[0], c[1 + idx]) for c in checks if c[1 + idx] > 1 and c[0] > 2000]
    if len(pts) < 4: return None
    n = len(pts); lx = [math.log(s) for s, v in pts]; ly = [math.log(v) for s, v in pts]
    mx = sum(lx)/n; my = sum(ly)/n; den = sum((lx[i]-mx)**2 for i in range(n))
    return sum((lx[i]-mx)*(ly[i]-my) for i in range(n))/den if den else None


if __name__ == "__main__":
    rows = json.load(open('/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/dc5bdff5-0204-422a-affb-14b213107eb8/scratchpad/axis2_rows.json'))
    band = [r[0] for r in rows if r[3] is not None and r[3] <= 6]
    from collections import Counter
    cnt = Counter(); binary_o3 = 0
    for sp in band:
        Bmax, checks = signals(sp)
        aS = expo(checks, 0)   # digit-sum growth
        aN = expo(checks, 1)   # #blocks growth
        # classify
        if Bmax <= 2:
            binary_o3 += 1
            cnt['o3-EXACT (blocks in {1,2}, binary digits)'] += 1
        elif aS is not None and aS >= 0.35:
            cnt['value-present (digit-sum grows => odometer/Type-I)'] += 1
        elif aS is not None and aS < 0.15:
            cnt['o3-like (log digit-sum, no value)'] += 1
        else:
            cnt['ambiguous'] += 1
    print(f"bounded-digit band (B<=6): {len(band)} machines")
    for k, v in cnt.most_common():
        print(f"  {k:48}: {v}")
    print(f"\n  o3-EXACT (binary {{1,2}}-block) machines: {binary_o3}")
