#!/usr/bin/env python3
"""
o3 generation dissection (2026-07-06): dump the digit string at EVERY milestone
inside a window of steps, to see what unbounded state the chunk skeleton encodes.
"""
import sys
from collections import defaultdict

def parse(spec):
    M=[[None,None] for _ in range(6)]
    for k,blk in enumerate(spec.split('_')):
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[k][r]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,"ABCDEF".index(c[2]))
    return M
M=parse("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC")

def digits_str(tape,lo,hi):
    b=[]; i=lo
    while i<=hi:
        s=tape[i]; j=i
        while j<=hi and tape[j]==s: j+=1
        b.append((s,j-i)); i=j
    while b and b[0][0]==0: b=b[1:]
    while b and b[-1][0]==0: b=b[:-1]
    if not b: return None
    return ''.join(str(n-1) for s,n in b if s==1)

if __name__=='__main__':
    s0=int(sys.argv[1]); s1=int(sys.argv[2])
    SZ=1<<24
    tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; lo=hi=pos
    for step in range(s1):
        r=tape[pos]; a=M[st][r]
        if a is None: print(f"HALT {step}"); break
        if st==0 and pos==lo and step>=s0:
            d=digits_str(tape,lo,hi)
            if d is not None:
                print(f"step {step:>10,}  {d}")
        w,dd,ns=a
        tape[pos]=w; pos+=dd; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
