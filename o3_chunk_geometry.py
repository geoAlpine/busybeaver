#!/usr/bin/env python3
"""
o3 chunk geometry (2026-07-06): per milestone chunk, record
  lo, hi (global extremes), chunk head-span, chunk step count,
  defect tape position (leftmost length-2 block), marker start,
to pin what the head touches per chunk.
"""
import sys

def parse(spec):
    M=[[None,None] for _ in range(6)]
    for k,blk in enumerate(spec.split('_')):
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[k][r]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,"ABCDEF".index(c[2]))
    return M
M=parse("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC")

def blocks(tape,lo,hi):
    b=[]; i=lo
    while i<=hi:
        s=tape[i]; j=i
        while j<=hi and tape[j]==s: j+=1
        b.append((s,j-i,i)); i=j
    return [x for x in b if x[0]==1]

if __name__=='__main__':
    s0=int(sys.argv[1]); s1=int(sys.argv[2])
    SZ=1<<24
    tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; lo=hi=pos
    clo=chi=pos; cstart=0
    for step in range(s1):
        r=tape[pos]; a=M[st][r]
        if a is None: print(f"HALT {step}"); break
        if st==0 and pos==lo and step>=s0:
            ones=blocks(tape,lo,hi)
            twos=[x for x in ones if x[1]==2]
            d2 = twos[0][2]-off if twos else None
            # marker = maximal run of length-2 blocks at the right end
            print(f"step {step:>10,} chunk_steps={step-cstart:>6} chunk_span=[{clo-off:>6},{chi-off:>6}] "
                  f"lo={lo-off:>6} hi={hi-off:>6} head={pos-off:>6} first2blk@{d2} n2={len(twos)} nblk={len(ones)}")
            clo=chi=pos; cstart=step
        w,dd,ns=a
        tape[pos]=w; pos+=dd; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        if pos<clo: clo=pos
        if pos>chi: chi=pos
