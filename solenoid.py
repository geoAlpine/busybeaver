import numpy as np
from collections import Counter
# Antihydra orbit c_{n+1}=floor(3c/2), c0=8. The solenoid automorphism alpha=x(3/2) is hyperbolic:
# expand in R(inf) and Q2, contract in Q3. GENERICITY check: are the place-projections jointly
# equidistributed & INDEPENDENT (CRT-generic)? If yes => orbit is measure-generic; obstruction is purely
# effective-vs-ae. If degenerate => solenoid adds no leverage.
N=300000
c=8
k=4
m2=[]; m3=[]
for n in range(N):
    m2.append(c % (2**k)); m3.append(c % (3**k)); c=3*c//2

# (1) marginal equidistribution
c2=Counter(m2); c3=Counter(m3)
chi2=sum((c2[r]-N/2**k)**2/(N/2**k) for r in range(2**k))/(2**k-1)
chi3=sum((c3[r]-N/3**k)**2/(N/3**k) for r in range(3**k))/(3**k-1)
print(f"marginal chi2/dof: c_n mod 2^{k} = {chi2:.3f}, c_n mod 3^{k} = {chi3:.3f} (->1 uniform)")

# (2) INDEPENDENCE across the 2-adic (expanding) and 3-adic (contracting) places: mutual information
joint=Counter(zip(m2,m3))
H2=-sum((c2[r]/N)*np.log2(c2[r]/N) for r in c2)
H3=-sum((c3[r]/N)*np.log2(c3[r]/N) for r in c3)
Hj=-sum((v/N)*np.log2(v/N) for v in joint.values())
MI=H2+H3-Hj
print(f"\nentropies: H(2-adic)={H2:.3f}, H(3-adic)={H3:.3f}, H(joint)={Hj:.3f}")
print(f"mutual information I(2-adic ; 3-adic) = {MI:.4f} bits  (0 => INDEPENDENT = CRT-generic)")
print(f"  (max possible MI = min(H2,H3) = {min(H2,H3):.3f}; ratio = {MI/min(H2,H3):.4f})")

# (3) does the EXPANDING 2-adic carry the SAME info as the real (inf) place? real frac {(3/2)^n}:
def frac32(n):
    r=pow(3,n,1<<n); return (r>>(n-52))/(1<<52) if n>52 else r/(1<<n)
# bit just below point of real frac vs low bit of c_n: are they the same data? (unstable degeneracy)
realbit=[int(frac32(n)*2)&1 for n in range(1,2000)]   # top bit of {(3/2)^n}
# correlation with c_n's structure
print("\n(unstable-degeneracy check is structural: {(3/2)^n}=(3^n mod 2^n)/2^n = the SAME bits as the")
print(" 2-adic content, so R(inf) and Q2 unstable directions carry the same data -- not independent.)")
print("\nVERDICT: if I(2-adic;3-adic)~0 AND marginals uniform => orbit is JOINTLY equidistributed &")
print("independent across the stable(3) vs unstable(2) places = measure-GENERIC. Then the ONLY gap is")
print("effective-vs-a.e. for THIS specific point = the BLMV Diophantine-genericity input.")
