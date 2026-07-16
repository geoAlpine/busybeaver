#!/usr/bin/env python3
"""x2ur_sweep.py -- characterize the descent glue a->4 as a SWEEP with a closed form.
Extract the 'peak' g-lengths (>5) inside each descent glue and test:
  (i)  arithmetic-progression staircase (odometer counting sweep signature)
  (ii) closed-form total length as a function of a
  (iii) the exact tape transform (Lean Cfg) at start and end -- what block height in / out.
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
def tw(k): g=TERM[k]; return [(A[i],A[i+1]) for i in range(len(A)-1) if A[i+1]-A[i]==g]
def rw(k): L=REGEN[k]; return [(e-L,e) for (s,e) in tw(k)]

# descent windows (from x2ur_descent)
DESC={5:(13453,14542), 6:(33830,37982), 7:(114703,131134)}

def peaks(s,e):
    """anchor-gap sequence inside [s,e]; return the full gap list."""
    na=[c for c in A if s<=c<=e]
    gaps=[na[i+1]-na[i] for i in range(len(na)-1)]
    # prepend gap from s to first anchor, append last anchor to e
    lead=(na[0]-s) if na else 0
    trail=(e-na[-1]) if na else 0
    return [lead]+gaps+[trail]

print("===== descent glue a->4: peak (anchor-gap) staircase =====")
for a in (5,6,7):
    s,e=DESC[a]; g=peaks(s,e)
    big=[x for x in g if x>5]
    print(f"\n a={a}  len={e-s}")
    print(f"   big peaks (>5): {big}")
    # arithmetic progression check
    diffs=[big[i+1]-big[i] for i in range(len(big)-1)]
    print(f"   #peaks={len(big)}  max={max(big)}  consecutive diffs set={sorted(set(diffs))}")

print("\n===== closed-form total length vs a =====")
lens={a:DESC[a][1]-DESC[a][0] for a in DESC}
print("  lengths:", lens)
# test len(a) ~ c*4^a + ...  and ratios
import math
for a in (5,6):
    print(f"  len({a+1})/len({a}) = {lens[a+1]/lens[a]:.4f}")
# fit len = alpha*4^a + beta*2^a + gamma ; solve with 3 points a=5,6,7
import numpy as np
M=np.array([[4**a,2**a,1] for a in (5,6,7)],dtype=float)
v=np.array([lens[a] for a in (5,6,7)],dtype=float)
coef=np.linalg.solve(M,v)
print(f"  fit len(a) = {coef[0]:.6f}*4^a + {coef[1]:.6f}*2^a + {coef[2]:.6f}")
for a in (5,6,7):
    pred=coef[0]*4**a+coef[1]*2**a+coef[2]
    print(f"    a={a}: pred={pred:.2f} actual={lens[a]}")

# exact tape transform start/end
def snap(n):
    sim=build(2); sim.step()
    while sim.n<n:
        if not sim.step(): break
    leanL=sim.L[::-1]; R=sim.R[::-1]
    return sim.st, sim.pos, leanL, sim.h, R
print("\n===== exact tape transform (Lean Cfg) at descent start/end =====")
for a in (5,6):
    s,e=DESC[a]
    st0,p0,L0,h0,R0=snap(s); st1,p1,L1,h1,R1=snap(e)
    def runs(bits):
        out=[]; i=0
        while i<len(bits):
            b=bits[i]; j=i
            while j<len(bits) and bits[j]==b: j+=1
            out.append((b,j-i)); i=j
        return out
    print(f"\n a={a}: [{s},{e}] dpos={p1-p0}")
    print(f"   START st={st0} h={h0} Lruns={runs(L0)[:8]} Rruns={runs(R0)[:10]}")
    print(f"   END   st={st1} h={h1} Lruns={runs(L1)[:8]} Rruns={runs(R1)[:10]}")
    print(f"   |L|:{len(L0)}->{len(L1)}  |R|:{len(R0)}->{len(R1)}")
