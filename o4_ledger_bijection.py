# o4 a-ledger: itinerary bijection theorem + ruin constant (2026-07-06)
# Odometer: 3G' = 4G + e(rho), rho = G mod 3, e = {0:9, 1:14, 2:1}.
# THEOREM [PROVEN]: for every L>=1 the map {seed G mod 3^L} -> itinerary (rho_0..rho_{L-1})
# is a BIJECTION. Proof: G=3H+rho => G' = 4H + s(rho), s={0:3,1:6,2:3}; 4 invertible mod
# 3^{L-1}; induction on L.  Verified exhaustively L=1..8 below.
e={0:9,1:14,2:1}
def step(G):
    rho=G%3
    return rho,(4*G+e[rho])//3

if __name__=='__main__':
    for L in range(1,9):
        M=3**L; seen=set()
        for G0 in range(M):
            G=G0; it=[]
            for _ in range(L):
                rho,G=step(G); it.append(rho)
            seen.add(tuple(it))
        assert len(seen)==M, f"L={L}: NOT a bijection"
        print(f'L={L}: bijection over 3^{L} seeds: OK')
    # proof identity
    s={0:3,1:6,2:3}
    import random
    for _ in range(10000):
        H=random.randrange(10**9); rho=random.randrange(3)
        _,Gp=step(3*H+rho)
        assert Gp==4*H+s[rho]
    print("proof identity G=3H+rho => G'=4H+s(rho): OK")
    # annealed ruin constant: eta solving E[eta^X]=1, X in {-1,+4,+6} uniform
    def f(eta): return (eta**-1+eta**4+eta**6)/3
    lo,hi=0.01,0.999
    for _ in range(200):
        mid=(lo+hi)/2
        if f(mid)>1: lo=mid
        else: hi=mid
    eta=(lo+hi)/2
    print(f'annealed ruin base eta = {eta:.6f}; ruin from a: a=8 {eta**8:.2e}, a=34 {eta**34:.2e}, a=124 {eta**124:.2e}')
