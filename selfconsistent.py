import numpy as np
# Renewal low-bit chain: incoming bit (=a future parity) feeds the chain; output = parity sequence.
# SELF-CONSISTENCY: incoming bits ARE parity bits (bit_k(c_n)=parity(c_{n+k})), so the law of incoming
# = law of output. For iid model: incoming Bernoulli(q), q=P(incoming=1)=P(odd)=1-E where E=even-density.
# Output even-density = Efun(q). Fixed point: E = Efun(1-E). Check if E=1/2 is UNIQUE & if any E<=1/3 solves.
def Efun(q,k=9):
    K=1<<k; P=np.zeros((K,K))
    for s in range(K):
        for hb,pr in ((0,1-q),(1,q)):
            c=s+(hb<<k); cp=(3*c)//2; P[s,cp%K]+=pr
    w,v=np.linalg.eig(P.T); i=np.argmin(np.abs(w-1)); st=np.real(v[:,i]); st/=st.sum()
    return sum(st[s] for s in range(K) if s%2==0)
print("self-consistency map  E -> Efun(1-E)  (fixed point = real even-density):")
print(" E_in    q=1-E    E_out=Efun(q)   (fixed pt where E_out==E_in)")
for E in (0.10,0.20,0.30,1/3,0.40,0.50,0.60,0.70):
    q=1-E; Eo=Efun(q)
    fp = "  <-- FIXED POINT" if abs(Eo-E)<0.01 else ""
    print(f" {E:.3f}   {q:.3f}    {Eo:.4f}{fp}")
# solve fixed point by iteration from several starts
print("\nfixed-point iteration E_{t+1}=Efun(1-E_t) from various starts:")
for E0 in (0.05,0.2,0.34,0.45,0.6,0.8):
    E=E0
    for _ in range(60): E=Efun(1-E)
    print(f"  start {E0:.2f} -> converges to E={E:.4f}")
print("\n=> if the ONLY fixed point is E=1/2 (>1/3), self-consistency FORCES even-density 1/2 in the iid model.")
print("   (open part: does the REAL correlated process admit a fixed point with E<=1/3? = the remaining gap)")
