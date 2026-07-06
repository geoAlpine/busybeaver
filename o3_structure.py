#!/usr/bin/env python3
"""
o3 STRUCTURE (2026-07-06) -- port of the o4 pipeline, step 2 (+ sweep detection for step 3).
(a) sweep-period detection: maximal periodic stretches of (state,read,write,dir)
    in the concrete microstep trace -- what are o3's uniform sweep cycles?
(b) milestone census: state A at left frontier; digit string (block len-1 -> digit 0,
    block len-2 -> digit 1, single-0 gaps); language check.
(c) generation structure: generation starts = digit string of form 0^a 1^k
    (per O3_TRANSDUCER.md: migrating defect + trailing marker). Record (a,k) per
    generation and measure the counter law Delta-k exactly; test determinism of
    Delta-k on (k mod m, a mod m, ...) small features AND on the FULL previous
    digit string (is the generation map a function of the whole string? it must be --
    the point is what part suffices).
"""
import sys
from collections import defaultdict, Counter

def parse(spec):
    M=[[None,None] for _ in range(6)]
    for k,blk in enumerate(spec.split('_')):
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[k][r]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,"ABCDEF".index(c[2]))
    return M
M=parse("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC")
SN="ABCDEF"

def digits(tape,lo,hi):
    """digit string: scan 1-blocks; digit = len-1; also validate language."""
    b=[]; i=lo
    while i<=hi:
        s=tape[i]; j=i
        while j<=hi and tape[j]==s: j+=1
        b.append((s,j-i)); i=j
    while b and b[0][0]==0: b=b[1:]
    while b and b[-1][0]==0: b=b[:-1]
    if not b: return None,False
    blk=[n for s,n in b if s==1]; gap=[n for s,n in b if s==0]
    ok=all(x in (1,2) for x in blk) and all(g==1 for g in gap)
    return ''.join(str(n-1) for n in blk), ok

def sweep_census(N=200_000):
    """(a) find maximal periodic (period p<=6) stretches >= 12 steps in the trace."""
    tape=defaultdict(int); pos=0; st=0
    trace=[]
    for _ in range(N):
        r=tape[pos]; a=M[st][r]
        if a is None: break
        w,d,ns=a
        trace.append((st,r,w,d))
        if w: tape[pos]=w
        else: tape.pop(pos,None)
        pos+=d; st=ns
    found=Counter()
    i=0; n=len(trace); covered=0
    while i<n:
        best=None
        for p in (2,3,4,5,6):
            j=i
            while j+p<n and trace[j+p]==trace[j]: j+=1
            L=j+p-i
            if L>=12 and len(set(trace[i:i+p]))==p:
                best=(p,L); break
        if best:
            p,L=best
            cyc=tuple(trace[i:i+p])
            take=L-(L%p)
            found[cyc]+=take; covered+=take; i+=take
        else:
            i+=1
    print(f"(a) SWEEP CENSUS over {n:,} steps: coverage {100*covered/n:.1f}%")
    for cyc,tot in found.most_common(12):
        s=' '.join(f"{SN[c[0]]}{c[1]}->{c[2]}{'R' if c[3]==1 else 'L'}" for c in cyc)
        print(f"    p={len(cyc)}  steps={tot:>8,}  cycle: {s}")
    return found

def milestones(N=60_000_000):
    SZ=1<<24
    tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; lo=hi=pos
    ms=[]; lang_bad=0
    for step in range(N):
        r=tape[pos]; a=M[st][r]
        if a is None:
            print(f"HALT step {step}"); break
        if st==0 and pos==lo:
            dig,ok=digits(tape,lo,hi)
            if dig is not None:
                if not ok: lang_bad+=1
                else: ms.append((step,dig))
        w,d,ns=a
        tape[pos]=w; pos+=d; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return ms,lang_bad

if __name__=='__main__':
    sweep_census()
    N=int(sys.argv[1]) if len(sys.argv)>1 else 60_000_000
    ms,lang_bad=milestones(N)
    print(f"\n(b) milestones (A at left frontier, nonempty digit string): {len(ms):,}  "
          f"language violations: {lang_bad}")
    # deduplicate consecutive identical digit strings
    uniq=[]
    for s,d in ms:
        if not uniq or uniq[-1][1]!=d: uniq.append((s,d))
    print(f"    distinct consecutive: {len(uniq):,}")
    print("    first 25 digit strings:")
    for s,d in uniq[:25]: print(f"      step {s:>9,}  {d}")
    # (c) generations: digit string == 0^a 1^k, k>=1
    gens=[]
    for s,d in uniq:
        t=d.rstrip('1'); k=len(d)-len(t)
        if k>=1 and set(t)<={'0'}:
            a=len(t)
            if not gens or gens[-1][1:]!=(a,k): gens.append((s,a,k))
    print(f"\n(c) generations (0^a 1^k form): {len(gens)}")
    print("    (step, a, k):")
    for g in gens[:60]: print(f"      {g[0]:>11,}  a={g[1]:<4} k={g[2]}")
    ks=[k for _,a,k in gens]; aa=[a for _,a,k in gens]
    dk=[ks[i+1]-ks[i] for i in range(len(ks)-1)]
    da=[aa[i+1]-aa[i] for i in range(len(aa)-1)]
    print(f"    k sequence: {ks}")
    print(f"    Delta-k:    {dk}   dist {dict(Counter(dk))}")
    print(f"    a sequence: {aa}")
    print(f"    Delta-a:    {da}   dist {dict(Counter(da))}")
    # determinism probes for Delta-k
    for feat,name in [ (lambda i:(ks[i]%2,), 'k%2'),
                       (lambda i:(ks[i]%2,aa[i]%2), 'k%2,a%2'),
                       (lambda i:(ks[i]%3,aa[i]%3), 'k%3,a%3'),
                       (lambda i:(ks[i]%4,aa[i]%4), 'k%4,a%4'),
                       (lambda i:(aa[i],), 'a exact'),
                       (lambda i:(ks[i],aa[i]), 'k,a exact') ]:
        T=defaultdict(set)
        for i in range(len(dk)): T[feat(i)].add((dk[i],da[i]))
        amb=sum(1 for v in T.values() if len(v)>1)
        print(f"    (dk,da) determined by ({name})? ambiguous {amb}/{len(T)} keys")
