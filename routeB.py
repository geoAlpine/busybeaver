import numpy as np, math
# ROUTE B: non-halt <=> centered jump-sum Sigma_{j<=J}(D_j-1) <= J for all J. True ~sqrt(J); need <=J (margin).
N=400000
c=8; D=[]
def v2(x):
    r=0
    while x and x&1==0: x>>=1; r+=1
    return r
for n in range(N):
    if c%2==0: D.append(v2(3*(c//2)-1))
    c=3*c//2
D=np.array(D)
cum=np.cumsum(D-1)   # centered jump-sum
J=len(D)
print(f"Route B reframing: non-halt <=> centered jump-sum Sigma(D_j-1) <= J for all J")
print(f"  #cycles J={J}; max centered jump-sum = {cum.max():.0f}; the BOUND we need = J = {J}")
print(f"  ratio max(centered)/J = {cum.max()/J:.5f}  (need < 1; true ~1/sqrt(J)={1/math.sqrt(J):.4f})")
print(f"  => MASSIVE margin: centered sum is ~{cum.max():.0f}, the linear bound J is ~{J}; off by ~{J/max(cum.max(),1):.0f}x")
print()
# THE one-sided sub-target (weaker than equidistribution): Sigma_{j<=J} v2(3c'-1) <= C*J for SOME constant C.
# = positive even-density >= 1/C. C<=2 suffices. Is there an unconditional constant-C bound? 
SD=np.cumsum(D)
print(f"  Sigma D_j up to J = {SD[-1]} ; 2J = {2*J} ; ratio = {SD[-1]/(2*J):.4f}  (need <1 for even-density>1/3)")
print(f"  even-density = J/(J+Sigma D) = {J/(J+SD[-1]):.4f}")
print()
print("ROUTE B verdict [honest]: the one-sided target is 'Sigma_{j<=J} v2(3c'_j-1) <= C*J for some constant C'")
print("  = POSITIVE even-density >= 1/C (C<=2 gives >1/3). This is STRICTLY WEAKER than equidistribution")
print("  (which gives the exact C=2 with o(J) error). The margin (need <=J, true ~sqrt J) is ENORMOUS.")
print("  BUT no unconditional constant-C bound is known: trivial depth<=0.585*pos gives only n_J<=1.585^J")
print("  (exponential => only Omega(log) evens), far from n_J<=3J. The sharp open Route-B sub-problem:")
print("  prove Sigma_{j<=J} v2(3c'_j-1) = O(J) unconditionally (any constant) = positive even-density.")
