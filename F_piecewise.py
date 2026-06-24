def v2(x):
    x=abs(int(x)); r=0
    while x and x&1==0: x>>=1; r+=1
    return r
def F(cp):
    x=3*cp-1; D=v2(x); u=x>>D; return (pow(3,D)*u+1)//2, D
# Verify F is PIECEWISE AFFINE: on {c': v2(3c'-1)=D}, F(c') = (3^{D+1} c' - 3^D + 2^D)/2^{D+1}.
print("(1) Piecewise-affine check: on cylinder v2(3c'-1)=D, is F(c') = (3^{D+1} c' - 3^D + 2^D)/2^{D+1}?")
import random; random.seed(3); ok=True
for _ in range(100000):
    cp=random.randrange(1,1<<30)
    Fa,D=F(cp)
    pred=(pow(3,D+1)*cp - pow(3,D) + (1<<D))//(1<<(D+1))
    if (pow(3,D+1)*cp - pow(3,D) + (1<<D)) % (1<<(D+1))!=0 or pred!=Fa: ok=False; break
print(f"    piecewise-affine formula holds: {ok}  => F is piecewise affine, 2-adic slope (3/2)^{{D+1}}, expansion 2^{{D+1}}")

# (2) Branch structure: the pieces P_D={v2(3c'-1)=D} have Haar measure 2^{-(D+1)} (geometric). Is F|P_D
#     a bijection onto Z_2 (full branch / Markov)? Check: as c' ranges over P_D, does F(c') cover Z_2 uniformly?
print("\n(2) Branch widths and images (is each branch full / Markov?):")
for D in (0,1,2,3):
    # sample c' in P_D = {c' = 3^{-1} + 2^D*(odd) ...}; actually v2(3c'-1)=D
    inv3=pow(3,-1,1<<20)
    base = inv3  # 3c'-1 ≡ 0 mod 2^D needs c' ≡ 3^{-1} mod 2^D; v2 exactly D needs the next bit set
    cnt=0; imgs=set()
    for t in range(2000):
        cp = (inv3 + (2*t+1)*(1<<D)) % (1<<20)   # c' with v2(3c'-1) ≈ D (ensure)
        if v2(3*cp-1)!=D: continue
        Fa,_=F(cp); imgs.add(Fa & 0xff); cnt+=1
    meas=2.0**-(D+1)
    print(f"    D={D}: Haar measure(P_D)=2^-{D+1}={meas:.4f}; sampled {cnt}, distinct F mod 256 = {len(imgs)}/256 (full branch => ~256)")
print("\n=> F is a PIECEWISE-AFFINE EXPANDING map of Z_2 (compact), slopes (3/2)^{D+1} (|.|_2 = 2^{D+1}>=2),")
print("   branch widths 2^-(D+1) (geometric). FUNCTION SPACE (reviewer's Q): the Ruelle operator acts on")
print("   LOCALLY-CONSTANT / Lipschitz functions w.r.t. the 2-adic metric; the additive-energy observables")
print("   (2^k-cylinder indicators) ARE locally constant => in the space. This is the CLASSICAL setting for a")
print("   Lasota-Yorke / spectral-gap argument -- a piecewise expanding map, not the moving-diagonal wall.")
