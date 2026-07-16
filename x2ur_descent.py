#!/usr/bin/env python3
"""x2ur_descent.py -- DECISIVE Q1 probe for the unified-recursion feasibility study.

Extract the DESCENT GLUE a->4 (the odometer carry-completion re-cascade) cell-for-cell
from the faithful build(2) orbit, at a=5,6,7 (inside REGEN(7),(8),(9)), and test whether
it DECOMPOSES into REGEN / TERM / sweepEF proven pieces -- i.e. whether the glue family is
itself REGEN-shaped (one self-referential recursion) or a genuinely different function
(mutual recursion).  Also tests SELF-SIMILARITY: is glue(a->4) = prefix ++ glue((a-1)->4) ++ suffix?
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def exitSteps(k): return 2**(2*k-3)+k*2**(k-1)+2**(k-2)+2
def termSteps(k): return 2**(k+1)+k+5
REGEN={k:exitSteps(k) for k in range(4,11)}
TERM ={k:termSteps(k) for k in range(3,12)}

CAP=141000
sim=build(2); sim.step(); A=[]
while sim.n<CAP:
    if sim.st=='E' and sim.h==0: A.append(sim.n)
    if not sim.step(): break
print(f"anchors: {len(A)} last={A[-1]}")

def tw(k): g=TERM[k]; return [(A[i],A[i+1]) for i in range(len(A)-1) if A[i+1]-A[i]==g]
def rw(k): L=REGEN[k]; return [(e-L,e) for (s,e) in tw(k)]

# full token decomposition of window [a,b] using REGEN/TERM landmarks + glue 'g'
def decompose(a,b,maxk):
    RB=[(s,e,('R',kk),e-s) for kk in range(4,maxk+1) for (s,e) in rw(kk) if a<=s and e<=b and e-s<b-a]
    TB=[(s,e,('T',kk),e-s) for kk in range(3,maxk+2) for (s,e) in tw(kk) if a<=s and e<=b and e-s<b-a]
    all_=RB+TB; seg=[]; pos=a
    while pos<b:
        here=[x for x in all_ if x[0]==pos]
        if here:
            here.sort(key=lambda x:-x[3]); x=here[0]; seg.append((x[2][0],x[2][1],x[3])); pos=x[1]
        else:
            na=[c for c in A if c>pos and c<=b]; nxt=na[0] if na else b
            seg.append(('g',None,nxt-pos)); pos=nxt
    return seg

# identify the descent glue a->4 windows: between a REGEN(a) call and the following REGEN(4)
def descent_windows(k):
    """inside REGEN(k), find [end of REGEN(a), start of next REGEN(4)] windows for a>=5."""
    a,b=rw(k)[0]; seg=decompose(a,b,k-1)
    pos=a; out=[]; calls=[]
    spans=[]
    for t in seg:
        spans.append((pos,pos+t[2],t)); pos+=t[2]
    # walk consecutive REGEN calls
    Rspans=[(s,e,t[1]) for (s,e,t) in spans if t[0]=='R']
    for i in range(len(Rspans)-1):
        s0,e0,k0=Rspans[i]; s1,e1,k1=Rspans[i+1]
        if k0>=5 and k1==4:
            out.append((k0, e0, s1))   # descent glue window
    return out

print("\n===== DESCENT GLUE a->4 windows =====")
descs={}
for k in range(7,10):
    if not rw(k): continue
    for (a, s, e) in descent_windows(k):
        print(f"  in REGEN({k}): descent {a}->4  [{s},{e}] len={e-s}")
        descs.setdefault(a,[]).append((k,s,e,e-s))

print("\n===== Q1: DECOMPOSE each descent glue a->4 into REGEN/TERM/glue pieces =====")
for a in sorted(descs):
    for (k,s,e,ln) in descs[a]:
        seg=decompose(s,e,9)
        toks=[(t[0] if t[0]=='g' else f"{t[0]}{t[1]}", t[2]) for t in seg]
        Rcalls=[t[1] for t in seg if t[0]=='R']
        Tcalls=[t[1] for t in seg if t[0]=='T']
        print(f"  descent {a}->4 (len {ln}, in REGEN({k})):")
        print(f"      tokens={toks}")
        print(f"      REGEN sub-calls={Rcalls}  TERM sub-calls={Tcalls}")

print("\n===== Q1b: SELF-SIMILARITY -- is glue(a->4) a suffix-extension of glue((a-1)->4)? =====")
# compare relative (state,head,dpos) traces of descent 6->4 vs 5->4 (suffix alignment)
def rel_trace(s,e):
    sim=build(2); sim.step()
    while sim.n<s:
        if not sim.step(): break
    p0=sim.pos; tr=[]
    while sim.n<e:
        tr.append((sim.st,sim.h,sim.pos-p0));
        if not sim.step(): break
    return tr
if 5 in descs and 6 in descs:
    t5=rel_trace(descs[5][0][1],descs[5][0][2])
    t6=rel_trace(descs[6][0][1],descs[6][0][2])
    print(f"  len(5->4)={len(t5)} len(6->4)={len(t6)}")
    # suffix match: does t6 end with t5 (relative to their own ends)?
    def suffix_match(big,small):
        m=0
        for i in range(1,min(len(big),len(small))+1):
            if big[-i][:2]==small[-i][:2]: m=i
            else: break
        return m
    def prefix_match(big,small):
        m=0
        for i in range(min(len(big),len(small))):
            if big[i][:2]==small[i][:2]: m=i+1
            else: break
        return m
    print(f"  common (state,head) SUFFIX length: {suffix_match(t6,t5)} of {len(t5)}")
    print(f"  common (state,head) PREFIX length: {prefix_match(t6,t5)} of {len(t5)}")
