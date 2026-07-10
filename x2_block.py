#!/usr/bin/env python3
"""Derive the macro-machine block-crossing rules: how the head traverses a 1^n block.
For each (entry state, entry side) place head at a block boundary in a controlled local
tape and simulate until the head exits the block+pad region; record exit state/side and
the transformation, for several n, to test uniformity (=> finite macro-machine)."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
SPEC="1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN="ABCDEF"
M=parse(SPEC)

def cross(state, side, n, pad=30):
    """Local tape: pad zeros, block 1^n, pad zeros. Head placed at the block boundary.
    side='L': head just left of block (on the 0), moving into it. state given.
    Returns (exit_state, exit_side, steps, local_rle_after, halted)."""
    SZ=2*pad+n+4
    tape=bytearray(SZ)
    bstart=pad
    for i in range(n): tape[bstart+i]=1
    if side=='L': pos=bstart-1
    else: pos=bstart+n
    st="ABCDEF".index(state)
    step=0; lo=hi=pos
    L=pad-2; R=pad+n+1  # block+/-2 window; exit when head leaves [L,R]
    while step<10*(n+pad)+100:
        r=tape[pos] if 0<=pos<SZ else 0
        if st==1 and r==1: return ('HALT',None,step,None,True)
        act=M[st][r]
        if act is None: return ('HALTo',None,step,None,True)
        ww,d,ns=act
        if 0<=pos<SZ: tape[pos]=ww
        pos+=d; st=ns; step+=1
        if pos< L or pos> R:
            side_out='L' if pos<L else 'R'
            return (STN[st], side_out, step, rle(tape,max(0,min(pos,pad-3)),min(SZ-1,pad+n+3)), False)
    return ('TIMEOUT',None,step,None,False)

if __name__=="__main__":
    print("Block-crossing rules (entry -> exit), testing uniformity in n:")
    for state in "ABCDEF":
        for side in ('L','R'):
            rows=[]
            for n in (5,6,7,8,15,16,30,31):
                es,eside,steps,rr,h=cross(state,side,n)
                rows.append((n,es,eside,steps,h))
            # summarize
            print(f"\n enter {state} from {side}:")
            for n,es,eside,steps,h in rows:
                print(f"   n={n:>3}: -> {es} exit {eside}  steps={steps}  {'HALT' if h else ''}")
