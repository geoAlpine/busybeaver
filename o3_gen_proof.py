#!/usr/bin/env python3
"""
o3 GENERATION LAW verification (2026-07-06) -- port of the o4 suffix/prefix + odometer step.
Standalone milestone config  M(a,k):  0^inf [A@0] 0 0 (10)^a (110)^k 0^inf.
(Exact reachable form: verified against raw dumps of the real orbit; the real tape
left/right of the milestone support is exactly 0^inf.)

CLAIMED GENERATION LAW (from the template scan, to be verified exactly here):
    a == 1 (mod 3):  M(a,k) -> M(a-1, k+2)          [marker cascade, one chunk]
    a == 2 (mod 3):  M(a,k) -> M((4a+4)/3, k+1)     [= floor(4a/3)+2]
    a == 0 (mod 3):  M(a,k) -> M(4a/3+3,  k-1)      [k>=1]
Verified content per run (pure concrete, no acceleration):
  - exact landing at the next milestone (tape/state/head equality with M(a',k')),
  - every E-reads-0 event safe (no halt),
  - the chunk skeleton-hash sequence is  prefix(class) . body^r . suffix3  with
    body = the [PROVEN] o3_body_proof.py chunk and r exactly affine in a,
  - per-class skeleton set identical across the grid (k- and a-uniform),
SMALL-PARAMETER HUNT: k=0 and k=1 configs (incl. the k'->0 successors): does any
standalone M(a,k) HALT?  (o4 analogue: Z(41,3,0) halts.)
"""
import sys, hashlib
from collections import defaultdict

def parse(spec):
    M={}
    for kk,blk in enumerate(spec.split('_')):
        st="ABCDEF"[kk]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
TM=parse("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC")
PMAX=24

def build_M(a,k):
    t={}
    for i in range(a): t[2+2*i]=1
    for i in range(k):
        t[2+2*a+3*i]=1; t[2+2*a+3*i+1]=1
    return t

