#!/usr/bin/env python3
"""DEEP screen of the 1104-holdout residual (2026-07-25) — sizing the template island.

The first screen (preflight_1104.py) ran 5e6 steps and demanded >=4 frontier-record clusters, so
machines with long epochs were missed. This one runs 2e7 and uses the SHARPER signature established
by x2's control run: width ratio -> 2 AND time ratio -> 4, on >=3 consecutive epochs.

Why it matters: Completion.lean carries the 1087 residual as ONE opaque axiom. If the template
island is large the axiom decomposes; if small it does not. That decides whether Phase B is
hand-work or needs automation.

No machine decided. No label upgraded.
"""
import sys
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

def probe(spec, N, span):
    T = parse(spec)
    tape = bytearray(2*span); pos = span; st = 0; mx = 0; mn = 0
    recL = []; recR = []
    for t in range(1, N+1):
        e = T[st][tape[pos]]
        if e is None: return None
        w, d, st = e
        tape[pos] = w; pos += d
        r = pos - span
        if r > mx: mx = r; recR.append((t, mx-mn))
        if r < mn: mn = r; recL.append((t, mx-mn))
        if pos < 1 or pos >= 2*span-1: return None
    out = []
    for side, rec in (('L', recL), ('R', recR)):
        if len(rec) < 4: continue
        for f in (0.25, 1.0):
            idx = [i for i in range(len(rec)) if i == 0 or rec[i][0]-rec[i-1][0] > f*rec[i-1][0]]
            ws = [rec[i][1] for i in idx][-6:]; ts = [rec[i][0] for i in idx][-6:]
            if len(ws) < 4: continue
            wr = [ws[i+1]/ws[i] for i in range(len(ws)-1) if ws[i]]
            tr = [ts[i+1]/ts[i] for i in range(len(ts)-1) if ts[i]]
            for base, tbase, lbl in ((2.0,4.0,'x2'), (4.0,16.0,'x4'), (8.0,64.0,'x8')):
                if (len(wr) >= 3 and all(abs(x-base) < 0.03*base for x in wr[-3:])
                        and all(abs(x-tbase) < 0.10*tbase for x in tr[-3:])):
                    out.append((side, f, lbl, [round(x,4) for x in wr[-3:]],
                                [round(x,3) for x in tr[-3:]], ws))
    return out

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2*10**7
    span = 1 << 19
    specs = [l.strip() for l in open(HOLDOUTS) if l.strip()]
    print(f"deep screen: {len(specs)} holdouts, {N} steps, (ratio, time) signature", flush=True)
    hits = 0
    for i, sp in enumerate(specs, 1):
        r = probe(sp, N, span)
        if r:
            hits += 1
            side, f, lbl, wr, tr, ws = r[0]
            print(f"  HIT[{lbl}] {sp}  {side} gap>{f}t  w={wr} t={tr} ws={ws}", flush=True)
        if i % 50 == 0: print(f"  ...{i}/{len(specs)}  hits={hits}", flush=True)
    print(f"\nTOTAL: {hits} / {len(specs)}")
