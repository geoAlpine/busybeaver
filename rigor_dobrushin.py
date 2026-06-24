from fractions import Fraction as F
# RIGOROUS contraction of the renewal chain (no floating point). Transition matrix P on Z/2^k,
# P(s,s')=(1/2)#{hb in{0,1}: step(s,hb)=s'} (incoming bit uniform). Dobrushin coeff:
#   delta(P) = max_{s1,s2} (1 - sum_{s'} min(P(s1,s'),P(s2,s'))).  delta<1 => rigorous contraction.
# Compute delta(P^m) exactly (rational) to certify a contraction rate.
def build_P(k):
    K=1<<k
    P=[[F(0)]*K for _ in range(K)]
    for s in range(K):
        for hb in (0,1):
            c=s+(hb<<k); t=(3*c)//2 % K
            P[s][t]+=F(1,2)
    return P,K
def matmul(A,B,K):
    C=[[F(0)]*K for _ in range(K)]
    for i in range(K):
        Ai=A[i]
        for l in range(K):
            a=Ai[l]
            if a:
                Bl=B[l]
                for j in range(K):
                    if Bl[j]: C[i][j]+=a*Bl[j]
    return C
def dobrushin(P,K):
    # max over pairs of (1 - overlap). Overlap=sum_j min(P[s1][j],P[s2][j]). Exact.
    worst=F(0)
    for s1 in range(K):
        for s2 in range(s1+1,K):
            ov=F(0)
            for j in range(K):
                a=P[s1][j]; b=P[s2][j]
                ov+= a if a<b else b
            d=1-ov
            if d>worst: worst=d
    return worst
for k in (3,4,5):
    P,K=build_P(k)
    # find smallest m with delta(P^m) < 1 (rigorous contraction), report delta exactly
    Pm=P; 
    for m in range(1,9):
        d=dobrushin(Pm,K)
        status = "CONTRACTION (delta<1)" if d<1 else "not yet"
        print(f"k={k} m={m}: Dobrushin delta(P^{m}) = {d}  (~{float(d):.4f})  {status}")
        if d<1: break
        Pm=matmul(Pm,P,K)
    print()
