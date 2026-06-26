"""Phase 2: annealed spectral gap vs cylinder depth k (Antihydra renewal operator).
k2_deepdig.py found the mod-4 (k=2) empirical renewal transition operator T mixes in ~1 step
(gap ~0.95). Question now: as k grows (mod 2^k), does the gap STAY bounded away from 0 (uniform
mixing at all scales -> the whole obstruction is purely quenched-vs-annealed at every scale), or
does lambda_2(k) -> 1 (difficulty concentrates at large k)?

Object: T_k[r,r'] = P(c'_{j+1} = r' mod 2^k | c'_j = r mod 2^k), empirical over the renewal
subsequence c'_j = c/2 at even steps of c->floor(3c/2), seed 8. Each renewal step advances >=1
2-adic bit (branch D=v2(3c'-1)>=1), so the residue process genuinely mixes (unlike the direct orbit,
which advances ~0.58 bit/step and is near-deterministic mod 2^k). lambda_2(T_k) = annealed mixing
rate at scale k. Honest: this is the empirical (annealed/Markov) operator; the quenched orbit is NOT
Markov (c'_{j+1} mod 2^k depends on higher bits) -- that gap is the open problem, not measured here.
"""
import numpy as np

# Efficiency: store only the LOW bits of each renewal residue, computed in O(1) from c.
# renewal residue = c//2 (taken at even steps). Its value mod 2^KMAX = ((c & mask)>>1) where
# mask = 2^(KMAX+1)-1. c & smallmask is O(1) in CPython (result fits one limb); this avoids
# right-shifting / mod-ing the full ~10^5-bit orbit integer (the previous version's bottleneck).
KMAX = 7
SMASK = (1 << (KMAX+1)) - 1   # low KMAX+1 bits of c -> low KMAX bits of c//2
N_REN = 250000
c=8; low=[]
while len(low)<N_REN:
    if c & 1 == 0:
        low.append((c & SMASK) >> 1)   # (c//2) mod 2^KMAX, cheap
    c=(3*c)//2
renew=np.array(low, dtype=np.int64)   # residues mod 2^KMAX, small ints

print("="*76)
print("Annealed renewal operator: spectral gap vs cylinder depth k  (Antihydra, seed 8)")
print(f"renewal samples N={len(renew)}")
print("="*76)
print(f"{'k':>2} {'#states 2^k':>11} {'samples/state':>14} {'lambda_2':>9} {'gap=1-l2':>9} {'mix time ~1/gap':>16}")
res=[]
for k in range(1,KMAX+1):
    M=2**k
    if len(renew)//M < 200:   # need enough samples per state for a reliable matrix
        print(f"{k:>2} {M:>11} {len(renew)//M:>14}  (undersampled -- skipped)")
        continue
    rk=renew & (M-1)          # residues mod 2^k (vectorized)
    # count transitions via bincount on flattened pair index
    pair = rk[:-1].astype(np.int64)*M + rk[1:].astype(np.int64)
    T=np.bincount(pair, minlength=M*M).reshape(M,M).astype(float)
    rs=T.sum(axis=1,keepdims=True); rs[rs==0]=1
    T=T/rs
    vals=np.sort(np.abs(np.linalg.eigvals(T)))[::-1]
    l2=vals[1]
    res.append((k,l2))
    print(f"{k:>2} {M:>11} {len(renew)//M:>14} {l2:9.3f} {1-l2:9.3f} {1/(1-l2):16.2f}")

print("\n--- trend ---")
if len(res)>=3:
    ks=[r[0] for r in res]; l2s=[r[1] for r in res]
    # does lambda_2 grow toward 1 with k?
    slope=np.polyfit(ks,l2s,1)[0]
    print(f"lambda_2(k): {[round(x,3) for x in l2s]}  (k={ks[0]}..{ks[-1]})")
    print(f"linear slope d(lambda_2)/dk = {slope:+.4f}")
    print(f"max lambda_2 = {max(l2s):.3f}  (if << 1 uniformly: gap bounded away from 0 at all scales)")
print("\nReading (CORRECTED -- the script's first draft posed a false binary):")
print(" OBSERVED: lambda_2(k) grows mildly (0.001->0.33 over k=1..7), mixing time grows ~linearly")
print(" (1.0->1.5 steps, fit ~0.88+0.083k). This is NOT 'arithmetic difficulty at large k'; it is the")
print(" trivial bounded-expansion fact: each renewal step advances only E[D+1]~2 bits, so resolving")
print(" 2^k takes O(k) steps -> per-step gap shrinks ~1/k while the PER-BIT mixing stays efficient.")
print(" The annealed operator mixes FAST at every tested depth (<=1.5 steps at k=7).")
print(" CONCLUSION: the annealed (provable) side is efficient at all scales; the wall is STILL purely")
print(" quenched-vs-annealed (deterministic self-feeding), uniformly -- no scale is arithmetically")
print(" special. We do NOT extrapolate the k->inf asymptotic from 7 points (would be unsound).")
print(" Honest: this is the annealed/Markov operator; the QUENCHED gap (the real problem) is untouched.")
