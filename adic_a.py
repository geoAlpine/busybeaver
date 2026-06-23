# The bits of 3^n live in Z_2 under x->3x, which is an ISOMETRY (|3|_2=1): zero entropy, NO spectral gap.
# Verify: each FIXED 2-adic digit bit_k(3^n) is PERIODIC in n (period = ord(3 mod 2^{k+1}) = 2^{k-1}).
# The hard object bit_n(3^n) reads this zero-entropy isometry at a MOVING (diagonal) position.
def bitk(n,k): return (pow(3,n,1<<(k+1))>>k)&1
print("fixed 2-adic digit bit_k(3^n) is periodic in n (isometry => zero entropy):")
for k in (1,2,3,5,8):
    seq=[bitk(n,k) for n in range(1,200)]
    # find period
    per=None
    for p in range(1,100):
        if all(seq[i]==seq[i+p] for i in range(100)):
            per=p; break
    print(f"  k={k}: period in n = {per}  (predicted 2^(k-1)={2**(k-1)})")
print("\n=> the place carrying the BITS (2-adic, x3) is an ISOMETRY: no mixing, no spectral gap.")
print("   the place with a spectral gap (real beta=3/2 map, gap 0.27) does NOT carry the bits.")
print("   bit_n(3^n) = DIAGONAL read of the zero-entropy isometry at the moving position n.")

# Confirm the two-place split = the product formula hyperbolicity is SPLIT across factors:
import math
print(f"\nproduct formula for x(3/2): |3/2|_inf={3/2}, |3/2|_2={2}, |3/2|_3={1/3:.4f}; product={1.5*2/3:.1f}")
print("  real place expands (3/2), 2-adic expands (2) BUT as an isometry on the digit-shift it gives")
print("  zero-entropy rotation dynamics for fixed digits; only the MOVING diagonal digit is complex.")
