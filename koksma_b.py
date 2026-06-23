import math, cmath
# Diagonal points x_n = {(3/2)^n} = (3^n mod 2^n)/2^n. 
# (A) mean-square over a multiplier t: M(N)= (1/T)Σ_t |Σ_{n<=N} e(t x_n)|^2. If ~N => sqrt-cancel in mean (provable-ish).
# (B) separation/gaps of {x_n}: well-separated => large-sieve mean-square bound applies.
N=4000
xs=[]
for n in range(1,N+1):
    r=pow(3,n,1<<n)
    xs.append((r>>(n-52))/(1<<52) if n>52 else r/(1<<n))

# (A) average |S_N(h)|^2 over integer h=1..H  (proxy for mean-square over multiplier)
H=200
tot=0.0
for h in range(1,H+1):
    S=sum(cmath.exp(2j*math.pi*h*x) for x in xs)
    tot+=abs(S)**2
print(f"mean over h<=H of |S_N(h)|^2 = {tot/H:.1f}   N={N}   ratio/N={tot/H/N:.3f}")
print("  (=> if ~N, square-root cancellation holds IN MEAN over multipliers = classical Koksma/Weyl-a.e. regime)")

# (B) point separation: sort xs, min gap. Large-sieve needs gaps >> 1/N for a clean bound.
srt=sorted(xs)
gaps=[srt[i+1]-srt[i] for i in range(len(srt)-1)]
mingap=min(gaps)
print(f"\n{N} points in [0,1): min gap={mingap:.2e}  (uniform spacing would be {1/N:.2e})")
print(f"  min gap / (1/N^2) = {mingap*N*N:.3f}   (large-sieve clean if min gap >> 1/N)")

# (C) the SPECIFIC point t=1 vs the average: is t=1 an outlier? compare |S_N(1)| to typical |S_N(h)|
import statistics
mags=[abs(sum(cmath.exp(2j*math.pi*h*x) for x in xs)) for h in range(1,51)]
print(f"\n|S_N(1)|={mags[0]:.1f}  median over h<=50={statistics.median(mags):.1f}  max={max(mags):.1f}")
print("  (t=1 is NOT an outlier => no numerical sign the specific point misbehaves; but averaged proof can't isolate it)")
