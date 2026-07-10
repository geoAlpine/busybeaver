#!/usr/bin/env python3
"""Capture full block transformation (resulting RLE) for each crossing, to read the
odometer arithmetic. Local tape: 0^pad 1^n 0^pad, head at a boundary; run till head
exits; print before/after local RLE."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
SPEC="1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN="ABCDEF"; M=parse(SPEC)

def cross(state, side, n, pad=40):
    SZ=2*pad+n+4; tape=bytearray(SZ); bstart=pad
    for i in range(n): tape[bstart+i]=1
    pos = bstart-1 if side=='L' else bstart+n
    st="ABCDEF".index(state); step=0
    L=pad-3; R=pad+n+2
    while step<12*(n+pad)+200:
        r=tape[pos] if 0<=pos<SZ else 0
        if st==1 and r==1: return ('HALT',None,step,rle(tape,pad-3,pad+n+2))
        act=M[st][r]
        if act is None: return ('HALTo',None,step,None)
        ww,d,ns=act
        if 0<=pos<SZ: tape[pos]=ww
        pos+=d; st=ns; step+=1
        if pos<L or pos>R:
            return (STN[st],'L' if pos<L else 'R',step,rle(tape,max(0,pad-4),min(SZ-1,pad+n+3)))
    return ('TO',None,step,None)

def rs(rr):
    return ' '.join(f"{c}^{n}" if n>1 else f"{c}" for c,n in rr)

if __name__=="__main__":
    cases=[('B','R'),('C','R'),('D','L'),('F','L'),('E','L'),('C','L'),('A','R'),('D','R'),('E','R'),('F','R'),('B','L')]
    for state,side in cases:
        print(f"\n### enter {state} from {side}   (before: 0^pad 1^n 0^pad, head at {'left 0' if side=='L' else 'right 0'})")
        for n in (6,7,8,9):
            es,eside,steps,rr=cross(state,side,n)
            print(f"  n={n}: -> {es}/{eside} steps={steps}   after: {rs(rr) if rr else rr}")
