import numpy as np
# THE untested route: does proven top-freshness propagate DOWN one position per step (recursion),
# surviving the x3 carry-mixing, to reach the parity? 
# Dynamics: bit_k(c_{n+1}) = bit_{k+1}(3 c_n). The x3 carry mixes in LOWER bits. Measure the transfer:
# how much of bit_k(c_{n+1}) is determined by bit_{k+1}(c_n) (clean shift) vs lower bits (carry contamination)?
N=300000
c=8; B=[]
for n in range(N):
    B.append(c); c=3*c//2
def bit(x,k): return (x>>k)&1
# (1) transfer: corr( bit_k(c_{n+1}) , bit_{k+1}(c_n) ) -- clean shift would be ~1
print("per-step transfer corr( bit_k(c_{n+1}) , bit_{k+1}(c_n) )  vs  contamination from lower bits:")
for k in (3,6,10):
    a=np.array([bit(B[n+1],k) for n in range(N-1)],float)
    b=np.array([bit(B[n],k+1) for n in range(N-1)],float)
    shift_corr=np.corrcoef(a,b)[0,1]
    # contamination: how much does bit_k(c_{n+1}) depend on the LOW bits (mod 2^k) of c_n? (the carry)
    low=np.array([B[n]&((1<<k)-1) for n in range(N-1)])
    # mutual info between a and (low parity) as proxy
    par=np.array([bit(B[n],0) for n in range(N-1)],float)
    carry_corr=np.corrcoef(a,par)[0,1]
    print(f"  k={k:2d}: shift-corr(clean transfer)={shift_corr:+.3f}   carry-corr(to parity)={carry_corr:+.4f}")

# (2) THE decisive test: if I make the TOP bits genuinely fresh (random) but keep dynamics, does the
# RECURSION carry that freshness down to the parity? Simulate the EXACT low-window dynamics where the
# incoming bit at the window edge is supplied by the (proven-fresh) top via the shift chain.
# Model: a cascade of k positions; fresh random injected at top; each step shifts down with x3 carry.
# Measure: does parity (bottom) decorrelate when ONLY the top is fed randomness?
def cascade(depth, T=200000, fresh_top=True):
    # state = integer window of 'depth' bits; each step: new = floor(3*state/2) but top bit refreshed
    import random
    random.seed(1)
    s=8 % (1<<depth); par=[]
    for t in range(T):
        par.append(s&1)
        topbit = random.getrandbits(1) if fresh_top else ((s>>(depth-1))&1)
        s = s & ((1<<(depth-1))-1)        # drop old top
        s = s | (topbit<<(depth-1))        # inject fresh top (proven zone)
        s = (3*s)//2 % (1<<depth)
    par=np.array(par,float)
    m=par.mean(); ac=np.mean((par[:-1]-m)*(par[1:]-m))/(par.var()+1e-12)
    return m, ac
for depth in (8,16,24):
    m,ac=cascade(depth)
    print(f"\ncascade depth={depth}, fresh top only: parity density={m:.4f} autocorr={ac:+.4f}")
print("\n=> if parity decorrelates (density~0.5, autocorr~0) with ONLY top fed fresh => recursion PROPAGATES")
print("   freshness down through x3-carry => proven top-freshness COULD reach parity => a real path!")
print("   if parity stays correlated/biased => carry-mixing blocks it => wall confirmed.")
