"""Sharpening the 2-adic valuation budget for c_{n+1}=floor(3c_n/2).

Tests the chain:  persistent parity bias p!=1/2
  <=> avg gap (=avgD_odd) != 2
  <=> the depths D_i=v2(3c_i-1) over odd steps deviate from geometric (mean 2)
  <=> the odd values o_j confine to thin 2-adic sets {o ≡ 3^{-1} mod 2^k}.

KEY LEMMA tested: the gap from an odd step to the NEXT odd step equals D_i=v2(3c_i-1) EXACTLY.
  (c odd, D=v2(3c-1): c->(3c-1)/2 = 2^{D-1}*m, m odd, then D-1 forced even steps, next odd at +D.)
This makes the budget Sum D_odd = n + O(log) a TAUTOLOGY (renewal: #gaps*avg gap = total time),
so the entire arithmetic content is the DISTRIBUTION of D over odd steps.

Also tests self-correction: corr(D_j,D_{j+1}); thin-set occupation; induced-map residue equidistribution.
All exact big-int arithmetic. .venv python only.
"""
import math
from collections import Counter

def v2(x):
    if x == 0: return 10**9
    r = 0
    while x & 1 == 0:
        x >>= 1; r += 1
    return r

def run(c0, N):
    c = c0
    Ds = []            # D_i for each odd step, in order
    odd_times = []     # n where step is odd
    odd_vals_mod = []  # o_j mod 2^K for residue test
    K = 6
    M = 1 << K
    n_even = 0; n_odd = 0
    gap_lemma_ok = True
    prev_odd_n = None
    pending_D = None
    for n in range(N):
        if c & 1:
            n_odd += 1
            D = v2(3 * c - 1)
            Ds.append(D)
            odd_vals_mod.append(c % M)
            # gap lemma: gap from this odd step to the NEXT odd step should == D
            if pending_D is not None:
                gap = n - prev_odd_n
                if gap != pending_D:
                    gap_lemma_ok = False
            prev_odd_n = n
            pending_D = D
            c = (3 * c - 1) // 2
        else:
            n_even += 1
            c = (3 * c) // 2
    # final pending gap unverifiable (orbit continues); fine
    return dict(Ds=Ds, n_even=n_even, n_odd=n_odd, gap_lemma_ok=gap_lemma_ok,
                odd_vals_mod=odd_vals_mod, K=K, M=M, c_final=c)

def report(c0, N):
    r = run(c0, N)
    Ds = r['Ds']; n_odd = r['n_odd']; n_even = r['n_even']; n = n_odd + n_even
    p_odd = n_odd / n
    avgD = sum(Ds) / len(Ds)
    print(f"\n=== c0={c0}, N={N} ===")
    print(f"p_odd={p_odd:.5f}  even-dens={n_even/n:.5f}  avgD_odd={avgD:.5f}  p_odd*avgD={p_odd*avgD:.5f}")
    print(f"GAP LEMMA (gap to next odd == D_i exactly): {r['gap_lemma_ok']}")
    print(f"v2(c_final)={v2(r['c_final'])}  bitlen(c_final)~{r['c_final'].bit_length()}")

    # D distribution vs geometric P(D=k)=2^{-k} (mean 2)
    cnt = Counter(Ds); tot = len(Ds)
    print(" D :  empirical   geometric(2^-k)")
    for k in range(1, 9):
        emp = cnt.get(k, 0) / tot
        geo = 2.0 ** (-k)
        print(f" {k:>2}:  {emp:.5f}    {geo:.5f}")
    # thin-set occupation: freq(D>=k) vs 2^{1-k}
    print(" thin-set: freq(D>=k) vs Haar 2^{1-k}")
    for k in range(2, 9):
        fge = sum(1 for d in Ds if d >= k) / tot
        haar = 2.0 ** (1 - k)
        print(f"   k={k}: freq(D>={k})={fge:.5f}  Haar={haar:.5f}  ratio={fge/haar:.3f}")

    # consecutive-D correlation (self-correction signature)
    if len(Ds) > 2:
        a = Ds[:-1]; b = Ds[1:]
        ma = sum(a)/len(a); mb = sum(b)/len(b)
        cov = sum((x-ma)*(y-mb) for x,y in zip(a,b))/len(a)
        va = sum((x-ma)**2 for x in a)/len(a)
        vb = sum((y-mb)**2 for y in b)/len(b)
        corr = cov/math.sqrt(va*vb) if va*vb>0 else 0.0
        print(f"corr(D_j,D_j+1)={corr:+.5f}  (0 => no self-correction in depth; <0 => mean-reverting)")
        # also lag tests
        for lag in (2,3,5):
            a=Ds[:-lag]; b=Ds[lag:]
            ma=sum(a)/len(a); mb=sum(b)/len(b)
            cov=sum((x-ma)*(y-mb) for x,y in zip(a,b))/len(a)
            va=sum((x-ma)**2 for x in a)/len(a); vb=sum((y-mb)**2 for y in b)/len(b)
            cr=cov/math.sqrt(va*vb) if va*vb>0 else 0.0
            print(f"   corr lag {lag}: {cr:+.5f}")

    # induced-map residue equidistribution: odd values mod 2^K, vs uniform over odds (2^{K-1} classes)
    K=r['K']; M=r['M']
    rc = Counter(r['odd_vals_mod'])
    nclass = M//2  # odd residues
    exp = len(r['odd_vals_mod'])/nclass
    chi2 = sum((rc.get(res,0)-exp)**2/exp for res in range(1,M,2))
    print(f"odd-value residues mod 2^{K}: chi2={chi2:.1f}  dof={nclass-1}  (chi2~dof => uniform => equidistributed)")

def self_correction_test():
    """Does a large D_j get followed by anomalously small D? Conditional mean E[D_{j+1}|D_j=k]."""
    r = run(8, 200000)
    Ds = r['Ds']
    print("\n=== conditional E[D_{j+1} | D_j=k]  (Haar/iid => flat at 2 regardless of k) ===")
    from collections import defaultdict
    nxt = defaultdict(list)
    for j in range(len(Ds)-1):
        nxt[Ds[j]].append(Ds[j+1])
    for k in range(1,7):
        if nxt[k]:
            print(f"  D_j={k}: count={len(nxt[k]):>6}  E[D_j+1]={sum(nxt[k])/len(nxt[k]):.4f}")

if __name__ == "__main__":
    report(8, 100000)
    report(2**200, 100000)
    # a forced-deep start: c0 = 3^{-1} mod 2^40 style (3c0-1 highly divisible) to seed large D
    inv3_mod = pow(3, -1, 1 << 40)   # 3*inv3 == 1 mod 2^40 => v2(3c-1)>=40 at start
    report(inv3_mod | 1, 100000)     # ensure odd
    self_correction_test()
