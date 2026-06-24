import numpy as np
# Attack bit_k(c_n) ⊥ (c_n mod 2^k). Is it EXACT (a symmetry) or asymptotic (=equidistribution)?
# (1) cross-correlation C_N(k,j)=(1/N)Σ (bit_k-1/2)(bit_j-1/2) for j<k: magnitude vs 1/sqrt(N) (random)?
N=400000
c=8; B=np.zeros((N,12),dtype=np.int8)
for n in range(N):
    for k in range(12): B[n,k]=(c>>k)&1
    c=3*c//2
Bc=B.astype(float)-0.5
print("cross-corr (bit_k, bit_j) over orbit (j<k); compare to random ~1/sqrt(N)=%.2e:"%(1/np.sqrt(N)))
for k in (4,8,11):
    row=[]
    for j in range(k):
        Cv=np.mean(Bc[:,k]*Bc[:,j])
        row.append(Cv)
    print(f"  k={k:2d}: max|corr over j<k| = {max(abs(x) for x in row):.2e}  (random scale {1/np.sqrt(N):.2e})")

# (2) Is it EXACT at finite N? running correlation vs N (does it -> 0 like 1/sqrt(N), or is it ~0 always?)
print("\nrunning |corr(bit_8, bit_0)| vs N (1/sqrt(N) if random-decay; ~0 always if exact symmetry):")
for M in (1000,10000,100000,400000):
    Cv=np.mean(Bc[:M,8]*Bc[:M,0]); print(f"  N={M:6d}: |corr|={abs(Cv):.2e}  1/sqrt(N)={1/np.sqrt(M):.2e}")

# (3) PROOF PROBE: does the dynamics give a recursion forcing decay? bit structure of c_{n+1} from c_n.
#  c_{n+1}=floor(3c/2). Test if conditional P(bit_k(c_n)=1 | c_n mod 2^k = s) is uniform for each s.
k=6; K=1<<k
from collections import defaultdict
cnt=defaultdict(lambda:[0,0])
c=8
for n in range(N):
    s=c&(K-1); hk=(c>>k)&1; cnt[s][hk]+=1; c=3*c//2
devs=[abs(cnt[s][1]/(cnt[s][0]+cnt[s][1])-0.5) for s in cnt if cnt[s][0]+cnt[s][1]>50]
print(f"\nconditional P(bit_k=1 | low state s) deviation from 1/2: max={max(devs):.4f} mean={np.mean(devs):.4f}")
print("  (uniform conditional => independence; deviations ~1/sqrt(count) if just statistical)")
