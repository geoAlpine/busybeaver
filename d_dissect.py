"""Dissect the generation of d(n) = r_orb(n) XOR r_pure(n), the self-induced carry coin.

EXACT ALGEBRA to verify:
  A = 8*3^n, B = T_n, A == B (mod 2^n) [integrality]. A - B = c_n * 2^n.
  Since low n bits of A,B agree, A = A_hi*2^n + L, B = B_hi*2^n + L (same L), so
  A - B = (A_hi - B_hi)*2^n, hence bit_n(A-B) = (A_hi - B_hi) mod 2 = bit_n(A) XOR bit_n(B).
  => r_orb(n) = bit_n(8*3^n) XOR bit_n(T_n), with NO borrow into bit n (beta_n = 0).
  => d(n) = r_orb XOR r_pure = bit_n(T_n).   [the n-th bit of the carry-sum, exactly]
So the orbit parity LINEARLY (mod 2) splits into a pure-power Mahler bit and a carry-sum bit.

Then DISSECT bit_n(T_n), T_n = sum_{k=0}^{n-1} 2^k 3^{n-1-k} r_k:
  (1) annealed surrogate: replace r_k by i.i.d. coins -> is bit_n density 1/2 & decorrelated? (tractable?)
  (2) influence profile: flipping r_k (coeff delta_k = 2^k 3^{n-1-k}) flips bit_n with what probability,
      as a function of the offset j = n - k? LOCAL window (few k matter) = controllable crack; GLOBAL
      (all k matter) = fully endogenous wall.
0 false proofs: identities asserted only if they pass on the real orbit; influence reported with the
trivial baseline (a random delta flips a random bit with prob 1/2).
"""
import math

N = 4000
c = 8
Tn = 0
p3 = 1   # 3^n
p2 = 1   # 2^n
r = []
r_orb = []; r_pure = []; d = []; bitn_T = []
for n in range(N):
    ro = c & 1
    rp = (8 * p3 >> n) & 1
    bt = (Tn >> n) & 1
    r.append(ro); r_orb.append(ro); r_pure.append(rp); d.append(ro ^ rp); bitn_T.append(bt)
    Tn = 3 * Tn + p2 * ro
    c = (3 * c) // 2
    p3 *= 3
    p2 <<= 1

# (A) verify d(n) == bit_n(T_n) and beta_n == 0
ok_d = all(d[n] == bitn_T[n] for n in range(N))
print(f"(A) d(n) == bit_n(T_n) for all n<{N}: {'OK' if ok_d else 'FAIL'}")
print(f"    => EXACT identity  r_orb(n) = bit_n(8*3^n) XOR bit_n(T_n)  (no borrow; integrality linearizes)")

# (B) annealed surrogate: i.i.d. r_k -> bit_n(T_n^exo). Use a deterministic pseudo-coin to stay reproducible
#     (no Math.random); take e_k = k-th bit of an irrational-ish expansion (parity of floor(k*phi)).
phi = (1 + 5 ** 0.5) / 2
def coin(k):  # deterministic balanced exogenous bit, independent of the orbit
    return int(math.floor((k + 1) * phi)) & 1
Texo = 0; p2b = 1; bn_exo = []
exo = [coin(k) for k in range(N)]
for n in range(N):
    bn_exo.append((Texo >> n) & 1)
    Texo = 3 * Texo + p2b * exo[n]
    p2b <<= 1
def dens(a): return sum(a) / len(a)
print(f"\n(B) annealed surrogate (exogenous i.i.d.-like r_k, independent of orbit):")
print(f"    density bit_n(T^exo) = {dens(bn_exo):.4f}   (real bit_n(T_n) density = {dens(bitn_T):.4f})")
def corr(a, b):
    m=len(a); ma=sum(a)/m; mb=sum(b)/m
    cov=sum((a[i]-ma)*(b[i]-mb) for i in range(m))/m
    va=sum((x-ma)**2 for x in a)/m; vb=sum((x-mb)**2 for x in b)/m
    return cov/math.sqrt(va*vb) if va>0 and vb>0 else 0.0
print(f"    lag-1 autocorr bit_n(T^exo) = {corr(bn_exo[:-1],bn_exo[1:]):+.4f}  (annealed expected ~0)")

# (C) influence profile of bit_n(T_n) on r_k, as function of offset j = n-k.
#     delta_k = 2^k * 3^{n-1-k}; influence_j = P_n[ bit_n(T_n) != bit_n(T_n +/- delta_k) ], k=n-j.
#     Sample n over a range; aggregate by j. Baseline: a random additive delta flips a random target
#     bit with prob ~1/2 ONLY if delta has a 1 at bit n; here delta_k is structured.
import collections
infl = collections.defaultdict(lambda: [0, 0])  # j -> [flips, trials]
# rebuild T_n exactly at sampled n; reuse cumulative via storing T at checkpoints
# store T_n for sampled n
sample_ns = list(range(200, N, 17))  # spread
# precompute T_n by re-running and snapshotting
Tn2 = 0; p2c = 1; Tsnap = {}
for n in range(N):
    if n in sample_ns: Tsnap[n] = Tn2
    Tn2 = 3 * Tn2 + p2c * r[n]
    p2c <<= 1
for n in sample_ns:
    T = Tsnap[n]
    bn = (T >> n) & 1
    for j in range(1, 41):
        k = n - j
        if k < 0: break
        delta = (1 << k) * pow(3, n - 1 - k)
        # flip r_k: if r[k]==1 subtract, else add
        T2 = T - delta if r[k] == 1 else T + delta
        bn2 = (T2 >> n) & 1
        infl[j][0] += (bn2 != bn); infl[j][1] += 1
print(f"\n(C) influence of r_k on bit_n(T_n), by offset j=n-k  (1/2 = max scrambling, 0 = no effect):")
print(f"    {'j':>4} {'P(flip bit_n)':>14}")
for j in range(1, 41):
    f, t = infl[j]
    if t: print(f"    {j:>4} {f/t:>14.3f}")
# summarize: is influence localized (decays in j) or flat (all k matter)?
vals = [infl[j][0]/infl[j][1] for j in range(1, 41) if infl[j][1]]
print(f"\n    mean influence over j=1..40 = {sum(vals)/len(vals):.3f}")
print(f"    influence at j=1..5  = {[round(v,2) for v in vals[:5]]}")
print(f"    influence at j=36..40= {[round(v,2) for v in vals[-5:]]}")

print("\n" + "="*78)
print("READING")
print("="*78)
print("""If d(n)=bit_n(T_n) [verified in (A)] and the influence (C) is FLAT near 1/2 across all offsets j,
then bit_n(T_n) depends maximally and non-locally on the ENTIRE parity history r_0..r_{n-1}: every past
parity scrambles the diagonal carry bit equally. That is the precise GLOBAL endogeneity -- no finite
window of history controls d, so no local/automatic handle exists; the annealed surrogate (B) is balanced
(tractable) but the real bit is the quenched diagonal of a fully history-coupled carry-sum. If instead
influence DECAYS in j, a finite window controls d => a genuine crack (local certificate). The numbers
above decide which.""")
