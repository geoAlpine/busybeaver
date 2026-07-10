#!/usr/bin/env python3
"""
hc_sim.py -- HOLDOUT sweep, PASS 1: sound cheap deciders on all 1104.
  (a) concrete simulation to a HIGH cap -> any HALT is a SOUND [DECIDED-halt].
  (b) halt_unreachable (suite, sound) -> any True is a SOUND [DECIDED-nonhalt].
Also records per-machine dynamics for the classifier: width-growth exponent a,
block stats (max 1-block B, #blocks N, growth), and the gate (which halt edge, in-degree).
Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python  (exact big-int not needed here).
Decides nothing beyond (a)/(b), both sound; everything else is [OBSERVED] recon.
"""
import sys, math, json, os
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from suite import halt_unreachable

HOLD = '/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt'


def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] in 'Z-')
                        else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M


def maxblk_nblk(tape, lo, hi):
    B = 0; N = 0; i = lo
    while i <= hi:
        if tape[i] == 1:
            n = 0
            while i <= hi and tape[i] == 1:
                n += 1; i += 1
            N += 1
            if n > B:
                B = n
        else:
            i += 1
    return B, N


def run(spec, maxsteps, SZ=1 << 22):
    M = parse(spec)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    checks = []; nexts = 1000
    Bmid = None; midstep = maxsteps // 4
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None:
            B, N = maxblk_nblk(tape, lo, hi)
            return ('HALT', step, hi - lo + 1, B, N, Bmid, checks)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo:
            lo = pos
            if lo < 4:  # would overflow left; abandon (should not happen at these caps)
                return ('OVR', step, hi - lo + 1, 0, 0, Bmid, checks)
        elif pos > hi:
            hi = pos
            if hi > SZ - 4:
                return ('OVR', step, hi - lo + 1, 0, 0, Bmid, checks)
        if step >= nexts:
            checks.append((step, hi - lo + 1)); nexts = int(nexts * 1.7)
        if Bmid is None and step >= midstep:
            Bmid, _ = maxblk_nblk(tape, lo, hi)
    B, N = maxblk_nblk(tape, lo, hi)
    return ('MAX', step, hi - lo + 1, B, N, Bmid, checks)


def expo(checks):
    pts = [(s, w) for s, w in checks if s > 500 and w > 2]
    if len(pts) < 5:
        return None
    n = len(pts)
    lx = [math.log(s) for s, w in pts]; ly = [math.log(w) for s, w in pts]
    mx = sum(lx) / n; my = sum(ly) / n
    den = sum((lx[i] - mx) ** 2 for i in range(n))
    if den == 0:
        return None
    return sum((lx[i] - mx) * (ly[i] - my) for i in range(n)) / den


def gate_info(spec):
    """Which halt edge(s) and the in-degree of the halting state (structural gate proxy)."""
    M = parse(spec)
    halts = []
    for s in range(6):
        for sym in (0, 1):
            if M[s][sym] is None:
                halts.append((chr(ord('A') + s), sym))
    # in-degree of each state
    indeg = [0] * 6
    for s in range(6):
        for sym in (0, 1):
            if M[s][sym] is not None:
                indeg[M[s][sym][2]] += 1
    return halts, indeg


def work(args):
    i, sp, cap = args
    out, step, W, B, N, Bmid, checks = run(sp, cap)
    a = expo(checks)
    hu = halt_unreachable(sp)
    halts, indeg = gate_info(sp)
    return dict(spec=sp, out=out, step=step, W=W, B=B, N=N, Bmid=Bmid,
                a=a, hu=bool(hu), halts=halts, indeg=indeg)


if __name__ == "__main__":
    import multiprocessing as mp
    specs = [l.strip() for l in open(HOLD) if l.strip()]
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    OUT = sys.argv[2] if len(sys.argv) > 2 else '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad/hc_sim_rows.json'
    args = [(i, sp, cap) for i, sp in enumerate(specs)]
    ctx = mp.get_context('fork')
    with ctx.Pool(8) as pool:
        rows = pool.map(work, args, chunksize=8)
    halted = [(r['spec'], r['step']) for r in rows if r['out'] == 'HALT']
    nonhalt_unreach = [r['spec'] for r in rows if r['hu']]
    json.dump(rows, open(OUT, 'w'))
    print(f"=== PASS 1: sound cheap deciders on 1104 (cap={cap}) ===")
    print(f"HALT within cap (SOUND [DECIDED-halt] candidates): {len(halted)}")
    for sp, s in halted[:40]:
        print(f"  HALT@{s}: {sp}")
    print(f"halt_unreachable=True (SOUND [DECIDED-nonhalt]): {len(nonhalt_unreach)}")
    for sp in nonhalt_unreach[:40]:
        print(f"  NONHALT: {sp}")
    print(f"rows -> {OUT}")
