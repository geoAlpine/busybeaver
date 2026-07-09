from fractions import Fraction as F

def v(n, q):
    if n == 0: return 10**9
    k = 0
    while n % q == 0:
        n //= q; k += 1
    return k

def oddpart(n):
    while n % 2 == 0: n //= 2
    return n

# ---------- (A) Shared (2,3)-solenoid membership: product formula for p/q units ----------
def vp(n, p):  # p-adic valuation of integer (n!=0)
    if n == 0: return None
    k=0
    while n % p == 0: n//=p; k+=1
    return k
def val_place(fr, p):  # |x|_p^{-1 exponent}: returns v_p(fr)
    num, den = fr.numerator, fr.denominator
    return (vp(num,p) if num%p==0 else 0) - (vp(den,p) if den%p==0 else 0)

print("=== Shared (2,3)-solenoid membership (|u|_inf * |u|_2 * |u|_3 = 1 iff {2,3}-unit) ===")
for name,u in [("Antihydra 3/2",F(3,2)),("o4 4/3",F(4,3)),("o15/o18 8/3",F(8,3)),
               ("A^2 9/4",F(9,4)),("SpaceNeedle 5/2",F(5,2))]:
    v2 = val_place(u,2); v3 = val_place(u,3)
    # |u|_inf = u ; |u|_2 = 2^{-v2}; |u|_3=3^{-v3}; product over remaining primes captures 5 etc
    import math
    # check if u is {2,3}-smooth unit: numerator and denominator only have primes 2,3
    def smooth23(n):
        for p in (2,3):
            while n%p==0: n//=p
        return n==1
    ok = smooth23(u.numerator) and smooth23(u.denominator)
    print(f"  {name:18s}: v2={v2:+d} v3={v3:+d}  {'IN (2,3)-solenoid host' if ok else 'NOT {2,3}-smooth -> disjoint solenoid'}")

# ---------- (B) Antihydra reload map: exact identities linking consecutive run depths ----------
print("\n=== Antihydra exact reload map (run-depth recursion), verify on real orbit ===")
c = 8
runs = []  # (parity, depth, entry)
n = 0; NMAX = 200000
# collect maximal runs
cur_par = c % 2; runlen = 0; entry = c
prev = c
while n < NMAX:
    par = c % 2
    if par == cur_par:
        runlen += 1
    else:
        runs.append((cur_par, runlen, entry))
        cur_par = par; runlen = 1; entry = c
    # step
    c = (3*c)//2
    n += 1
runs.append((cur_par, runlen, entry))

# verify run-length == v2(entry - x), x_even=0, x_odd=1
mm = 0
for par, L, e in runs:
    x = 0 if par==0 else 1
    if v(e - x, 2) != L: mm += 1
print(f"  run-length == v2(entry - x): mismatches = {mm} / {len(runs)}")

# verify reload map: for an even-run (par0,depth Ke,entry ve) followed by odd-run (par1,Ko,vo):
#   Ko = v2(3^{Ke} * oddpart(ve) - 1)
# and odd->even: Ke' = v2(3^{Ko} * oddpart(vo-1) + 1)
mm_eo = 0; mm_oe = 0; ne=0; no=0
for i in range(len(runs)-1):
    par,L,e = runs[i]
    par2,L2,e2 = runs[i+1]
    if par==0 and par2==1:
        u = oddpart(e)
        pred = v(3**L * u - 1, 2)
        if pred != L2: mm_eo += 1
        ne += 1
    elif par==1 and par2==0:
        u = oddpart(e-1)
        pred = v(3**L * u + 1, 2)
        if pred != L2: mm_oe += 1
        no += 1
print(f"  even->odd reload  Ko = v2(3^Ke * oddpart(ve) - 1): mismatches = {mm_eo} / {ne}")
print(f"  odd->even reload  Ke = v2(3^Ko * oddpart(vo-1) + 1): mismatches = {mm_oe} / {no}")

# ---------- (C) whiteness vs heavy-tail: an i.i.d. heavy-tail sequence is perfectly white ----------
print("\n=== Whiteness does NOT bound the tail: i.i.d. heavy-tail is white (demonstration) ===")
import random
random.seed(1)
# heavy-tail K: P(K=k) ~ 1/k^2 (E[K]<inf, E[K^2]=inf), i.i.d. -> white by construction
def sample_heavy(Nn):
    xs=[]
    for _ in range(Nn):
        # inverse-ish: draw so that tail ~ 1/k
        u=random.random()
        k=int(1.0/(1.0-u))  # P(K>=k) ~ 1/k  => E[K^2]=inf
        xs.append(k)
    return xs
xs = sample_heavy(200000)
import statistics
def autocorr(xs,lag):
    m=sum(xs)/len(xs); n=len(xs)
    num=sum((xs[i]-m)*(xs[i+lag]-m) for i in range(n-lag))
    den=sum((x-m)**2 for x in xs)
    return num/den
print(f"  heavy-tail i.i.d. K:  mean={sum(xs)/len(xs):.2f}  max={max(xs)}  autocorr(1)={autocorr(xs,1):+.4f} autocorr(2)={autocorr(xs,2):+.4f}")
print("  -> perfectly white yet E[K^2] divergent: whiteness is BLIND to the tail obstruction.")
