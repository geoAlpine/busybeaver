import numpy as np
# Non-crude attack: ADDITIVE ENERGY / 2nd moment of c'_j mod 2^k. Collisions #{(i,j): c'_i=c'_j mod 2^k}.
# Random would be ~ J + J^2/2^k. If close, the c'_j are additively generic mod 2^k => a 2nd-moment method
# could give the one-sided count bound that Markov (1st moment) cannot.
Nsteps=6000
c=8; cps=[]
for n in range(Nsteps):
    if c%2==0: cps.append(c//2)
    c=3*c//2
J=len(cps)
print(f"J={J} induced values c'_j")
print("\nadditive energy: #{(i,j),i<j : c'_i = c'_j mod 2^k}  vs random J(J-1)/2^{k+1}:")
for k in (4,6,8,10,12):
    mod=1<<k
    res=[cp % mod for cp in cps]
    # count collisions via residue histogram
    from collections import Counter
    h=Counter(res)
    coll=sum(v*(v-1)//2 for v in h.values())
    rand=J*(J-1)//2/mod
    print(f"  k={k:2d}: collisions={coll:7d}  random={rand:9.1f}  ratio={coll/max(rand,1):.3f}  (max bin={max(h.values())}, J/2^k={J/mod:.1f})")
print("\n=> ratio ~1 => c'_j ADDITIVELY GENERIC mod 2^k (few collisions, no clustering).")
print("   This means the 2nd moment IS controlled (empirically). KEY QUESTION for the non-crude route:")
print("   can the additive energy / collision count #{2^k | c'_i - c'_j} be bounded UNCONDITIONALLY?")
print("   Collisions = pairs with v2(c'_i - c'_j) >= k. c'_j grow ~ (9/4)^j; v2 of differences of a")
print("   geometric-growth sequence -- is THERE a Baker/linear-forms bound on v2(c'_i - c'_j)? <-- the lead.")
# probe: distribution of v2(c'_i - c'_{i+1}) (consecutive differences) -- bounded? Baker-accessible?
def v2(x):
    x=abs(int(x)); r=0
    while x and x&1==0: x>>=1; r+=1
    return r
dv=[v2(cps[i+1]-cps[i]) for i in range(J-1)]
print(f"\n  v2(c'_{{i+1}} - c'_i) consecutive: mean={np.mean(dv):.3f} max={max(dv)} (bounded avg => few high-k collisions)")
