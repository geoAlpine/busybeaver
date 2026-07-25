#!/usr/bin/env python3
"""PRE-FLIGHT screen of the whole 1104-holdout residual (2026-07-25).

x2 -- the one machine this programme has PROVEN non-halting -- is a member of this list and has
epoch width ratio EXACTLY 2 (carry-transparent). This screens all 1104 for the same signature:
a ratio that is a power of the tape base. Those are the Phase-B (template-island) candidates.

Calibration is built in: x2 itself is in the list and must come out at 2.0.

No machine decided. No label upgraded.
"""
import sys, math
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')

HOLDOUTS = '/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt'

def parse(spec):
    T = []
    for blk in spec.split('_'):
        row = []
        for k in (0, 3):
            f = blk[k:k+3]
            row.append(None if f[0] == '-' else (int(f[0]), 1 if f[1] == 'R' else -1, ord(f[2])-65))
        T.append(row)
    return T

def epoch_ratio(spec, N, span):
    try: T = parse(spec)
    except Exception: return None
    tape = bytearray(2*span); pos = span; st = 0; mx = 0; mn = 0
    recL = []; recR = []
    for t in range(1, N+1):
        try: e = T[st][tape[pos]]
        except Exception: return None
        if e is None: return ('HALT', t, None, None)
        w, d, st = e
        tape[pos] = w; pos += d
        r = pos - span
        if r > mx: mx = r; recR.append((t, mx-mn))
        if r < mn: mn = r; recL.append((t, mx-mn))
        if pos < 1 or pos >= 2*span-1: return ('OVF', t, None, None)
    best = None
    for side, rec in (('L', recL), ('R', recR)):
        if len(rec) < 4: continue
        idx = [i for i in range(len(rec)) if i == 0 or rec[i][0]-rec[i-1][0] > rec[i-1][0]/4]
        ws = [rec[i][1] for i in idx][-5:]
        rats = [ws[i+1]/ws[i] for i in range(len(ws)-1) if ws[i]]
        if len(rats) >= 2:
            r = rats[-1]
            if best is None or abs(math.log(r) - math.log(2)) < abs(math.log(best[1]) - math.log(2)):
                best = (side, r, ws)
    return ('RUN', N, best, None)

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    span = 1 << 17
    specs = [l.strip() for l in open(HOLDOUTS) if l.strip()]
    print(f"screening {len(specs)} holdouts, {N} steps each")
    hits = []; done = 0
    for sp in specs:
        out = epoch_ratio(sp, N, span)
        done += 1
        if out and out[0] == 'RUN' and out[2]:
            side, r, ws = out[2]
            for base, lbl in ((2.0,'2'), (4.0,'4'), (8.0,'8')):
                if abs(r - base) < 0.03*base:
                    hits.append((sp, side, round(r,4), ws, lbl))
                    print(f"  HIT ratio~{lbl}  {sp}  side={side} r={r:.4f} ws={ws}", flush=True)
        if done % 100 == 0: print(f"  ...{done}/{len(specs)}  hits so far: {len(hits)}", flush=True)
    print(f"\nTOTAL power-of-two-ratio candidates: {len(hits)} / {len(specs)}")
    for sp, side, r, ws, lbl in hits: print(f"  {sp}  {side} {r} {ws}")
