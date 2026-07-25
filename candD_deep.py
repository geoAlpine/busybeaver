#!/usr/bin/env python3
"""Decisive long-run judgement of candidate D -- the next genuinely independent (2,4) candidate.

A = 1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE  (graph-canon differs from x2's, verified)

x2's control fingerprint: width ratio -> 2 AND time ratio -> 4, stable under every cluster
threshold. A's short-run readings were (~2, ~4) but noisy (width up to 2.16). This decides it.
"""
import sys
def parse(spec):
    T=[]
    for blk in spec.split('_'):
        row=[]
        for k in (0,3):
            f=blk[k:k+3]
            row.append(None if f[0]=='-' else (int(f[0]), 1 if f[1]=='R' else -1, ord(f[2])-65))
        T.append(row)
    return T
SPECS=[("x2 (control)","1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"),
       ("cand-D","1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---")]
N=int(sys.argv[1]) if len(sys.argv)>1 else 4*10**8
span=1<<21
for name,spec in SPECS:
    T=parse(spec); tape=bytearray(2*span); pos=span; st=0; mx=0; mn=0
    recL=[];recR=[]; status='RUN'
    for t in range(1,N+1):
        e=T[st][tape[pos]]
        if e is None: status=f'HALT@{t}'; break
        w,d,st=e; tape[pos]=w; pos+=d; r=pos-span
        if r>mx: mx=r; recR.append((t,mx-mn))
        if r<mn: mn=r; recL.append((t,mx-mn))
        if pos<1 or pos>=2*span-1: status=f'OVF@{t}'; break
    print(f"\n=== {name}  [{status}] ===", flush=True)
    for side,rec in (('L',recL),('R',recR)):
        for f in (0.25,1.0,2.0):
            if len(rec)<4: continue
            idx=[i for i in range(len(rec)) if i==0 or rec[i][0]-rec[i-1][0]>f*rec[i-1][0]]
            ws=[rec[i][1] for i in idx][-8:]; ts=[rec[i][0] for i in idx][-8:]
            if len(ws)<4: continue
            wr=[round(ws[i+1]/ws[i],4) for i in range(len(ws)-1) if ws[i]]
            tr=[round(ts[i+1]/ts[i],3) for i in range(len(ts)-1) if ts[i]]
            print(f"  {side} gap>{f}t  ws={ws}")
            print(f"        w={wr}")
            print(f"        t={tr}", flush=True)
