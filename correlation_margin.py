import numpy as np
# How much incoming-bit CORRELATION is needed to push output even-density down to 1/3?
# Model incoming bits as a 2-state Markov chain with stationary bias q and lag-1 correlation rho.
# Transition: P(1|0)=a, P(1|1)=b; stationary P(1)=q=a/(1+a-b); correlation rho = b-a (in [..]).
# Augment the renewal state with the last incoming bit. Compute stationary output even-density vs rho.
def out_even(q, rho, k=8):
    # a,b from q,rho:  b-a=rho ; q=a/(1+a-b)=a/(1-rho) => a=q(1-rho); b=a+rho=q(1-rho)+rho
    a=q*(1-rho); b=a+rho
    if not (0<=a<=1 and 0<=b<=1): return None
    K=1<<k
    # state=(low-bits s, last incoming bit L). incoming next bit ~ P(1|L).
    P=np.zeros((2*K,2*K))
    for s in range(K):
        for L in (0,1):
            idx=s*2+L
            pnext1 = b if L==1 else a
            for hb,pr in ((1,pnext1),(0,1-pnext1)):
                c=s+(hb<<k); cp=(3*c)//2 % K
                P[idx, cp*2+hb]+=pr
    w,v=np.linalg.eig(P.T); i=np.argmin(np.abs(w-1)); st=np.real(v[:,i]); st/=st.sum()
    return sum(st[idx] for idx in range(2*K) if (idx//2)%2==0)
print("output even-density vs incoming-bit lag-1 correlation rho (q=0.5):")
print(" rho      E_out     (need rho << to push E_out below 1/3=0.333)")
for rho in (-0.9,-0.7,-0.5,-0.3,-0.1,0.0,0.1,0.3,0.5,0.7,0.9):
    E=out_even(0.5,rho)
    flag="  <-- below 1/3!" if (E is not None and E<=1/3) else ""
    print(f" {rho:+.2f}    {E if E is None else round(E,4)}{flag}")
print("\nmeasured incoming-bit autocorr on the REAL orbit: ~0.001 (essentially 0)")
print("=> at rho~0 the output is ~0.5. Find the THRESHOLD rho* where E_out=1/3:")
# bisect for negative rho threshold
lo,hi=-0.99,0.0
for _ in range(40):
    mid=(lo+hi)/2; E=out_even(0.5,mid)
    if E is None or E<=1/3: lo=mid
    else: hi=mid
print(f"  threshold rho* (E_out=1/3) ~ {hi:.3f}  => need correlation |rho|>{abs(hi):.2f} to break it")
print(f"  measured |rho|~0.001 << {abs(hi):.2f} => margin factor ~{abs(hi)/0.001:.0f}x")
