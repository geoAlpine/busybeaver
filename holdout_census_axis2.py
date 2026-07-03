#!/usr/bin/env python3
"""
BB(6) 1104-holdout census -- SECOND AXIS: block structure.
For each holdout record final (width W, max 1-block length B, #1-blocks N) and B at an
earlier checkpoint, giving:
  - B bounded (never grows past a small constant)  => bounded-digit outlier (o3-class)
  - N small (~1-3), B ~ W                          => unary counter / scalar (o2/o7/SpaceNeedle-class)
  - N large (grows ~W), B small/slow               => digit-string (o17/sea-class)
Cross-tabulate with the width class from holdout_census. [OBSERVED recon; decides nothing.]
"""
import sys
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


def maxblk_nblk(tape, lo, hi):
    B = 0; N = 0; i = lo
    while i <= hi:
        if tape[i] == 1:
            n = 0
            while i <= hi and tape[i] == 1: n += 1; i += 1
            N += 1
            if n > B: B = n
        else:
            i += 1
    return B, N


def run(spec, maxsteps, SZ=1 << 21):
    M = parse(spec)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    Bmid = None; midstep = maxsteps // 4
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None:
            B, N = maxblk_nblk(tape, lo, hi)
            return ('HALT', hi - lo + 1, B, N, Bmid)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if Bmid is None and step >= midstep:
            Bmid, _ = maxblk_nblk(tape, lo, hi)
    B, N = maxblk_nblk(tape, lo, hi)
    return ('MAX', hi - lo + 1, B, N, Bmid)


def struct_class(W, B, N, Bmid):
    grew = (Bmid is not None and B > Bmid + 2)
    if B <= 6 and not grew:
        return 'bounded-digit (o3-class)'
    if N <= 4:
        return 'unary-counter/scalar (o2/o7/SN)'
    if N >= 8:
        return 'digit-string (o17/sea)'
    return 'mixed/small'


if __name__ == "__main__":
    specs = [l.strip() for l in open('/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt') if l.strip()]
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 400_000
    from collections import Counter
    sc = Counter(); rows = []
    named = {'1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA': 'Antihydra',
             '1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA': 'o2',
             '1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC': 'o3',
             '1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC': 'o7',
             '1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD': 'SpaceNeedle',
             '1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF': 'o11'}
    nlog = []
    for i, sp in enumerate(specs):
        out, W, B, N, Bmid = run(sp, cap)
        c = struct_class(W, B, N, Bmid)
        sc[c] += 1; rows.append((sp, out, W, B, N))
        if sp in named:
            nlog.append(f"  {named[sp]:12} W={W} maxblk={B} nblk={N} -> {c}")
        if (i+1) % 200 == 0: print(f"  {i+1}/1104", file=sys.stderr)
    print(f"=== SECOND AXIS: block structure (cap={cap}) ===")
    for k, v in sc.most_common(): print(f"  {k:34}: {v}")
    print("\nnamed cryptids:")
    for l in nlog: print(l)
    import json
    json.dump(rows, open('/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/dc5bdff5-0204-422a-affb-14b213107eb8/scratchpad/axis2_rows.json', 'w'))
