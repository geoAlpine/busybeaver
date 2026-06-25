# New-engine attempt: the two-scale bootstrap. c->floor(3c/2) is exactly 2-to-1 => k-step map is a bijection
# {0,1}^k <-> Z/2^k (delta(P^k)=0) => equidist mod 2^k <=> diagonal-bit seq is k-distributed. Bootstrap k->k+1
# needs ONE fresh uniform bit per scale (not implied by k-distribution) = the irreducible requirement = the wall.
from collections import defaultdict
for k in (6,8,10):
    cnt=defaultdict(int)
    for s in range(2**(k+1)): cnt[(3*s)//2 % 2**k]+=1
    sizes=set(cnt.values())
    print(f"k={k}: preimage-count mod 2^(k+1) per state mod 2^k = {sizes} (==2 => clean 2-to-1, bijective k-step, delta(P^k)=0)")
print("=> equidist mod 2^k <=> diagonal-bit seq b_n=floor((3/2)^n) mod 2 is k-distributed.")
print("   bootstrap needs 1 fresh uniform bit/scale = prove b_n is NORMAL = the wall. Irreducible core named.")

# Normality dissection: constructed normals are provably normal via a DESIGNED certificate (enumeration/Weyl/
# self-similarity); floor((3/2)^n) mod 2 has none -- and is MORE uniform / zero-autocorrelation than Champernowne,
# i.e. 'too random to certify'. (See NEW_ENGINE.md table.)
from collections import Counter
import numpy as np
def champ(N):
    s=bytearray(); m=1
    while len(s)<N:
        for ch in bin(m)[2:]: s.append(ord(ch)-48)
        m+=1
    return bytes(s[:N])
def arith(N):
    c=8; s=bytearray()
    for _ in range(N): s.append(c&1); c=(3*c)//2
    return bytes(s)
N=200000
for name,seq in [("Champernowne",champ(N)),("arith",arith(N))]:
    f=1-2*np.frombuffer(seq,np.uint8).astype(float); f-=f.mean()
    ac=[round(float(np.mean(f[:-L]*f[L:])/np.var(f)),4) for L in (1,2,3,4)]
    print(f"{name}: density={sum(seq)/N:.4f}, autocorr(1-4)={ac}")
