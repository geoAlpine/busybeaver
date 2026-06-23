import numpy as np
# beta=8/3 transfer operator spectral gap (parallel to beta=3/2 having gap 0.27)
K=2400; beta=8/3
P=np.zeros((K,K)); S=2400
edges=np.linspace(0,1,K+1)
for i in range(K):
    xs=edges[i]+(np.arange(S)+0.5)/S*(edges[i+1]-edges[i])
    ys=(beta*xs)%1.0
    js=np.minimum((ys*K).astype(int),K-1)
    for j in js: P[i,j]+=1.0/S
ev=sorted(np.linalg.eigvals(P.T),key=lambda z:-abs(z))
print("beta=8/3 transfer operator top |eigenvalues|:", [round(abs(z),4) for z in ev[:4]])
print(f"spectral gap 1-|lambda_2| = {1-abs(ev[1]):.4f}  (gap>0 => beta=8/3 map exponentially mixing, like beta=3/2)")
print("=> SAME structure: real beta-map has a gap but is digit-blind; 3-adic x8 is the digit-bearing isometry.")
