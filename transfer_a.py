import numpy as np
# Perron-Frobenius (Ulam) matrix for the beta=3/2 map T(x)=(3/2)x mod 1 on [0,1).
# P[i,j] = fraction of bin i mapped into bin j (Lebesgue). Leading eig=1; |lambda_2|<1 => spectral GAP.
K=3000
beta=1.5
edges=np.linspace(0,1,K+1)
P=np.zeros((K,K))
S=2000  # subsamples per bin
for i in range(K):
    xs=edges[i]+(np.arange(S)+0.5)/S*(edges[i+1]-edges[i])
    ys=(beta*xs)%1.0
    js=np.minimum((ys*K).astype(int),K-1)
    for j in js:
        P[i,j]+=1.0/S
# eigenvalues
ev=np.linalg.eigvals(P.T)
ev=sorted(ev,key=lambda z:-abs(z))
print("top eigenvalues of beta=3/2 transfer operator (Ulam, K=%d):"%K)
for z in ev[:6]:
    print(f"   |lambda|={abs(z):.5f}   lambda={z.real:+.5f}{z.imag:+.5f}i")
lam2=abs(ev[1])
print(f"\nspectral gap: 1 - |lambda_2| = {1-lam2:.4f}")
print(f"=> beta=3/2 MAP is exponentially mixing (gap>0): mixing time ~ 1/log(1/|lambda_2|) = {1/np.log(1/lam2):.2f} steps")
print("   (This is the 'generic/averaged' tool that WORKS -- a.e. point under T_beta equidistributes fast.)")
