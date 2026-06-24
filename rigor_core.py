from fractions import Fraction as F
# (1) MODEL EXACTNESS: verify low-digit evolution is EXACTLY a function of (low digits, one incoming digit).
#     c_{n+1} mod p^k = floor(mu*c_n) mod p^k must depend only on c_n mod p^{k+1}. Verify for p=2,3.
def check_exact(p,a,b,k,trials=4000):
    # mu = 2^a/3^b ... map M(x)=floor(mu x). For p=2 (mu=3/2): floor(3x/2). For p=3 (mu=8/3): floor(8x/3).
    import random
    ok=True
    K=p**k; K1=p**(k+1)
    num=2**a; den=3**b if p==2 else 3   # mu numerator/denominator structure
    if p==2: f=lambda x:(3*x)//2
    else:    f=lambda x:(8*x)//3
    for _ in range(trials):
        x=random.randrange(0,p**(k+3))
        # does f(x) mod p^k depend only on x mod p^{k+1}?
        x2=x % K1
        if f(x)%K != f(x + K1*((x//K1+1)))%K and f(x)%K != f(x2)%K:
            # compare f(x) mod p^k to f(x mod p^{k+1}) mod p^k with same low part -- need careful test
            pass
    # cleaner: f(x) mod p^k determined by x mod p^{k+1}? test many x with same x mod p^{k+1}
    from collections import defaultdict
    d=defaultdict(set)
    for x in range(p**(k+2)):
        d[x%K1].add(f(x)%K)
    maxamb=max(len(v) for v in d.values())
    return maxamb==1
print("MODEL EXACTNESS (low-digit evolution determined by low digits + ONE incoming digit):")
print(f"  p=2 (floor(3x/2)), k=4: exact = {check_exact(2,1,1,4)}")
print(f"  p=3 (floor(8x/3)), k=4: exact = {check_exact(3,3,1,4)}")

# (2) base-3 Dobrushin: delta(P^k)=0 in k steps? (rigorous contraction for o18)
def build_P3(k):
    K=3**k; P=[[F(0)]*K for _ in range(K)]
    for s in range(K):
        for ht in (0,1,2):
            c=s+ht*K; t=(8*c)//3 % K
            P[s][t]+=F(1,3)
    return P,K
def matmul(A,B,K):
    C=[[F(0)]*K for _ in range(K)]
    for i in range(K):
        for l in range(K):
            a=A[i][l]
            if a:
                for j in range(K):
                    if B[l][j]: C[i][j]+=a*B[l][j]
    return C
def dobrushin(P,K):
    worst=F(0)
    for s1 in range(K):
        for s2 in range(s1+1,K):
            ov=sum((P[s1][j] if P[s1][j]<P[s2][j] else P[s2][j]) for j in range(K))
            if 1-ov>worst: worst=1-ov
    return worst
print("\nbase-3 (o18) rigorous Dobrushin delta(P^m):")
for k in (2,3):
    P,K=build_P3(k); Pm=P
    for m in range(1,k+2):
        d=dobrushin(Pm,K)
        print(f"  k={k} m={m}: delta = {d} ({'CONTRACTION' if d<1 else 'not yet'})")
        if d<1: break
        Pm=matmul(Pm,P,K)
