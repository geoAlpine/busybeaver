import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
LO,HI=-10,22
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
def cons(bits,tail): return ''.join(('true' if b else 'false')+' :: ' for b in bits)+tail
def snap(n):
    s=sim_to(n); d=tape(s); h=s.pos-BASE
    left=[d.get(BASE+r,0) for r in range(h-1,LO-1,-1)]
    right=[d.get(BASE+r,0) for r in range(h+1,HI+1)]
    head='true' if d.get(BASE+h,0) else 'false'
    return s.st,h,head,left,right
for n in (6591,6626,6638,6673,6708):
    st,h,head,left,right=snap(n)
    print(f"# n={n} st={st} pos={h} head={head}")
    print(f"  L= {cons(left,'L')}")
    print(f"  R= {cons(right,'R')}")
