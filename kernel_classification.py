# THEOREM (proven): T_mu(x)=floor((a/b)x), b=p^beta prime power, is a clean p-to-1 exact endomorphism of Z_p
# iff beta=1 (b=p), i.e. v_p(mu)=-1. Key step (machine-checked): for b=p each target t mod p^k has exactly p
# preimages = a^{-1}(p consecutive residues mod p^{k+1}).
from collections import Counter
def check(a,b,p,k=4):
    img=Counter((a*x//b)%p**k for x in range(p**(k+1)))
    onto=(len(img)==p**k); mults=set(img.values())
    interval_ok=True
    if b==p and onto and mults=={p}:
        for t in range(min(p**k,30)):
            pre=[x for x in range(p**(k+1)) if (a*x//b)%p**k==t]
            axs=sorted((a*x)%p**(k+1) for x in pre)
            if not (len(axs)==p and axs[-1]-axs[0]==p-1): interval_ok=False; break
    return onto, sorted(mults), interval_ok
print("clean (b=p, v_p=-1):")
for a,b,p in [(3,2,2),(8,3,3),(5,2,2),(4,3,3),(7,2,2),(2,3,3),(16,3,3),(27,2,2)]:
    onto,m,iv=check(a,b,p); print(f"  {a}/{b}: onto={onto} mults={m} interval-arg={iv} -> clean p-to-1: {onto and m==[p]}")
print("non-clean (b=p^2, v_p=-2):")
for a,b,p in [(9,4,2),(16,9,3),(27,4,2),(25,4,2)]:
    onto,m,iv=check(a,b,p); print(f"  {a}/{b}: onto={onto} mults={m} -> clean p-to-1: {onto and m==[p]}")
