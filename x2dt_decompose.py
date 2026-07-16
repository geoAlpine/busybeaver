#!/usr/bin/env python3
"""x2dt_decompose.py -- THE DECISIVE TEST for a BOUNDED-ARITY (<=4) transport recursion.

Lead: exitSteps(k) satisfies an order-4 linear recurrence (chi=(x-4)(x-2)^2(x-1)),
so maybe REGEN(k) reuses REGEN(k-1..k-4) a BOUNDED number of times + parametric glue,
under a decomposition ALIGNED with the recurrence -- which would close carry_step.

We test this two ways:
  (A) STRUCTURAL, cell-for-cell: for each REGEN(k) window (k=4..8) extracted from the
      faithful build(2) orbit, find its EXACT contiguous decomposition into lower REGEN
      and TERM windows + glue, and count the lower-REGEN ARITY. Does arity stay <=4?
  (B) ARITHMETIC: the recurrence coefficients are (9,-28,36,-16) -- NEGATIVE. A transport
      composition ADDS step counts, so it can only realize a NONNEGATIVE combination
      es(k)=sum c_i es(k-i)+g(k), c_i>=0 int, g(k)>=0. Test whether ANY bounded (sum c_i<=4)
      nonneg combination with SUBDOMINANT (o(4^k)) glue reproduces es(k) for all k.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def exitSteps(k):
    return 2**(2*k-3) + k*2**(k-1) + 2**(k-2) + 2
def termSteps(k):
    return 2**(k+1) + k + 5

REGEN = {k: exitSteps(k) for k in range(4,9)}   # 70,218,722,2530,9282
TERM  = {k: termSteps(k) for k in range(3,10)}  # 24,41,74,139,268,525,...

print("exitSteps k=4..9:", {k:exitSteps(k) for k in range(4,10)})
print("termSteps k=3..9:", {k:termSteps(k) for k in range(3,10)})

# ---- (B) arithmetic: recurrence & overshoot ----
print("\n===== (B) ARITHMETIC OBSTRUCTION =====")
def rec(k):  # es(k) = 9 es(k-1) -28 es(k-2) +36 es(k-3) -16 es(k-4)
    return 9*exitSteps(k-1)-28*exitSteps(k-2)+36*exitSteps(k-3)-16*exitSteps(k-4)
print("order-4 recurrence holds k=8..14:",
      all(exitSteps(k)==rec(k) for k in range(8,15)))
print("coefficients (9,-28,36,-16) -> two are NEGATIVE (cannot be a composition arity)")
print("residual es(k)-c*es(k-1) for c=1..4 (must be >=0 AND subdominant for a valid glue):")
for c in range(1,5):
    row=[]
    for k in range(6,12):
        row.append(exitSteps(k)-c*exitSteps(k-1))
    print(f"  c={c}: {row}")
print("  closed form es(k)-4es(k-1) = 2^(k-2)*(3-2k)-6  (NEGATIVE for k>=4):",
      [exitSteps(k)-4*exitSteps(k-1) for k in range(4,10)])

# brute: is there a FIXED nonneg (c1,c2,c3,c4), sum<=4, and a glue g(k) that is
# a fixed low-degree*exponential 'parametric' form, matching es(k) for all k>=8?
# We demand the residual r(k)=es(k)-sum c_i es(k-i) be >=0 for all k in test range
# AND be 'subdominant': r(k)/es(k) -> 0 (glue must not itself carry the 4^k weight,
# else it is not a bounded-description glue but re-encodes the whole transport).
print("\nbounded nonneg combos (sum c_i<=4) with r(k)>=0 all k in 8..20 and r subdominant:")
found=[]
KS=list(range(8,21))
for c1 in range(5):
 for c2 in range(5-c1):
  for c3 in range(5-c1-c2):
   for c4 in range(5-c1-c2-c3):
    if c1+c2+c3+c4==0: continue
    r=[exitSteps(k)-(c1*exitSteps(k-1)+c2*exitSteps(k-2)+c3*exitSteps(k-3)+c4*exitSteps(k-4)) for k in KS]
    if all(x>=0 for x in r):
        ratio=r[-1]/exitSteps(KS[-1])
        found.append((c1,c2,c3,c4,ratio,r[0],r[-1]))
for f in found:
    c1,c2,c3,c4,ratio,r0,rl=f
    tag="SUBDOMINANT glue" if ratio<0.05 else "glue is Theta(4^k) -> re-encodes whole transport"
    print(f"  (c1,c2,c3,c4)=({c1},{c2},{c3},{c4}) r(8)={r0} r(20)/es(20)={ratio:.4f}  [{tag}]")
if not found:
    print("  NONE: no bounded nonneg combination keeps residual >=0.")

# ---- (A) structural cell-for-cell decomposition ----
print("\n===== (A) STRUCTURAL cell-for-cell decomposition =====")
def left_solid(sim):
    L=sim.L; i=0
    while i<len(L) and L[-1-i]==1: i+=1
    return i
def anchors(cap):
    sim=build(2); sim.step(); A=[]
    while sim.n<cap:
        if sim.st=='E' and sim.h==0: A.append(sim.n)
        if not sim.step(): break
    return A
A=anchors(46000)
print(f"collected {len(A)} E-on-0 anchors up to n<46000")

def term_windows(k):
    g=TERM[k]; return [(A[i],A[i+1]) for i in range(len(A)-1) if A[i+1]-A[i]==g]
def regen_windows(k):
    L=REGEN[k]; return [(e-L,e) for (s,e) in term_windows(k)]

# recursive greedy: cover [a,b] preferring the LARGEST lower REGEN block, then TERM,
# else glue to next anchor. Count REGEN reuse arity per level.
def all_regen_blocks(maxk):
    B={}
    for k in range(4,maxk+1):
        B[k]=regen_windows(k)
    return B

def decompose(a,b,maxk):
    """left-to-right, at each pos take the largest lower-REGEN block (k'<current)
    starting exactly there that fits and isn't the whole window; else TERM; else glue."""
    RB=[]
    for k in range(4,maxk+1):
        for (s,e) in regen_windows(k):
            if a<=s and e<=b and (e-s)<(b-a): RB.append((s,e,k,e-s))
    TB=[]
    for k in range(3,maxk+2):
        for (s,e) in term_windows(k):
            if a<=s and e<=b and (e-s)<(b-a): TB.append((s,e,k,e-s))
    seg=[]; pos=a; arity=0
    while pos<b:
        # largest REGEN starting exactly at pos
        here=[x for x in RB if x[0]==pos]
        if here:
            here.sort(key=lambda x:-x[3]); x=here[0]
            seg.append(("REGEN",x[2],x[3])); pos=x[1]; arity+=1; continue
        hereT=[x for x in TB if x[0]==pos]
        if hereT:
            hereT.sort(key=lambda x:-x[3]); x=hereT[0]
            seg.append(("TERM",x[2],x[3])); pos=x[1]; continue
        na=[c for c in A if c>pos and c<=b]
        nxt=na[0] if na else b
        seg.append(("glue",None,nxt-pos)); pos=nxt
    return seg,arity

print("\n arity of strictly-lower REGEN reuse per level (largest-block greedy):")
for k in range(5,9):
    rw=regen_windows(k)
    if not rw:
        print(f"  REGEN({k}): NOT FOUND in orbit window (need larger cap)"); continue
    a,b=rw[0]
    seg,arity=decompose(a,b,k-1)
    calls=[s for s in seg if s[0]=="REGEN"]
    onebits=bin(2**k-3).count("1")
    print(f"  REGEN({k}) [{a},{b}] len={b-a}: lower-REGEN arity={arity}  "
          f"calls={[ (c[1]) for c in calls]}  (2^{k}-3 has {onebits} one-bits)")
    # show the segmentation compactly
    comp=[]
    for s in seg:
        comp.append(f"R{s[1]}" if s[0]=="REGEN" else (f"T{s[1]}" if s[0]=="TERM" else f"g{s[2]}"))
    print("       "+" ".join(comp))
