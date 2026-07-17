#!/usr/bin/env python3
"""x2lt_factor.py -- THE DECISIVE TEST.  Replay regen6_transport's OWN Lean IN config
(pos 11, forall L R) for 154 steps and compare the resulting config, cell for cell,
against regen4_transport's Lean IN config (pos 9).  Then continue 70 + 498 and compare
against regen6_transport's Lean OUT.

Free tails L,R are given DISTINCT SENTINEL values so we can see exactly how they thread."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim

def mk(st,pos,L,h,R):
    s=Sim('0'); s.st=st; s.pos=pos; s.h=h
    s.L=list(L)[::-1]; s.R=list(R)[::-1]; s.n=0
    return s
def snapL(s): return (s.st,s.pos,s.L[::-1],s.h,s.R[::-1])
def bs(x): return ''.join(map(str,x))

# ---------- regen6_transport IN (lean/X2.lean:6478), L:=[], R:=[] ----------
R6_IN_L = [1]*61 + [0,1,0,0,1]
R6_IN_R = ([0]+[1]*13+[0,0]+[1]*5+[0,0,1]+[0]*34)
R6_OUT_L = [0,1]
s = mk('E', 11, R6_IN_L, 0, R6_IN_R)
print("regen6 IN: pos=11 |L|=%d |R|=%d" % (len(R6_IN_L), len(R6_IN_R)))

for _ in range(154): s.step()
st,pos,L,h,R = snapL(s)
print("\n=== after 154 steps from regen6 IN ===")
print(f"  st={st} pos={pos} head={h}")
print(f"  L[0:26] = {bs(L[:26])}")
print(f"  R       = {bs(R)}   (|R|={len(R)})")

# ---------- regen4_transport IN (lean/X2.lean:4206) ----------
R4_IN_L = [1]*12+[1,0,1,0,0,1,0]
R4_IN_R = [0,1,0]+[0]*10
print("\n=== regen4_transport IN (Lean, pos 9) ===")
print(f"  st=E pos=9 head=0")
print(f"  L[0:19] = {bs(R4_IN_L)}  ++ L(free)")
print(f"  R[0:13] = {bs(R4_IN_R)}  ++ R(free)")

print("\n--- COMPARISON ---")
print("  state  :", st, "vs E        ->", st=='E')
print("  head   :", h, "vs 0        ->", h==0)
print("  pos    :", pos, "vs 9        ->", pos==9, "   (delta =", pos-9, ")")
print("  L[0:19]:", bs(L[:19]))
print("         :", bs(R4_IN_L), "-> MATCH" if L[:19]==R4_IN_L else "-> DIFFER")
print("  L free tail (L[19:]) =", bs(L[19:]))
print("  R      :", bs(R), " vs Lean-required prefix", bs(R4_IN_R))
if len(R) < 13:
    print("         -> orbit R is SHORTER (%d cells); Lean needs 13 explicit cells ++ R" % len(R))
    print("         -> matches only after PADDING with %d trailing blanks" % (13-len(R)))
    print("         -> as List Bool these are DIFFERENT VALUES:", R, "!=", R4_IN_R)

# ---------- continue 70 (the REGEN(4) segment) ----------
for _ in range(70): s.step()
st2,pos2,L2,h2,R2 = snapL(s)
print("\n=== after 154+70 = 224 steps ===")
print(f"  st={st2} pos={pos2} head={h2}  (regen4 OUT pos would be -7; delta = {pos2-(-7)})")
print(f"  L[0:8] = {bs(L2[:8])}")
print(f"  R[0:29]= {bs(R2[:29])}")

# ---------- continue 498 to the end ----------
for _ in range(498): s.step()
st3,pos3,L3,h3,R3 = snapL(s)
print("\n=== after 154+70+498 = 722 steps (should be regen6 OUT) ===")
print(f"  st={st3} pos={pos3} head={h3}   expected st=E pos=-53 head=0")
print(f"  L[0:2] = {bs(L3[:2])} expected {bs(R6_OUT_L)}")
print("  *** regen6 OUT reproduced:", (st3=='E' and pos3==-53 and h3==0 and L3[:2]==R6_OUT_L), "***")
print("\n  SPLIT CHECK: 154 + 70 + 498 =", 154+70+498)
