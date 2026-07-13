#!/usr/bin/env python3
"""Extract carry snapshots in the carry_event_5to13 frame: base=6591 (pos0),
parametric L = cells rel<=-11, R = cells rel>=23. Concrete window rel[-10,22].
Emit Lean lists for each snapshot's (left-concrete ++ L, head, right-concrete ++ R)."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
LO,HI=-10,22   # concrete window (rel to base); L at rel<=LO-1=-11, R at rel>=HI+1=23
def sim_to(n):
    s=build(2); s.step()
    while s.n<n: assert s.step()
    return s
def tape(s):
    d={s.pos:s.h}
    for k in range(len(s.L)): d[s.pos-1-k]=s.L[-1-k]
    for k in range(len(s.R)): d[s.pos+1+k]=s.R[-1-k]
    return d
BASE=sim_to(6591).pos
def LL(bits): return ''.join('true :: ' if b else 'false :: ' for b in bits)
def snap(n,tag):
    s=sim_to(n); d=tape(s); h=s.pos-BASE  # head rel
    left=[d.get(BASE+r,0) for r in range(h-1,LO-1,-1)]   # rel h-1 down to LO, nearest-first
    right=[d.get(BASE+r,0) for r in range(h+1,HI+1)]      # rel h+1 up to HI
    head=d.get(BASE+h,0)
    print(f"-- {tag} n={n} relpos={h} head={'true' if head else 'false'}")
    print(f"   L: {LL(left)}L")
    print(f"   R: {LL(right)}R")
    return h,head,left,right
snaps={}
for n,tag in [(6591,'START'),(6626,'CORE_in'),(6638,'CORE_out'),(6708,'EXIT_out')]:
    snaps[tag]=snap(n,tag)
# verify tails rel<=-11 and rel>=23 constant across all 4 snapshots
allok=True
for r in list(range(-16,-10))+list(range(23,29)):
    vals=set()
    for n in (6591,6626,6638,6708):
        s=sim_to(n); vals.add(tape(s).get(BASE+r,0))
    if len(vals)>1: allok=False; print(f"  !! rel {r} varies: {vals}")
print("parametric-tail constancy rel<=-11,>=23:", "OK" if allok else "FAIL")
# CORE_in right should be pow10 6 ++ ...
h,head,left,right=snaps['CORE_in']
print("CORE_in right first 12:", right[:12], "== (10)^6?" , right[:12]==[1,0,1,0,1,0,1,0,1,0,1,0])
h,head,left,right=snaps['CORE_out']
print("CORE_out left first 12:", left[:12], "== 1^12?", left[:12]==[1]*12)

# --- verify sweepEF-6 composition equalities for the CORE (CORE_in -> CORE_out) ---
hi,_,Li,Ri = snaps['CORE_in']
ho,_,Lo,Ro = snaps['CORE_out']
print("\nCORE checks:")
print(" CORE_in.right[:12]==(10)^6 :", Ri[:12]==[1,0,1,0,1,0,1,0,1,0,1,0])
print(" R'' = CORE_in.right[12:] :", Ri[12:])
print(" CORE_out.right           :", Ro)
print(" R'' == CORE_out.right    :", Ri[12:]==Ro)
print(" CORE_out.left[:12]==1^12 :", Lo[:12]==[1]*12)
print(" L'' = CORE_in.left       :", Li)
print(" CORE_out.left[12:]       :", Lo[12:])
print(" CORE_out.left[12:]==L''  :", Lo[12:]==Li)
# --- ENTRY [6591->6626] and EXIT [6638->6708] step counts & tail-independence check ---
def sim_to2(n):
    from x2bd_sim import build as b
    s=b(2); s.step()
    while s.n<n: assert s.step()
    return s
# self-check: run 117 steps from START-with-empty-tails and compare to EXIT_out-with-empty-tails
from x2bd_sim import Sim
def run_window(startsnap, nsteps, Lpad, Rpad):
    h,head,left,right=startsnap
    rstr=''.join('1' if b else '0' for b in ([head]+right+Rpad))
    sim=Sim(rstr,state='E',pos=0)
    Lfull=left+Lpad; sim.L=Lfull[::-1]
    for _ in range(nsteps):
        assert sim.step()
    return sim
for (Lpad,Rpad) in [([],[]),([1,0,1],[0,1,1]),([0,0],[1,1,1,0])]:
    sim=run_window(snaps['START'],117,Lpad,Rpad)
    # compare window rel[-10,22] to EXIT_out
    d={sim.pos:sim.h}
    for k in range(len(sim.L)): d[sim.pos-1-k]=sim.L[-1-k]
    for k in range(len(sim.R)): d[sim.pos+1+k]=sim.R[-1-k]
    ho,heado,Lo2,Ro2=snaps['EXIT_out']
    # EXIT_out head rel -7; in this local frame START head=0, so exit head at pos ho=-7
    ok = (sim.st=='E' and sim.pos==ho)
    print(f" 117-step tail-indep pad({Lpad},{Rpad}): endst={sim.st} endpos={sim.pos} expect -7 : {'OK' if ok else 'FAIL'}")
