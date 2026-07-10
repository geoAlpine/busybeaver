#!/usr/bin/env python3
"""Positive control for the halt characterization:
HALT <=> rightward E-scan meets a maximal 0-run of length EXACTLY 3.
Plant runs of length 1,2,3,4,5 directly in the E-scanner's path and check halt/no-halt."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from mse_extract import parse
SPEC="1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"; M=parse(SPEC)

def scan_run(gaplen, blockL=5, blockR=5, pad=20):
    """Tape: 1^blockL 0^gaplen 1^blockR, E-scanner starts at the left, entering the gap.
    Place E on the first 0 of the gap (left boundary), moving right. Report halt/exit."""
    SZ=pad*2+blockL+gaplen+blockR+4; tape=bytearray(SZ); i=pad
    for _ in range(blockL): tape[i]=1; i+=1
    gapstart=i
    for _ in range(gaplen): tape[i]=0; i+=1
    for _ in range(blockR): tape[i]=1; i+=1
    # E enters the gap at its left boundary (first 0), moving right
    pos=gapstart; st=4; step=0
    while step<500:
        r=tape[pos] if 0<=pos<SZ else 0
        if st==1 and r==1: return ('HALT',step)
        act=M[st][r]
        if act is None: return ('HALTother',step)
        ww,d,ns=act
        if 0<=pos<SZ: tape[pos]=ww
        pos+=d; st=ns; step+=1
        if abs(pos-gapstart)>gaplen+blockL+blockR+5:
            return ('escaped',step)
    return ('timeout',step)

if __name__=="__main__":
    print("E-scanner enters a maximal 0-run of length L (blocks both sides):")
    for L in range(1,7):
        r=scan_run(L)
        print(f"  gap 0^{L}: {r}   {'<== HALT (predicted only at L=3)' if r[0]=='HALT' else ''}")