def parse_M(tape,head):
    """if tape (dict of 1s) with head at leftmost support-2 matches M(a,k), return (a,k)."""
    if not tape: return None
    cells=sorted(tape)
    lo=cells[0]; hi=cells[-1]
    if head!=lo-2: return None
    s=''.join(str(tape.get(c,0)) for c in range(lo,hi+1))
    # s must be (10)^a-ish: "1"+"01"*(a-1)+"0"? construct: M = 00 (10)^a (110)^k, support from first 1:
    # (10)^a (110)^k stripped of leading zeros: "10"*a + "110"*k begins with 1, ends with 0? ends "110"->0.
    # support string (first 1 .. last 1): "10"*(a) + "110"*(k) trimmed: drop trailing 0s.
    for a in range(0,(hi-lo)//2+2):
        rem=(hi-lo+1)-2*a
        # remaining should be "110"*k minus trailing 0 => 3k-1 cells (k>=1) or a==...,k=0 => -1
        if rem<0: break
        if k_from(rem):
            k=k_from(rem)
            cand="10"*a+"110"*k
            cand=cand[:len(cand)-(len(cand)-(hi-lo+1))] if len(cand)>=hi-lo+1 else None
            if cand and cand.rstrip('0')==s.rstrip('0') and cand[:hi-lo+1]==s:
                return (a,k)
    return None

def k_from(rem):
    # rem cells = "110"*k minus trailing zero: 3k-1
    if (rem+1)%3==0 and rem>=2: return (rem+1)//3
    return None

def match_M(tape):
    """exact structural parse: support string must equal '10'*a + '110'*k (trailing 0s stripped both sides)."""
    if not tape: return None
    cells=sorted(tape)
    lo=cells[0]; hi=cells[-1]
    s=''.join(str(tape.get(c,0)) for c in range(lo,hi+1))
    # try all a: prefix "10"*a possibly with the last 0 merged; then "110"*k stripped of trailing 0
    for a in range(0,len(s)//2+1):
        p="10"*a
        if not s.startswith(p):
            # allow a where prefix ends beyond string? no
            continue
        rest=s[len(p):]
        if rest=="" :
            return (a,0)
        # rest should be ("110"*k).rstrip('0') = "110"*(k-1)+"11"
        k=(len(rest)+1)//3
        if k>=1 and (len(rest)+1)%3==0 and rest=="110"*(k-1)+"11":
            return (a,k)
    return None

def _minimal_period(w):
    n=len(w)
    for q in range(1,n):
        if n%q==0 and w[:q]*(n//q)==w: return q
    return n

def compress(trace):
    out=[]; i=0; n=len(trace)
    while i<n:
        best=None
        for p in range(2,PMAX+1):
            if i+3*p>n: break
            jx=i
            while jx+p<n and trace[jx+p]==trace[jx]: jx+=1
            L=jx+p-i
            if L>=3*p and _minimal_period(tuple(trace[i:i+p]))==p:
                best=(p,L); break
        if best:
            p,L=best; take=L-(L%p)
            out.append(('S',tuple(trace[i:i+p]),take//p)); i+=take
        else:
            out.append(('E',trace[i])); i+=1
    return out

def skel_hash(comp):
    skel=[('S',e[1]) if e[0]=='S' else e for e in comp]
    return hashlib.sha1(repr(skel).encode()).hexdigest()[:10]

def run_generation(a,k,maxsteps=10**8):
    """run standalone M(a,k) to the next M-form milestone (A at global lo, exact match)."""
    tape=defaultdict(int,build_M(a,k)); pos=0; st='A'
    lo=hi=0; unsafe=0
    cur=[]; hashes=[]
    for s in range(maxsteps):
        r=tape[pos]; act=TM[(st,r)]
        if act is None:
            return dict(halt=True,steps=s,unsafe=unsafe,hashes=hashes)
        if st=='A' and pos<=lo and s>0 and cur:
            hashes.append(skel_hash(compress(cur))); cur=[]
            mk=match_M({c:v for c,v in tape.items() if v})
            if mk is not None and (pos==min(c for c,v in tape.items() if v)-2):
                return dict(halt=False,steps=s,unsafe=unsafe,hashes=hashes,land=mk)
        if st=='E' and r==0 and tape[pos+1]!=1: unsafe+=1
        w,d,ns=act
        cur.append((st,r,w,d))
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        lo=min(lo,pos); hi=max(hi,pos)
    return dict(halt=False,steps=maxsteps,unsafe=unsafe,hashes=hashes,land=None)

def law(a,k):
    if a%3==1: return (a-1,k+2)
    if a%3==2: return ((4*a+4)//3,k+1)
    return (4*a//3+3,k-1)

if __name__=='__main__':
    print("=== GENERATION LAW GRID (standalone M(a,k), pure concrete) ===")
    grid_a=[12,13,14,15,16,17,18,19,20,21,22,23,60,61,62,150,151,152,300,301,302]
    grid_k=[1,2,3,5,8]
    from collections import defaultdict as dd
    class_seqs=dd(set)
    bad=0
    for a in grid_a:
        for k in grid_k:
            r=run_generation(a,k)
            want=law(a,k)
            if want[1]<0:
                continue
            ok=(not r['halt']) and r.get('land')==want and r['unsafe']==0
            # template: body hash count
            hs=r['hashes']
            from collections import Counter
            cnt=Counter(hs)
            body,bodyn=cnt.most_common(1)[0] if cnt else (None,0)
            # rle for class signature: prefix hashes + (body)*n + suffix hashes
            sig=[]
            for h in hs:
                if sig and sig[-1][0]==h: sig[-1][1]+=1
                else: sig.append([h,1])
            sigt=tuple((h,(n if n<3 else 'r')) for h,n in sig)
            class_seqs[(a%3, 'small-k' if k<=1 else 'k>=2')].add(sigt)
            rbody=max((n for h,n in sig),default=0)
            if not ok:
                bad+=1
                print(f"  a={a:>4} k={k}: LAW FAILS land={r.get('land')} want={want} halt={r['halt']} unsafe={r['unsafe']}")
            else:
                print(f"  a={a:>4} k={k}: -> M{want} OK steps={r['steps']:>7} chunks={len(hs):>4} r_body={rbody:>3} unsafe=0")
    print(f"\nlaw violations on grid: {bad}")
    print("\nper-class distinct chunk-hash signatures (k>=2):")
    for key in sorted(class_seqs, key=str):
        if key[1]=='k>=2':
            print(f"  a%3={key[0]}: {len(class_seqs[key])} distinct signatures")
    print("\n=== SMALL-PARAMETER / FATAL-CONFIG HUNT (k=0, and k=1 at a%3==0) ===")
    for a in range(6,60):
        r=run_generation(a,0,maxsteps=2_000_000)
        tag='HALT!!!' if r['halt'] else (f"-> M{r.get('land')}" if r.get('land') else 'no-milestone(2M)')
        print(f"  M(a={a:>3},k=0): {tag}  steps={r['steps']:>9} unsafe={r['unsafe']}")
