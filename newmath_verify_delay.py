# Verify the CA reduction's prediction on the REAL orbit: parity(c_n) == bit_k(c_{n-k})?
# If TRUE: the affine code is a pure delay => circular => CA randomization does NOT apply (wall).
N=100000
c=8; orbit=[]
for n in range(N): orbit.append(c); c=3*c//2
def bit(x,k): return (x>>k)&1
for k in (3,4,5,8):
    matches=sum(1 for n in range(k,N) if (orbit[n]&1)==bit(orbit[n-k],k))
    print(f"k={k}: parity(c_n) == bit_k(c_(n-k)) holds for {matches}/{N-k} = {matches/(N-k):.4f}")
print("\n=> if ~1.0: pure-delay confirmed, the CA is the trivial shift => randomization theorems DON'T apply")
print("   (shift = isometry, no mixing). The affine/permutive structure is real but TRIVIAL => reduces to")
print("   the wall (even-density of a fixed bit position = the open kernel). 5th over-claim caught.")
print("   if NOT ~1.0: the model G was not faithful at the parity level -- reconsider.")
