import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
def cell_at(sim,pos):
    if pos==sim.pos: return sim.h
    if pos>sim.pos:
        idx=pos-sim.pos-1; rn=sim.R[::-1]; return rn[idx] if idx<len(rn) else 0
    idx=sim.pos-pos-1; return sim.L[-1-idx] if idx<len(sim.L) else 0
def lean_list(bits): return "["+", ".join("true" if b else "false" for b in bits)+"]"
def cfg_term(sim, tail_symbolic=True):
    st=sim.st; pos=sim.pos; L=list(sim.L); h=sim.h
    # right prefix = pos+1..35 concrete, then (b::R) if head<36 else head is b
    if pos<36:
        rp=[cell_at(sim,p) for p in range(pos+1,36)]
        right=f"({lean_list(rp)} ++ (b :: R))" if rp else "(b :: R)"
        head = "false" if h==0 else "true"
    else: # pos==36, head=b, right=R
        right="R"; head="b"
    return f"⟨.{st}, {pos}, ⟨{lean_list(L)}, {head}, {right}⟩⟩"
def snap(g,k):
    sim=build(g)
    for _ in range(k): sim.step()
    return sim
# start config (step0) in nested form to match the theorem statement
sim0=build(4)
print("START =", cfg_term(sim0))
for k in [50,100,150,200,250]:
    print(f"C{k} =", cfg_term(snap(4,k)))
