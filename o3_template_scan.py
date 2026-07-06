#!/usr/bin/env python3
"""
o3 TEMPLATE SCAN (2026-07-06) -- port of the o4 pipeline, step 4 (discovery; pure concrete).
Segment the concrete run at milestones (state A at left frontier). For each
milestone-to-milestone CHUNK, compress the (state,read,write,dir) event stream
(maximal periodic runs, period<=6 -> SWEEP with length abstracted) and hash the
skeleton. Group chunks by generation (digit string == 0^a 1^k). Question: is each
generation a rigid  prefix-chunks . body-chunk^r . suffix-chunks  like o4?
Everything here is [OBSERVED] discovery -- the proof path is o3_body_proof.py.
"""
import sys, hashlib
from collections import Counter, defaultdict

def parse(spec):
    M=[[None,None] for _ in range(6)]
    for k,blk in enumerate(spec.split('_')):
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[k][r]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,"ABCDEF".index(c[2]))
    return M
M=parse("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC")
SN="ABCDEF"
PMAX=24

def _minimal_period(w):
    n=len(w)
    for q in range(1,n):
        if n%q==0 and w[:q]*(n//q)==w: return q
    return n

def compress(trace):
    """maximal periodic runs (minimal period p=2..PMAX, >=3 full periods) -> SWEEP."""
    out=[]; i=0; n=len(trace)
    while i<n:
        best=None
        for p in range(2,PMAX+1):
            if i+3*p>n: break
            j=i
            while j+p<n and trace[j+p]==trace[j]: j+=1
            L=j+p-i
            if L>=3*p and _minimal_period(tuple(trace[i:i+p]))==p:
                best=(p,L); break
        if best:
            p,L=best; take=L-(L%p)
            out.append(('S',tuple(trace[i:i+p]),take//p)); i+=take
        else:
            out.append(('E',trace[i])); i+=1
    return out

def skel_hash(comp):
    skel=[]; lens=[]
    for e in comp:
        if e[0]=='S': skel.append(('S',e[1])); lens.append(e[2])
        else: skel.append(e)
    h=hashlib.sha1(repr(skel).encode()).hexdigest()[:10]
    return h,tuple(lens)

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

def run(N):
    SZ=1<<25
    tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; lo=hi=pos
    chunks=[]   # (start_step, hash, lens, nsteps, marker) marker=(a,k) if 0^a1^k else None
    cur=[]; cstart=0
    for step in range(N):
        r=tape[pos]; a=M[st][r]
        if a is None:
            print(f"HALT step {step}"); break
        if st==0 and pos==lo and cur:
            d=digits_str(tape,lo,hi)
            mk=None
            if d:
                t=d.rstrip('1'); k=len(d)-len(t)
                if k>=1 and set(t)<={'0'}: mk=(len(t),k)
            h,lens=skel_hash(compress(cur))
            chunks.append((cstart,h,lens,step-cstart,mk))
            cur=[]; cstart=step
        w,dd,ns=a
        cur.append((st,r,w,dd))
        tape[pos]=w; pos+=dd; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return chunks

if __name__=='__main__':
    N=int(sys.argv[1]) if len(sys.argv)>1 else 120_000_000
    chunks=run(N)
    print(f"chunks (milestone-to-milestone): {len(chunks)}")
    # generation boundaries
    gi=[i for i,c in enumerate(chunks) if c[4] is not None]
    print(f"generation-marker chunks: {len(gi)}")
    # per generation: sequence of chunk hashes
    hcnt=Counter(h for _,h,_,_,_ in chunks)
    print(f"distinct chunk skeleton hashes overall: {len(hcnt)}; top 12: {hcnt.most_common(12)}")
    for a0 in range(len(gi)-1):
        i0,i1=gi[a0],gi[a0+1]
        seq=[chunks[i][1] for i in range(i0,i1)]
        mk=chunks[i0][4]
        # run-length encode the hash sequence
        rle=[]
        for h in seq:
            if rle and rle[-1][0]==h: rle[-1][1]+=1
            else: rle.append([h,1])
        s=' '.join(f"{h}x{c}" if c>1 else h for h,c in rle)
        if len(s)>200: s=s[:200]+'...'
        print(f"gen a={mk[0]:<5} k={mk[1]:<3} chunks={i1-i0:>5}: {s}")
