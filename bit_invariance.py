import numpy as np
# The self-consistency proof needs: law(incoming bit = bit_k(c_n)) == law(parity = bit_0(c_n)).
# I.e. all FIXED bit positions of the orbit share the same density & correlation (shift-invariance).
# Measure bit_k density & lag-1 autocorr for k=0..15 on the real orbit. If identical => self-consistency holds.
N=600000
c=8; bits=[[] for _ in range(16)]
for n in range(N):
    for k in range(16): bits[k].append((c>>k)&1)
    c=3*c//2
print(" k   density(bit_k)   lag1-autocorr")
dens=[]; 
for k in range(16):
    b=np.array(bits[k][2000:],dtype=float)
    d=b.mean(); m=d
    ac=np.mean((b[:-1]-m)*(b[1:]-m))/(b.var()+1e-12)
    dens.append(d)
    print(f" {k:2d}    {d:.4f}          {ac:+.4f}")
dens=np.array(dens)
print(f"\nbit-density spread across positions k=0..15: min={dens.min():.4f} max={dens.max():.4f} (range {dens.max()-dens.min():.4f})")
print("=> if all ~0.5 with tiny spread => shift-invariance holds empirically => incoming law = parity law")
print("   => the real parity process IS a self-consistent fixed point of Phi => (with proven contraction)")
print("   even-density forced to 1/2 > 1/3 => NON-HALT.  Remaining gap: PROVE shift-invariance unconditionally.")
