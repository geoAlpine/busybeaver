import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
def trace(g,N):
    sim=build(g); out=[]
    for _ in range(N):
        out.append((sim.n,sim.st,sim.pos,sim.h)); 
        if not sim.step(): break
    out.append((sim.n,sim.st,sim.pos,sim.h)); return out
Tg={g:trace(g,500) for g in [2,3,4,5]}
ml=min(len(Tg[g]) for g in Tg)
div=None
for i in range(ml):
    vals=set((Tg[g][i][1],Tg[g][i][2],Tg[g][i][3]) for g in Tg)
    if len(vals)!=1: div=i;break
print("first (st,pos,head) divergence idx:",div)
for g in Tg: print(f"  g={g} @div: n={Tg[g][div][0]} st={Tg[g][div][1]} pos={Tg[g][div][2]} h={Tg[g][div][3]}")
print("prev:")
for g in Tg: print(f"  g={g}: n={Tg[g][div-1][0]} st={Tg[g][div-1][1]} pos={Tg[g][div-1][2]} h={Tg[g][div-1][3]}")
# max pos reached before divergence
for g in Tg: print(f"  g={g}: maxpos before div={max(p for (_,_,p,_) in Tg[g][:div])}")
