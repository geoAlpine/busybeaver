#!/usr/bin/env python3
"""x2lf_glue.py -- STAGING (A) for the List.foldl closure of carry_step.

§5aa established: REGEN(k) call-list is list(k) = [4,5,...,k-2] ++ list(k-1), a CLEAN
self-similar Nat/List recursion (arity (k-5)(k-4)/2, unbounded -- but that is FINE for a
List.foldl WF recursion since each element k' < k).

The DECISIVE remaining question for the foldl closure:
  Is the PER-POSITION GLUE (the tape segment separating REGEN(k'_i) from REGEN(k'_{i+1})
  in the flattened call-list) forall-PARAMETRIC -- a fixed motif / computable-length
  transport, the SAME at every position and level -- or does it vary irregularly?

We extract, cell-for-cell from the faithful build(2) orbit, the FULL token decomposition of
REGEN(k) for k=5..8, then isolate every glue segment and organize it by call-list position.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def exitSteps(k): return 2**(2*k-3)+k*2**(k-1)+2**(k-2)+2
def termSteps(k): return 2**(k+1)+k+5
REGEN={k:exitSteps(k) for k in range(4,9)}
TERM ={k:termSteps(k) for k in range(3,10)}

# self-similar call-list list(k) = range'(4,k-5) ++ list(k-1), base list(4)=list(5)=[]
def call_list(k):
    if k<=5: return []
    return list(range(4,k-1)) + call_list(k-1)
for k in range(4,10):
    print(f"call_list({k}) = {call_list(k)}   arity={len(call_list(k))}  (k-5)(k-4)/2={(k-5)*(k-4)//2}")

def anchors(cap):
    sim=build(2); sim.step(); A=[]
    while sim.n<cap:
        if sim.st=='E' and sim.h==0: A.append(sim.n)
        if not sim.step(): break
    return A
A=anchors(46000)
print(f"\ncollected {len(A)} E-on-0 anchors up to n<46000")

def term_windows(k):
    g=TERM[k]; return [(A[i],A[i+1]) for i in range(len(A)-1) if A[i+1]-A[i]==g]
def regen_windows(k):
    L=REGEN[k]; return [(e-L,e) for (s,e) in term_windows(k)]

def decompose(a,b,maxk):
    """greedy largest-block cover; return full token list of
    ('R',k',len) / ('T',k',len) / ('g',None,len)."""
    RB=[(s,e,('R',kk),e-s) for kk in range(4,maxk+1) for (s,e) in regen_windows(kk) if a<=s and e<=b and e-s<b-a]
    TB=[(s,e,('T',kk),e-s) for kk in range(3,maxk+2) for (s,e) in term_windows(kk) if a<=s and e<=b and e-s<b-a]
    all_=RB+TB
    seg=[]; pos=a
    while pos<b:
        here=[x for x in all_ if x[0]==pos]
        if here:
            here.sort(key=lambda x:-x[3]); x=here[0]
            seg.append((x[2][0],x[2][1],x[3])); pos=x[1]
        else:
            na=[c for c in A if c>pos and c<=b]
            nxt=na[0] if na else b
            seg.append(('g',None,nxt-pos)); pos=nxt
    return seg

# ---- flatten to the REGEN-call skeleton: glue-runs BETWEEN consecutive REGEN calls ----
def regen_skeleton(seg):
    """Return (lead_glue_tokens, [(k', glue_after_tokens)...]) where glue tokens are the
    T/g pieces between this REGEN call and the next REGEN call (or end)."""
    calls=[]; cur=[]; lead=None; started=False
    for t in seg:
        if t[0]=='R':
            if not started:
                lead=cur; cur=[]; started=True
            else:
                calls.append(cur); cur=[]
            calls_marker=t[1]
            cur.append(('CALL',t[1]))
        else:
            cur.append(t)
    calls.append(cur)
    if not started:
        return cur, []   # no REGEN calls (k=5): all glue
    return lead, calls

def toklen(tok):
    if tok[0]=='CALL': return None
    return tok[2] if tok[0]=='g' else TERM[tok[1]]

def compact(seg):
    out=[]
    for t in seg:
        if t[0]=='R': out.append(f"R{t[1]}")
        elif t[0]=='T': out.append(f"T{t[1]}")
        else: out.append(f"g{t[2]}")
    return " ".join(out)

print("\n===== FULL TOKEN DECOMPOSITION, REGEN(k) k=5..8 =====")
decomps={}
for k in range(5,9):
    rw=regen_windows(k)
    if not rw:
        print(f"REGEN({k}): NOT FOUND"); continue
    a,b=rw[0]
    seg=decompose(a,b,k-1)
    decomps[k]=seg
    calls=[t[1] for t in seg if t[0]=='R']
    print(f"REGEN({k}) [{a},{b}] len={b-a} calls={calls}:")
    print("   "+compact(seg))

# ---- isolate glue BETWEEN consecutive REGEN calls, as PURE step counts (merge T into glue-run) ----
print("\n===== GLUE BETWEEN CONSECUTIVE REGEN CALLS (merged run lengths) =====")
def between_glue(seg):
    """list of glue-run TOTAL lengths: [lead ; between call_i and call_{i+1} ...; trailing]."""
    runs=[]; cur=0
    for t in seg:
        if t[0]=='R':
            runs.append(cur); cur=0
        else:
            cur += (t[2] if t[0]=='g' else TERM[t[1]])
    runs.append(cur)
    return runs
for k in range(5,9):
    if k in decomps:
        print(f"REGEN({k}): between-glue runs = {between_glue(decomps[k])}")

# ---- self-similarity test: is decomp(k) 's REGEN-call TAIL == call_list(k-1)?  and does the
#      glue in the tail match REGEN(k-1)'s glue?  (the foldl-closure requirement) ----
print("\n===== SELF-SIMILAR TAIL TEST (foldl closure requirement) =====")
for k in range(6,9):
    if k in decomps and (k-1) in decomps:
        ck=[t[1] for t in decomps[k] if t[0]=='R']
        ck1=[t[1] for t in decomps[k-1] if t[0]=='R']
        prefix=list(range(4,k-1))
        print(f"k={k}: calls={ck}  expected prefix{prefix}++calls(k-1){ck1} => {prefix+ck1}  MATCH={ck==prefix+ck1}")

# ---- decisive: token-sequence of the between-glue runs, per call position, across k ----
print("\n===== PER-POSITION GLUE TOKEN SEQUENCES (parametricity probe) =====")
def glue_token_runs(seg):
    """between-glue as TOKEN lists (not merged), so we can compare motif shape."""
    runs=[]; cur=[]
    for t in seg:
        if t[0]=='R':
            runs.append(cur); cur=[]
        else:
            cur.append(f"T{t[1]}" if t[0]=='T' else f"g{t[2]}")
    runs.append(cur)
    return runs
for k in range(5,9):
    if k in decomps:
        gr=glue_token_runs(decomps[k])
        print(f"REGEN({k}) glue-runs by position:")
        for i,r in enumerate(gr):
            print(f"    pos {i}: {r}")
