import itertools, numpy as np
def stepf(c): return (3*c)//2
def Gfunc(k, s0=0):
    K=1<<k; G={}
    for digs in itertools.product((0,1),repeat=k):
        s=s0
        for d in digs: s=stepf(s+(d<<k))%K
        G[digs]=s&1
    return G
# Permutivity: G is LEFT-permutive if flipping b0 ALWAYS flips output (for all other bits fixed);
# RIGHT-permutive if flipping b_{k-1} always flips output. Bipermutive = both.
def check_perm(k):
    G=Gfunc(k, s0=0)
    # need start-independent first
    left=True; right=True
    for rest in itertools.product((0,1),repeat=k-1):
        a=G[(0,)+rest]; b=G[(1,)+rest]
        if a==b: left=False
    for rest in itertools.product((0,1),repeat=k-1):
        a=G[rest+(0,)]; b=G[rest+(1,)]
        if a==b: right=False
    # is G AFFINE (XOR of a subset of bits + const)? test linearity over GF(2)
    import numpy as np
    pts=list(G.keys()); 
    # fit G = c0 + sum ci bi mod 2
    A=np.array([[1]+list(p) for p in pts])%2
    y=np.array([G[p] for p in pts])%2
    # solve over GF(2) by gaussian elim; check consistency
    M=np.concatenate([A,y[:,None]],axis=1)%2
    rows,cols=M.shape
    r=0
    for c in range(cols-1):
        piv=None
        for i in range(r,rows):
            if M[i,c]: piv=i;break
        if piv is None: continue
        M[[r,piv]]=M[[piv,r]]
        for i in range(rows):
            if i!=r and M[i,c]: M[i]=(M[i]+M[r])%2
        r+=1
    affine = all((M[i,:-1].sum()!=0) or M[i,-1]==0 for i in range(rows))
    return left,right,affine
print("permutivity / affinity of the parity sliding-block code G:")
for k in (4,5,6):
    l,r,aff=check_perm(k)
    print(f"  k={k}: LEFT-permutive={l}  RIGHT-permutive={r}  AFFINE over GF(2)={aff}")
print("\n=> LEFT-permutive (at least) => the code is SURJECTIVE & the uniform Bernoulli is invariant;")
print("   AFFINE => it's an ALGEBRAIC CA => Host-Maass-Martinez / Pivato-Yassawi RANDOMIZATION applies:")
print("   Cesaro-iterates of (almost) any measure converge to uniform Bernoulli = digit equidistribution.")
