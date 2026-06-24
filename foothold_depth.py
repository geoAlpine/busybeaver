import math
# How far DOWN from the top does the provable foothold reach?
# Top-K bit of 3^n is controlled by {n*log2(3)} resolved to scale 2^-(K-1) (mantissa m=2^frac in [1,2)).
# Foothold (Weyl) controls depth K while discrepancy D_N(frac) < 2^-(K-1). Measure K_max(N) empirically.
alpha=math.log2(3.0)
import mpmath as mp
mp.mp.dps=4000
alpha_hp=mp.log(3)/mp.log(2)
def fracs(N):
    return [float(mp.frac(n*alpha_hp)) for n in range(1,N+1)]
# discrepancy proxy: max over 2^m bins of |empirical - 1/2^m|, find largest m with good uniformity
def kmax(N):
    fr=fracs(N)
    fr.sort()
    # star discrepancy approx: D = max_i |fr[i] - i/N|
    D=max(max(abs(fr[i]-i/N), abs(fr[i]-(i+1)/N)) for i in range(N))
    return D, math.log2(1.0/D) if D>0 else 99
print("N      discrepancy D_N    log2(1/D_N)=K_max(top bits controlled)   0.585*log2-ish?")
for N in (200,500,1000,2000,5000,10000,20000):
    D,K=kmax(N)
    print(f"{N:6d}   {D:.6e}      {K:6.2f}        (log2 N = {math.log2(N):.2f})")
print()
print("INTERPRETATION:")
print(" - K_max (provable top bits) grows like ~log2(N): the foothold reaches LOGARITHMIC depth.")
print(" - the DIAGONAL bit sits at depth ~0.585n from the top (a POSITIVE FRACTION of all ~1.585n bits).")
print(" - to reach depth eps*n we'd need discrepancy ~2^-(eps n) (EXPONENTIALLY small), but {n*log2 3}")
print("   has discrepancy ~ (log N)/N (POLYNOMIALLY small). HARD BARRIER: foothold = O(log n), diag = Theta(n).")
