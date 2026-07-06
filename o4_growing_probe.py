# o4 growing-regime PROBE (2026-07-07)
# Targets: the three standalone configs Z(k, g=3, a=0), k in {21,23,27}, left [OPEN] by
# O4_LEDGER_ANALYSIS_2026-07-06 / o4_wander_certify.py: milestone-free, leftmost ~ sqrt(steps),
# 5 segments, no exact window recurrence (NOT translated cyclers).
# GOAL of this probe: dump the tape in run-length form at new-leftmost events (sampled) to
# identify the recurring "generation" structure (their own milestone-analogue).
from collections import defaultdict
import sys

def parse(spec):
    M={}
    for kk,blk in enumerate(spec.split('_')):
        st="ABCDEF"[kk]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

def build_Z(k,g,a):
    t={}
    for i in range(k): t[2*i]=1
    t[2*k]=1; t[2*k+3]=1
    base=2*k+4+g
    for i in range(a): t[base+2*i]=1
    t[base+2*a]=1; t[base+2*a+3]=1
    return t

def rle(tape, lo, hi):
    """run-length encoding of tape[lo..hi] as list of (bit, count); also compress (10)^m."""
    bits=[tape.get(i,0) for i in range(lo,hi+1)]
    # first plain RLE
    out=[]
    i=0
    while i<len(bits):
        j=i
        while j<len(bits) and bits[j]==bits[i]: j+=1
        out.append((bits[i], j-i))
        i=j
    return out

def rle_pattern(tape, lo, hi):
    """higher-level: compress alternating 10-blocks: return string like (10)^m 0^g ..."""
    bits=[tape.get(i,0) for i in range(lo,hi+1)]
    s=''.join(map(str,bits))
    out=[]
    i=0
    n=len(s)
    while i<n:
        # try (10)^m
        m=0
        j=i
        while j+1<n and s[j]=='1' and s[j+1]=='0':
            m+=1; j+=2
        if m>=2:
            out.append(f"(10)^{m}")
            i=j
            continue
        # run of same char
        j=i
        while j<n and s[j]==s[i]: j+=1
        c=s[i]; L=j-i
        if L==1: out.append(c)
        else: out.append(f"{c}^{L}")
        i=j
    return ' '.join(out)

def probe(k, horizon, n_dumps=40):
    tape=defaultdict(int,build_Z(k,3,0)); pos=0; st='E'
    lo=0; hi=max(build_Z(k,3,0)); step=0
    dumps=[]
    next_dump_lo=0
    lo_events=0
    while step<horizon:
        r=tape[pos]; tr=M[(st,r)]
        if tr is None:
            print(f"  Z({k},3,0) HALTS at step {step}!"); return
        w,d,ns=tr
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns; step+=1
        if pos<lo:
            lo=pos; lo_events+=1
            if lo<=next_dump_lo:
                # dump
                hi_now=max((c for c,v in tape.items() if v), default=pos)
                pat=rle_pattern(tape, lo, hi_now)
                dumps.append((step, lo, hi_now, st, pat))
                next_dump_lo=lo-max(2,(-lo)//6)   # geometric-ish sampling
        if pos>hi: hi=pos
    print(f"Z(k={k},g=3,a=0): {step} steps, leftmost={lo} ({lo_events} new-leftmost events), rightmost={hi}")
    for (s,l,h,stt,pat) in dumps:
        print(f"  step={s:>10} lo={l:>7} state={stt} span=[{l},{h}]")
        print(f"    {pat}")
    print()

if __name__=='__main__':
    horizon=int(sys.argv[1]) if len(sys.argv)>1 else 3_000_000
    for k in (21,23,27):
        probe(k,horizon)
