"""Phase 2: push i.i.d.-likeness to higher cylinders -- does the deterministic self-feeding leave a
FINITE-ORDER correlation signature (the quenched-vs-annealed seam, meeting Q2)?

STRUCTURAL FACT (hand-derived, verified below). For c_{n+1}=floor(a c_n/p), write c_n in base p as
digits d0,d1,d2,... Then
    c_{n+1} mod p = (a*d1 + floor(a*d0/p)) mod p,
and generally c_{n+k} mod p is a function of (d0,...,dk). The induced digit map is a BIJECTION on
(Z/p)^{k+1}. Hence:
   joint law of (c_n, c_{n+1}, ..., c_{n+k}) mod p  ==  law of (d0,...,dk)  ==  c_n mod p^{k+1}.
=> EVERY finite lag/joint statistic of the mod-p sequence is EXACTLY the mod-p^{k+1} cylinder law.
There is NO correlation beyond the cylinder marginals. PREDICTION: at every finite k the orbit is
i.i.d.-indistinguishable iff it equidistributes mod p^{k+1} -- the self-feeding is INVISIBLE to any
finite-order test; the quenched(deterministic)-vs-annealed(fresh-digit) difference lives strictly
below all finite correlations. This is WHY annealed mixes trivially but quenched is open.

TESTS (each could falsify the prediction):
  (T1) mod p^2 chi2 vs i.i.d. control  -- = joint (c_n,c_{n+1}) mod p uniformity.
  (T2) lag-k mutual information I(c_n mod p ; c_{n+k} mod p), k=1..4, vs a SHUFFLE control (the
       finite-N MI bias floor). A real self-feeding signature would show MI above the shuffle floor.
  (T3) block entropy rate of the mod-p sequence vs log2(p) (i.i.d. max).
Includes Antihydra (p=2, mu=3/2, seed 8) explicitly.
"""
from math import gcd, log2, log
from collections import Counter
import statistics, random

def orbit_res(a,p,seed,N,mod):
    c=seed; out=[]
    for _ in range(N):
        out.append(c % mod); c=(a*c)//p
    return out

def chi2(seq, M, N):
    c=Counter(seq[:N]); return N*sum((c[r]/N-1.0/M)**2 for r in range(M))

def iid_chi2(M,N,draws=30):
    random.seed(1); return statistics.mean(chi2([random.randrange(M) for _ in range(N)],M,N) for _ in range(draws))

def mutual_info(xs, ys, p):
    N=len(xs); jc=Counter(zip(xs,ys)); xc=Counter(xs); yc=Counter(ys); mi=0.0
    for (x,y),c in jc.items():
        pxy=c/N; px=xc[x]/N; py=yc[y]/N
        if pxy>0: mi+=pxy*log2(pxy/(px*py))
    return mi

def verify_digit_bijection(a,p):
    """check c_{n+1} mod p = (a*d1 + floor(a*d0/p)) mod p on random c."""
    random.seed(3); ok=True
    for _ in range(2000):
        c=random.randrange(1,10**6)
        d0=c%p; d1=(c//p)%p
        lhs=((a*c)//p)%p
        rhs=(a*d1+(a*d0)//p)%p
        if lhs!=rhs: ok=False; break
    return ok

print("="*80)
print("Higher-cylinder / finite-order correlation test (quenched-vs-annealed seam)")
print("="*80)

cases=[(2,3,8,"Antihydra"),(2,5,11,""),(2,7,11,""),(3,7,11,""),(3,8,11,""),(5,11,11,""),(5,12,11,"")]
N=60000
print(f"\nDigit-bijection identity c_{{n+1}} mod p = (a*d1+floor(a*d0/p)) mod p:")
for (p,a,_,_) in cases:
    print(f"   mu={a}/{p}: {verify_digit_bijection(a,p)}", end="  ")
print()

print(f"\n(T1) mod p^2 equidistribution = joint (c_n,c_{{n+1}}) mod p uniformity.  N={N}")
print(f"{'mu':>7} {'seed':>5} {'chi2 mod p^2':>13} {'iid p^2':>9} {'ratio':>7} {'tag':>10}")
for (p,a,s,tag) in cases:
    M=p*p; seq=orbit_res(a,p,s,N,M); ch=chi2(seq,M,N); ic=iid_chi2(M,N)
    print(f"{a}/{p:<5} {s:>5} {ch:13.3f} {ic:9.3f} {ch/ic:7.2f} {tag:>10}")

print(f"\n(T2) lag-k mutual information I(c_n mod p; c_{{n+k}} mod p) vs SHUFFLE floor (bits).")
print(f"{'mu':>7} {'k':>2} {'MI':>9} {'shuffle':>9} {'excess':>9}")
for (p,a,s,tag) in cases[:5]:
    base=orbit_res(a,p,s,N,p)
    sh=base[:]; random.seed(5); random.shuffle(sh)
    for k in (1,2,3,4):
        mi=mutual_info(base[:-k], base[k:], p)
        mish=mutual_info(sh[:-k], sh[k:], p)
        print(f"{a}/{p:<5} {k:>2} {mi:9.5f} {mish:9.5f} {mi-mish:+9.5f}"+("  <-Antihydra" if tag and k==1 else ""))

print(f"\n(T3) block entropy rate of mod-p sequence (bits/symbol) vs log2(p) (i.i.d. max).")
print(f"{'mu':>7} {'log2 p':>7} {'H(1)':>7} {'H2/2':>7} {'H3/3':>7}")
def block_entropy(seq,p,L):
    blocks=Counter(tuple(seq[i:i+L]) for i in range(len(seq)-L+1))
    tot=sum(blocks.values()); return -sum((c/tot)*log2(c/tot) for c in blocks.values())
for (p,a,s,tag) in cases[:5]:
    seq=orbit_res(a,p,s,N,p)
    h1=block_entropy(seq,p,1); h2=block_entropy(seq,p,2)/2; h3=block_entropy(seq,p,3)/3
    print(f"{a}/{p:<5} {log2(p):7.3f} {h1:7.4f} {h2:7.4f} {h3:7.4f}")

print("\n" + "="*80)
print("VERDICT")
print("="*80)
print("Prediction: self-feeding leaves NO finite-order signature. Confirmed iff (T1) mod p^2 chi2 ~")
print("i.i.d., (T2) lag MI excess over shuffle ~ 0 for all k, (T3) block entropy rate ~ log2(p).")
print("If so: at EVERY finite cylinder/lag the orbit is i.i.d.-indistinguishable; the quenched-vs-")
print("annealed difference is provably BELOW all finite-order tests -- this is the precise sense in")
print("which the wall is 'pure determinism': no finite statistic can see it, which is exactly why")
print("annealed (fresh digits) mixes trivially while quenched (the real orbit) stays open. The seam")
print("is not a detectable correlation; it is the demand that the orbit feed its OWN next digit.")
