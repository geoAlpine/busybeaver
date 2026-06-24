import numpy as np
# Phase-2 seed: Tao (2019) "Almost all orbits of the Collatz map attain almost bounded values".
# Method: the Syracuse random variable -- the 3-adic/2-adic valuation sequence along the orbit -- is shown
# to equidistribute (in a transport/entropy sense) for almost all starting points. Engage it honestly.
# (1) Our analogue of the Syracuse object: the sequence of jump heights D_j = v2(3c'-1) (the renewal jumps).
#     Tao's key: these "look like" iid geometric and their SUM concentrates. We already verified iid-geometric.
# (2) THE QUESTION: does Tao's METHOD give anything for our SINGLE specific orbit (seed 8)?
N=200000
c=8; jumps=[]; cp=None
prev_even=None
# extract renewal jump heights along the single orbit
def v2(x):
    r=0
    while x and x&1==0: x>>=1; r+=1
    return r
c=8
for n in range(N):
    if c%2==0:
        cprime=c//2
        jumps.append(v2(3*cprime-1))
    c=3*c//2
jumps=np.array(jumps)
print("(1) Our Syracuse-type object (renewal jump heights D_j) along the SINGLE orbit:")
print(f"    mean={jumps.mean():.4f} (Tao-style transport predicts ->1); empirical geometric P(D>=k):",
      [round(np.mean(jumps>=k),3) for k in range(1,6)])
print(f"    centered partial sum max |Σ(D_j-1)| = {np.max(np.abs(np.cumsum(jumps-1))):.0f} ~ sqrt(#)={np.sqrt(len(jumps)):.0f}")
print()
print("(2) HONEST ASSESSMENT of Tao's method for our problem:")
print("  - Tao's theorem is for ALMOST ALL starting n (logarithmic density 1) -- it explicitly does NOT")
print("    decide any SINGLE orbit. The Antihydra question is ONE specific orbit (seed 8).")
print("  - Tao's transport/entropy machinery shows the Syracuse distribution -> uniform AVERAGED over")
print("    starting points; for a fixed orbit it gives nothing (same specific-vs-generic wall).")
print("  - SO: Tao's method = the CLOSEST existing technique to (beta) (built for 3x+1 carry dynamics,")
print("    proves digit-distribution equidistribution) BUT inherits the almost-all/specific gap.")
print("  => Adds to the obstruction map: 'Tao transport (2019): almost-all, not a single orbit.'")
print("     The new tool (beta) must do for ONE orbit what Tao does for almost all -- a genuinely harder,")
print("     un-built step. (Single-orbit Collatz-type bounds are open even post-Tao.)")
