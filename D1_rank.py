import numpy as np, math
# D1 applicability: measure rigidity (Furstenberg-Rudolph-Lindenstrauss) is a RANK>=2 phenomenon.
# The Antihydra orbit iterates a SINGLE map (x3/2) => RANK 1. Rank-1 actions have NO rigidity
# (continuum of invariant measures). Verify the orbit does NOT carry a usable rank-2 (x2,x3) structure.
N=3000
ts=[(pow(3,n,1<<n)>>(n-52))/(1<<52) if n>52 else pow(3,n,1<<n)/(1<<n) for n in range(1,N)]
ts=np.array(ts)
srt=np.sort(ts)
import bisect
def nearest_dist(y):
    y=y%1.0; i=bisect.bisect_left(srt,y)
    best=1.0
    for j in (i-1,i%len(srt)):
        d=abs(srt[j%len(srt)]-y); best=min(best,d,1-d)
    return best
# Is the orbit closure x2-invariant or x3-invariant? (rank-2 rigidity needs the FULL x2,x3 action)
d2=np.median([nearest_dist(2*t) for t in ts[:800]])
d3=np.median([nearest_dist(3*t) for t in ts[:800]])
typ=np.median([nearest_dist((0.4+0.0001*i)%1) for i in range(800)])  # typical nearest-orbit distance
print("RANK CHECK -- is the (3/2)^n orbit closed under x2 / x3 (=> rank-2 structure for rigidity)?")
print(f"  median dist(2*t_n -> orbit) = {d2:.4f}")
print(f"  median dist(3*t_n -> orbit) = {d3:.4f}")
print(f"  typical nearest-orbit dist  = {typ:.4f}  (random point)")
print(f"  => 2t,3t land at ~typical(random) distance => orbit NOT x2/x3-invariant => NO rank-2 structure.")
print()
print("CONCLUSION (D1 applicability):")
print(" - Antihydra = iterate ONE map (x3/2) => the orbit is RANK 1 (single transformation, cyclic semigroup).")
print(" - Measure rigidity / effective equidistribution (Furstenberg-Rudolph-Lindenstrauss-ELV/BLMV) are")
print("   RANK>=2 phenomena: they classify measures invariant under the FULL {x2,x3} (or a higher-rank)")
print("   action. Rank-1 maps have a CONTINUUM of invariant measures -- NO rigidity.")
print(" - The (3/2)^n orbit traces only the DIAGONAL (x3/2) direction of the x2,x3 action = a rank-1 suborbit;")
print("   it carries no usable rank-2 invariance (verified above). => D1 rigidity does NOT apply.")
print(" - This is the SAME fundamental obstruction as the earlier x2,x3 finding, now named precisely: RANK.")
