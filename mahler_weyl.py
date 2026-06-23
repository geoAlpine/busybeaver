import math, cmath
# {(3/2)^n} = (3^n mod 2^n)/2^n, computed EXACTLY with big ints, then top bits for float frac.
def frac_32(n):
    r = pow(3,n,1<<n)            # 3^n mod 2^n, exact
    if n<=52: return r/(1<<n)
    return (r >> (n-52))/(1<<52)  # top 52 bits of the fractional part

N=200000
fracs=[frac_32(n) for n in range(1,N+1)]

# 1) Discrepancy proxy: count fraction in [0,1/2) (should -> 1/2). Also even-density of orbit.
in_lower=sum(1 for x in fracs if x<0.5)
print(f"#{{(3/2)^n}} in [0,1/2), n<= {N}: {in_lower}/{N} = {in_lower/N:.5f}  (equidist -> 0.5)")

# 2) Weyl sums S_N(h)=sum e(h (3/2)^n) for h=1,2,3; check |S_N|/sqrt(N) (sqrt-cancellation if ~O(1))
for h in (1,2,3):
    S=sum(cmath.exp(2j*math.pi*h*x) for x in fracs)
    print(f"  h={h}: |S_N|={abs(S):10.2f}  |S_N|/sqrt(N)={abs(S)/math.sqrt(N):.3f}  |S_N|/N={abs(S)/N:.5f}")

# 3) growth of |S_N(1)| with N (is it o(N)? sqrt-like?)
print("\n|S_N(1)| vs N (sqrt-cancellation test):")
S=0+0j
checkpoints={1000,5000,20000,80000,200000}
for i,x in enumerate(fracs,1):
    S+=cmath.exp(2j*math.pi*x)
    if i in checkpoints:
        print(f"  N={i:7d} |S|={abs(S):9.2f} |S|/sqrt(N)={abs(S)/math.sqrt(i):.3f}")

# 4) ANTIHYDRA-relevant: even-density of the REAL orbit c_{n+1}=floor(3c/2), c0=8
c=8; ev=0; dens=[]
for n in range(N):
    if c%2==0: ev+=1
    c=3*c//2
    if n+1 in (1000,5000,20000,80000,200000):
        dens.append((n+1,ev/(n+1)))
print("\nAntihydra orbit even-density E_n/n (need > 1/3 for non-halt; heuristic -> 1/2):")
for n,d in dens: print(f"  n={n:7d} E_n/n={d:.5f}")
