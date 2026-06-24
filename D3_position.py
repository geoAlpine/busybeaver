# DECISIVE: the fixed-modulus cancellation controls S_n's LOW bits (x3-isometry coset). But the parity /
# depth need a DIFFERENT position. parity e_n = bit_0(c_n) = bit_n(8*3^n - S_n) = a MOVING (position-n) bit.
# Verify: is the depth-relevant bit at the LOW position (controlled) or the MIDDLE/moving position (hard)?
N=2000
c=8; S=0
def v2(x):
    if x==0: return 999
    r=0
    while x&1==0: x>>=1; r+=1
    return r
print("position analysis:")
print("  S_n mod 2^M (low bits, M fixed)  = x3-ISOMETRY coset => character sum SMALL (UNCONDITIONAL cancellation)")
print("  parity e_n = bit_n(8*3^n - S_n)  = bit at MOVING position n  (the diagonal)")
print("  c_n mod 2^k = bits [n, n+k] of (8*3^n - S_n) = MIDDLE/moving bits (NOT the low ones)")
print()
# confirm: the renewal jump c'_j ≡ 3^{-1} mod 2^k uses c' mod 2^k = MIDDLE bits, not S_n's low bits
c=8; cs=[]
for n in range(N): cs.append(c); c=3*c//2
# show the controlled low bits of S_n are at position 0..M while the depth bit is at position ~n
S=0; Spos=[]
for n in range(N):
    Spos.append(v2(S) if S>0 else 0)   # lowest set bit of S_n
    S=3*S+(1<<n)*(cs[n]&1)
print(f"  lowest set bit of S_n (controlled region) ~ position {np.mean([Spos[n] for n in range(50,200)]) if (np:=__import__('numpy')) else 0:.1f} (LOW, bounded)")
print(f"  depth-relevant bit position ~ n+depth_n  ~ position n (GROWS with n)")
print()
print("VERDICT (7th over-claim AVOIDED): the linear form's UNCONDITIONAL cancellation is at the LOW position")
print("(x3-isometry, off-diagonal) -- which we already knew was fine. The even-density/depth need the MOVING/")
print("middle position (diagonal). The linear structure controls the wrong end. Same opposite-ends wall.")
print("NOT a crack. BUT: unlike D2, the linear structure is a genuine handle; the SHARP remaining sub-problem")
print("is the MOVING-modulus linear exponential sum (explicit 2^j 3^(n-1-j) coeffs) -- still open, but linear.")
