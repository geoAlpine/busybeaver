#!/usr/bin/env python3
"""
o3 skeleton diff (2026-07-06): print the full compressed skeletons of a few
consecutive milestone chunks (a=60 generation) to see WHY they differ.
"""
import sys
from collections import defaultdict
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from o3_template_scan import M, compress, SN

def run_chunks(s0,s1):
    SZ=1<<24
    tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; lo=hi=pos
    cur=[]; out=[]
    for step in range(s1):
        r=tape[pos]; a=M[st][r]
        if a is None: break
        if st==0 and pos==lo and cur:
            if step>s0: out.append((step,compress(cur)))
            cur=[]
        w,dd,ns=a
        cur.append((st,r,w,dd))
        tape[pos]=w; pos+=dd; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return out

def show(comp):
    parts=[]
    for e in comp:
        if e[0]=='S':
            cyc=''.join(f"{SN[c[0]]}{c[1]}" for c in e[1])
            parts.append(f"[{cyc}]x{e[2]}")
        else:
            c=e[1]; parts.append(f"{SN[c[0]]}{c[1]}{c[2]}{'R' if c[3]==1 else 'L'}")
    return ' '.join(parts)

if __name__=='__main__':
    chunks=run_chunks(8792,10500)
    for step,comp in chunks:
        print(f"=== chunk ending step {step} ({sum(e[2]*len(e[1]) if e[0]=='S' else 1 for e in comp)} steps) ===")
        print(show(comp))
        print()
