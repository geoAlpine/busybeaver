import numpy as np
from collections import Counter
# FINDING: c_n mod 3 encodes parity of c_{n-1}. Verify + see what higher 3-adic digits encode,
# and whether the CONTRACTING 3-adic direction gives any control the (open) 2-adic direction lacks.
N=200000
c=8; seq=[]
for n in range(N): seq.append(c); c=3*c//2
seq=np.array(seq,dtype=object)
# (1) verify c_n mod 3 == [c_{n-1} odd]
ok=all( (seq[n]%3==0) == (seq[n-1]%2==0) for n in range(1,5000))
print(f"c_n mod 3 == [c_{{n-1}} even]?  {ok}   (c_n mod 3 never 2: {all(seq[n]%3!=2 for n in range(N))})")
# even-density = freq(c_n mod 3 == 0)
ed=np.mean([seq[n]%3==0 for n in range(N)])
print(f"even-density = freq(c_n=0 mod 3) = {ed:.4f} (need >1/3)")

# (2) what does c_n mod 9 encode? relate to (parity c_{n-1}, parity c_{n-2})
from collections import defaultdict
tab=defaultdict(Counter)
for n in range(2,N):
    key=(seq[n-1]%2, seq[n-2]%2)
    tab[key][seq[n]%9]+=1
print("\nc_n mod 9 given (parity c_{n-1}, parity c_{n-2}):")
for key in sorted(tab):
    common=tab[key].most_common(3)
    print(f"  prev parities {key}: c_n mod 9 distribution {dict(tab[key])}")

# (3) KEY question: the 3-adic direction CONTRACTS under alpha. Does that mean the parity-history
# encoding is 'rigid' = controllable? Test: do two orbits with DIFFERENT seeds but same recent history
# converge 3-adically (stable manifold)? i.e., is there a 3-adic Lipschitz contraction giving control?
def orbit(c0,M):
    c=c0; out=[]
    for _ in range(M): out.append(c); c=3*c//2
    return out
o1=orbit(8,200); o2=orbit(8+2*3**10,200)   # differ by a multiple of 2*3^10
def v3(x):
    x=abs(int(x));
    if x==0: return 50
    r=0
    while x%3==0: x//=3; r+=1
    return r
d3=[v3(o1[n]-o2[n]) for n in range(200)]
print(f"\n3-adic v3(orbit1 - orbit2) for seeds differing by 2*3^10 (contraction => grows):")
print(f"  v3 at n=0,5,20,50,100,199: {[d3[i] for i in (0,5,20,50,100,199)]}")
print("  (if v3 GROWS => 3-adic contraction confirmed => differences vanish 3-adically = stable direction)")
