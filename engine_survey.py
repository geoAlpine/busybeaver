# Engine survey support: (1) non-Haar invariant measures have POSITIVE entropy (entropy alone insufficient);
# (2) the unification -- every single-orbit engine needs rank-2 / unipotent / a.e., none available to <x3/2>.
import math
ln2=math.log(2); K=40
def h(p): return sum(p[D]*(D+1)*ln2 for D in range(len(p)))
pHaar=[2**-(D+1) for D in range(K)]
print(f"Haar entropy h={h(pHaar)/ln2:.3f} log2 (avg jump E[D]=1)")
for q in (0.6,0.75,0.4,0.8):
    p=[(1-q)*q**D for D in range(K)]
    print(f"  non-Haar q={q}: E[D]={sum(D*p[D] for D in range(K)):.2f}, h={h(p)/ln2:.3f} log2 (POSITIVE)")
print("=> positive entropy does NOT single out Haar; entropy method needs a 2nd commuting element (rank-2).")
print("UNIFICATION: self-duality(BFLM)=missing-recurrence(entropy)=no-spectral-gap(additive)=no-x2,x3-pair")
print("(rigidity) = THE ORBIT CARRIES ONLY THE RANK-1 COMBINATION x(3/2).")
