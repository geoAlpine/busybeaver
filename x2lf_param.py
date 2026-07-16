#!/usr/bin/env python3
"""x2lf_param.py -- DECISIVE per-position-glue PARAMETRICITY test for the foldl closure.

From x2lf_glue.py the call-list is clean self-similar list(k)=[4..k-2]++list(k-1) and the
between-REGEN glue depends on the (k'->k'') TRANSITION.  This probe:
  (1) CONFIRMS the 'short' transitions are byte-identical TRANSLATION-INVARIANT transports
      (constant (state,head,dpos) trace + constant length across all occurrences/levels).
  (2) QUANTIFIES the 'ascending' transitions -- do they carry a CORE sweepEF build-up whose
      LENGTH GROWS with the odometer height at that position (=> NOT a fixed motif)?
  (3) tries to reach REGEN(9) to test growth of the (5->6) and (6->4) glue across levels.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def exitSteps(k): return 2**(2*k-3)+k*2**(k-1)+2**(k-2)+2
def termSteps(k): return 2**(k+1)+k+5
REGEN={k:exitSteps(k) for k in range(4,10)}
TERM ={k:termSteps(k) for k in range(3,11)}

CAP=140000
def run_full():
    sim=build(2); sim.step()
    A=[]; trace=[]  # trace[n] = (state,head) rel snapshot for TI comparison
    while sim.n<CAP:
        if sim.st=='E' and sim.h==0: A.append(sim.n)
        if not sim.step(): break
    return A
A=run_full()
print(f"anchors up to {CAP}: {len(A)}, last={A[-1] if A else None}")

def term_windows(k):
    g=TERM[k]; return [(A[i],A[i+1]) for i in range(len(A)-1) if A[i+1]-A[i]==g]
def regen_windows(k):
    L=REGEN[k]; return [(e-L,e) for (s,e) in term_windows(k)]
for k in range(5,10):
    rw=regen_windows(k)
    print(f"REGEN({k}): {len(rw)} window(s); first={rw[0] if rw else None}")

# --- decompose a window into full token list; return list of ('R',k')/('T',k')/('g',len) ---
def decompose(a,b,maxk):
    RB=[(s,e,('R',kk),e-s) for kk in range(4,maxk+1) for (s,e) in regen_windows(kk) if a<=s and e<=b and e-s<b-a]
    TB=[(s,e,('T',kk),e-s) for kk in range(3,maxk+2) for (s,e) in term_windows(kk) if a<=s and e<=b and e-s<b-a]
    all_=RB+TB; seg=[]; pos=a
    while pos<b:
        here=[x for x in all_ if x[0]==pos]
        if here:
            here.sort(key=lambda x:-x[3]); x=here[0]; seg.append((x[2][0],x[2][1],x[3])); pos=x[1]
        else:
            na=[c for c in A if c>pos and c<=b]; nxt=na[0] if na else b
            seg.append(('g',None,nxt-pos)); pos=nxt
    return seg

# between-glue as (transition, raw_window[start,end]) so we can grab the exact tape trace
def transitions(k):
    a,b=regen_windows(k)[0]; seg=decompose(a,b,k-1)
    # positions of REGEN calls (their [s,e]) inside [a,b]
    Rpos=[]; pos=a
    for t in seg:
        if t[0]=='R': Rpos.append((pos,pos+t[2],t[1])); pos+=t[2]
        else: pos+=t[2]
    # glue windows: [a, first R start], [R_i end, R_{i+1} start], [last R end, b]
    calls=[t[1] for t in seg if t[0]=='R']
    out=[]
    prev_end=a; prev_k='START'
    for (rs,re,rk) in Rpos:
        out.append((prev_k,rk,prev_end,rs)); prev_end=re; prev_k=rk
    out.append((prev_k,'END',prev_end,b))
    return calls,out

print("\n===== between-glue windows by TRANSITION =====")
allglue={}  # (fromk,tok) -> list of (k, [start,end], len)
for k in range(6,10):
    if not regen_windows(k): continue
    calls,tr=transitions(k)
    print(f"REGEN({k}) calls={calls}:")
    for (fk,tk,s,e) in tr:
        print(f"    {fk}->{tk}: [{s},{e}] len={e-s}")
        allglue.setdefault((fk,tk),[]).append((k,s,e,e-s))

# (1) byte-identical TI test for repeated transitions: compare relative (state,head,dpos) trace
def rel_trace(s,e):
    sim=build(2); sim.step()
    while sim.n<s:
        if not sim.step(): break
    p0=sim.pos; tr=[]
    while sim.n<e:
        tr.append((sim.st,sim.h,sim.pos-p0))
        if not sim.step(): break
    return tuple(tr)

print("\n===== (1) TRANSLATION-INVARIANCE of repeated transitions (byte-identical trace) =====")
for key,occ in sorted(allglue.items(), key=lambda x:str(x[0])):
    if len(occ)<2: continue
    lens={o[3] for o in occ}
    traces=[rel_trace(o[1],o[2]) for o in occ]
    ident=all(t==traces[0] for t in traces)
    print(f"  {key[0]}->{key[1]}: {len(occ)} occurrences  lengths={sorted(lens)}  "
          f"BYTE-IDENTICAL={ident}")

# (2) growth of ascending build-ups: characterize each transition's max sweep peak (=height)
def token_peaks(s,e):
    """merge into g-run/token; return the ascending glue 'peaks' (g-lengths >5) as a proxy
    for the CORE sweepEF build-up height."""
    a,b=s,e
    seg=decompose(a,b,9)
    peaks=[t[2] for t in seg if t[0]=='g' and t[2]>5]
    return peaks
print("\n===== (2) ASCENDING build-up size per transition (max glue peak ~ CORE height) =====")
for key,occ in sorted(allglue.items(), key=lambda x:str(x[0])):
    for (k,s,e,ln) in occ:
        pk=token_peaks(s,e)
        print(f"  {key[0]}->{key[1]} @REGEN({k}): len={ln}  #peaks={len(pk)}  maxpeak={max(pk) if pk else 0}")
