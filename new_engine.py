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
