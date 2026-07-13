#!/usr/bin/env python3
"""x2lm_lean.py -- derive the EXACT minimal tile transport from the real orbit."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

TT = {
    ('A', 0): (1, +1, 'B'), ('A', 1): (0, +1, 'E'),
    ('B', 0): (1, +1, 'C'), ('B', 1): None,
    ('C', 0): (0, -1, 'D'), ('C', 1): (1, -1, 'E'),
    ('D', 0): (0, +1, 'E'), ('D', 1): (1, -1, 'D'),
    ('E', 0): (1, +1, 'F'), ('E', 1): (0, -1, 'C'),
    ('F', 0): (0, +1, 'A'), ('F', 1): (1, +1, 'E'),
}

class Z:
    def __init__(self, L, h, R, st='E', pos=0):
        self.L=list(L); self.h=h; self.R=list(R); self.st=st; self.pos=pos
    def step(self):
        t=TT[(self.st,self.h)]
        if t is None: return False
        w,mv,ns=t; self.h=w
        if mv==+1:
            self.L.append(self.h); self.h=self.R.pop() if self.R else 0
        else:
            self.R.append(self.h); self.h=self.L.pop() if self.L else 0
        self.st=ns; self.pos+=mv; return True
    def run(self,n):
        for _ in range(n):
            if not self.step(): return False
        return True

def to_M3(g):
    s=build(g); s.step(); mc=0
    while True:
        if s.is_milestone():
            mc+=1
            if mc==2: return s
        if not s.step(): return s

# g=4: capture full configs at tile boundaries n=215 and n=244, and the max reach in between
s=to_M3(g:=4)
snap={}
reach_hi=-10**9
while s.n<=273:
    if 215<=s.n<=244:
        reach_hi=max(reach_hi,s.pos)
    if s.n in (215,244,273):
        snap[s.n]=(s.st,s.pos,s.h,list(s.L),list(s.R))
    if not s.step(): break
print(f"max head pos during tile 215->244 = {reach_hi}")

st0,p0,h0,L0,R0=snap[215]
st1,p1,h1,L1,R1=snap[244]
print(f"start n=215: st={st0} pos={p0} h={h0} |L|={len(L0)} |R|={len(R0)}")
print(f"end   n=244: st={st1} pos={p1} h={h1} |L|={len(L1)} |R|={len(R1)}")

# L grows on top (nearest = end of list). check L1 == deposit ++ ... no: L stored nearest at END.
# deposit is the NEW nearest cells = L1[len(L0):]
assert L1[:len(L0)]==L0, "L bottom (far frame) preserved?"
deposit = L1[len(L0):]
print(f"L far-frame preserved: {L1[:len(L0)]==L0};  deposit (pushed, oldest->newest) = {deposit}")

# R context must cover pos p+1 .. reach_hi (cells actually read).
nctx = reach_hi - p0            # number of near cells right of head that are touched
Rc0 = R0[len(R0)-nctx:]         # near part at start (far->near; nearest last)
# end: same physical frame boundary. |R1| smaller by 7; end near part = R1 minus same far frame.
far_frame = R0[:len(R0)-nctx]
assert R1[:len(far_frame)]==far_frame, "far frame preserved beyond reach"
Rc1 = R1[len(far_frame):]
print(f"R start near part (far->near): {Rc0}")
print(f"R end   near part (far->near): {Rc1}")

# Build the minimal tile lemma with arbitrary frames.
# nearest-first for Lean: head cell, then R near reversed.
# In Lean Tape.right is nearest-first. Sim.R is reversed(nearest-first) i.e. nearest last.
# So Lean-right near context = reversed(Rc0). Lean-left deposit nearest-first = reversed(deposit).
Rctx_lean = list(reversed(Rc0))
Rout_lean = list(reversed(Rc1))
Ldep_lean = list(reversed(deposit))
print(f"\nLEAN tile lemma (arbitrary L,R frames):")
print(f"  steps 29  <E, p, <L, {h0}, {Rctx_lean} ++ R>>")
print(f"    = <E, p+{p1-p0}, <{Ldep_lean} ++ L, {h1}, {Rout_lean} ++ R>>")

# VERIFY with arbitrary frames in the Lean zipper
def check(Lf,Rf):
    # Sim.R nearest-last: far frame Rf first, then near ctx Rc0. Sim.L nearest-last: Lf then deposits.
    z=Z(list(Lf), h0, list(Rf)+Rc0, st='E', pos=0)
    ok=z.run(29)
    expL=list(Lf)+deposit        # deposits appended after Lf
    expR=list(Rf)+Rc1
    return ok and z.st=='E' and z.h==h1 and z.pos==p1-p0 and z.L==expL and z.R==expR, z
allok=True
for Lf,Rf in [([],[]),([1,1,0,1],[0,1,1,0,0,1]),([0],[1]*15),([1,0,1,0,1,0],[0,0,1])]:
    m,z=check(Lf,Rf); allok&=m
    print(f"  frame L={Lf} R={Rf[:5]}: {'OK' if m else 'FAIL '+str((z.st,z.pos,z.h,z.L,z.R))}")
print("TILE (arbitrary frames):","VERIFIED" if allok else "FAILED")

# ---- forward RUN chaining on the REAL orbit ----
print("\n--- forward run chaining (real orbit) ---")
def to_M3b(g):
    s=build(g); s.step(); mc=0
    while True:
        if s.is_milestone():
            mc+=1
            if mc==2: return s
        if not s.step(): return s
for g in (2,4,6):
    s=to_M3b(g)
    while not (s.st=='E' and s.h==0 and s.pos==23):
        if not s.step(): break
    tiles=0
    while True:
        st,p,h=s.st,s.pos,s.h; L=list(s.L); R=list(s.R); n=s.n
        moved=all(s.step() for _ in range(29))
        if moved and s.st=='E' and s.h==0 and s.pos==p+7:
            tiles+=1
        else:
            s.st,s.pos,s.h,s.L,s.R,s.n=st,p,h,L,R,n
            break
    print(f"  g={g}: consecutive +7 forward tiles from pos23 = {tiles}   (u=g-1={g-1})")
