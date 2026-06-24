import math, numpy as np
# The ONE provable ingredient: 2 and 3 are multiplicatively independent => log2(3/2) irrational
# => {n*log2(3/2)} equidistributes (Weyl) => the MANTISSA of (3/2)^n equidistributes in [1,2) (Benford).
# This PROVES the TOP bits of (3/2)^n are equidistributed. Question: how far down does 'provable' reach?
a=math.log2(3/2)
N=200000
# mantissa m_n = 2^{frac(n*a)} in [1,2); its top-K bits = top bits of (3/2)^n. PROVABLY equidistributed.
fr=[(n*a)%1.0 for n in range(1,N+1)]
mant=[2**f for f in fr]
# top-K bit of mantissa = bit just below the binary point at depth K
print("PROVABLE (Weyl/Benford): top-K bits of (3/2)^n equidistribute for any FIXED K:")
for K in (1,2,5,10):
    bits=[int(m*2**K)&1 for m in mant]
    print(f"  bit at depth K={K:2d} from the TOP: density of 1s = {sum(bits)/N:.4f} (->0.5, PROVABLE)")

# Now the KERNEL needs the bit at a MOVING position ~ c*n (the diagonal). Show it is NOT a 'top-K' bit.
# bit_n(3^n) = the n-th bit = at depth ~n from the top (since 3^n has ~1.585n bits, (3/2)^n has ~0.585n
# integer bits; the 'diagonal' parity bit sits at the BOTTOM, depth ~0.585n from top = MOVING with n).
def diag(n): 
    r=pow(3,n,1<<n); return (r>>(n-1))&1
db=[diag(n) for n in range(2,N)]
print(f"\nKERNEL target: diagonal bit at MOVING depth ~0.585n: density {sum(db)/len(db):.4f} (looks 0.5 but UNPROVABLE)")
print()
print("THE GAP, made exact:")
print("  PROVABLE: bit at any FIXED depth-from-top K  (Weyl: mantissa equidistributes)")
print("  OPEN:     bit at depth GROWING with n (~0.585n) = the diagonal = Mahler/Erdos")
print("  => multiplicative independence gives the TOP (fixed) bits FREE, but the moving diagonal bit")
print("     is exactly where it stops. Same fixed-vs-moving gap as the subspace theorem.")

# KILL-BOTH probe: is there JOINT structure? correlation between bit_n(3^n) [monster1] and trit_n(2^n) [monster2]?
def tritn(n):
    return (pow(2,n)//pow(3,n))%3 if False else ( (2**n // 3** (int(n*math.log(2)/math.log(3)) )) )  # messy
# cleaner: monster2 diagonal trit = floor((8/3)^n) mod 3
def dtrit(n):
    return (pow(8,n)//pow(3,n))%3
m1=np.array([diag(n) for n in range(2,20000)])           # base-2 diagonal of 3^n
m2=np.array([1 if dtrit(n)==2 else 0 for n in range(2,20000)])  # base-3 diagonal-2 of 8^n
print(f"\nKILL-BOTH joint probe: corr( monster1 bit , monster2 'digit=2' ) = {np.corrcoef(m1,m2)[0,1]:+.4f}")
print("  (~0 => the two monsters' diagonals are statistically independent -- no joint sum-rule to exploit)")
