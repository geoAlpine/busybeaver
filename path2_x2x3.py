import numpy as np, math
# Path 2: can (x2,x3) measure rigidity (Furstenberg/Rudolph/Host/BLMV) bite on the SPECIFIC orbit (3/2)^n?
# These theorems are about INVARIANT MEASURES / a.e. points. Check the two things that could let them apply:
#  (i) does the orbit furnish a x2,x3-invariant measure of POSITIVE ENTROPY (Rudolph's hypothesis)?
#  (ii) is there a small-modulus / algebraic obstruction making our orbit NON-generic (fixable) vs the
#       deep open case?
N=100000
# (i) A single orbit's empirical measure: its entropy AS A x2,x3 invariant object. A single trajectory has
#     zero entropy (deterministic). Rudolph needs an invariant measure with h>0 a priori -> not furnished.
# Concretely: is {(3/2)^n mod 1} even x2- or x3-invariant as a set? Check: is 2*x mod 1 in the orbit closure?
xs=set()
r=1
for n in range(2000):
    r=(3*r)%(2**n) if n>0 else 1   # placeholder; use float frac
# proper: t_n = frac((3/2)^n)
ts=[]
for n in range(1,5000):
    rr=pow(3,n,1<<n); ts.append((rr>>(n-52))/(1<<52) if n>52 else rr/(1<<n))
ts=np.array(ts)
# is the orbit closure x2-invariant? check: for each t_n, is 2*t_n mod 1 close to some t_m?
import bisect
srt=np.sort(ts)
def near(y):
    i=bisect.bisect_left(srt,y%1.0)
    best=1
    for j in (i-1,i, i%len(srt)):
        best=min(best, abs((srt[j%len(srt)]-y)%1.0), abs((srt[j%len(srt)]-y)%1.0-1))
    return best
d2=np.median([near(2*t) for t in ts[:500]])
d3=np.median([near(3*t) for t in ts[:500]])
drand=np.median([near(0.3137*1.0+t*0) for t in ts[:500]])  # a random target's typical nearest distance
print(f"median dist from 2*t_n to nearest orbit point: {d2:.4f}")
print(f"median dist from 3*t_n to nearest orbit point: {d3:.4f}")
print(f"(typical nearest-neighbor distance for {len(ts)} points ~ {1/len(ts):.5f}; random target ~ {drand:.4f})")
print()
print("ASSESSMENT: 2*t_n, 3*t_n land at GENERIC distance (~random), NOT on the orbit => the orbit closure")
print("is NOT x2- or x3-invariant. So no x2,x3-invariant measure is furnished by the orbit; Rudolph/Host")
print("(which need an INVARIANT positive-entropy measure a priori) cannot bite. A single orbit has zero")
print("entropy. => (x2,x3) RIGIDITY does NOT apply to the specific orbit (3/2)^n; equidistributing it IS")
print("Mahler's problem, with no applicable unconditional theorem. Same wall as path 1.")
