import numpy as np
# M1 structural engine: does an incoming-bit perturbation's INFLUENCE on future parity DECAY?
# If influence(n) -> 0 geometrically, the chain "forgets" incoming flips => Phi is a contraction
# (Lipschitz with factor sum(influence) ; if the response is summable & the per-step map contracts,
#  unique fixed point follows). Measure influence via coupling: two runs identical incoming except bit 0.
k=12; K=1<<k
def step(s,h): return (3*(s+(h<<k)))//2 % K
def influence(T=40, trials=20000):
    # for each trial: random start + random incoming stream; flip h_0; track P(parity differs) at each lag
    diff=np.zeros(T)
    x=2024
    def rnd():
        nonlocal x; x=(1103515245*x+12345)&0x7fffffff; return x
    for _ in range(trials):
        s0=rnd()%K
        hs=[(rnd()>>5)&1 for _ in range(T)]
        # run A (h0 as is) and B (h0 flipped)
        sA=s0; sB=s0
        for n in range(T):
            hA=hs[n]; hB=hs[n] if n>0 else 1-hs[0]
            sA=step(sA,hA); sB=step(sB,hB)
            if (sA&1)!=(sB&1): diff[n]+=1
    return diff/trials
inf=influence()
print("influence(lag) = P(parity at lag differs | incoming bit 0 flipped):")
for n in [0,1,2,3,4,5,8,12,16,24,39]:
    print(f"  lag {n:2d}: {inf[n]:.4f}")
print(f"\nsum of influence over all lags = {inf.sum():.3f}")
print(f"ratio inf[n+1]/inf[n] (geometric decay rate): {[round(inf[n+1]/inf[n],3) for n in range(2,10)]}")
print("\n=> if influence DECAYS geometrically (summable): a single incoming flip perturbs only O(1) future")
print("   parities => Phi is Lipschitz/contracting in the incoming process => UNIQUE fixed point.")
print("   This is the structural engine for M1 (delta(P^k)=0 gives the per-step forgetting).")
