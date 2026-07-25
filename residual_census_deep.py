#!/usr/bin/env python3
"""DEEP census of the 1104 residual, per GRAPH (2026-07-26).

The 5e6 census left 673/1104 unresolved and reported per ENTRY, but the 1104 entries comprise only
909 distinct transition graphs. This runs 3e7 steps and aggregates by GRAPH-CANONICAL form, so
start-state variants are not double counted (the exact trap candidate C set).

No machine decided. No label upgraded.
"""
import sys, collections, itertools
HOLDOUTS = '/Users/aokiyousuke/busybeaver/_bbdata/bb6_holdouts_1104.txt'
S = "ABCDEF"

def parse(spec):
    T=[]
    for blk in spec.split('_'):
        row=[]
        for k in (0,3):
            f=blk[k:k+3]
            row.append(None if f[0]=='-' else (int(f[0]), 1 if f[1]=='R' else -1, ord(f[2])-65))
        T.append(row)
    return T

def relabel(spec, sig):
    out=[None]*6
    for i,blk in enumerate(spec.split('_')):
        new=""
        for k in (0,3):
            f=blk[k:k+3]
            new += "---" if f[0]=='-' else f[0]+f[1]+sig[f[2]]
        out[S.index(sig[S[i]])]=new
    return "_".join(out)

def gcanon(spec):
    best=None
    for p in itertools.permutations(S):
        v=relabel(spec, dict(zip(S,p)))
        if best is None or v<best: best=v
    return best

def ratio(spec, N, span):
    T=parse(spec); tape=bytearray(2*span); pos=span; st=0; mx=0; mn=0
    recL=[]; recR=[]
    for t in range(1,N+1):
        e=T[st][tape[pos]]
        if e is None: return ('HALT', None)
        w,d,st=e; tape[pos]=w; pos+=d; r=pos-span
        if r>mx: mx=r; recR.append((t, mx-mn))
        if r<mn: mn=r; recL.append((t, mx-mn))
        if pos<1 or pos>=2*span-1: return ('OVF', None)
    best=None
    for side,rec in (('L',recL),('R',recR)):
        if len(rec)<4: continue
        for f in (0.25,1.0):
            idx=[i for i in range(len(rec)) if i==0 or rec[i][0]-rec[i-1][0]>f*rec[i-1][0]]
            ws=[rec[i][1] for i in idx][-5:]; ts=[rec[i][0] for i in idx][-5:]
            if len(ws)<4: continue
            wr=[ws[i+1]/ws[i] for i in range(len(ws)-1) if ws[i]]
            tr=[ts[i+1]/ts[i] for i in range(len(ts)-1) if ts[i]]
            if len(wr)<3: continue
            m=sum(wr[-3:])/3; spread=max(wr[-3:])-min(wr[-3:])
            tm=sum(tr[-3:])/3
            if spread < 0.05*m and (best is None or spread < best[1]):
                best=(m, spread, tm)
    if best is None: return ('UNRESOLVED', None)
    return ('OK', (best[0], best[2]))

def label(r):
    best=None
    for q in range(1,9):
        for p in range(q+1, 6*q+1):
            if abs(p/q - r) < 0.02*r and (best is None or q < best[1]): best=(f"{p}/{q}", q)
    return best[0] if best else f"~{r:.3f}"

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv)>1 else 3*10**7
    span = 1 << 19
    specs=[l.strip() for l in open(HOLDOUTS) if l.strip()]
    print(f"deep census: {len(specs)} entries, {N} steps, aggregated by GRAPH", flush=True)
    seen={}; hist=collections.Counter(); rows=[]
    for i,sp in enumerate(specs,1):
        g=gcanon(sp)
        if g in seen:
            continue                      # one representative per graph
        seen[g]=sp
        st,val = ratio(sp, N, span)
        if st=='OK':
            w,tm = val
            lab=label(w); hist[lab]+=1; rows.append((lab, round(w,4), round(tm,3), sp))
        else: hist[st]+=1
        if i%100==0: print(f"  ...{i}/{len(specs)}  graphs so far {len(seen)}", flush=True)
    print(f"\n=== DEEP CENSUS, per GRAPH ({len(seen)} distinct graphs) ===")
    for k,v in hist.most_common(): print(f"  {k:>14} : {v}")
    print("\ngraphs at ratio 2 with time ratio near 4 (transparent candidates):")
    for lab,w,tm,sp in rows:
        if lab in ('2/1','4/2') and abs(tm-4) < 0.4: print(f"  w={w} t={tm}  {sp}")
