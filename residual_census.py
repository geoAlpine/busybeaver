#!/usr/bin/env python3
"""CENSUS of the 1104-holdout residual (2026-07-25) — what IS the block Completion.lean axiomatises?

The named 19 were characterised by their epoch width ratio (3/2, 4/3, 8/3, 5/2 = odd-prime Mahler
= (K); x2 = 2 = carry-transparent). This runs the SAME measurement over the whole residual and
histograms the result, so the 1087-residual axiom stops being opaque.

Reports every machine whose ratio resolves, with a nearest-simple-fraction label.
Calibration is inside: x2 is in the list and must come out at 2.

No machine decided. No label upgraded.
"""
import sys, collections
from fractions import Fraction
HOLDOUTS = '/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt'

def parse(spec):
    T=[]
    for blk in spec.split('_'):
        row=[]
        for k in (0,3):
            f=blk[k:k+3]
            row.append(None if f[0]=='-' else (int(f[0]), 1 if f[1]=='R' else -1, ord(f[2])-65))
        T.append(row)
    return T

def ratio(spec, N, span):
    T = parse(spec)
    tape = bytearray(2*span); pos = span; st = 0; mx = 0; mn = 0
    recL=[]; recR=[]
    for t in range(1, N+1):
        e = T[st][tape[pos]]
        if e is None: return ('HALT', None, None)
        w,d,st = e
        tape[pos]=w; pos+=d; r=pos-span
        if r>mx: mx=r; recR.append((t, mx-mn))
        if r<mn: mn=r; recL.append((t, mx-mn))
        if pos<1 or pos>=2*span-1: return ('OVF', None, None)
    best=None
    for side,rec in (('L',recL),('R',recR)):
        if len(rec)<4: continue
        for f in (0.25,1.0):
            idx=[i for i in range(len(rec)) if i==0 or rec[i][0]-rec[i-1][0]>f*rec[i-1][0]]
            ws=[rec[i][1] for i in idx][-5:]
            if len(ws)<4: continue
            rs=[ws[i+1]/ws[i] for i in range(len(ws)-1) if ws[i]]
            if len(rs)<3: continue
            m=sum(rs[-3:])/3
            spread=max(rs[-3:])-min(rs[-3:])
            if spread < 0.06*m and (best is None or spread < best[1]):
                best=(m, spread, side, f, ws)
    if best is None: return ('UNRESOLVED', None, None)
    return ('OK', best[0], best)

def label(r):
    best=None
    for q in range(1,9):
        for p in range(q+1, 6*q+1):
            v=p/q
            if abs(v-r) < 0.02*r and (best is None or q < best[1]):
                best=(f"{p}/{q}", q)
    return best[0] if best else f"{r:.3f}"

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv)>1 else 5_000_000
    span = 1 << 18
    specs=[l.strip() for l in open(HOLDOUTS) if l.strip()]
    hist=collections.Counter(); rows=[]
    for i,sp in enumerate(specs,1):
        st, r, det = ratio(sp, N, span)
        if st=='OK':
            lab=label(r); hist[lab]+=1; rows.append((lab, round(r,4), sp))
        else: hist[st]+=1
        if i%100==0:
            print(f"  ...{i}/{len(specs)}", flush=True)
            print("   running histogram:", dict(hist.most_common(12)), flush=True)
    print("\n=== EPOCH-RATIO CENSUS OF THE 1104 RESIDUAL ===")
    for k,v in hist.most_common(): print(f"  {k:>14} : {v}")
    print("\nmachines at ratio 2 (carry-transparent candidates):")
    for lab,r,sp in rows:
        if lab in ('2/1','4/2','6/3','8/4'): print(f"  {r} {sp}")
