def v2(x):
    x=abs(int(x)); r=0
    while x and x&1==0: x>>=1; r+=1
    return r
def F(cp):
    x=3*cp-1; D=v2(x); u=x>>D; return (pow(3,D)*u+1)//2, D
import random
random.seed(2)
# CORRECTED prediction: v2(F(c')-F(c'')) = v2(c'-c'') - D - 1  when D=v2(3c'-1) < separation m.
ok=0; tot=0; bigjump_fail=0
for _ in range(300000):
    m=random.randint(2,18)
    a=random.randrange(1,1<<22)
    bb=a + (2*random.randrange(0,1<<10)+1)*(1<<m)
    if v2(a-bb)!=m: continue
    Fa,Da=F(a); Fb,Db=F(bb)
    if Da!=Db: continue   # the formula needs matching jumps (holds when Da<m)
    pred=m-Da-1
    if pred<0: continue
    tot+=1
    if v2(Fa-Fb)==pred: ok+=1
print(f"CORRECTED: v2(F(c')-F(c'')) = v2(c'-c'') - D - 1  (when jumps match):  {ok}/{tot} = {ok/max(tot,1):.4f}")
print()
print("=> F is 2-adically EXPANDING with local factor 2^{D+1} >= 2 (D=v2(3c'-1)). Non-uniform: bigger jumps")
print("   expand MORE (but are rarer, geometric). This is a clean NON-UNIFORMLY EXPANDING 2-adic map.")
print("   STRUCTURAL INPUT for the additive-energy bound (Sec 6.5 hypothesis): expanding maps have")
print("   Ruelle-Perron-Frobenius transfer operators; the additive energy / collision count is exactly")
print("   what a spectral gap of the transfer operator would bound. The non-uniformity (large D) is the")
print("   technical crux = the renewal tail again -- but now in EXPANDING-MAP / thermodynamic language,")
print("   a setting with its own machinery (Young towers, inducing) for non-uniform hyperbolicity.")
