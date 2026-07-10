#!/usr/bin/env python3
"""Certify halt char + dump configs at right-turnarounds across a generation.
HALT claim: halt <=> rightward E-scan reads b0b1b2b3 = 0001 (E=0,F=0,A=0,B=1).
Instrument: at each B-visit record the 0-run the scanner sits in and the bit after it."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN="ABCDEF"

def dump_gen(s0, s1, SZ=1<<20):
    M = parse(SPEC)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    while step < s1:
        r = tape[pos]
        act = M[st][r]
        if act is None: print("HALT",step); return
        ww,d,ns = act
        # print at C-entry turning left at a new-ish spot, or just sample sparsely
        tape[pos]=ww; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        elif pos>hi: hi=pos
        if s0<=step<=s1 and st==2 and d==-1:  # entered C moving left (turnaround)
            rr = rle(tape,lo,hi)
            mx = max((n for c,n in rr if c==1),default=0)
            print(f"step={step:>7} C-turn pos={pos-off:>5} mx={mx:>4} tot1={sum(n for c,n in rr if c==1):>5}  {rr}")

def zerorun_at_B(maxsteps, SZ=1<<24):
    """At each B-visit, measure the 0-run [scanner is inside] and the bit that ends it."""
    M=parse(SPEC); tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; step=0; lo=hi=pos
    stats={}  # (leftrun0, rightbit) -> count ; also max 0-run to the right of B
    maxzr=0; ex=[]
    while step<maxsteps:
        r=tape[pos]
        if st==1:  # B about to read tape[pos]
            # count contiguous zeros starting at pos going right
            j=pos; z=0
            while j<hi+2 and tape[j]==0: z+=1; j+=1
            endbit = tape[j] if j<=hi+1 else 0
            key=(z,endbit)
            stats[key]=stats.get(key,0)+1
            if z>maxzr: maxzr=z; ex.append((step,z,endbit,pos-off))
            if r==1: print("HALT B reads 1",step); return stats,maxzr,ex
        act=M[st][r]
        if act is None: return stats,maxzr,ex
        ww,d,ns=act; tape[pos]=ww; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        elif pos>hi: hi=pos
    return stats,maxzr,ex

if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "zr"
    if mode=="gen":
        dump_gen(int(sys.argv[2]),int(sys.argv[3]))
    else:
        cap=int(sys.argv[2]) if len(sys.argv)>2 else 20_000_000
        stats,maxzr,ex=zerorun_at_B(cap)
        print(f"B-visit 0-run stats (zeros-to-right-of-B-pos, ending-bit): ")
        for k in sorted(stats): print(f"  zeros={k[0]} endbit={k[1]}: count={stats[k]:,}")
        print(f"max zeros-run seen at B = {maxzr}")
        print("examples (step, zeros, endbit, pos):", ex[-8:])
