import numpy as np, itertools
# M1: characterize ALL order-2-Markov self-consistent fixed points of the renewal operator Phi.
# Phi: incoming parity-process (order-2 Markov) -> drive renewal chain -> output parity-process; fit order-2.
# Self-consistent fixed point: input law == output law. Find ALL; check even-density. (D2 / Milestone M1.)
k=10; K=1<<k
def step(s,h): return (3*(s+(h<<k)))//2 % K
def Phi2(params, T=200000):
    # order-2 incoming process: P(h=1 | last two incoming bits b1b0). params = 4 probs p[b1b0].
    p=params
    s=1; l1=1; l0=1; outs=[]
    x=12347+int(sum(params)*1e5)
    def rnd():
        nonlocal x; x=(1103515245*x+12345)&0x7fffffff; return x/0x7fffffff
    for n in range(T):
        ctx=(l1<<1)|l0
        h=1 if rnd()<p[ctx] else 0
        if n>1000: outs.append(s&1)
        s=step(s,h); l1,l0=l0,h
    o=np.array(outs)
    # fit order-2 Markov to the OUTPUT process: P(out=1 | prev two outs)
    fit=[0.0]*4; cnt=[0]*4
    for n in range(2,len(o)):
        c=(o[n-2]<<1)|o[n-1]; cnt[c]+=1; fit[c]+=o[n]
    fit=[fit[c]/cnt[c] if cnt[c]>0 else 0.5 for c in range(4)]
    even_density=1-o.mean()
    return np.array(fit), even_density
# iterate from a grid of starts; collect fixed points
fps=[]; eds=[]
grid=[0.1,0.3,0.5,0.7,0.9]
import random
starts=[np.array([a,b,c,d]) for a in (0.2,0.5,0.8) for b in (0.5,) for c in (0.5,) for d in (0.2,0.5,0.8)]
# add adversarial-ish skewed starts
starts+=[np.array([0.9,0.9,0.1,0.1]),np.array([0.1,0.5,0.5,0.9]),np.array([0.05,0.05,0.05,0.05]),np.array([0.95,0.95,0.95,0.95])]
print("M1 — order-2 self-consistent fixed points (iterate Phi to convergence):")
seen=[]
for st in starts:
    p=st.copy()
    for _ in range(15): p,ed=Phi2(p)
    # report
    near=any(np.linalg.norm(p-q)<0.03 for q in seen)
    if not near: seen.append(p)
    print(f"  start {np.round(st,2)} -> fixed pt {np.round(p,4)}  even-density={ed:.4f}  {'<=1/3 !!' if ed<=1/3 else 'OK >1/3'}")
print(f"\ndistinct fixed points found: {len(seen)}")
for q in seen: print(f"   {np.round(q,4)} (Bernoulli-1/2 = [0.5,0.5,0.5,0.5])")
print("=> if the ONLY fixed point is Bernoulli(1/2) (even-density 1/2): M1 holds for order-2 =>")
print("   no order-<=2 self-consistent parity process halts. A rigorous partial toward (H).")
