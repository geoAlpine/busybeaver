import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
def cell_at(sim, pos):
    # cell value at absolute position pos; head at sim.pos, R nearest-first = sim.R[::-1] for pos>sim.pos
    if pos==sim.pos: return sim.h
    if pos>sim.pos:
        idx=pos-sim.pos-1
        rn=sim.R[::-1]
        return rn[idx] if idx<len(rn) else 0
    else:
        idx=sim.pos-pos-1
        return sim.L[-1-idx] if idx<len(sim.L) else 0
def snap(g,k):
    sim=build(g)
    for _ in range(k): sim.step()
    # concrete right prefix = cells pos+1 .. 35 ; tail starts pos36
    rp=[cell_at(sim,p) for p in range(sim.pos+1,36)]
    return sim.st,sim.pos,list(sim.L),sim.h,rp
def to_lean(bits): return "["+", ".join("true" if b else "false" for b in bits)+"]"
for k in [50,100,150,200,250]:
    st,pos,L,h,rp=snap(4,k)
    print(f"k={k}: st={st} pos={pos} h={h}")
    print(f"   L={to_lean(L)}")
    print(f"   Rprefix(pos{pos+1}..35)={to_lean(rp)}  (then b::R at pos36)")
