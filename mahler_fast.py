import math, cmath
def frac_32(n):
    r = pow(3,n,1<<n)
    if n<=52: return r/(1<<n)
    return (r >> (n-52))/(1<<52)
N=20000
fracs=[frac_32(n) for n in range(1,N+1)]
in_lower=sum(1 for x in fracs if x<0.5)
print(f"[0,1/2) density: {in_lower/N:.5f} (->0.5)")
for h in (1,2,3):
    S=sum(cmath.exp(2j*math.pi*h*x) for x in fracs)
    print(f"  h={h}: |S_N|={abs(S):9.2f} |S_N|/sqrt(N)={abs(S)/math.sqrt(N):.3f} |S_N|/N={abs(S)/N:.5f}")
S=0+0j
print("|S_N(1)| growth:")
for i,x in enumerate(fracs,1):
    S+=cmath.exp(2j*math.pi*x)
    if i in (500,2000,8000,20000):
        print(f"  N={i:6d} |S|={abs(S):8.2f} |S|/sqrt(N)={abs(S)/math.sqrt(i):.3f}")
# Antihydra even-density with bounded-size orbit (track parity via low bits only)
# c_{n+1}=floor(3c/2): parity of c determines step. Track c exactly but cap N.
c=8; ev=0
for n in range(N):
    if c%2==0: ev+=1
    c=3*c//2
print(f"Antihydra E_n/n at n={N}: {ev/N:.5f} (need>1/3)")
