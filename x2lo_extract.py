import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def snap(g,N):
    sim=build(g)
    for _ in range(N): sim.step()
    return sim.st, sim.pos, list(sim.L), sim.h, list(sim.R)

# entry at step 250: verify L identical across g, capture L_end
for g in [2,3,4,5]:
    st,pos,L,h,R = snap(g,250)
    print(f"g={g}: st={st} pos={pos} h={h} L(nearest-first)={L}")

def to_lean_list(bits):
    # bits nearest-first list of 0/1 -> Lean List Bool literal
    return "[" + ", ".join("true" if b else "false" for b in bits) + "]"

st,pos,L,h,R = snap(4,250)
print("\nL_end nearest-first length", len(L))
print("L_end Lean =", to_lean_list(L))
# sanity: the start right tape prefix pos0..35 = 0^22 1 0^6 1 0^6, then tail at pos36
# For g=4 pos36 cell:
sim=build(4)
bits=[sim.h]+sim.R[::-1]
print("start cells pos0..40:", bits[:41])
