import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim

def to_lean(bits):
    return "[" + ", ".join("true" if b else "false" for b in bits) + "]"

def run_lowphase(tailblock):
    # register: 0^22 (1 0^6)^3 1 0^10 then tailblock string
    reg = "0"*22 + ("1"+"0"*6)*3 + "1" + "0"*10 + tailblock
    sim = Sim(reg, state='E', pos=0)
    miles=[]
    minp=maxp=0
    sim.step()
    while len(miles)<5:
        minp=min(minp,sim.pos);maxp=max(maxp,sim.pos)
        if sim.is_milestone(): miles.append(sim.n)
        if not sim.step():
            return ('HALT',sim.n)
    n=miles[4]  # M6
    # rewind: rerun to exactly n steps
    sim2=Sim(reg,state='E',pos=0)
    for _ in range(n): sim2.step()
    return n, sim2.st, sim2.pos, list(sim2.L), sim2.h, list(sim2.R), (minp,maxp)

for tb in ["1"*4+"0"*2, "1"*20+"0"*2]:
    r=run_lowphase(tb)
    print(f"tail={tb!r}: M6 n={r[0]} st={r[1]} pos={r[2]} window={r[7-0] if False else r[-1]}")
    print(f"   L={r[3]}")
    print(f"   h={r[4]} R={r[5]}")

# Emit Lean tapes for the 1^4 0^2 truncation
n,st,pos,L,h,R,win = run_lowphase("1"*4+"0"*2)
print("\n=== g=4 even anchor, tail 1^4 0^2 ===")
print("steps:",n,"end st",st,"pos",pos,"window",win)
print("L_lean =", to_lean(L))
print("h =", "true" if h else "false")
print("R_lean =", to_lean(R[::-1]))  # R is stored reversed; right list nearest-first = R (as pop order). In Lean right is nearest-first = sim.R reversed? 
# In Sim, self.R stores reversed so pop()=nearest. nearest-first list = self.R[::-1]? pop() takes last elt = nearest. So nearest-first = reversed(self.R)= R[::-1]. Yes.
print("R(nearest-first) =", R[::-1])
