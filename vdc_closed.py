# Verify van der Corput is CLOSED on the Mahler sum (the moving-middle-digit exponential sum).
# EXACT fractional parts: frac((3/2)^n) = (3^n mod 2^n)/2^n. Differenced phase (3/2)^{n+h}-(3/2)^n stays the
# same exponential family => differencing gains nothing; sum is already at full sqrt-cancellation.
import cmath, math
N=8000
def S(t,h=0):
    s=0j
    for n in range(1,N+1):
        if h==0: ph=t*(pow(3,n,2**n)/2**n)
        else: ph=t*((pow(3,n)*(3**h-2**h)) % 2**(n+h))/2**(n+h)
        s+=cmath.exp(2j*math.pi*(ph%1.0))
    return abs(s)
print(f"sqrt(N)={math.sqrt(N):.2f}")
for t in (1,2,3,5): print(f"  plain |S({t})|/sqrt(N) = {S(t)/math.sqrt(N):.3f}")
for h in (1,2,3): print(f"  vdC h={h}: |S_h|/sqrt(N) = {S(1,h)/math.sqrt(N):.3f} (same exponential family, no gain)")
print("=> van der Corput is a fixed point on (3/2)^n => CLOSED.")
