import numpy as np
# (I) Verify T(x)=floor(3x/2) is a measure-preserving 2-to-1 EXACT endomorphism of Z_2.
# Check on Z/2^k: every target has exactly 2 preimages (=> measure preserving), for x ranging Z/2^{k+1}.
for k in (8,):
    K=1<<k; pre=[0]*K
    for x in range(2*K):
        y=((3*x)//2)%K
        pre[y]+=1
    print(f"T on Z/2^{k}: preimage counts over Z/2^{k+1}: min={min(pre)} max={max(pre)} (exactly 2 => measure-preserving 2-to-1)")

# (II) THE conditional-bound attack: model incoming high bit as Bernoulli(q) (q=bias), NOT necessarily 1/2.
# Build the low-bit Markov chain on Z/2^k with P(incoming=1)=q; get stationary even-density as fn of q.
# If even-density>1/3 for ALL q in (eps,1-eps), then Antihydra non-halts PROVIDED incoming bits are
# merely NON-DEGENERATE (not eventually constant) -- a far weaker statement than full equidistribution.
def even_density(q,k=8):
    K=1<<k; P=np.zeros((K,K))
    for s in range(K):
        for hb,pr in ((0,1-q),(1,q)):
            c=s+(hb<<k); cp=(3*c)//2
            P[s,cp%K]+=pr
    w,v=np.linalg.eig(P.T); i=np.argmin(np.abs(w-1))
    stat=np.real(v[:,i]); stat/=stat.sum()
    return sum(stat[s] for s in range(K) if s%2==0)
print("\nstationary even-density vs incoming-bit bias q:")
for q in (0.01,0.05,0.1,0.2,0.3,0.5,0.7,0.9,0.95,0.99):
    print(f"  q={q:.2f}: even-density={even_density(q):.4f}  {'>1/3 OK' if even_density(q)>1/3 else '<=1/3 !!'}")

# (III) also the spectral gap as fn of q (is mixing robust to bias?)
def gap(q,k=8):
    K=1<<k; P=np.zeros((K,K))
    for s in range(K):
        for hb,pr in ((0,1-q),(1,q)):
            c=s+(hb<<k); cp=(3*c)//2; P[s,cp%K]+=pr
    ev=sorted(np.linalg.eigvals(P.T),key=lambda z:-abs(z))
    return 1-abs(ev[1])
print("\nspectral gap vs q (mixing robust?):")
for q in (0.05,0.2,0.5,0.8,0.95):
    print(f"  q={q:.2f}: gap={gap(q):.4f}")
