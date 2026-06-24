import numpy as np, math
# CAN the proven top-freshness feed the renewal? The renewal needs the INCOMING bit (at position = current
# window size ~ depth) to be fresh. The foothold proves the TOP ~log n bits are fresh. Are these the SAME bits?
N=200000
c=8; Ls=[]; depths=[]
def v2(x):
    if x<=0: return 0
    r=0
    while x&1==0: x>>=1; r+=1
    return r
for n in range(N):
    L=c.bit_length()            # total bits of c_n ~ 0.585n
    d=v2(c-1) if c>1 else 0      # depth = renewal window size = position of the incoming bit that matters
    Ls.append(L); depths.append(d)
    c=3*c//2
Ls=np.array(Ls); depths=np.array(depths)
# the incoming bit relevant to the renewal sits at position ~ depth (the window edge). The proven-fresh
# zone is the TOP ~log2(n) bits = positions [L - log2(n), L]. Is 'depth' inside the proven-fresh zone?
ns=np.arange(1,N+1)
topzone_lo = Ls - np.log2(ns+1)   # bottom of the proven-fresh top zone
print("position of renewal-relevant incoming bit (=depth) vs the proven-fresh TOP zone:")
for n in (1000,10000,100000,199999):
    L=Ls[n]; d=depths[n]; tz=L-math.log2(n+1)
    print(f"  n={n:6d}: total bits L={L}, depth(window pos)={d}, proven-fresh zone = positions [{tz:.0f}..{L}]")
print(f"\n  typical depth ~ {depths[depths>0].mean():.1f} (= O(log n), near the BOTTOM)")
print(f"  proven-fresh top zone bottom ~ L - log2(n) ~ {(Ls-np.log2(ns+1))[N//2]:.0f} (near the TOP, ~0.585n)")
gap = (Ls-np.log2(ns+1))[N//2] - depths[depths>0].mean()
print(f"\n  GAP between proven-fresh top zone and renewal-needed position ~ {gap:.0f} bits of UNCONTROLLED MIDDLE")
print("\nVERDICT: the renewal needs freshness at position ~log n (near BOTTOM); the foothold proves freshness")
print("at position ~0.585n (TOP). They are at OPPOSITE ENDS, separated by ~0.585n uncontrolled middle bits.")
print("=> the two proven tools CANNOT be combined; the weak point is not killable by them. It IS the open kernel.")
