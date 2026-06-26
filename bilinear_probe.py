"""Phase 2: attempt the bilinear / sum-product attack on the character sum S_N = sum_n chi_{-4}(c_n).
Vaughan/bilinear and sum-product methods need MULTIPLICATIVE structure -- the index n interacting with
the multiplicative structure of the summand. Our summand f(n)=chi_{-4}(c_n) (0 if c_n even, +-1 if odd)
is governed by c_n mod 4, and c_n=(3^n c_0 - T_n)/2^n => c_n mod 4 depends on the HIGH bits of the
dynamical carry T_n (the whole parity history), NOT on any multiplicative function of n. So Vaughan has
no entry point. We TEST this concretely (each test could falsify 'no multiplicative handle'):
  (T1) correlation of f(n) with the Liouville function lambda(n) (the canonical multiplicative test):
       if |sum f(n)lambda(n)| ~ sqrt -> uncorrelated -> no multiplicative coupling.
  (T2) is f(n) equidistributed over arithmetic progressions n == a mod q? (does n's residue structure
       couple to c_n mod 4?) -- chi^2 over progressions.
  (T3) raw cancellation of S_N itself (baseline) and of the Liouville sum (sanity).
If f(n) is uncorrelated with lambda and flat over n-progressions, the orbit is 'multiplicatively
structureless' in n: bilinear/sum-product/Vaughan have NO handle -> Q4's 'out of reach' is the answer.
"""
import numpy as np, math

N=100_000
# orbit: record c_n mod 4 and parity (need big-int iteration; mod 4 via c&3)
c=8
f=np.zeros(N, dtype=np.int8)   # f[n]=chi_{-4}(c_n): +1 if c_n==1(4), -1 if ==3(4), 0 if even
for n in range(N):
    r=c & 3
    if r==1: f[n]=1
    elif r==3: f[n]=-1
    else: f[n]=0
    c=(3*c)//2

# Liouville lambda(n) via smallest-prime-factor sieve
spf=np.zeros(N+1, dtype=np.int32)
for i in range(2,N+1):
    if spf[i]==0:
        spf[i::i]=np.where(spf[i::i]==0, i, spf[i::i])
lam=np.ones(N+1, dtype=np.int8)
for n in range(2,N+1):
    m=n; om=0
    while m>1:
        p=spf[m]
        while m%p==0: m//=p; om+=1
    lam[n]=-1 if om&1 else 1

print("="*78)
print("Bilinear / multiplicative-structure probe of S_N = sum_n chi_{-4}(c_n)  (Antihydra)")
print("="*78)
idx=np.arange(N)
odd=f!=0
print(f"N={N}, #odd c_n = {odd.sum()} ({odd.mean()*100:.1f}%)")

# (T3) baseline cancellation
S=f.cumsum()
print(f"\n(T3) raw S_N = sum chi(c_n) = {S[-1]}   |S_N|/sqrt(#odd) = {abs(S[-1])/math.sqrt(odd.sum()):.3f}  (sqrt-cancellation if ~O(1))")

# (T1) correlation with Liouville
fl = f.astype(int) * lam[ :N].astype(int)   # f(n) lambda(n), n=0..N-1 (lam[0]=1 unused weight)
Sfl=fl.sum()
print(f"\n(T1) Liouville correlation: sum_n f(n)lambda(n) = {Sfl}   |.|/sqrt(#odd) = {abs(Sfl)/math.sqrt(odd.sum()):.3f}")
print(f"     (compare raw |S_N|/sqrt = {abs(S[-1])/math.sqrt(odd.sum()):.3f}; if similar magnitude, lambda")
print(f"      multiplies in like a random +-1 -> f is UNCORRELATED with the multiplicative lambda.)")

# (T2) equidistribution of f over n-progressions n==a mod q
print(f"\n(T2) f(n) over arithmetic progressions n == a mod q (mean of chi over each class):")
for q in (2,3,4,5,8):
    means=[]
    for a in range(q):
        sel=(idx%q==a)&odd
        means.append(f[sel].mean() if sel.sum()>0 else 0.0)
    spread=max(means)-min(means)
    print(f"   q={q}: class-means {[f'{m:+.4f}' for m in means]}  spread={spread:.4f}")
print("   (means all ~0 with small spread => f(n) does NOT depend on n's residue mod q: no")
print("    arithmetic-progression structure for a bilinear/Type-I sum to exploit.)")

print("\n" + "="*78)
print("VERDICT")
print("="*78)
print("Structural: c_n = (3^n c_0 - T_n)/2^n, so c_n mod 4 is set by the HIGH bits of the dynamical")
print("carry T_n (the whole parity history) -- there is NO multiplicative function of n controlling it.")
print("Tests: if f(n) is uncorrelated with lambda(n) (T1 ~ raw rate) and flat over n-progressions (T2),")
print("then S_N = sum chi(c_n) has NO multiplicative/bilinear structure: Vaughan's identity, sum-product,")
print("and Type-I/II decompositions have NO entry point (they need n to couple to multiplicative")
print("structure of the summand; here the summand is a positive-entropy DYNAMICAL function of n).")
print("=> Q4 answer (from inside): a single floor(mu*)-orbit is OUT OF REACH of character-sum technology")
print("   precisely because it is multiplicatively structureless. The only cancellation is dynamical")
print("   (Birkhoff for the specified point) = the equidistribution wall. Honest: empirical, N=1e5.")
