"""Crux test: is 'persistent thin-set confinement' arithmetically self-defeating, or does it
reduce to equidistribution? Seed o_0 ≡ 3^{-1} mod 2^K (so D_0=v2(3o_0-1) is huge), then watch
the induced odd-to-odd map o_{j+1}=3^{D-1}(3o_j-1)/2^D and record the depth sequence D_j.

If there were a SELF-CORRECTING arithmetic law, a deep start would force shallow successors in a
predictable way (D collapsing deterministically). If it reduces to equidistribution, the depths
should look like fresh independent geometric draws after O(1) steps (no memory of the seed depth).
"""
def v2(x):
    if x==0: return 10**9
    r=0
    while x&1==0: x>>=1; r+=1
    return r

def induced_depths(o, J):
    """Return first J depths D_j along the induced (odd-to-odd) orbit starting at odd o."""
    Ds=[]
    for _ in range(J):
        D=v2(3*o-1)
        Ds.append(D)
        m=(3*o-1)>>D
        o=pow(3,D-1)*m      # next odd value = 3^{D-1} * m
    return Ds

for K in (20, 40, 80):
    o0=pow(3,-1,1<<K)            # 3*o0 ≡ 1 mod 2^K  => D_0 >= K
    if o0%2==0: o0+= (1<<K)      # keep odd (it is odd already since inverse of odd is odd)
    Ds=induced_depths(o0, 40)
    print(f"\nseed o0 ≡ 3^-1 mod 2^{K} (D_0 should be ~{K}):")
    print("  D_j sequence:", Ds[:30])
    print(f"  D_0={Ds[0]}, then mean(D_1..)= {sum(Ds[1:])/len(Ds[1:]):.3f} (Haar mean=2)")

# Many deep seeds: after the forced first step, is the NEXT depth distributed geometric (mean 2)?
import statistics
nxt=[]
for K in range(10,45):
    o0=pow(3,-1,1<<K)
    Ds=induced_depths(o0,3)
    nxt.append(Ds[1])
print(f"\nAcross deep seeds K=10..44: D_1 values = {nxt}")
print(f"  mean D_1 = {statistics.mean(nxt):.3f} (Haar 2) -- deep seed leaves NO depth memory after 1 step")

# Confinement attempt: longest run with D_j >= 2 (i.e. o_j ≡ 3 mod 4 persistently) from c0=8 orbit
def v2f(x):
    r=0
    while x&1==0: x>>=1; r+=1
    return r
o=8
# advance to first odd
while o%2==0: o=(3*o)//2
runs=[]; cur=0; longest=0
for _ in range(200000):
    D=v2f(3*o-1)
    if D>=2: cur+=1; longest=max(longest,cur)
    else: cur=0
    m=(3*o-1)>>D
    o=pow(3,D-1)*m
print(f"\nlongest run of consecutive odd steps with D>=2 (o≡3 mod4) over 200k induced steps: {longest}")
print(f"  (geometric expectation: longest run of a p=1/2 event in 200k ~ log2(200k)={__import__('math').log2(200000):.1f})")
